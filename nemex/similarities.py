# -*- coding: utf-8 -*-

import math
from Levenshtein import editops


class JaccardSimilarity:
    
    def find_tau_min_overlap(self, entity_len, string_len, t):
        #
        # |e ∩ s| >= (|e| + |s|) * t/(1 + t)
        #
        return math.ceil((entity_len + string_len) * (t / (1 + t)))
    
    def find_min_size(self, tokens_len, t):
        #
        # |X| * t
        #
        return math.ceil(tokens_len * t)
    
    def find_max_size(self, tokens_len, t):
        #
        # |X| / t
        #
        return math.floor(tokens_len / t)
    
    def find_lower_bound_of_entity(self, tokens_len, t):
        #
        # |X| * t
        #
        return math.ceil(tokens_len * t)
    
    def tighter_upper_window_size(self, entity_len, Pe_ij_len, t):
        #
        # low_e <= |D[pi...pj]| <= min(|e|, |P_e[pi,...,pj]|) / t
        #
        return math.floor(min(entity_len, Pe_ij_len) / t)


class CosineSimilarity:
    
    def find_tau_min_overlap(self, entity_len, string_len, t):
        #
        # |e ∩ s| >= (|e| * |s|) * t
        #
        return math.ceil(math.sqrt(entity_len * string_len) * t)
    
    def find_min_size(self, tokens_len, t):
        #
        # |X| * t^2
        #
        return math.ceil(tokens_len * t**2)
    
    def find_max_size(self, tokens_len, t):
        #
        # |X| / t^2
        #
        return math.floor(tokens_len / t**2)
    
    def find_lower_bound_of_entity(self, tokens_len, t):
        #
        # |X| * t^2
        #
        return math.ceil(tokens_len * t**2)
    
    def tighter_upper_window_size(self, entity_len, Pe_ij_len, t):
        #
        # low_e <= |D[pi...pj]| <= min(|e|, |P_e[pi,...,pj]|) / (t^2)
        #
        return math.floor(min(entity_len, Pe_ij_len) / t**2)


class DiceSimilarity:
    
    def find_tau_min_overlap(self, entity_len, string_len, t):
        #
        # |e ∩ s| >= (|e| + |s|) * (t / 2)
        #
        return math.ceil((entity_len + string_len) * (t / 2))
    
    def find_min_size(self, tokens_len, t):
        #
        # |X| * (t / (2 - t))
        #
        return math.ceil(tokens_len * (t / (2 - t)))
    
    def find_max_size(self, tokens_len, t):
        #
        # |X| * ((2 - t) / t)
        #
        return math.floor(tokens_len * ((2 - t) / t))
    
    def find_lower_bound_of_entity(self, tokens_len, t):
        #
        # |X| * (t / (2 - t))
        #
        return math.ceil(tokens_len * (t / (2 - t)))
    
    def tighter_upper_window_size(self, entity_len, Pe_ij_len, t):
        #
        # low_e <= |D[pi...pj]| <= min(|e|, |P_e[pi,...,pj]|) * ((2 - t) / t)
        #
        return math.floor(min(entity_len, Pe_ij_len) * ((2 - t) / t))


class EditSimilarity:
    
    def find_tau_min_overlap (self, entity_len, string_len, t, q):
        #
        # |e ∩ s| >= max(|e|, |s|) - (max(|e|, |s|) + q - 1) * (1 - t) * q
        #
        return math.ceil(max(entity_len, string_len) - ((max(entity_len, string_len) + q - 1) * (1 - t) * q))
    
    def find_min_size(self, tokens_len, t, q):
        #
        # ((|X| + q - 1) * t) - (q - 1)
        # 
        return math.ceil(((tokens_len + q - 1) * t) - (q - 1))
    
    def find_max_size(self, tokens_len, t, q):
        #
        # ((|X| + q - 1) / t) - (q - 1)
        #
        return math.floor(((tokens_len + q - 1) / t) - (q - 1))
    
    def find_lower_bound_of_entity(self, tokens_len, t, q):
        #
        # |X| - ((|X| + q - 1) * ((1 - t) / t) * q)
        #
        return math.ceil(tokens_len - ((tokens_len + q - 1) * ((1 - t) / t) * q))
    
    def tighter_neighbor_bound(self, entity_len, t, q):
        #
        # pi+1 - pi - 1 > ((|e| + q - 1) / t) * (1 - t) * q (cf. page 534, left column para 5)
        #
        return math.floor(((entity_len + q - 1) / t) * (1 - t) * q)


class EditDistance:
    
    def find_tau_min_overlap(self, entity_len, string_len, tau, q):
        #
        # |e ∩ s| <= max(|e|, |s|) - (τ * q)
        #
        return max(entity_len, string_len) - (tau * q)
    
    def find_min_size(self, tokens_len, tau):
        #
        # |X| - τ
        #
        return tokens_len - tau
    
    def find_max_size(self, tokens_len, tau):
        #
        # |X| + τ
        #
        return tokens_len + tau
    
    def find_lower_bound_of_entity(self, tokens_len, tau, q):
        #
        # |X| - (τ * q)
        #
        return tokens_len - (tau * q)
    
    def tighter_neighbor_bound(self, tau, q):
        #
        # pi+1 - pi - 1 > τ * q (cf. page 534, left column para 5)
        #
        return tau * q


class Similarity:
    
    def __init__(self):
        self._sims = {
            'jaccard': JaccardSimilarity(),
            'cosine': CosineSimilarity(),
            'dice': DiceSimilarity(),
            'edit_sim': EditSimilarity(),
            'edit_dist': EditDistance()
        }
    
    def find_tau_min_overlap(self, *args):
        return self._sims[self.similarity].find_tau_min_overlap(*args)
    
    def find_min_size(self, *args):
        return self._sims[self.similarity].find_min_size(*args)
    
    def find_max_size(self, *args):
        return self._sims[self.similarity].find_max_size(*args)
    
    def find_lower_bound_of_entity(self, *args):
        return self._sims[self.similarity].find_lower_bound_of_entity(*args)
    
    def tighter_upper_window_size(self, *args):
        if self.similarity in ("edit_dist", "edit_sim"):
            raise AttributeError("Tighter upper window size is not supported with {}".format(self.similarity))
        return self._sims[self.similarity].tighter_upper_window_size(*args)
    
    def tighter_neighbor_bound(self, *args):
        if self.similarity not in ("edit_dist", "edit_sim"):
            raise AttributeError("Tighter neighbor bound is not supported with {}".format(self.similarity))
        return self._sims[self.similarity].tighter_neighbor_bound(*args)


# Actual similarity / distance scores


def jaccard(r_tokens, s_tokens):
    #
    # jaccard(r, s) = |r ∩ s| / |r ∪ s|
    #
    r_set = set(r_tokens)
    s_set = set(s_tokens)
    return len(r_set.intersection(s_set)) / len(r_set.union(s_set))


def cosine(r_tokens, s_tokens):
    #
    # cos(r, s) = |r ∩ s| / sqrt(|r| * |s|)
    #
    return len(set(r_tokens).intersection(s_tokens)) / math.sqrt(len(r_tokens) * len(s_tokens))


def dice(r_tokens, s_tokens):
    #
    # dice(r, s) = 2 * |r ∩ s| / |r| + |s|
    #
    return (2 * len(set(r_tokens).intersection(s_tokens))) / (len(r_tokens) + len(s_tokens))


def edit_dist(r_string, s_string):
    #
    # ED(r, s) = number of edit operations
    #
    return len(editops(r_string, s_string))


def edit_sim(r_string, s_string):
    #
    # EDS(r, s) = 1 - (ED(r, s) / max(len(r), len(s)))
    #
    return 1 - (edit_dist(r_string, s_string) / max(len(r_string), len(s_string)))


class Verify:
    
    @classmethod
    def check(cls, r, s, method, t):
        
        if method in ("jaccard", "cosine", "dice"):
        
            if not (isinstance(r, list) and isinstance(s, list)):
                raise ValueError("Both candidate and entity are expected to be list of tokens")
            
            if method == "jaccard":
                true_t = jaccard(r, s)
            elif method == "cosine":
                true_t = cosine(r, s)
            elif method == "dice":
                true_t = dice(r, s)
            
            valid = true_t >= t
            
            return valid, true_t
        
        elif method in ("edit_dist", "edit_sim"):
            
            if not (isinstance(r, str) and isinstance(s, str)):
                raise ValueError("Both candidate and entity are expected to be strings")
            
            if method == "edit_dist":
                true_t = edit_dist(r, s)
                valid = true_t <= t
            elif method == "edit_sim":
                true_t = edit_sim(r, s)
                valid = true_t >= t
            
            return valid, true_t
        
        else:
            raise ValueError("Invalid method %s" % method)
