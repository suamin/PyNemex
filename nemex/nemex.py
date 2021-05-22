import time

from .data import EntitiesDictionary
from .utils import *
from .similarities import Verify
from .faerie import Faerie


logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


class Nemex:
    """Nemex class.

    The Nemex class performs approximate 'Named Entity Matching and Extraction' based on the 'Faerie' algorithm.

    Parameters
    ----------
    list_or_file_entities : {list, str}
        List or file with entities.
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
    similarity : str
        Similarity method.
    t : int
        Similarity threshold.
    pruner : str
        Pruning method.
    verify : bool
        If true, verify candidates.
    """

    def __init__(self, list_or_file_entities, char=True, q: int = 2, special_char: str = "_", unique: bool = False,
                 lower: bool = True, similarity: str = Sim.EDIT_DIST, t: int = 2, pruner: str = Pruner.BATCH_COUNT,
                 verify: bool = True):

        # character-level
        if char:
            if similarity not in Sim.CHAR_BASED:
                raise ValueError("Change similarity method to 'edit_dist' or 'edit_sim' for character level.")

            if similarity == Sim.EDIT_DIST:
                t = int(t)
                if not t >= 1:
                    raise ValueError("Edit distance threshold must be >= 1")
            else:
                if not (0. < t <= 1.0):
                    raise ValueError("Similarity score should be in (0, 1]")

            q = int(q)

            if not q >= 1:
                raise ValueError("q-gram must be at least 1")

        # token-level
        else:
            if similarity in Sim.CHAR_BASED:
                raise ValueError("Change similarity method to 'cosine', 'dice' or 'jaccard' for token level.")

            if not (0. < t <= 1.0):
                raise ValueError("Similarity score should be in (0, 1]")

        # tokenizer
        self.tokenizer = Tokenizer(char, q, special_char, unique, lower)
        self.char = char

        # log start
        logger.info("Building entities dictionary ...")
        T = time.time()

        # check input
        if isinstance(list_or_file_entities, list):
            self.E = EntitiesDictionary.from_list(list_or_file_entities, self.tokenizer.tokenize)
        elif isinstance(list_or_file_entities, str):
            # else it is file of tsv id\tent lines or just text of ent lines
            self.E = EntitiesDictionary.from_tsv_file(list_or_file_entities, self.tokenizer.tokenize)
        else:
            logger.error("Bad input type.")
            logger.error("Expected `list` or `str`, but got ", type(list_or_file_entities))
            exit(0)

        # cache
        self.cache_ent_repr = dict()

        # log end
        T = time.time() - T
        logger.info("Building dictionary took {} seconds.".format(int(T)))

        # setup model
        self.faerie = Faerie(self.E, similarity=similarity, t=t, q=q, pruner=pruner)
        self.verify = verify

        return
    
    def __call__(self, document: str, valid_only: bool = True) -> dict:
        """Executes the Nemex algorithm.

        Parameters
        ----------
        document : str
            Text document.
        valid_only : bool
            If true, use only valid substrings.

        Returns
        -------
        Dictionary with document and match list.

        """

        # doc type
        assert isinstance(document, str), "Expected a string as document."

        # tokenize
        doc_tokens = self.tokenizer.tokenize(document)

        # char-level
        if self.char:
            doc_tokens_str = qgrams_to_char(doc_tokens).replace(self.tokenizer.special_char, " ")
        else:
            doc_tokens_str = " ".join(doc_tokens)

        # init spans
        spans = tokens_to_whitespace_char_spans(doc_tokens)

        # init output
        output = {"document": doc_tokens_str, "matches": list()}
        
        # returns pair of <entity index, (start, end) positions in doc_tokens>
        for e, (i, j) in self.faerie(doc_tokens):
            match_tokens = doc_tokens[i:j+1]
            match_span = spans[i:j+1]
            if len(match_span) == 1:
                start, end = match_span[0]
            else:
                start, end = match_span[0][0], match_span[-1][1]
            
            if self.char:
                q = self.tokenizer.q
                start, end = start - (i * q), end - (j * q)
                match = doc_tokens_str[start:end]
                
                if e not in self.cache_ent_repr:
                    entity = qgrams_to_char(self.E[e].tokens).replace(self.tokenizer.special_char, " ")
                    self.cache_ent_repr[e] = entity
                else:
                    entity = self.cache_ent_repr[e]

                output["matches"].append({
                    "entity": [entity, self.E[e].id],
                    "span": [start, end],
                    "match": match,
                    "score": None,
                    "valid": None
                })

                if self.verify:
                    valid, score = Verify.check(match, entity, self.faerie.similarity, self.faerie.t)
                    output["matches"][-1]["score"] = score
                    output["matches"][-1]["valid"] = valid
                    if valid_only and not valid:
                        del output["matches"][-1]
            else:
                # end = spans[j][-1]
                match = doc_tokens_str[start:end]
                
                if e not in self.cache_ent_repr:
                    entity = " ".join(self.E[e].tokens)
                    self.cache_ent_repr[e] = entity
                else:
                    entity = self.cache_ent_repr[e]
                
                output["matches"].append({
                    "entity": [entity, self.E[e].id],
                    "span": [start, end],
                    "match": match,
                    "score": None,
                    "valid": None
                })

                if self.verify:
                    valid, score = Verify.check(
                        match_tokens, self.E[e].tokens, self.faerie.similarity, self.faerie.t
                    )
                    output["matches"][-1]["score"] = score
                    output["matches"][-1]["valid"] = valid
                    if valid_only and not valid:
                        del output["matches"][-1]
        
        return output
