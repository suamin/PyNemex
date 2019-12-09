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
surauijt_cha
ijt_chadhuri
t_chadhuris
chadhurisig
chadhurisigm
chadhuris
_chadhuri
jt_chadhuri
jt_chadhuris
_chadhuris
t_chadhurisi
rauijt_chadh
chadhuri
_chadhurisi
t_chadhuri
_chadhurisig
chadhurisi

Entity: venkatesh
----------------------------
venkaee_shga
venkaee_shg
._venkaee_sh
_venkaee_shg
venkaee_sh
_venkaee_sh

Entity: surajit ch
----------------------------
surauijt_cha
_surauijt_cha
,_surauijt_ch
surauijt_chad
surauijt_ch
_surauijt_ch
```

## History
The authors of Faerie [1] released the binary for the code, which was written in C++. The first open-source version, called NEMEX, was originally written in [Java](https://github.com/gueneumann/nemexa) by [Günter Neumann](https://www.dfki.de/~neumann/) and then maintained partly by Amir Moin at DFKI, Saarbrücken.

## References
[1] Li, G., Deng, D., & Feng, J. (2011, June). Faerie: efficient filtering algorithms for approximate dictionary-based entity extraction. In _Proceedings of the 2011 ACM SIGMOD International Conference on Management of data_ (pp. 529-540). ACM.
