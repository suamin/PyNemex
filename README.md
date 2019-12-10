# NEMEX 
**N**amed **E**ntity **M**atching and **Ex**traction (NEMEX) is a python package for approximate entity extraction. Currently, it is mainly based on Faerie [1] algorithm.

## Installation
Soon as:
```bash
pip install nemex
```

## Quickstart
Here we show a simple example to extract entities from a pre-defined dictionary.
```python
import nemex
import collections

## define entities as simple list
E = [
    "kaushik ch",
    "chakrabarti",
    "chaudhuri",
    "venkatesh",
    "surajit ch"
]
    
## setup tokenizer

# size of q-gram, it splits string as overlapping sub-tokens 
# (e.g. "nemex" with q=2 becomes ["ne", "em", "me", "ex"])
q = 2
# select char or token-based approach
char = True
# a special character that will be used to replace whitespaces in a string
special_char = "_"
# whether to consider to unique tokens only
unique = False
tokenizer = nemex.Tokenizer(char, q, special_char, unique).tokenize

# create entities dictionary
ents_dict = nemex.EntitiesDictionary.from_list(E, tokenizer)

## similarity selection

# can be one of "edit_dist", "edit_sim", "jaccard", "dice" or "cosine"
similarity = "edit_dist"
# distance threshold
t = 2

## faerie algorithm

# count based pruning strategy to use, can be one of "batch_count", "bucket_count", "lazy_count" or None
pruner = "batch_count"
faerie = nemex.Faerie(ents_dict, similarity, t, q, pruner)

# run on document to find approximate entities from dictionary
D = "an efficient filter for approximate membership checking. venkaee shga kamunshik kabarati, dong xin, surauijt chadhurisigmod." # query document
doc_tokens = tokenizer(D)
entity2candidates = collections.defaultdict(set)

# yields matched entity and span of sub-string in document tokens
for e, (i, j) in faerie(doc_tokens):
    substring = doc_tokens[i:j+1]
    if char:
        substring = nemex.utils.qgrams_to_char(substring)
    else:
        substring = " ".join(substring)
    entity2candidates[e].add(substring)

for e, candidates in entity2candidates.items():
    if len(candidates) == 0:
        continue
    print("Entity:", ents_dict[e].entity)
    print("----------------------------")
    for candidate in candidates:
        print(candidate)
    print()


```
Running the example gives results as:

```bash
Entity: chaudhuri
----------------------------
[True] chadhuri -- t_true=1 <= 2=t_bounded
[False] chadhurisi -- t_true=3 <= 2=t_bounded
[True] _chadhuri -- t_true=2 <= 2=t_bounded
[False] t_chadhuris -- t_true=4 <= 2=t_bounded
[False] t_chadhurisi -- t_true=5 <= 2=t_bounded
[False] rauijt_chadh -- t_true=10 <= 2=t_bounded
[False] _chadhurisi -- t_true=4 <= 2=t_bounded
[False] jt_chadhuri -- t_true=4 <= 2=t_bounded
[False] jt_chadhuris -- t_true=5 <= 2=t_bounded
[False] _chadhuris -- t_true=3 <= 2=t_bounded
[False] _chadhurisig -- t_true=5 <= 2=t_bounded
[False] chadhurisig -- t_true=4 <= 2=t_bounded
[False] chadhurisigm -- t_true=5 <= 2=t_bounded
[False] ijt_chadhuri -- t_true=5 <= 2=t_bounded
[True] chadhuris -- t_true=2 <= 2=t_bounded
[False] t_chadhuri -- t_true=3 <= 2=t_bounded
[False] surauijt_cha -- t_true=10 <= 2=t_bounded

Entity: venkatesh
----------------------------
[True] venkaee_sh -- t_true=2 <= 2=t_bounded
[False] venkaee_shg -- t_true=3 <= 2=t_bounded
[False] _venkaee_shg -- t_true=4 <= 2=t_bounded
[False] _venkaee_sh -- t_true=3 <= 2=t_bounded
[False] venkaee_shga -- t_true=4 <= 2=t_bounded
[False] ._venkaee_sh -- t_true=4 <= 2=t_bounded

Entity: surajit ch
----------------------------
[False] ,_surauijt_ch -- t_true=4 <= 2=t_bounded
[False] _surauijt_ch -- t_true=3 <= 2=t_bounded
[True] surauijt_ch -- t_true=2 <= 2=t_bounded
[False] surauijt_chad -- t_true=4 <= 2=t_bounded
[False] _surauijt_cha -- t_true=4 <= 2=t_bounded
[False] surauijt_cha -- t_true=3 <= 2=t_bounded
```
With verified examples only:
```bash
Entity: chaudhuri
----------------------------
[True] _chadhuri -- t_true=2 <= 2=t_bounded
[True] chadhuris -- t_true=2 <= 2=t_bounded
[True] chadhuri -- t_true=1 <= 2=t_bounded

Entity: venkatesh
----------------------------
[True] venkaee_sh -- t_true=2 <= 2=t_bounded

Entity: surajit ch
----------------------------
[True] surauijt_ch -- t_true=2 <= 2=t_bounded
```

## History
The authors of Faerie [1] released the binary for the code, which was written in C++. The first open-source version, called NEMEX, was originally written in [Java](https://github.com/gueneumann/nemexa) by [Günter Neumann](https://www.dfki.de/~neumann/) and then maintained partly by Amir Moin at DFKI, Saarbrücken.

## References
[1] Li, G., Deng, D., & Feng, J. (2011, June). Faerie: efficient filtering algorithms for approximate dictionary-based entity extraction. In _Proceedings of the 2011 ACM SIGMOD International Conference on Management of data_ (pp. 529-540). ACM.
