"""
Pruning module.

Classes:
    - NoPruning
    - LazyCountPruning
    - BucketCountPruning
    - BatchCountPruning

"""

import math
import logging


logger = logging.getLogger(__name__)


class NoPruning:
    """No Pruning class.

    Does not perform any pruning.

    """

    @classmethod
    def filter(cls,
               Pe: list,
               Le: int,
               Te: int,
               *args
               ) -> None:
        """Does not perform any pruning.

        Parameters
        ----------
        Pe : list
            Sorted position list.
        Le : int
            Lower bound of |s| = |G(s)| (number of s's q-grams).
        Te : int
            Upper bound of |s| = |G(s)| (number of s's q-grams).
        args :
            More arguments.

        Yields
        -------
        Count spans: start (i) and end (j) indexes in position list (Pe).

        """

        for i in range(1, len(Pe)+1):
            for j in range(i+1, len(Pe)+1):
                yield i, j

        return


class LazyCountPruning:
    """Lazy-Count Pruning class.

    Performs Lazy-Count Pruning:
     - Condition: |Pe| < Tl <= T (Lemma 3)

    """

    @classmethod
    def filter(cls,
               Pe: list,
               Le: int,
               Te: int,
               Tl: int,
               *args
               ) -> None:
        """Searches invalid windows using Lazy-Count Pruning.

        1. Count e's occurrence number (len(Pe)).
        2. If occurrence number < Tl, then the entity is pruned.

        Parameters
        ----------
        Pe : list
            Sorted position list.
        Le : int
            Lower bound of |s| = |G(s)| (number of s's q-grams).
        Te : int
            Upper bound of |s| = |G(s)| (number of s's q-grams).
        Tl : int
            Lower bound of shared tokens between e and s (lazy-count bound).
        args:
            More arguments.

        Yields
        -------
        Start and end position of invalid (removable) window.

        """

        if len(Pe) >= Tl:
            yield from NoPruning.filter(Pe, Le, Te)


class BucketCountPruning:
    """Bucket-Count Pruning class.

    Performs Bucket-Count Pruning:
     - 1. Perform Lazy-Count Pruning
     - 2.

    """

    @classmethod
    def filter(cls,
               Pe: list,
               Le: int,
               Te: int,
               Tl: int,
               tighter_bound_func,
               *bound_args
               ) -> None:
        """Searches count spans using Bucket Count Pruning.

        TODO: No partitioning? --> size(bucket) < Tl, then prune elements in bucket
        TODO: Check condition? --> (j - i + 1 >= Tl)
        TODO:

        Parameters
        ----------
        Pe : list
            Sorted position list.
        Le : int
            Lower bound of |s| = |G(s)| (number of s's q-grams).
        Te : int
            Upper bound of |s| = |G(s)| (number of s's q-grams).
        Tl  : int
            Lower bound of shared tokens between e and s (lazy-count bound)
        tighter_bound_func :
            Tighter bound function for edit distance and edit similarity.
        bound_args :
            Tighter bound function arguments.

        Yields
        -------
        Start (i) and end (j) indexes of sublists of Pe.

        """

        # lazy-count pruning: |Pe| < Tl <= T (Lemma 3)
        # TODO: why condition for 'No Pruning' ?
        if len(Pe) >= Tl:

            try:
                Te_diff_Tl = tighter_bound_func(*bound_args)

            # tighter bound is not supported for jaccard, cosine and dice -- uses Te - Tl
            except Exception:
                Te_diff_Tl = Te - Tl

            # partitioning
            for i, j in cls.iter_bucket_spans(Pe, Te_diff_Tl):

                # Check length of bucket
                # TODO: Reuse existing class: yield from LazyCountPruning.filter(Pe[i:j], Le, Te, Tl)
                if j - i + 1 >= Tl:
                    yield i, j

    @classmethod
    def iter_bucket_spans(cls,
                          Pe: list,
                          t: int
                          ):
        """Iterate over position list (Pe).

        1. Loop over position list (Pe)
            a. Get neighbour positions pi, pj
            b.
            c. Move to next neighbours

        If p_(i+1) - p_i - 1 > t, create new partition.
        Threshold t may vary for different similarity functions.

        TODO: Check condition? --> (pj - pi + 1 > t) --> (pj - pi - 1 > t)

        Parameters
        ----------
        Pe : list
            Sorted position list.
        t : int
            Threshold for partitioning.

        Yields
        -------
        Start and end position of current bucket window.

        """

        # neighbour indexes
        i, j = 1, 2

        # bucket indexes (Pe[k;l])
        k = i
        l = i

        while True:

            try:
                # get elements
                pi, pj = Pe[i-1], Pe[j-1]

            # check for end of position list
            except IndexError:

                # last position
                l = i

                # return bucket indexes
                yield k, l

                # end
                break

            else:
                # TODO: Check paper for correct formulae
                # condition for new bucket
                if pj - pi + 1 > t:

                    # last position
                    l = i
                    yield k, l

                    # create new bucket
                    k = j

            # move span by 1
            i += 1
            j += 1


class BatchCountPruning:
    """Batch-Count Pruning class.

    Performs Batch-Count pruning:
     - Condition:

    """

    @classmethod
    def filter(cls,
               Pe: list,
               Le: int,
               Te: int,
               Tl: int,
               tighter_bound_func,
               *bound_args
               ) -> None:
        """Searches invalid window using Batch-Count Pruning.

        Parameters
        ----------
        Pe : list
            Sorted position list.
        Le : int
            Lower bound of |s| = |G(s)| (number of s's q-grams).
        Te : int
            Upper bound of |s| = |G(s)| (number of s's q-grams).
        Tl : int
            Lower bound of shared tokens between e and s (lazy-count bound).
        tighter_bound_func :
            Tighter bound function for edit distance and edit similarity.
        bound_args :
            Tighter bound function arguments.

        Returns
        -------
        Start and end position of the candidate window.

        """

        # lazy-count pruning: |Pe| <= Tl < T (Lemma 3)
        if len(Pe) >= Tl:

            # find possible candidate windows using ``binary_span`` and ``binary_shift``
            for i, j in cls.iter_possible_candidate_windows(Pe, Te, Tl):

                try:
                    # |e|, |Pe[i. . .j]|, t
                    tighter_Te = tighter_bound_func(bound_args[0], j-i+1, bound_args[1])

                except Exception as e:
                    logger.info(e)

                    # tighter bound is not supported for edit distance and similarity -- uses Te
                    tighter_Te = Te

                # check if possible candidate window is an actual candidate window
                if cls.check_possible_candidate_window(i, j, Pe, Le, Te, Tl, tighter_Te):

                    # return the span for counting
                    yield i, j

    @classmethod
    def check_possible_candidate_window(cls,
                                        i: int,
                                        j: int,
                                        Pe: list,
                                        Le: int,
                                        Te: int,
                                        Tl: int,
                                        tighter_Te: int = None
                                        ) -> bool:
        """Checks whether a window is a ``possible candidate window''.

        Parameters
        ----------
        i : int
            Window start position.
        j : int
            Window end position.
        Pe : list
            Sorted position list.
        Le : int
            Lower bound of |s| = |G(s)| (number of s's q-grams).
        Te : int
            Upper bound of |s| = |G(s)| (number of s's q-grams).
        Tl : int
            Lower bound of shared tokens between e and s (lazy-count bound).
        tighter_Te : int
            Even tighter upper bound Te.

        Returns
        -------
        True, if window is ``possible candidate window''.

        """

        # (j-1)+1 = j (-1 due to 0-based indexing and +1 because python list is non-inclusive)
        Pe_ij = Pe[i-1:j]

        # this is redundant to check because it is made sure by ``find_possible_candidate_spans``
        # valid window: make sure that we have a valid window (cf. Definition 3, condition 1)
        if Tl <= len(Pe_ij) <= Te:
            pi = Pe[i-1]
            pj = Pe[j-1]

            if tighter_Te is None:
                tighter_Te = Te

            # candidate window: make sure we have a candidate window (cf. Definition 3, condition 2)
            if Le <= pj - pi + 1 <= tighter_Te:
                return True

        return False

    @classmethod
    def iter_possible_candidate_windows(cls,
                                        Pe: list,
                                        Te: int,
                                        Tl: int
                                        ):
        """TODO: Documentation

        Parameters
        ----------
        Pe : list
            Sorted position list.
        Te : int
            Upper bound of |s| = |G(s)| (number of s's q-grams).
        Tl : int
            Lower bound of shared tokens between e and s (lazy-count bound).

        Yields
        -------
        TODO: Documentation

        """

        i = 1
        while i <= len(Pe) - Tl + 1:

            # pg. 535 left column, last line (initially Pe[1,..,Tl])
            j = i + Tl - 1

            # 0 based indexing; add -1
            pj, pi = Pe[j-1], Pe[i-1]

            # length for substring |D[pi...pj]| = pj-pi+1 is not larger than upper bound
            if (pj - pi + 1) <= Te:

                # we have a valid substring with size, Tl ≤ |Pe[i · · · j]| ≤ Te
                # Hence, find candidate window ⊥e ≤ |D[pi · · · pj]| ≤ Te
                mid = cls.binary_span(i, j, Pe, Te)
                yield i, mid
                i += 1
            else:

                # candidate windows are too long
                i = cls.binary_shift(i, j, Pe, Te, Tl)

    @classmethod
    def binary_shift(cls,
                     i: int,
                     j: int,
                     Pe: list,
                     Te: int,
                     Tl: int
                     ):
        """Performs binary shift on position list Pe.

        Parameters
        ----------
        i : int
            Window start position.
        j : int
            Window end position.
        Pe : list
            Sorted position list.
        Te : int
            Upper bound of |s| = |G(s)| (number of s's q-grams).
        Tl : int
            Lower bound of shared tokens between e and s (lazy-count bound).

        Returns
        -------
        Lower bound of shifted window.

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

        # if j jumps over, clip it to the length of position list
        if j > len(Pe):
            j = len(Pe)

        pi, pj = Pe[i-1], Pe[j-1]

        if (pj - pi + 1) > Te:
            # TODO: Recursion Error
            i = cls.binary_shift(i, j, Pe, Te, Tl)

        return i

    @classmethod
    def binary_span(cls,
                    i: int,
                    j: int,
                    Pe: list,
                    Te: int
                    ) -> int:
        """Performs binary span on position list Pe.

        Parameters
        ----------
        i : int
            Window start position.
        j : int
            Window end position.
        Pe : list
            Sorted position list.
        Te : int
            Upper bound of |s| = |G(s)| (number of s's q-grams).

        Returns
        -------
        Returns the new right span, which is the medium of lower and upper.

        """

        lower = j
        upper = i + Te - 1

        while lower <= upper:

            # mid is new right span, eventually larger than j (i.e. lower)
            # if mid jumps out of len(Pe) then it will raise IndexError!
            mid = int(math.ceil((upper + lower)/2))

            if mid <= len(Pe):
                pmid, pi = Pe[mid-1], Pe[i-1]
                if pmid - pi + 1 > Te:
                    upper = mid - 1
                else:
                    lower = mid + 1

            # this is heuristic based, if mid exceeds the length, we decrement it;
            # without this condition we miss many candidate windows e.g. 'surauijt ch'
            # in Table 1 document for entity 'surajit ch' 
            else:
                upper = mid - 1

        mid = upper

        return mid
