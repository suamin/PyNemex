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

# 1) define the entities
E = [
    "kaushik ch",
    "chakrabarti",
    "chaudhuri",
    "venkatesh",
    "surajit ch"
]

# 2) setup tokenizer
tokenizer = nemex.Tokenizer(char=True, q=2).tokenize

# 3) create entities dictionary
ents_dict = nemex.EntitiesDictionary.from_list(E, tokenizer)

# 4) setup search algorithm
faerie = nemex.Faerie(ents_dict, similarity="edit_dist", t=2, q=2, pruner="batch_count")

    
D = "an efficient filter for approximate membership checking. venkaee shga kamunshik kabarati, dong xin, surauijt chadhurisigmod."

doc_tokens = tokenizer(D)

# returns pair of <entity index, (start, end) positions in doc_tokens> 
for e, (i, j) in faerie(doc_tokens):
    match = doc_tokens[i:j+1]
    match = nemex.utils.qgrams_to_char(match)
    entity = nemex.utils.qgrams_to_char(ents_dict[e].tokens)
    print("<{}, {}>".format(entity, match))

```
Running the example gives results as:

```bash
<chaudhuri, surauijt_cha>
<chaudhuri, rauijt_chadh>
<chaudhuri, ijt_chadhuri>
<chaudhuri, jt_chadhuri>
<chaudhuri, jt_chadhuris>
<chaudhuri, t_chadhuri>
<chaudhuri, t_chadhuris>
<chaudhuri, t_chadhurisi>
<chaudhuri, _chadhuri>
<chaudhuri, _chadhuris>
<chaudhuri, _chadhurisi>
<chaudhuri, _chadhurisig>
<chaudhuri, chadhuri>
<chaudhuri, chadhuris>
<chaudhuri, chadhurisi>
<chaudhuri, chadhurisig>
<chaudhuri, chadhurisigm>
<venkatesh, ._venkaee_sh>
<venkatesh, _venkaee_sh>
<venkatesh, _venkaee_shg>
<venkatesh, venkaee_sh>
<venkatesh, venkaee_shg>
<venkatesh, venkaee_shga>
<surajit_ch, ,_surauijt_ch>
<surajit_ch, _surauijt_ch>
<surajit_ch, _surauijt_cha>
<surajit_ch, surauijt_ch>
<surajit_ch, surauijt_cha>
<surajit_ch, surauijt_chad>
```
Additionally, we can add verification step:
```python
# returns pair of <entity index, (start, end) positions in doc_tokens> 
for e, (i, j) in faerie(doc_tokens):
    match = doc_tokens[i:j+1]
    match = nemex.utils.qgrams_to_char(match)
    entity = nemex.utils.qgrams_to_char(ents_dict[e].tokens)
    # verify
    valid, score = nemex.Verify.check(match, entity, "edit_dist", 2)
    if valid:
        print("<{}, {}>".format(entity, match))
```
Which results in:
```bash
<chaudhuri, _chadhuri>
<chaudhuri, chadhuri>
<chaudhuri, chadhuris>
<venkatesh, venkaee_sh>
<surajit_ch, surauijt_ch>
```

## History
The authors of Faerie [1] [released](https://dongdeng.github.io/code/faerie.tar.gz) the binary for the code, which was written in C++. The first open-source version, called NEMEX, was originally written in [Java](https://github.com/gueneumann/nemexa) by [Günter Neumann](https://www.dfki.de/~neumann/) and then maintained partly by Amir Moin at DFKI, Saarbrücken.

## References
[1] Li, G., Deng, D., & Feng, J. (2011, June). Faerie: efficient filtering algorithms for approximate dictionary-based entity extraction. In _Proceedings of the 2011 ACM SIGMOD International Conference on Management of data_ (pp. 529-540). ACM.
