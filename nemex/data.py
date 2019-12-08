# -*- coding: utf-8 -*-

import collections
import pickle
import heapq
import logging


logger = logging.getLogger("nemex")


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
                if len(line) == 0:
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
    
    def __init__(self, ents_dict):
        self.ents_dict = ents_dict
        self.inv_index = InvertedIndex.from_ents_dict(ents_dict)
        self._heap = list()
    
    def init_from_inv_lists(self, inv_lists):
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
        self.ent2positions = collections.defaultdict(list)
        self.position2topidx = dict()
        
        for position in inv_lists:
            for eidx in inv_lists[position]:
                self.ent2positions[eidx].append(position)
            
            self.position2topidx[position] = 0
    
    def reset_count(self):
        self.V = collections.defaultdict(lambda: collections.defaultdict(int))
    
    def count(self, position, min_len, max_len):
        for l in range(min_len, max_len+1):
            start_idx = max(0, position-l+1)
            end_idx = position
            for j in range(start_idx, end_idx+1):
                self.V[j][l] += 1
    
    def step(self, e):
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
