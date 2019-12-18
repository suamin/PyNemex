# -*- coding: utf-8 -*-

import collections
import logging

logger = logging.getLogger(__name__)


class Tokenizer:
    
    def __init__(self, char=True, q=2, special_char="_", unique=False, lower=True):
        self.char = char
        self.q = q
        self.special_char = special_char
        self.unique = unique
        self.lower = lower
    
    def tokenize(self, string):
        if self.lower:
            string = string.lower()
        if self.char:
            if self.special_char:
                string = string.replace(" ", self.special_char)
            tokens = [string[i:i+self.q] for i in range(len(string) - self.q + 1)]
        else:
            tokens = string.split()
        if self.unique:
            # hacky way to preserve order with uniqueness
            temp = collections.OrderedDict()
            for token in tokens:
                if tokens not in temp:
                    temp[token] = None
            tokens = list(temp.keys())
            del temp
        return tokens


def qgrams_to_char(s):
    return "".join([s[0]] + [s[i][-1] for i in range(1, len(s))])
