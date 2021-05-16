# -*- coding: utf-8 -*-

import collections
import logging
from typing import List, Tuple


logger = logging.getLogger(__name__)


class Tokenizer:
    """Tokenizer class.

    Parameters
    ----------
    char : bool
        If true, performs character-level similarity instead of token-level.
    q : int
        Size of q-grams.
    special_char : str
        Special character for substitution of space character.
    unique : bool
        If true, preserves order with uniqueness.
    lower : bool
        If true, converts document to lower case.
    """

    def __init__(self, char: bool = True, q: int = 2, special_char: str = "_", unique: bool = False, lower: bool = True):
        self.char = char
        self.q = q
        self.special_char = special_char
        self.unique = unique
        self.lower = lower
    
    def tokenize(self, string: str) -> list:
        """Tokenizes the string and returns the tokens as list.

        Parameters
        ----------
        string : str
            Document string which should be tokenized.

        Returns
        -------
        A list of `q`-grams.
        """

        # lower
        if self.lower:
            string = string.lower()

        # char
        if self.char:
            if self.special_char:
                string = string.replace(" ", self.special_char)
            tokens = [string[i:i+self.q] for i in range(len(string) - self.q + 1)]
        else:
            tokens = string.split()

        # unique
        if self.unique:
            # hacky way to preserve order with uniqueness
            temp = collections.OrderedDict()
            for token in tokens:
                if tokens not in temp:
                    temp[token] = None
            tokens = list(temp.keys())
            del temp

        return tokens


def qgrams_to_char(s: list) -> str:
    """Converts a list of q-grams to a string.

    Parameters
    ----------
    s : list
        List of q-grams.

    Returns
    -------
    A string from q-grams.

    """

    if len(s) == 1:
        return s[0]

    return "".join([s[0]] + [s[i][-1] for i in range(1, len(s))])


def tokens_to_whitespace_char_spans(tokens: list) -> List[Tuple[int, int]]:
    """TODO: Documentation

    Parameters
    ----------
    tokens: list
        Tokens.

    Returns
    -------
    ???

    """

    i = 0
    spans = list()  # list of tuple of (start_char_index, end_char_index) in " ".join(tokens)
    for t in tokens:
        start = i
        end = i + len(t)
        spans.append((start, end))
        i = end + 1  # +1 for whitespace

    return spans
