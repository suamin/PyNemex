import math
import logging

from typing import List


logger = logging.getLogger(__name__)


class NoPruning:
    """No Pruning class.

    TODO: Documentation

    """

    @classmethod
    def filter(cls, Pe: List[int], Le: int, Te: int, *args):
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

        Yields
        -------
        Start and end position of invalid (removable) window.

        """

        for i in range(1, len(Pe)+1):
            for j in range(i+1, len(Pe)+1):
                yield i, j

        return


class LazyCountPruning:
    """Lazy Count class.

    TODO: Documentation

    """

    @classmethod
    def filter(cls, Pe: List[int], Le: int, Te: int, Tl: int, *args):
        """Searches invalid windows using Lazy-Count Pruning.
        1. Count e's occurrence number (i.e. len(Pe))
        2. If occurrence number < Tl, then the entity is pruned

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

        Yields
        -------
        Start and end position of invalid (removable) window.

        """

        # lazy-count pruning: |Pe| <= Tl < T (Lemma 3)
        if len(Pe) >= Tl:
            yield from NoPruning.filter(Pe, Le, Te)


class BucketCountPruning:
    """Bucket Count Pruning class.

    TODO: Documentation

    """

    @classmethod
    def filter(cls, Pe: List[int], Le: int, Te: int, Tl: int, tighter_bound_func, *bound_args):
        """Searches invalid windows using Bucket-Count Pruning.

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
            Tighter bound for edit distance and edit similarity.
        bound_args :
            Tighter bound arguments.

        Yields
        -------
        Start and end position of invalid (removable) window.

        """

        # lazy-count pruning: |Pe| <= Tl < T (Lemma 3)
        if len(Pe) >= Tl:

            try:
                Te_diff_Tl = tighter_bound_func(*bound_args)

            # tighter bound is not supported for jaccard, cosine and dice -- uses Te - Tl
            except Exception:
                Te_diff_Tl = Te - Tl

            for i, j in cls.iter_bucket_spans(Pe, Te_diff_Tl):
                if j - i + 1 >= Tl:
                    yield i, j

    @classmethod
    def iter_bucket_spans(cls, Pe: List[int], t: int):
        """Iterate over bucket windows.

        Parameters
        ----------
        Pe : list
            Sorted position list.
        t : int
            Threshold.

        Yields
        -------
        Start and end position of current bucket window.

        """

        # initialize window indexes
        i, j = 1, 2

        # initialize bucket with starting position
        k = i

        while True:
            try:
                pi, pj = Pe[i-1], Pe[j-1]
            except IndexError:
                l = i
                yield k, l
                break
            else:
                if pj - pi + 1 > t:
                    l = i
                    yield k, l
                    k = j
            i += 1
            j += 1


class BatchCountPruning:
    """Batch Count Pruning class.

    TODO: Documentation

    """

    @classmethod
    def filter(cls, Pe: List[int], Le: int, Te: int, Tl: int, tighter_bound_func, *bound_args):
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
            Tighter bound for edit distance and edit similarity.
        bound_args :
            Tighter bound arguments.

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

                except Exception:
                    # tighter bound is not supported for edit distance and similarity -- uses Te
                    tighter_Te = Te

                # check if possible candidate window is an actual candidate window
                if cls.check_possible_candidate_window(i, j, Pe, Le, Te, Tl, tighter_Te):

                    # return the span for counting
                    yield i, j

    @classmethod
    def check_possible_candidate_window(cls, i: int, j: int, Pe: List[int], Le: int, Te: int, Tl: int,
                                        tighter_Te: int = None) -> bool:
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

            # candid window: make sure we have a candidate window (cf. Definition 3, condition 2)
            if Le <= pj - pi + 1 <= tighter_Te:
                return True

        return False

    @classmethod
    def iter_possible_candidate_windows(cls, Pe: List[int], Te: int, Tl: int):
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
    def binary_shift(cls, i: int, j: int, Pe: List[int], Te: int, Tl: int):
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
            i = cls.binary_shift(i, j, Pe, Te, Tl)

        return i

    @classmethod
    def binary_span(cls, i: int, j: int, Pe: List[int], Te: int):
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

        """

        lower = j
        upper = i + Te - 1

        while lower <= upper:

            # mid is new right span, eventually larger than j (i.e. lower)
            # if mid jumps out of len(Pe) then it will raise IndexError!
            mid = math.ceil((upper + lower)/2)

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
