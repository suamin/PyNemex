from nemex.data import EntitiesDictionary
from nemex.faerie import Faerie
from nemex.utils import *
from nemex.nemex import Verify


class Main:
    """Main class.

    """

    def __init__(self,
                 doc: str,
                 entity_dict: list,
                 q_size: int = 2,
                 sim_thresh: int = 2,
                 char: bool = True,
                 unique: bool = False,
                 pruner: str = Pruner.BATCH_COUNT,
                 similarity: str = "edit_dist",
                 verified_only: bool = True,
                 special_char: str = "_"):

        # document
        self.D = doc

        # entity dictionary
        self.E = entity_dict

        # ???
        self.verified_only = verified_only

        '''
        tokenizer settings (see nemex.utils.Tokenizer)
        '''
        self.tokenizer = None
        self.q = q_size
        self.special_char = special_char
        self.char = char
        self.unique = unique

        '''
        faerie settings (see nemex.faerie.Faerie)
        '''
        self.faerie = None
        self.t = sim_thresh
        self.pruner = pruner
        self.similarity = similarity

        return

    def run(self):
        """Run main.

        """

        # setup tokenizer
        self.setupTokenizer()

        # create entity dictionary
        entities_dict = self.createEntityDict()

        # setup faerie model
        self.createModel(entities_dict)

        # tokenize document
        doc_tokens = self.createDocumentTokens()

        # check and verify
        candidates = self.findCandidates(doc_tokens)
        self.verifyCandidates(candidates, entities_dict)

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

        return EntitiesDictionary.from_list(self.E, self.tokenizer)

    def createModel(self, entities_dict: EntitiesDictionary):
        """Create model.

        Parameters
        ----------
        entities_dict : EntitiesDictionary

        """

        self.faerie = Faerie(entities_dict, self.similarity, self.t, self.q, self.pruner)
        return

    def createDocumentTokens(self) -> list:
        """Tokenize document.

        Returns
        -------
        List with document tokens.

        """

        doc_tokens = self.tokenizer(self.D)
        return doc_tokens

    def findCandidates(self, doc_tokens: list):
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
        for e, (i, j) in self.faerie(doc_tokens):

            #
            substring = doc_tokens[i:j + 1]

            #
            if self.char:
                substring = qgrams_to_char(substring)
            else:
                substring = " ".join(substring)

            #
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
                    valid, candidate, score, "<=" if self.similarity == "edit_dist" else ">=", self.t))

        return


if __name__ == '__main__':

    D = "an efficient filter for approximate membership checking. venkaee shga kamunshik kabarati, " \
             "dong xin, surauijt chadhurisigmod."

    E = [
        "kaushik ch",
        "chakrabarti",
        "chaudhuri",
        "venkatesh",
        "surajit ch"
    ]

    main = Main(doc=D, entity_dict=E)
    main.run()
