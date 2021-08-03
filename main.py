from nemex.data import EntitiesDictionary
from nemex.defaults import Default
from nemex.faerie import Faerie
from nemex.utils import *
from nemex.nemex import Verify


class Main:
    """Main class.
    TODO: See Nemex.

    """

    def __init__(self,
                 document: str,
                 entities: list,
                 tok_thresh: int = Default.TOKEN_THRESH,
                 sim_thresh: int = Default.SIM_THRESH,
                 char: bool = Default.CHAR,
                 unique: bool = Default.UNIQUE,
                 pruner: str = Default.PRUNER,
                 similarity: str = Default.SIMILARITY,
                 verified_only: bool = Default.VERIFIED,
                 special_char: str = Default.SPECIAL_CHAR):

        # document
        self.doc: str = document

        # entity dictionary
        self.entities: list = entities

        # ???
        self.verified_only: bool = verified_only

        '''
        tokenizer settings (see nemex.utils.Tokenizer)
        '''
        self.tokenizer = None
        self.q: int = tok_thresh
        self.special_char: str = special_char
        self.char: bool = char
        self.unique: bool = unique

        '''
        faerie settings (see nemex.faerie.Faerie)
        '''
        self.faerie = None
        self.t: float = sim_thresh
        self.pruner: str = pruner
        self.similarity: str = similarity

        '''
        intermediate results
        '''
        # proper entity dict
        self.entities_dict = None
        # document tokens
        self.doc_tokens: list = []
        # found candidates
        self.candidates: collections.defaultdict = collections.defaultdict(set)

        return

    def run(self):
        """Run main.

        """

        # setup tokenizer
        self.setupTokenizer()

        # create entity dictionary
        self.entities_dict = self.createEntityDict()

        # setup faerie model
        self.faerie = self.createModel(self.entities_dict)

        # tokenize document
        self.doc_tokens = self.createDocumentTokens()

        # check and verify
        self.candidates = self.findCandidates(self.doc_tokens)
        self.verifyCandidates(self.candidates, self.entities_dict)

        return

    def setupTokenizer(self):
        """Setup tokenizer.

        Create tokenizer generator without args.

        """

        self.tokenizer = Tokenizer(self.char, self.q, self.special_char, self.unique).tokenize
        return

    def createEntityDict(self) -> EntitiesDictionary:
        """Create entities dictionary from entity list.

        Returns
        -------
        Entity dictionary.

        """

        return EntitiesDictionary.from_list(self.entities, self.tokenizer)

    def createModel(self, entities_dict: EntitiesDictionary):
        """Create model.

        Parameters
        ----------
        entities_dict : EntitiesDictionary

        """

        return Faerie(entities_dict, self.similarity, self.t, self.q, self.pruner)

    def createDocumentTokens(self) -> list:
        """Tokenize document.

        Returns
        -------
        List with document tokens.

        """

        return self.tokenizer(self.doc)

    def findCandidates(self, doc_tokens: list) -> dict:
        """Find candidates.

        Parameters
        ----------
        doc_tokens : list
            Document tokens.

        Returns
        -------
        Dictionary of entities mapping to candidates.

        """

        # candidates
        entity2candidates = collections.defaultdict(set)

        # run faerie on tokens
        # perform pruning on doc tokens and return candidates.
        for e, (i, j) in self.faerie(doc_tokens):

            # get substring
            substring = doc_tokens[i:j + 1]

            # char or token based
            if self.char:
                substring = qgrams_to_char(substring)
            else:
                substring = " ".join(substring)

            # add substring to list of candidates
            entity2candidates[e].add(substring)

        return entity2candidates

    def verifyCandidates(self, entity2candidates: dict, entity_dict: EntitiesDictionary):
        """Verify candidates.

        Parameters
        ----------
        entity2candidates : dict
            Dictionary of entities mapping to candidates.
        entity_dict: dict
            Entity dictionary.

        """

        # loop
        for e, candidates in entity2candidates.items():

            #
            if len(candidates) == 0:
                continue

            print("\nEntity:", entity_dict[e].entity)
            print("----------------------------")

            #
            if self.char:
                entity = qgrams_to_char(entity_dict[e].tokens)
            else:
                entity = entity_dict[e].tokens

            #
            for candidate in candidates:

                #
                if not self.char:
                    substring = self.tokenizer(candidate)
                else:
                    substring = candidate

                #
                valid, score = Verify.check(substring, entity, self.similarity, self.t)

                #
                if self.verified_only:
                    if not valid:
                        continue

                #
                print("[{}] {} -- t_true={} {} {}=t_bounded".format(
                    valid, candidate, score, "<=" if self.similarity == Sim.EDIT_DIST else ">=", self.t))

        return


if __name__ == '__main__':

    document = "an efficient filter for approximate membership checking. venkaee shga kamunshik kabarati, " \
             "dong xin, surauijt chadhurisigmod."

    entities = [
        "kaushik ch",
        "chakrabarti",
        "chaudhuri",
        "venkatesh",
        "surajit ch"
    ]

    # run with default settings
    main = Main(document=document, entities=entities)
    main.run()
