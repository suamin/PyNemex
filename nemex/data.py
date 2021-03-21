# -*- coding: utf-8 -*-

import collections
import pickle
import heapq
import logging


logger = logging.getLogger(__name__)


class Entity:
    
    def __init__(self, uid, text, tokens=None):
        self.id = uid
        self.entity = text
        self.tokens = tokens
    
    @property
    def tokens(self):
        return self._tokens
    
    @tokens.setter
    def tokens(self, tokens):
        self._tokens = tokens
        if tokens is None:
            self._len = 0
        else:
            self._len = len(tokens)
    
    def __len__(self):
        return self._len
    
    def __repr__(self):
        return "Entity <id: {}, text: {}, len: {}>".format(self.id, self.entity, len(self))


class EntitiesDictionary:
    
    def __init__(self, tokenizer=None):
        self.idx2ent = dict()
        self.uid2idx = dict()
        self.tokenizer = tokenizer
    
    def add(self, string, uid=None):
        if self.tokenizer is None:
            tokens = string.split()
        else:
            tokens = self.tokenizer(string)
        idx = len(self.idx2ent)
        if uid is None:
            uid = idx
        self.uid2idx[uid] = idx
        self.idx2ent[idx] = Entity(uid, string, tokens)
    
    @staticmethod
    def from_tsv_file(fname, tokenizer=None):
        ents_dict = EntitiesDictionary(tokenizer)
        # each line is tab separated id and string value
        with open(fname, encoding='utf-8', errors='ignore') as rf:
            for line in rf:
                line = line.strip()
                if not line:
                    continue
                line = line.split("\t")
                if len(line) == 1:
                    uid = None
                    string = line[0]
                else:
                    uid, string = line
                ents_dict.add(string, uid)
        return ents_dict
    
    @staticmethod
    def from_list(list_strings, tokenizer=None):
        ents_dict = EntitiesDictionary(tokenizer)
        for string in list_strings:
            ents_dict.add(string, None)
        return ents_dict
    
    def __len__(self):
        return len(self.idx2ent)
    
    def __getitem__(self, idx):
        return self.idx2ent[idx]
    
    def __delitem__(self, idx):
        # get uid
        uid = self[idx].id
        del self.uid2idx[uid]
        del self.idx2ent[idx]
    
    def __iter__(self):
        for eidx in self.idx2ent:
            yield eidx
    
    def get_item_by_uid(self, uid):
        return self.idx2ent[self.uid2idx[uid]]
    
    def save(self, fname):
        with open(fname, "wb") as wf:
            dump = {
                "idx2ent": self.idx2ent, 
                "uid2idx": self.uid2idx, 
                "tokenizer": tokenizer
            }
            pickle.dump(dump, wf)
    
    @classmethod
    def load_from_file(cls, fname):
        ents_dict = EntitiesDictionary()
        with open(fname, "rb") as rf:
            dump = pickle.load(rf)
            ents_dict.idx2ent = dump["idx2ent"]
            ents_dict.uid2idx = dump["uid2idx"]
            ents_dict.tokenizer = dump["tokenizer"]
        return ents_dict  


class InvertedIndex:
    
    def __init__(self, token2ents):
        self.token2ents = token2ents
    
    @classmethod
    def from_ents_dict(cls, ents_dict):
        token2ents = collections.defaultdict(list)
        
        # for each entity in dictionary
        for eidx, entity in ents_dict.idx2ent.items():
            # for each token / q-gram of entity
            for token in entity.tokens:
                token2ents[token].append(eidx)
        
        return cls(token2ents)
    
    def __getitem__(self, tokens):
        # order preserving mapping
        inv_lists = collections.OrderedDict()
        for position, token in enumerate(tokens):
            if token in self.token2ents:
                inv_lists[position] = self.token2ents[token]
        return inv_lists


class FaerieDataStructure:
    """Main class to hold all the data structures needed for Faerie.
        Initializes min-heap from top elements of inverted lists.
    
    Notes
    -----
    A single min-heap is created from the top elements of each inverted 
    list. As an example, take fig. 5 from paper:
    ```
    inverted_lists = [[4], [4], [4], [1, 4], [1, 4], [1, 4], [1, 4], [1]]
                       ^    ^    ^    ^       ^       ^       ^       ^
    sub_indexes:       0    0    0    0  1    0   1   0  1    0  1    0
    token_index:       0    1    2      3       8      13      18     19    
    ```
    then, heap will be made of all entity ids marked with ^ for
    initialization.
    
    Next, we also need to maintain pointers to first elements' index
    in each (sub)-list. At initialization it will be all 0's (because
    ^ points to first positions in each list).
    
    At pop of first "1", the picture will look like
    ```
    inverted_lists = [[4], [4], [4], [x, 4], [1, 4], [1, 4], [1, 4], [1]]
                       ^    ^    ^       ^    ^       ^       ^       ^
    sub_indexes:       0    0    0    0  1    0   1   0  1    0  1    0
    token_index:       0    1    2      3       8      13      18     19 
    ```
    We can see that the pointer ^ of fourth sublist moved to position
    1 of sublist. Note, in implementation, the poped entity is never
    removed from actual inverted list so, `x` here is only for visualization
    purposes.
    
    However, we **CAN** create a mapping from entity index to position lists.
    ```
    ent2positions = { 1 : [3, 8, 13, 18, 19], 4 : [0, 1, 2, 3, 8, 13, 18] }
    ```
    We create dictionaries and retrieve inverted lists in such a manner that
    all position lists are pre-computed and positions sorted. Since min-heap
    is generated from top-elements, we will see smallest indexed entity in heap
    until all its occurences exhaust e.g. after full cycle of heap-pop+push,
    we will have popped elements as [0, 0, 0, 0, 0, 4, 4, 4, 4, 4, 4, 4].
    This effectively allows to keep one active count occurence array only.
    The local pointer per entity list is just an integer ``self.current_e_indptr``.
    Lastly, we need to keep top pointers per postion. This we do it with a 
    simple dictionary in ``self.position2topidx``.
    
    Important note for possible improvement: because we already know the position 
    sizes (|Pe|) we **CAN** apply lazy-count pruning during initialization. This will
    eliminate all the unnecessary entities from being added in heap in first place.
    Thus the heap adjustment costs from these entities will be eliminated. However, 
    this will come at cost of space complexity as we are pre-computing all the 
    position lists.
    
    """
    def __init__(self, ents_dict):
        self.ents_dict = ents_dict
        self._heap = list()
    
    def init_from_inv_lists(self, inv_lists):
        """Faerie data-structures initialization.
        
        Creates min-heap from top elements of inverted lists. Record
        positions, maintains top pointers and count array per entity.
        
        Parameters
        ----------
        inverted_lists : dict of [int, list]
            A mapping from token position in document, where the sublist is non-empty, 
            to the inverted list. Where each list is sorted in ascending order.
        
        """
        self.heap = inv_lists
        self.init_position_data(inv_lists)
        self.inv_lists = inv_lists
        self.reset_count()
        self.current_e_indptr = 0
    
    @property
    def heap(self):
        return self._heap
    
    @heap.setter
    def heap(self, inv_lists):
        self._heap = [inv_lists[position][0] for position in inv_lists]
        # generate inplace min-heap from list
        heapq.heapify(self._heap)
    
    def init_position_data(self, inv_lists):
        # mapping from entity index to sorted list of token positions
        self.ent2positions = collections.defaultdict(list)
        
        # mapping from non-empty sublist token positions to the index of current 
        # top element (the element currently in heap) in inverted list
        self.position2topidx = dict()
        
        # since we used ``OrderedDict`` in :meth:`~nemex.data.InvertedIndex.__getitem__`, 
        # looping over it will return keys in asecending order
        for position in inv_lists:
            # since we used enumeration in :meth:`~nemex.data.InvertedIndex.__getitem__`, 
            # looping over each sublist will return token positions in asecending order
            for eidx in inv_lists[position]:
                self.ent2positions[eidx].append(position)
            
            # set each sub-lists' pointer where the top element index is (initially at 0)
            self.position2topidx[position] = 0
    
    def reset_count(self):
        """Initialize or clear a counter for current entity being processed.
        
        Notes
        -----
        The counter ``V`` is a nested dictionary, where the primary key
        is the token position and secondary key is the number of tokens
        from their to the right:
        ```
        V[ith token][l tokens to right from i] = count ==> V[i][l]
        ```
        
        """
        self.V = collections.defaultdict(lambda: collections.defaultdict(int))
    
    def count(self, position, min_len, max_len):
        """Increment count of entity's occurence in relevant positions.
        
        Parameters
        ----------
        position : int
            End position (right position).
        
        min_len : int
            Minimum length to look behind from end position to update
            (position - l + 1, left position).
        
        max_len : int
            Maximum length to look behind from end position to update
            (position - l + 1, left position).
        
        Notes
        -----
        See pg. 532 second column last para for a good running example.
        
        """
        for l in range(min_len, max_len+1):
            # relevant entries for this increment starts from ``start_idx`` 
            # and goes up to ``position``; less than 0 case: when looking 
            # back from current index is larger than number of elements before 
            # that position, so we clamp at 0
            start_idx = max(0, position-l+1)
            end_idx = position
            for j in range(start_idx, end_idx+1):
                # j = the right position in document index, marking as end of substring
                # l = length to consider before position j 
                # (effectively starting at j-l+1 to j for substring D[j-l+1, l])
                self.V[j][l] += 1
    
    def step(self, e):
        """A Faerie step to update its data structures.
        
        Steps involved:
            1. Pop element from heap.
            2. If heap is empty raise stop flag
            3. Else, if popped entity is different than last entity,
               reset the running sub-list pointer.
            4. Get the position from which this element came from.
            5. Update pointers.
            6. If current position inverted list still has element,
               push it to the heap.
            7. Return popped entity, its position and stop flag.
        
        """
        stop = False
        try:
            # pop the top element from heap
            ei = heapq.heappop(self.heap)
        except:
            stop = True
            ei = None
            pi = None
        else:
            if ei != e:
                self.current_e_indptr = 0 
            pi = self.ent2positions[ei][self.current_e_indptr]
            self.position2topidx[pi] += 1 # increment top pointer of sublist at position pi
            self.current_e_indptr += 1
            
            pi_top_pointer = self.position2topidx[pi]
            if pi_top_pointer < len(self.inv_lists[pi]):
                ej = self.inv_lists[pi][pi_top_pointer]
                heapq.heappush(self.heap, ej)
        
        return ei, pi, stop
