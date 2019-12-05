# -*- coding: utf-8 -*-

import math
import collections
import heapq
import logging

from similarity import similarities


logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s -   %(message)s',
                    datefmt='%m/%d/%Y %H:%M:%S',
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)


def get_tokens(string, char=True, q=2, whitespace_char='_', unique=False):
    if char:
        if whitespace_char:
            string = string.replace(" ", whitespace_char)
        tokens = [string[i:i+q] for i in range(len(string)-q+1)]
    else:
        tokens = string.split()
    if unique:
        # hacky way to preserve order with uniqueness
        temp = collections.OrderedDict()
        for token in tokens:
            if tokens not in temp:
                temp[token] = None
        tokens = list(temp.keys())
        del temp
    return tokens


class Entity:
    
    def __init__(self, entity_id, entity, char=True, q=2, whitespace_char='_', unique=False):
        self.id = entity_id
        self.entity = entity
        self.tokens = get_tokens(entity, char, q, whitespace_char, unique)
        self.is_char = char
    
    def __len__(self):
        return len(self.tokens)
    
    def __repr__(self):
        return "Entity: {} (id={}, tokens={})".format(self.entity, self.id, self.tokens)
    
    def char_repr(self):
        if self.is_char:
            return "".join([self.tokens[0]] + [self.tokens[i][-1] for i in range(1, len(self.tokens))])



class EntitiesDict:
    
    @staticmethod
    def from_file(fname, **kwargs):
        # map from  internal entity index to ``Entity``
        index2entity = dict()
        index = 0
        # each line is tab separated id and entity
        with open(fname, encoding='utf-8', errors='ignore') as rf:
            for line in rf:
                line = line.strip()
                if not line:
                    continue
                entity_id, entity = line.split("\t")
                index2entity[index] = Entity(entity_id, entity, **kwargs)
                index += 1
        return index2entity
    
    @staticmethod
    def from_list(entities_list, **kwargs):
        # map from  internal entity index to ``Entity``
        index2entity = dict()
        for index, entity in enumerate(entities_list):
            index2entity[index] = Entity(index, entity, **kwargs)
        return index2entity
    
    @staticmethod
    def from_dict(entities_dict, **kwargs):
        # map from  internal entity index to ``Entity``
        index2entity = dict()
        for index, (entity_id, entity) in enumerate(entities_dict.items()):
            index2entity[index] = Entity(entity_id, entity, **kwargs)
        return index2entity


class InvertedIndex:
    
    def __init__(self, index, entities_length):
        self.index = index
        self.lens = entities_length
    
    @classmethod
    def from_entities_dict(cls, entities_dict):
        index = collections.defaultdict(list)
        entities_length = dict()
        
        # for each entity in dictionary
        for entity_index, entity in entities_dict.items():
            # for each token / q-gram of entity
            for token in entity.tokens:
                index[token].append(entity_index)
            
            entities_length[entity_index] = len(entity)
        
        return cls(index, entities_length)
    
    def __getitem__(self, string):
        return self.index[string]
    
    def get_inverted_lists(self, tokens):
        # order preserving mapping
        inverted_lists = collections.OrderedDict()
        for token_index, token in enumerate(tokens):
            if token in self.index:
                inverted_lists[token_index] = self.index[token]
        return inverted_lists



class Faerie:
    
    def __init__(self, entities_dict, similarity='edit_dist', threshold=2, q=2, whitespace_char='_', unique=False):
        
        if similarity in ('edit_dist', 'edit_sim'):
            if q is None:
                raise ValueError("`q` is required for char-based similarity and distance methods")
            self.is_char = True
        else:
            self.is_char = False
        
        self.E = entities_dict
        self.I = InvertedIndex.from_entities_dict(entities_dict)
        self.q = q
        self.whitespace_char = whitespace_char
        self.unique = unique
        # FIXME: raise error when entities are char based and token based similarity is used and vice versa
        self.method = similarity
        self.similarity = similarities[similarity]
        # FIXME: raise error if for similarity threshold is not in (0, 1] and int > 0 for distance
        self.t = threshold
        
        # pre-compute length bounds
        self.init_bounds()
    
    def compute_entity_valid_substrings_lower_bound(self, e_idx):
        """
        Computes similarity function specific entity lower bound, 
        denoted as ⊥e in paper (Lemma 2). Used for considering
        valid substrings.
        
        """
        # get entity length
        l = self.I.lens[e_idx]
        
        if self.method == 'edit_sim':
            lower_e = self.similarity.find_min_size(l, self.t, self.q)
        else:
            lower_e = self.similarity.find_min_size(l, self.t)
        
        # add inplace as entity's class property
        self.E[e_idx].lower_e = lower_e
        
        return lower_e
    
    def compute_entity_valid_substrings_upper_bound(self, e_idx):
        """
        Computes similarity function specific entity upper bound, 
        denoted as Te in paper (Lemma 2). Used for considering
        valid substrings.
        
        """
        # get entity length
        l = self.I.lens[e_idx]
        
        if self.method == 'edit_sim':
            upper_e = self.similarity.find_max_size(l, self.t, self.q)
        else:
            upper_e = self.similarity.find_max_size(l, self.t)
        
        # add inplace as entity's class property
        self.E[e_idx].upper_e = upper_e
        
        return upper_e
    
    def compute_entity_overlap_lower_bound(self, e_idx):
        """
        Computes similarity function specific overlap lower bound, 
        denoted as Tl in paper (Lemma 3). Used for Lazy-Count pruning.
        
        """
        # get entity length
        l = self.I.lens[e_idx]
        
        if self.method == 'edit_sim' or self.method == 'edit_dist':
            Tl = self.similarity.find_lower_bound_of_entity(l, self.t, self.q)
        else:
            Tl = self.similarity.find_lower_bound_of_entity(l, self.t)
        
        # add inplace as entity's class property
        self.E[e_idx].Tl = Tl
        
        return Tl
    
    def init_bounds(self):
        """
        Computes valid substring upper and lower bounds for all entities (Te, ⊥e), 
        their global versions (TE, ⊥E) and overlap similarity lower bound (Tl).
        
        """
        lower_es = list()
        upper_es = list()
        
        for e_idx in self.E:
            lower_es.append(self.compute_entity_valid_substrings_lower_bound(e_idx))
            upper_es.append(self.compute_entity_valid_substrings_upper_bound(e_idx))
            _ = self.compute_entity_overlap_lower_bound(e_idx)
        
        self.min_lower_e = min(lower_es) # T_E
        self.max_upper_e = max(upper_es) # ⊥_E
        
        logger.info("Global length constraints with this dictionary : {} <= |s| <= {}".format(self.min_lower_e, self.max_upper_e))
    
    def process_document_string(self, document):
        """Preprocess input document to be same as entities."""
        return get_tokens(document, self.is_char, self.q, self.whitespace_char, self.unique)
    
    def init_heap(self, inverted_lists):
        """Initializes min-heap from top elements of inverted lists.
        
        Parameters
        ----------
            inverted_lists : dict<int, list>
                A mapping from token position in document, where the sublist
                is non-empty, to the inverted list. Where each list is sorted
                in ascending order.
        
        Notes
        -----
            In this step we first create a new single min-heap from the 
            top elements of each inverted list. As an example, take fig.
            5 from paper:
            ```
            inverted_lists = [[4], [4], [4], [1, 4], [1, 4], [1, 4], [1, 4], [1]]
                               ^    ^    ^    ^       ^       ^       ^       ^
            sub_indexes:       0    0    0    0  1    0   1   0  1    0  1    0
            token_index:       0    1    2      3       8      13      18     19    
            ```
            then, heap will be made of all entity ids marked with ^ for
            initialization.
        
        """
        self.heap = [inverted_lists[non_empty_position_index][0] for non_empty_position_index in inverted_lists]
        # generate inplace min-heap from list
        heapq.heapify(self.heap)
    
    def init_positions_and_top_pointers(self, inverted_lists):
        """Initializes min-heap from top elements of inverted lists.
        
        Parameters
        ----------
            inverted_lists : dict<int, list>
                A mapping from token position in document, where the sublist
                is non-empty, to the inverted list. Where each list is sorted
                in ascending order.
        
        Notes
        -----
            Re-using the example from above, recall:
            ```
            inverted_lists = [[4], [4], [4], [1, 4], [1, 4], [1, 4], [1, 4], [1]]
                               ^    ^    ^    ^       ^       ^       ^       ^
            sub_indexes:       0    0    0    0  1    0   1   0  1    0  1    0
            token_index:       0    1    2      3       8      13      18     19    
            ```
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
            positions = { 1 : [3, 8, 13, 18, 19], 4 : [0, 1, 2, 3, 8, 13, 18] }
            ```
            The sublists are identified by their token index (i.e. position in the
            document). We **CAN** take advantage of the fact that each list is sorted in
            ascending order and therefore, min-heap generated on top elements of these
            sublists will process entities in order as well. So, we expect all positions
            of current entity to be seen until we see a different one. We can maintain
            a simple counter for time period till a different entity is seen and reset
            it at that point to 0. This counter will work for us as pointer.
            
            But for now, follow something close to Faerie, we add pointers per entity
            in positions.
            ```
            positions = { 1 : ([3, 8, 13, 18, 19], 0), 4 : ([0, 1, 2, 3, 8, 13, 18], 0) }
            ```
            after one pop of 1:
            ```
            positions = { 1 : ([3, 8, 13, 18, 19], 1), 4 : ([0, 1, 2, 3, 8, 13, 18], 0) }
            ```
            means that current top entity is 1 and is coming from sublist 8 <ei,pi> = <1,8>
            
            Lastly, we need to keep top pointers. We do it with a dictionary.
            
            Important note for possible improvement: because we already know the position 
            sizes (|Pe|) we **CAN** apply lazy-count pruning during initialization. This will
            eliminate all the unnecessary entities from being added in heap in first place.
            Thus the heap adjustment costs from these entities will be eliminated. However, 
            this will come at cost of space complexity as we are pre-computing all the 
            position lists.
        
        """
        # mapping from entity index to sorted list of token positions
        self.positions = collections.defaultdict(list)
        
        # mapping from non-empty sublist token positions to the index of current 
        # top element (the element currently in heap) in inverted list
        self.top_pointers = dict()
        
        # since we use ``OrderedDict`` in ``InvertedIndex``, looping over it
        # will generate keys in asecending order
        for token_index in inverted_lists:
            
            # since we used enumeration in ``get_inverted_lists`` method, looping
            # over each sublist will generate token positions in asecending order
            for entity_index in inverted_lists[token_index]:
                self.positions[entity_index].append(token_index)
            
            # set each sub-lists' pointer where the top element index is (initially at 0)
            self.top_pointers[token_index] = 0
        
        # change mapping from dict<int, list> to dict<int, list(list, int)>
        # where the keys are entity indexes and each element is a two elemenet
        # list, where first element is position list and second element points
        # to index of that list giving us the the position from which sublist
        # the entity is coming from
        for entity_index, tokens_index in self.positions.items():
            self.positions[entity_index] = [self.positions[entity_index], 0]
    
    def reset_count_occurence(self, doc_len):
        """Initialize a counter for current entity being processed.
        
        Notes
        -----
            The counter ``V`` is a nested dictionary, where the primary key
            is the token position and secondary key is the number of tokens
            from their to the right:
            ```
            V[ith token][l tokens to right from i] = count ==> V[i][l]
            ```
        
        """
        self.V = collections.defaultdict(dict)
        
        # initialize all the counts to zero
        for token_i in range(doc_len):
            for l in range(self.min_lower_e, self.max_upper_e + 1):
                self.V[token_i][l] = 0
    
    def increment_count(self, i, l):
        """Increment the relevant entries from given position index and length.
        
        Parameters
        ----------
            i : int
                The right position in document index, marking as end of substring.
            
            l : int
                Length to consider before position i (effectively starting at 
                i-l+1 to i for substring D[i-l+1, l]). 
        
        """
        # relevant entries for this increment starts from ``start_index`` and 
        # goes up to ``i``
        start_index = i-l+1
        
        # when looking back from current index is larger than number of elements
        # before that position
        if start_index < 0:
            # note 0 based indexing
            for j in range(i+1):
                self.V[j][l] += 1
        else:
            for j in range(start_index, i+1):
                self.V[j][l] += 1
    
    def count(self, spans, lower_e, upper_e):
        """
        ADD DOCUMENTATION HERE!
        """
        for length in range(lower_e, upper_e+1):
            for start, _ in spans:
                self.increment_count(start, length)
    
    def enumerate_cadidate_windows(self, i, j, Pe, e):
        """
        ADD DOCUMENTATION HERE!
        """
        pi = Pe[i-1]
        # edge case when pi is start of list
        if i-1 == 0:
            pi_prev = -math.inf
        else:
            pi_prev = Pe[i-2]
        
        pj = Pe[j-1]
        # edge case when pj is last of list
        if j == len(Pe):
            pj_next = math.inf
        else:
            pj_next = Pe[j]
        
        Te = self.E[e].upper_e
        # pg. 535, left column 2 para
        lo = max(pj - Te + 1, pi_prev + 1)
        up = min(pi + Te - 1, pj_next - 1)
        
        if self.method in ('edit_dist', 'edit_sim'):
            upper_e = self.E[e].upper_e
        else:
            # using tighther upper bound for Jaccard, Cosine and Dice
            e_len = self.I.lens[e]
            Pe_ij_len = j - i + 1
            upper_e = self.similarity.tighter_upper_window_size(e_len, Pe_ij_len, self.t)
        
        spans = list()
        
        # lo <= p_start <= pi
        for p_start in range(lo, pi+1):
            # pj <= p_end <= up
            for p_end in range(pj, up+1):
                # |s| = |D[p_start · · · p_end ]| 
                s_len = p_end - p_start + 1
                if self.E[e].lower_e <= s_len <= upper_e:
                    spans.append((p_start, s_len))
        
        # count select windows
        self.count(spans, self.E[e].lower_e, self.E[e].upper_e)
        # compute the overlap similarity to prune candidates
        spans = self.similarity_overlap_prune(spans, e)
        
        return spans
    
    def similarity_overlap_prune(self, candidate_windows, e):
        """
        ADD DOCUMENTATION HERE!
        """
        final_spans = list()
        e_len = self.I.lens[e]
        
        for start, length in candidate_windows:
            
            if self.method in ('edit_sim', 'edit_dist'):
                T = self.similarity.find_tau_min_overlap(e_len, length, self.t, self.q)
            else:
                T = self.similarity.find_tau_min_overlap(e_len, length, self.t)
            
            count_overlap = self.V[start][length]
            print(count_overlap, T)
            if count_overlap >= T:
                final_spans.append((start, length))
        
        return final_spans
    
    def binary_span(self, i, j, Pe, Te, e):
        """
        ADD DOCUMENTATION HERE!
        """
        lower = j
        upper = i + Te - 1
        
        while lower <= upper:
            # mid is new right span, eventually larger than j (i.e. lower)
            # if mid jumps out of len(Pe) then it will raise IndexError!
            mid = math.ceil((upper + lower)/2)
            
            # first condition is ported from java version (does this fix IndexError?)
            if mid <= len(Pe):
                pmid, pi = Pe[mid-1], Pe[i-1]
                if (pmid - pi + 1 > Te):
                    upper = mid - 1
                else:
                    lower = mid + 1
            else:
                lower = mid + 1
        
        mid = upper
        # clip mid to max length if it is out of bound (is there systematic way to fix it?)
        if mid > len(Pe):
            mid = len(Pe)
        
        candidate_windows = self.enumerate_cadidate_windows(i, mid, Pe, e)
         
        return candidate_windows
    
    def binary_shift(self, i, j, Pe, Te, Tl):
        """
        ADD DOCUMENTATION HERE!
        """
        lower = i
        upper = j
        
        while lower <= upper:
            mid = math.ceil((lower + upper) / 2)
            pmid, pj = Pe[mid-1], Pe[j-1]
            
            if ((pj + (mid - i)) - pmid + 1) > Te:
                lower = mid + 1
            else:
                upper = mid - 1
        
        i = lower
        j = i + Tl - 1
        # clip if larger than size of position list
        if j > len(Pe):
            j = len(Pe)
        
        pi, pj = Pe[i-1], Pe[j-1]
        
        if (pj - pi + 1) > Te:
            i = self.binary_shift(i, j, Pe, Te, Tl)
        
        return i
    
    def find_candidate_windows(self, e, Pe):
        """
        ADD DOCUMENTATION HERE!
        """
        # upper bound of token numbers
        Te = self.E[e].upper_e
        # lower bound of overlap similarity
        Tl = self.E[e].Tl
        candidate_windows = list()
        
        i = 1
        while i <= len(Pe) - Tl + 1:
            # pg. 535 left column, last line (intially Pe[1,..,Tl])
            j = i + Tl - 1
            # 0 based indexing; add -1
            pj, pi = Pe[j-1], Pe[i-1]
            # (j-1)+1 = j (-1 due to 0-based indexing and +1 because python list is non-inclusive)
            Pe_ij = Pe[i-1:j]
            
            # length for substring |D[pi...pj]| = pj-pi+1 is not larger than upper bound
            if (pj - pi + 1) <= Te:
                # we have a valid substring with size, Tl ≤ |Pe[i · · · j]| ≤ Te
                # Hence, find candidate window ⊥e ≤ |D[pi · · · pj ]| ≤ Te
                # Inside binary_span, we will eventually use tighter upper bounds
                
                # -------------------
                # <BINARY SPAN HERE>
                # -------------------
                candidate_windows.extend(self.binary_span(i, j, Pe, Te, e))
                i += 1
            else:
                # candidate windows are too long
                
                # --------------------
                # <BINARY SHIFT HERE>
                # --------------------
                i = self.binary_shift(i, j, Pe, Te, Tl)
        
        return candidate_windows
    
    def __call__(self, document):
        """Runs Faerie algorithm on a document.
        
        Parameters
        ----------
            document : str
                Input document as string.
        
        """
        ## STEP 1. Tokenize the input document and save it to `D`
        self.D = self.process_document_string(document)
        
        ## STEP 2. Get inverted lists of each token in the document
        inverted_lists = self.I.get_inverted_lists(self.D)
        
        ## STEP 3. Initialize heap, top pointers and positions list
        self.init_heap(inverted_lists)
        self.init_positions_and_top_pointers(inverted_lists)
        
        ## STEP 4. Initialize count array.
        self.reset_count_occurence(len(self.D))
        
        # current minimal entity in heap
        e = self.heap[0]
        Pe = list()
        
        # final (entity -> candidates) map
        entity2candidates = collections.defaultdict(set)
        
        while len(self.heap) > 0:
            
            # pop the top element from heap
            ei = heapq.heappop(self.heap)
            
            # get position list for ei and obtain its current position
            #
            #    (___position_list___)[_index_of_position_list_]
            #
            pi = self.positions[ei][0][self.positions[ei][1]]
            
            # increment top pointer of sublist at position pi
            self.top_pointers[pi] += 1
            # move index to next position in sublist as well
            self.positions[ei][1] += 1
            
            # while we have same entity, we keep popping it to build position list
            if ei == e:
                Pe.append(pi)
            # else we see a new entity, 
            else:
                print(self.E[e])
                if len(Pe) >= self.E[e].Tl:
                    # find candidate windows using Algorithm 1
                    entity2candidates[e].update(self.find_candidate_windows(e, Pe))
                
                e = ei
                Pe = [pi]
                self.reset_count_occurence(len(self.D))
            
            # add new element to heap if there
            pi_top_pointer = self.top_pointers[pi]
            if pi_top_pointer < len(inverted_lists[pi]):
                e_to_add = inverted_lists[pi][pi_top_pointer]
                heapq.heappush(self.heap, e_to_add)
            
            # otherwise we have nothing to add and heap is already adjusted with heappop
        
        return entity2candidates

    def print_candidate_substrings(self, entity2candidates):
        """
        ADD DOCUMENTATION HERE!
        """
        for e, candidates in entity2candidates.items():
            print("Entity:", self.E[e].entity)
            print("----------------------------")
            for start, length in candidates:
                substring = self.D[start:start+length]
                if self.is_char:
                    substring = "".join([substring[0]] + [substring[i][-1] for i in range(1, len(substring))]) 
                else:
                    substring = " ".join(substring)
                print(substring)
            print("----------------------------")


if __name__=="__main__":
    E = [
        'kaushik ch',
        'chakrabarti',
        'chaudhuri',
        'venkatesh',
        'surajit ch'
    ]
    D = 'an efficient filter for approximate membership checking. venkaee shga kamunshik kabarati, dong xin, surauijt chadhurisigmod.'
    # D = 'venkaee shga kamunshi'

    entities_configs = dict(char=True, q=2, whitespace_char='_', unique=False)
    entities_dict = EntitiesDict.from_list(E, **entities_configs)
     
    faerie_configs = dict(
        similarity='edit_dist', threshold=2, q=entities_configs['q'], 
        whitespace_char=entities_configs['whitespace_char'], 
        unique=entities_configs['unique']
    )
    faerie = Faerie(entities_dict, **faerie_configs)
    entity2candidates = faerie(D)
    faerie.print_candidate_substrings(entity2candidates)
