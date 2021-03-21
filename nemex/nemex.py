# -*- coding: utf-8 -*-

import logging
import time

from nemex import utils
from .data import EntitiesDictionary
from .utils import Tokenizer
from .similarities import Verify
from .faerie import Faerie

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


class Nemex:
    
    def __init__(self, list_or_file_ents, char=True, q=2, special_char="_", unique=False, 
                 lower=True, similarity="edit_dist", t=2, pruner="batch_count", verify=True):
        if char:
            if similarity not in ("edit_dist", "edit_sim"):
                raise ValueError("Change similarity method to 'edit_dist' or 'edit_sim' for character level.")
            if similarity == "edit_dist":
                t = int(t)
                if not t >= 1:
                    raise ValueError("Edit distance threshold must be >= 1")
            else:
                if not (0. < t <= 1.0):
                    raise ValueError("Similarity score should be in (0, 1]")
            q = int(q)
            if not q >= 1:
                raise ValueError("q-gram must be at least 1")
        else:
            if similarity in ("edit_dist", "edit_sim"):
                raise ValueError("Change similarity method to 'cosine', 'dice' or 'jaccard' for token level.")
            if not (0. < t <= 1.0):
                raise ValueError("Similarity score should be in (0, 1]")
        
        self.tokenizer = Tokenizer(char, q, special_char, unique, lower)
        self.char = char
        
        logger.info("Building entities dictionary ...")
        T = time.time()
        
        if isinstance(list_or_file_ents, list):
            self.E = EntitiesDictionary.from_list(list_or_file_ents, self.tokenizer.tokenize)
        else: # else it is file of tsv id\tent lines or just text of ent lines
            self.E = EntitiesDictionary.from_tsv_file(list_or_file_ents, self.tokenizer.tokenize)
        self.cache_ent_repr = dict()
        
        T = time.time() - T
        logger.info("Building dictionary took {} seconds.".format(int(T)))
        
        self.faerie = Faerie(self.E, similarity=similarity, t=t, q=q, pruner=pruner)
        self.verify = verify
    
    def __call__(self, document, valid_only=True):
        assert isinstance(document, str), "Expected a string as document."
        
        doc_tokens = self.tokenizer.tokenize(document)
        
        if self.char:
            doc_tokens_str = utils.qgrams_to_char(doc_tokens).replace(self.tokenizer.special_char, " ")
        else:
            doc_tokens_str = " ".join(doc_tokens)
        
        spans = utils.tokens_to_whitespace_char_spans(doc_tokens)
        
        output = {"document": doc_tokens_str, "matches": list()}
        
        # returns pair of <entity index, (start, end) positions in doc_tokens>
        for e, (i, j) in self.faerie(doc_tokens):
            match_tokens = doc_tokens[i:j+1]
            match_span = spans[i:j+1]
            if len(match_span) == 1:
                start, end = match_span[0]
            else:
                start, end = match_span[0][0], match_span[-1][1]
            
            if self.char:
                q = self.tokenizer.q
                start, end = start - (i * q), end - (j * q)
                match = doc_tokens_str[start:end]
                
                if e not in self.cache_ent_repr:
                    entity = utils.qgrams_to_char(self.E[e].tokens).replace(self.tokenizer.special_char, " ")
                    self.cache_ent_repr[e] = entity
                else:
                    entity = self.cache_ent_repr[e]
                
                output["matches"].append({
                    "entity": [entity, self.E[e].id],
                    "span": [start, end],
                    "match": match,
                    "score": None,
                    "valid": None
                })
                if self.verify:
                    valid, score = Verify.check(match, entity, self.faerie.similarity, self.faerie.t)
                    output["matches"][-1]["score"] = score
                    output["matches"][-1]["valid"] = valid
                    if valid_only and not valid:
                        del output["matches"][-1]
            else:
                # end = spans[j][-1]
                match = doc_tokens_str[start:end]
                
                if e not in self.cache_ent_repr:
                    entity = " ".join(self.E[e].tokens)
                    self.cache_ent_repr[e] = entity
                else:
                    entity = self.cache_ent_repr[e]
                
                output["matches"].append({
                    "entity": [entity, self.E[e].id],
                    "span": [start, end],
                    "match": match,
                    "score": None,
                    "valid": None
                })
                if self.verify:
                    valid, score = Verify.check(
                        match_tokens, self.E[e].tokens, self.faerie.similarity, self.faerie.t
                    )
                    output["matches"][-1]["score"] = score
                    output["matches"][-1]["valid"] = valid
                    if valid_only and not valid:
                        del output["matches"][-1]
        
        return output
