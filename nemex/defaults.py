from nemex import Pruner, Sim, Tokenizer


class Default:

    TOKEN_THRESH: int = 2
    SIM_THRESH: int = 2
    CHAR = True
    UNIQUE = False
    PRUNER = Pruner.BUCKET_COUNT
    SIMILARITY = Sim.EDIT_DIST
    VERIFY = True
    SPECIAL_CHAR = "_"
    TOKENIZER = Tokenizer(CHAR, TOKEN_THRESH, SPECIAL_CHAR, UNIQUE).tokenize
    LOWER = True
    VALID_ONLY = True
