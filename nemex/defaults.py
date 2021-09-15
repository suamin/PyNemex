"""
Defaults module.

Classes:
    - Default

"""

from nemex import Pruner, Sim, Tokenizer


class Default:

    TOKEN_THRESH: int = 2
    SIM_THRESH_CHAR: int = 2
    SIM_THRESH_TOKEN: float = 0.7
    CHAR: bool = True
    UNIQUE: bool = False
    PRUNER: str = Pruner.BATCH_COUNT
    SIMILARITY: str = Sim.EDIT_DIST
    VERIFY: bool = True
    SPECIAL_CHAR: str = "_"
    TOKENIZER = Tokenizer(CHAR, TOKEN_THRESH, SPECIAL_CHAR, UNIQUE).tokenize
    LOWER: bool = True
    VALID_ONLY: bool = True
