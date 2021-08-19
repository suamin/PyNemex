"""
Faerie module.

Classes:
    - Faerie

"""

import math
import logging

from nemex import FaerieDataStructure, InvertedIndex, Similarity, EntitiesDictionary
from nemex import pruning
from nemex.utils import Pruner, Sim


logger = logging.getLogger(__name__)


class Faerie(FaerieDataStructure, Similarity):
    """Approximate dictionary-based entity extraction using Faerie.

    Faerie is an approximate dictionary-based entity extraction algorithm [1]_.
    It employs various filtering approaches to reduce the search space, both in
    entities and in documents' sub-strings. Faerie provides a unified approach
    to various similarity and distance functions with theoretical upper and lower
    bounds on overlaps. A combination of these bounds and appropriate data
    structures makes it an efficient algorithm. For details see [1]_.

    Parameters
    ----------
    entities_dict : :class:`~nemex.data.EntitiesDictionary`
        Instance of entities dictionary.

    similarity : str, {"cosine", "jaccard", "dice", "edit_dist", "edit_sim"}, optional
        Similarity function.

    t : float, optional
        Threshold value for the similarity function.

    q : int, optional
        Value of q-gram (required when ``similarity`` is "edit_dist" or "edit_sim").

    pruner : str, {"batch_count", "bucket_count", "lazy_count"}, optional
        Pruning method to apply before counting. If none provided, no pruning
        will be applied.

    See Also
    --------
    :class:`~nemex.data.FaerieDataStructure`
        Class that holds all data structures used in Faerie.

    :class:`~nemex.similarities.Similarity`
        Main similarity interface.

    References
    ----------
    .. [1] Li, G., Deng, D., & Feng, J. (2011, June). Faerie: efficient filtering algorithms
       for approximate dictionary-based entity extraction. In Proceedings of the 2011 ACM
       SIGMOD International Conference on Management of data (pp. 529-540). ACM.

    """

    def __init__(self, entities_dict: EntitiesDictionary, similarity: str = Sim.COSINE, t: float = 0.7, q: int = None,
                 pruner: str = Pruner.BATCH_COUNT):

        FaerieDataStructure.__init__(self, entities_dict)
        Similarity.__init__(self)

        # setup similarity interface
        if similarity in Sim.CHAR_BASED and q is None:
            raise ValueError("`q` is required for char-based similarity and distance methods")

        self.similarity = similarity

        if similarity != Sim.EDIT_DIST and (0.0 <= t > 1.0):
            raise ValueError("`t` must be in the range (0, 1] for similarity functions")

        self.t = t
        self.q = q
        
        # setup pruner
        if pruner == Pruner.BATCH_COUNT:
            self.pruner = pruning.BatchCountPruning

        elif pruner == Pruner.BUCKET_COUNT:
            self.pruner = pruning.BucketCountPruning

        elif pruner == Pruner.LAZY_COUNT:
            self.pruner = pruning.LazyCountPruning

        else:
            self.pruner = pruning.NoPruning

        self.prune_method = pruner
        
        # pre-compute length bounds
        self.init_bounds()

        self.min_Le = 0
        self.max_Te = 0

        # create inverted index
        self.inv_index = InvertedIndex.from_entities_dict(entities_dict)

        return
    
    def _compute_upper_lower_bounds(self, e_idx: int) -> (int, int):
        """Computes similarity function specific entity lower bound (denoted as
        ⊥e in paper) and upper bound (denoted as Te in paper) (Lemma 2). Used
        for considering valid substrings.

        Parameters
        ----------
        e_idx : int
            Entity id.

        Returns
        -------
        Lower and upper bounds of entity.

        """

        # get entity length
        dl = len(self.entities_dict[e_idx])
        
        if self.similarity == Sim.EDIT_SIM:
            Le = self.find_min_size(dl, self.t, self.q)
            Te = self.find_max_size(dl, self.t, self.q)
        else:
            Le = self.find_min_size(dl, self.t)
            Te = self.find_max_size(dl, self.t)
        
        # add inplace as entity's class attribute
        self.entities_dict[e_idx].Le = Le
        self.entities_dict[e_idx].Te = Te
        
        return Le, Te
    
    def _compute_overlap_lower_bound(self, e_idx: int) -> int:
        """Computes similarity function specific overlap lower bound,
        denoted as Tl in paper (Lemma 3). Used for Lazy-Count pruning.

        Parameters
        ----------
        e_idx : int
            Entity id.

        Returns
        -------
        Overlap lower bound of entity.

        """

        # get entity length
        dl = len(self.entities_dict[e_idx])
        
        if self.similarity in Sim.CHAR_BASED:
            Tl = self.find_lower_bound_of_entity(dl, self.t, self.q)
        else:
            Tl = self.find_lower_bound_of_entity(dl, self.t)
        
        # add inplace as entity's class attribute
        self.entities_dict[e_idx].Tl = Tl
        
        return Tl
    
    def init_bounds(self):
        """Computes valid substring upper and lower bounds for all entities (Te, ⊥e),
        their global versions (TE, ⊥E) and overlap similarity lower bound (Tl).

        """

        all_Le = list()
        all_Te = list()
        del_ents = list()
        
        for e_idx in self.entities_dict:
            Le, Te = self._compute_upper_lower_bounds(e_idx)
            Tl = self._compute_overlap_lower_bound(e_idx)
            if any(i < 0 for i in (Le, Te, Tl)):
                del_ents.append(e_idx)
            else:
                all_Le.append(Le)
                all_Te.append(Te)
        
        for e_idx in del_ents:
            del self.entities_dict[e_idx]

        self.min_Le = min(all_Le)  # T_E
        self.max_Te = max(all_Te)  # ⊥_E
        
        logger.info("Global length constraints with this dictionary : {} <= |s| <= {}".format(self.min_Le, self.max_Te))

        return
    
    def find_candidates(self, Pe: list, Le: int, Te: int, count_spans: list,
                        entity_len: int) -> (int, int):
        """Given candidate spans, find candidates.
        
        Parameters
        ----------
        Pe : list
            Position list of entity.

        Le : int
            Lower bound on length of valid substring.

        Te : int
            Upper bound on length of valid substring.

        count_spans : list
            List of start (i) and end (j) indexes in position list.
            Each element of these sub-lists (Pe_ij) will be used to
            count entity's occurrence in sub-strings.

        entity_len : int
            Length of entity. Required for calculating threshold `T`.
        
        See Also
        --------
        :meth:`~nemex.faerie.Faerie.check_overlap_similarity`
            Computes and compare min-tau overlap `T`.
        
        Yields
        ------
        Tuple of candidate start and end indexes in position list.
        
        Notes
        -----
        This method implements the methodology explained on pg. 535
        first column and first paragraph. For Pe[i. . .j], sub-strings 
        containing tokens in D[pi. . .pj] can be candidates of e. The
        sub-strings in D[p_start. . .p_end] should only be checked, where
        max(pj - Te + 1, p_i-1 + 1) = lo <= p_start <= pi and
        pj <= p_end <= up = min(pi + Te - 1, p_j+1 - 1). If final constraints
        of ⊥e <= |s| = p_end − p_start + 1 <= Te and |e ∩ s| >= T are
        met, D[p_start. . .p_end] is a final candidate.
        
        """

        candidates = list()
        count_positions = set()
        
        for i, j in count_spans:
            # positions that should be counted
            count_positions.update(Pe[i-1:j])

            pi, pj = Pe[i-1], Pe[j-1]
            Pe_ij = Pe[i-1:j]
            
            logger.debug("Candidate Window : Pe[{}. . .{}] ; Pe_ij = {} ; pi={}, pj={}".format(i, j, Pe_ij, pi, pj))
            
            # edge case when pi is start of list
            if i-1 == 0:
                pi_prev = -math.inf
            else:
                pi_prev = Pe[i-2]
            
            # edge case when pj is last of list
            if j == len(Pe):
                pj_next = math.inf
            else:
                pj_next = Pe[j]
            
            # pg. 535, left column 2 para
            # ``lo`` goes to minus sometimes! that's why clamping to 0
            lo = max(0, max(pj - Te + 1, pi_prev + 1))
            up = min(pi + Te - 1, pj_next - 1)
            
            for p_start in range(lo, pi+1):                     # lo <= p_start <= pi
                for p_end in range(pj, up+1):                   # pj <= p_end <= up
                    s_len = p_end - p_start + 1                 # |s| = |D[p_start · · · p_end ]| 
                    if Le <= s_len <= Te:                       # ⊥e ≤ |s| ≤ Te
                        candidates.append((p_start, s_len))
        
        # do the actual counting
        for pk in count_positions:
            self.count(pk, Le, Te)
        
        # note that this should be outside the previous loop to allow counts
        # to be fully updated before this pruning step is applied
        for candidate_start, candidate_len in candidates:
            # if |e ∩ s| >= T (where overlap size is estimated by count array)
            if self.check_overlap_similarity(candidate_start, candidate_len, entity_len):
                yield candidate_start, candidate_len

        return
    
    def check_overlap_similarity(self, candidate_start: int, candidate_len: int, entity_len: int) -> bool:
        """Computes the overlap similarity threshold `T` and compares with entity's count occurrence.

        Parameters
        ----------
        candidate_start : int
            TODO: Documentation
        candidate_len : int
            TODO: Documentation
        entity_len : int
            TODO: Documentation

        Returns
        -------
        TODO: Documentation

        """
        
        # compute overlap similarity threshold
        if self.similarity in Sim.CHAR_BASED:
            T = self.find_tau_min_overlap(entity_len, candidate_len, self.t, self.q)
        else:
            T = self.find_tau_min_overlap(entity_len, candidate_len, self.t)

        count_overlap = self.V[candidate_start][candidate_len]
        
        return count_overlap >= T
    
    def __call__(self, doc_tokens):
        """Main Faerie algorithm (cf. Algorithm 2. in [1]_).
        
        See Also
        --------
        :meth:`~nemex.data.FaerieDataStructure.step`
            A convenience method around single Faerie update.

        Yields
        -------
        Minimal entity with its start and end position.
        
        """

        # get inverted lists of doc tokens
        inv_lists = self.inv_index[doc_tokens]
        
        # if we don't match any token of document to any of entities'
        if len(inv_lists) == 0:
            logger.info("No matching tokens found!")
            return dict()
        
        # initialize faerie data-structures
        self.init_from_inv_lists(inv_lists)

        # initial minimal entity
        e = self.heap[0]
        Pe = list()

        # counter for number of iterations (should be equal to sum(length of inv. lists))
        i = 0

        # the sequence of elements popped from heap (should be ascending and 
        # consecutive e.g. [0,0,0,1,1,2,2,2,3,3,...])
        pop_sequence = list()
        
        while True:
            '''
            take faerie step
            we use ``stop`` as flag to break the loop because
            while len(self.heap) > 0 does not process last entity
            '''
            ei, pi, stop = self.step(e)
            
            pop_sequence.append(ei)
            
            '''
            while we have same entity, we keep popping it to build position list
            cf. pg 535 first column, first paragraph on Complexity
            '''
            if ei == e:
                Pe.append(pi)

            # else we see a new entity
            else:

                # this should be equal to pre-computed list
                assert Pe == self.ent2positions[e], \
                    "Invalid position list, expected `{}` but collected `{}`".format(self.ent2positions[e], Pe)
                
                '''
                get entity specific attributes
                note: len of entity is also pre-computed
                '''
                entity = self.entities_dict[e]
                entity_len = len(entity)
                Le, Te, Tl = entity.Le, entity.Te, entity.Tl
                logger.debug("Analyzing e={} (id={}) Pe={} ⊥e={} Te={} Tl={}".format(entity, e, Pe, Le, Te, Tl))
                
                # here we set pruning arguments
                # first common args
                pruner_args = (Pe, Le, Te, Tl,)
                
                # "batch_count" has tighter upper bounds on window size for jaccard,
                # dice and cosine which needs to be taken care of (cf. last lines pg. 534)
                if self.prune_method == Pruner.BATCH_COUNT:
                    pruner_args = pruner_args + (self.tighter_upper_window_size, entity_len, self.t)

                # "bucket_count" has tighter neighbor difference bounds for edit distance
                # and similarity which needs to be taken care of (cf. pg. 534 first column 5th para)
                elif self.prune_method == Pruner.BUCKET_COUNT:

                    if self.similarity == Sim.EDIT_SIM:
                        bound_args = (entity_len, self.t, self.q)

                    elif self.similarity == Sim.EDIT_DIST:
                        bound_args = (self.t, self.q)

                    else:
                        bound_args = ()

                    pruner_args = pruner_args + (self.tighter_neighbor_bound, *bound_args)
                
                # apply pruning techniques to count entity's occurrence in filtered candidates only
                count_spans = self.pruner.filter(*pruner_args)

                # further prune to get final candidates
                candidate_spans = self.find_candidates(Pe, Le, Te, count_spans, entity_len)
                
                for start, length in candidate_spans:
                    i, j = start, start + length - 1
                    yield e, (i, j)
                
                # make new (different) entity as current entity
                e = ei
                Pe = [pi]

                # reset count array as well
                self.reset_count()
            
            i += 1
            if stop:
                break
        
        logger.debug("Total iterations: {}".format(i))
        logger.debug("Heap-popped elements sequence: {}".format(pop_sequence[:-1]))

        return
