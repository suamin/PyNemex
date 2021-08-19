"""
Similarities module.

Classes:
    - JaccardSimilarity
    - CosineSimilarity
    - DiceSimilarity
    - EditSimilarity
    - EditDistance
    - Similarity
    - Verify

"""

import math

from Levenshtein import editops
from nemex.utils import Sim


class JaccardSimilarity:
    """Jaccard Similarity class.

    This class provides the unified methods for the 'Jaccard Similarity' algorithm.

    """
    
    @staticmethod
    def find_tau_min_overlap(entity_len: int, string_len: int, delta: float) -> float:
        """Computes the overlap similarity threshold T.
        (cf. page 530, right column)

        T = ⌈ (|e| + |s|) * δ/(1 + δ) ⌉ <= |e ∩ s|

        Parameters
        ----------
        entity_len : int
            Length of dictionary entity, i.e., number of tokens.
        string_len : int
            Length of document substring, i.e., number of tokens.
        delta : float
           Similarity threshold.

        Returns
        -------
        Overlap similarity threshold T.

        """

        return math.ceil((entity_len + string_len) * (delta / (1 + delta)))

    @staticmethod
    def find_min_size(entity_len: int, delta: float) -> float:
        """Computes the lower bound ⊥e.
        (cf. page 531, left column)

        ⊥e = ⌈ |e| * δ ⌉ <= |s|

        Parameters
        ----------
        entity_len : int
            Length of dictionary entity, i.e., number of tokens.
        delta : float
            Similarity threshold.

        Returns
        -------
        Lower bound ⊥e for number of tokens.

        """

        return math.ceil(entity_len * delta)

    @staticmethod
    def find_max_size(entity_len: int, delta: float) -> float:
        """Computes the upper bound ⊤e.
        (cf. page 531, left column)

        ⊤e = ⌊ |e| / δ ⌋ >= |s|

        Parameters
        ----------
        entity_len : int
            Length of dictionary entity, i.e., number of tokens.
        delta : float
            Edit distance threshold.

        Returns
        -------
        Upper bound ⊤e for number of tokens.

        """

        return math.floor(entity_len / delta)

    @staticmethod
    def find_lower_bound_of_entity(entity_len: int, delta: float) -> float:
        """Computes lower overlap similarity threshold T, i.e., Tl.
        (cf. page 533, right column)

        Tl = ⌈ |e| * δ ⌉

        Parameters
        ----------
        entity_len : int
            Length of dictionary entity, i.e., number of tokens.
        delta : float
            Similarity threshold.

        Returns
        -------
        Lower overlap similarity threshold Tl.

        """

        return math.ceil(entity_len * delta)

    @staticmethod
    def tighter_upper_window_size(entity_len: int, Pe_ij_len: int, delta: float) -> float:
        """Computes a tighter upper window size for document D.
        (cf. page 534, right column)

        ⊥e <= |D[pi...pj]| <= min(|e|, |P_e[i...j]|) / δ = ⊤e

        Parameters
        ----------
        entity_len : int
            Length of dictionary entity, i.e., number of tokens.
        Pe_ij_len : int
            Length of sorted position list.
        delta : float
            Similarity threshold.

        Returns
        -------
        Tighter upper window size ⊤e.

        """

        return math.floor(min(entity_len, Pe_ij_len) / delta)


class CosineSimilarity:
    """Cosine Similarity class.

    This class provides the unified methods for the 'Cosine Similarity' algorithm.

    """
    
    @staticmethod
    def find_tau_min_overlap(entity_len: int, string_len: int, delta: float) -> float:
        """Computes the overlap similarity threshold T.
        (cf. page 530, right column)

        T = ⌈ (|e| * |s|)^(0.5) * δ ⌉ <= |e ∩ s|

        Parameters
        ----------
        entity_len : int
            Length of dictionary entity, i.e., number of tokens.
        string_len : int
            Length of document substring, i.e., number of tokens.
        delta : float
            Similarity threshold.

        Returns
        -------
        Overlap similarity threshold T.

        """

        return math.ceil(math.sqrt(entity_len * string_len) * delta)
    
    @staticmethod
    def find_min_size(entity_len: int, delta: float) -> float:
        """Computes the lower bound ⊥e.
        (cf. page 531, left column)

        ⊥e = ⌈ |e| * δ^2 ⌉

        Parameters
        ----------
        entity_len : int
            Length of dictionary entity, i.e., number of tokens.
        delta : float
            Similarity threshold.

        Returns
        -------
        Lower bound ⊥e for number of tokens.

        """

        return math.ceil(entity_len * delta**2)
    
    @staticmethod
    def find_max_size(entity_len: int, delta: float) -> float:
        """Computes the upper bound Te.
        (cf. page 531, left column)

        ⊤e = ⌊ |e| / δ^2 ⌋

        Parameters
        ----------
        entity_len : int
            Length of dictionary entity, i.e., number of tokens.
        delta : float
            Similarity threshold.

        Returns
        -------
        Upper bound ⊤e for number of tokens.

        """

        return math.floor(entity_len / delta**2)
    
    @staticmethod
    def find_lower_bound_of_entity(entity_len: int, delta: float) -> float:
        """Computes lower overlap similarity threshold T, i.e., Tl.
        (cf. page 533, right column)

        Tl = ⌈ |e| * δ^2 ⌉

        Parameters
        ----------
        entity_len : int
            Length of dictionary entity, i.e., number of tokens.
        delta : float
            Similarity threshold.

        Returns
        -------
        Lower overlap similarity threshold Tl.

        """

        return math.ceil(entity_len * delta**2)
    
    @staticmethod
    def tighter_upper_window_size(entity_len: int, Pe_ij_len: int, delta: float) -> float:
        """Computes a tighter upper window size for document D.
        (cf. page 534, right column)

        ⊥e <= |D[pi...pj]| <= min(|e|, |P_e[i...j]|) / (δ^2)

        Parameters
        ----------
        entity_len : int
            Length of dictionary entity, i.e., number of tokens.
        Pe_ij_len : int
            Length of sorted position list.
        delta : float
            Similarity threshold.

        Returns
        -------
        Tighter upper window size.

        """

        return math.floor(min(entity_len, Pe_ij_len) / delta**2)


class DiceSimilarity:
    """Dice Similarity class.

    This class provides the unified methods for the 'Dice Similarity' algorithm.

    """
    
    @staticmethod
    def find_tau_min_overlap(entity_len: int, string_len: int, delta: float) -> float:
        """Computes the overlap similarity threshold T.
        (cf. page 530, right column)

        T = ⌈ (|e| + |s|) * (δ / 2) ⌉ <= |e ∩ s|

        Parameters
        ----------
        entity_len : int
            Length of dictionary entity, i.e., number of tokens.
        string_len : int
            Length of document substring, i.e., number of tokens.
        delta : float
            Similarity threshold.

        Returns
        -------
        Overlap similarity threshold T.

        """

        return math.ceil((entity_len + string_len) * (delta / 2))
    
    @staticmethod
    def find_min_size(entity_len: int, delta: float) -> float:
        """Computes the lower bound ⊥e.
        (cf. page 531, left column)

        ⊥e = ⌈ |e| * (δ / (2 - δ)) ⌉

        Parameters
        ----------
        entity_len : int
            Length of dictionary entity, i.e., number of tokens.
        delta : float
            Similarity threshold.

        Returns
        -------
        Lower bound ⊥e for number of tokens.

        """

        return math.ceil(entity_len * (delta / (2 - delta)))
    
    @staticmethod
    def find_max_size(entity_len: int, delta: float) -> float:
        """Computes the upper bound ⊤e.
        (cf. page 531, left column)

        ⊤e = ⌊ |e| * ((2 - δ) / δ) ⌋

        Parameters
        ----------
        entity_len : int
            Length of dictionary entity, i.e., number of tokens.
        delta : float
            Similarity threshold.

        Returns
        -------
        Upper bound ⊤e for number of tokens.

        """

        return math.floor(entity_len * ((2 - delta) / delta))
    
    @staticmethod
    def find_lower_bound_of_entity(entity_len: int, delta: float) -> float:
        """Computes lower overlap similarity threshold T, i.e., Tl.
        (cf. page 533, right column)

        Tl = ⌈ |e| * (δ / (2 - δ)) ⌉

        Parameters
        ----------
        entity_len : int
            Length of dictionary entity, i.e., number of tokens.
        delta : float
            Similarity threshold.

        Returns
        -------
        Lower overlap similarity threshold Tl.

        """

        return math.ceil(entity_len * (delta / (2 - delta)))
    
    @staticmethod
    def tighter_upper_window_size(entity_len: int, Pe_ij_len: int, delta: float) -> float:
        """Computes a tighter upper window size for document D.
        (cf. page 534, right column)

        ⊥e <= |D[pi...pj]| <= min(|e|, |P_e[i...j]|) * ((2 - δ) / δ)

        Parameters
        ----------
        entity_len : int
            Length of dictionary entity, i.e., number of tokens.
        Pe_ij_len : int
            Length of sorted position list.
        delta : float
            Similarity threshold.

        Returns
        -------
        Tighter upper window size.

        """

        return math.floor(min(entity_len, Pe_ij_len) * ((2 - delta) / delta))


class EditSimilarity:
    """Edit Similarity class.

    This class provides the unified methods for the 'Edit Similarity' algorithm.

    """

    @staticmethod
    def find_tau_min_overlap(entity_len: int, string_len: int, delta: float, q: int) -> float:
        """Computes the overlap similarity threshold T.
        (cf. page 530, right column)

        T = ⌈ max(|e|,|s|) - (max(|e|,|s|) + q - 1) * (1 - δ) * q ⌉ <= |e ∩ s|

        Parameters
        ----------
        entity_len : int
            Length of dictionary entity, i.e., number of tokens.
        string_len: int
            Length of document substring, i.e., number of tokens.
        delta : float
            Similarity threshold.
        q : int
            Token size.

        Returns
        -------
        Overlap similarity threshold.

        """
        if q > entity_len or q > string_len:
            raise ValueError("Token size q must be smaller or equal entity/string length |e|.")

        return math.ceil(max(entity_len, string_len) - ((max(entity_len, string_len) + q - 1) * (1 - delta) * q))
    
    @staticmethod
    def find_min_size(entity_len: int, delta: float, q: int) -> float:
        """Computes the lower bound ⊥e.
        (cf. page 531, left column)

        ⊥e = ⌈ ((|e| + q - 1) * δ) - (q - 1) ⌉

        Parameters
        ----------
        entity_len : int
            Length of dictionary entity, i.e., number of tokens.
        delta : int
            Similarity threshold.
        q : int
            Token size.

        Returns
        -------
        Lower bound ⊥e for number of tokens.

        """
        if q > entity_len:
            raise ValueError("Token size q must be smaller or equal entity length |e|.")

        return math.ceil(((entity_len + q - 1) * delta) - (q - 1))
    
    @staticmethod
    def find_max_size(entity_len: int, delta: float, q: int) -> float:
        """Computes the upper bound ⊤e.
        (cf. page 531, left column)

        ⊤e = ⌊ ((|e| + q - 1) / δ) - (q - 1) ⌋

        Parameters
        ----------
        entity_len : int
            Length of dictionary entity, i.e., number of tokens.
        delta : float
            Similarity threshold.
        q : int
            Token size.

        Returns
        -------
        Upper bound ⊤e for number of tokens.

        """
        if q > entity_len:
            raise ValueError("Token size q must be smaller or equal entity length |e|.")

        return math.floor(((entity_len + q - 1) / delta) - (q - 1))
    
    @staticmethod
    def find_lower_bound_of_entity(entity_len: int, delta: float, q: int) -> float:
        """Computes lower overlap similarity threshold T, i.e., Tl.
        (cf. page 533, right column)

        Tl = ⌈ |e| - ((|e| + q - 1) * ((1 - δ) / δ) * q) ⌉

        Parameters
        ----------
        entity_len : int
            Length of dictionary entity, i.e., number of tokens.
        delta : float
            Similarity threshold.
        q : int
            Token size.

        Returns
        -------
        Lower overlap similarity threshold Tl.

        """
        if q > entity_len:
            raise ValueError("Token size q must be smaller or equal entity length |e|.")

        return math.ceil(entity_len - ((entity_len + q - 1) * ((1 - delta) / delta) * q))
    
    @staticmethod
    def tighter_neighbor_bound(entity_len: int, delta: float, q: int) -> float:
        """Computes the threshold for pruning neighbouring tokens.
        If below condition holds, neighbouring tokens pi+1 and pi are pruned.
        (cf. page 534, left column)

        pi+1 - pi - 1 > ⌊ ((|e| + q - 1) / δ) * (1 - δ) * q ⌋

        Parameters
        ----------
        entity_len : int
            Length of dictionary entity, i.e., number of tokens.
        delta : float
            Similarity threshold.
        q : int
            Token size.

        Returns
        -------
        Pruning threshold.

        """
        if q > entity_len:
            raise ValueError("Token size q must be smaller or equal entity length |e|.")

        return math.floor(((entity_len + q - 1) / delta) * (1 - delta) * q)


class EditDistance:
    """Edit Distance class.

    This class provides the unified methods for the 'Edit Distance' algorithm.

    """
    
    @staticmethod
    def find_tau_min_overlap(entity_len: int, string_len: int, tau: int, q: int) -> int:
        """Computes the overlap similarity threshold T.
        (cf. page 530, right column)

        T = max(|e|, |s|) - (τ * q) <= |e ∩ s|

        Parameters
        ----------
        entity_len : int
            Length of dictionary entity, i.e., number of tokens.
        string_len : int
            Length of document substring, i.e., number of tokens.
        tau : int
            Edit distance threshold.
        q : int
            Token size.

        Returns
        -------
        Overlap similarity threshold.

        """
        if q > entity_len or q > string_len:
            raise ValueError("Token size q must be smaller or equal entity/string length |e|.")
        elif tau > entity_len or tau > string_len:
            raise ValueError("Edit distance threshold τ must be smaller or equal entity/string length |e|.")

        return max(entity_len, string_len) - (tau * q)

    @staticmethod
    def find_min_size(entity_len: int, tau: int) -> int:
        """Computes the lower bound ⊥e.
        (cf. page 531, left column)

        ⊥e = |e| - τ

        Parameters
        ----------
        entity_len : int
            Length of dictionary entity, i.e., number of tokens.
        tau : int
            Edit distance threshold.

        Returns
        -------
        Lower bound ⊥e for number of tokens.

        """
        if tau > entity_len:
            raise ValueError("Edit distance threshold τ must be smaller or equal entity length |e|.")

        return entity_len - tau

    @staticmethod
    def find_max_size(entity_len: int, tau: int) -> int:
        """Computes the upper bound ⊤e.
        (cf. page 531, left column)

        ⊤e = |e| + τ

        Parameters
        ----------
        entity_len : int
            Length of dictionary entity, i.e., number of tokens.
        tau : int
            Edit distance threshold.

        Returns
        -------
        Upper bound ⊤e for number of tokens.

        """
        if tau > entity_len:
            raise ValueError("Edit distance threshold τ must be smaller or equal entity length |e|.")

        return entity_len + tau
    
    @staticmethod
    def find_lower_bound_of_entity(entity_len: int, tau: int, q: int) -> int:
        """Computes lower overlap similarity threshold T, i.e., Tl.
        (cf. page 533, right column)

        Tl = |e| - (τ * q)

        Parameters
        ----------
        entity_len : int
            Length of dictionary entity, i.e., number of tokens.
        tau : int
            Edit distance threshold.
        q : int
            Token size.

        Returns
        -------
        Lower overlap similarity threshold Tl.

        """
        if q > entity_len:
            raise ValueError("Token size q must be smaller or equal entity length |e|.")
        elif tau > entity_len:
            raise ValueError("Edit distance threshold τ must be smaller or equal entity length |e|.")

        return entity_len - (tau * q)
    
    @staticmethod
    def tighter_neighbor_bound(tau: int, q: int) -> int:
        """Computes the threshold for pruning neighbouring tokens.
        If below condition holds, neighbouring tokens pi+1 and pi are pruned.
        (cf. page 534, left column)

        pi+1 - pi - 1 > τ * q

        Parameters
        ----------
        tau : int
            Edit distance threshold.
        q : int
            Token size.

        Returns
        -------
        Pruning threshold.

        """

        return tau * q


class Similarity:
    """Similarity class.

    This class provides the unified methods for multiple similarity algorithms.

    """

    def __init__(self):
        self.similarity = None
        self._sims = {
            Sim.JACCARD: JaccardSimilarity(),
            Sim.COSINE: CosineSimilarity(),
            Sim.DICE: DiceSimilarity(),
            Sim.EDIT_SIM: EditSimilarity(),
            Sim.EDIT_DIST: EditDistance()
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
        if self.similarity in Sim.CHAR_BASED:
            raise AttributeError("Tighter upper window size is not supported with {}".format(self.similarity))
        return self._sims[self.similarity].tighter_upper_window_size(*args)
    
    def tighter_neighbor_bound(self, *args):
        if self.similarity not in Sim.CHAR_BASED:
            raise AttributeError("Tighter neighbor bound is not supported with {}".format(self.similarity))
        return self._sims[self.similarity].tighter_neighbor_bound(*args)


'''
Actual similarity / distance scores
'''


def jaccard(r_tokens: list, s_tokens: list) -> float:
    """Computes jaccard similarity.

    JAC(r, s) = |r ∩ s| / |r ∪ s|

    Parameters
    ----------
    r_tokens : list
        First token list.
    s_tokens : list
        Second token list.

    Returns
    -------
    Jaccard similarity of r and s.

    """

    r_set = set(r_tokens)
    s_set = set(s_tokens)
    return len(r_set.intersection(s_set)) / len(r_set.union(s_set))


def cosine(r_tokens: list, s_tokens: list) -> float:
    """Computes cosine similarity.

    COS(r, s) = |r ∩ s| / sqrt(|r| * |s|)

    Parameters
    ----------
    r_tokens : list
        First token list.
    s_tokens : list
        Second token list.

    Returns
    -------
    Cosine similarity of r and s.

    """

    return len(set(r_tokens).intersection(s_tokens)) / math.sqrt(len(r_tokens) * len(s_tokens))


def dice(r_tokens: list, s_tokens: list) -> float:
    """Computes dice similarity.

    DICE(r, s) = 2 * |r ∩ s| / |r| + |s|

    Parameters
    ----------
    r_tokens : list
        First token list.
    s_tokens : list
        Second token list.

    Returns
    -------
    Dice similarity of r and s.

    """

    return (2 * len(set(r_tokens).intersection(s_tokens))) / (len(r_tokens) + len(s_tokens))


def edit_dist(r_string: str, s_string: str) -> int:
    """Computes edit distance.

    ED(r, s) = number of edit operations

    Parameters
    ----------
    r_string : str
        First string.
    s_string : str
        Second string.

    Returns
    -------
    Edit distance of r and s.

    """

    return round(len(editops(r_string, s_string)), 3)


def edit_sim(r_string: str, s_string: str) -> float:
    """Computes edit similarity.

    EDS(r, s) = 1 - (ED(r, s) / max(len(r), len(s)))

    Parameters
    ----------
    r_string : str
        First input string.
    s_string : str
        Second input string.

    Returns
    -------
    Edit similarity of r and s.

    """

    return round(1 - (edit_dist(r_string, s_string) / max(len(r_string), len(s_string))), 3)


class Verify:
    """Verification class.

    This class models the verification step in the 'Filter-and-Verify' framework.
    In the verify step, the candidate pairs are verified by computing the real similarity/dissimilarity.

    """

    @classmethod
    def check(cls, r, s, method: str, t: float) -> (bool, float):
        """Verifies whether the candidates from the unified framework (i.e. overlap similarity)
        are valid candidates (i.e. based on their true similarity).

        Parameters
        ----------
        r :
            Tokens of dictionary entity. Token representation depends on similarity method.
        s :
            Tokens of document string. Token representation depends on similarity method.
        method : str
            Similarity method.
        t : float
            Overlap similarity threshold.

        Returns
        -------
        1. Whether the true similarity is greater-equal the overlap similarity.
        2. The true similarity.

        """

        true_t: float = 0.0
        valid: bool = False

        if method in Sim.TOKEN_BASED:
        
            if not (isinstance(r, list) and isinstance(s, list)):
                raise ValueError("Both candidate and entity are expected to be list of tokens")
            
            if method == Sim.JACCARD:
                true_t = jaccard(r, s)
            elif method == Sim.COSINE:
                true_t = cosine(r, s)
            elif method == Sim.DICE:
                true_t = dice(r, s)
            
            valid = true_t >= t
            
            return valid, true_t
        
        elif method in Sim.CHAR_BASED:
            
            if not (isinstance(r, str) and isinstance(s, str)):
                raise ValueError("Both candidate and entity are expected to be strings")
            
            if method == Sim.EDIT_DIST:
                true_t = edit_dist(r, s)
                valid = true_t <= t
            elif method == Sim.EDIT_SIM:
                true_t = edit_sim(r, s)
                valid = true_t >= t
            
            return valid, true_t
        
        else:
            raise ValueError("Invalid method %s" % method)
