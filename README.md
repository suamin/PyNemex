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
from nemex import Nemex
import json

E = [
    "kaushik ch",
    "chakrabarti",
    "chaudhuri",
    "venkatesh",
    "surajit ch"
]
D = "an efficient filter for approximate membership checking. venkaee shga kamunshik kabarati, dong xin, surauijt chadhurisigmod."

nemex = Nemex(E) # initialize with dictionar
output = nemex(D) # query document

print(json.dumps(output, indent=2))
```
Running the example gives results as:

```json
{
  "document": "an efficient filter for approximate membership checking. venkaee shga kamunshik kabarati, dong xin, surauijt chadhurisigmod.",
  "matches": [
    {
      "valid": true,
      "entity": [
        "chaudhuri",
        2
      ],
      "score": 2,
      "match": " chadhuri",
      "span": [
        108,
        117
      ]
    },
    {
      "valid": true,
      "entity": [
        "chaudhuri",
        2
      ],
      "score": 1,
      "match": "chadhuri",
      "span": [
        109,
        117
      ]
    },
    {
      "valid": true,
      "entity": [
        "chaudhuri",
        2
      ],
      "score": 2,
      "match": "chadhuris",
      "span": [
        109,
        118
      ]
    },
    {
      "valid": true,
      "entity": [
        "chaudhuri",
        2
      ],
      "score": 2,
      "match": "hadhuri",
      "span": [
        110,
        117
      ]
    },
    {
      "valid": true,
      "entity": [
        "venkatesh",
        3
      ],
      "score": 2,
      "match": "venkaee sh",
      "span": [
        57,
        67
      ]
    },
    {
      "valid": true,
      "entity": [
        "surajit ch",
        4
      ],
      "score": 2,
      "match": "surauijt ch",
      "span": [
        100,
        111
      ]
    }
  ]
}
```

## History
The authors of Faerie [1] [released](https://dongdeng.github.io/code/faerie.tar.gz) the binary for the code, which was written in C++. The first open-source version, called NEMEX, was originally written in [Java](https://github.com/gueneumann/nemexa) by [Günter Neumann](https://www.dfki.de/~neumann/) and then maintained partly by Amir Moin at DFKI, Saarbrücken.

## References
[1] Li, G., Deng, D., & Feng, J. (2011, June). Faerie: efficient filtering algorithms for approximate dictionary-based entity extraction. In _Proceedings of the 2011 ACM SIGMOD International Conference on Management of data_ (pp. 529-540). ACM.
