import unittest
import nemex
import collections


class TestMain(unittest.TestCase):

    def setUp(self) -> None:

        # (E)ntity dictionary
        self.E = [
            "kaushik ch",
            "chakrabarti",
            "chaudhuri",
            "venkatesh",
            "surajit ch"
        ]

        # (D)ocument
        self.D = "an efficient filter for approximate membership checking. venkaee shga kamunshik kabarati, dong xin, surauijt chadhurisigmod."

        # ???
        self.verified_only = True

        '''
        tokenizer settings (see nemex.Tokenizer)
        '''
        self.tokenizer = None
        self.q = 2
        self.special_char = "_"
        self.char = True
        self.unique = False

        '''
        faerie settings (see nemex.Faerie)
        '''
        self.faerie = None
        self.t = 2
        self.pruner = "batch_count"
        self.similarity = "edit_dist"

        return None

    def test_main(self) -> None:
        '''
        run
        '''

        # setup tokenizer
        self.setupTokenizer()

        # create entity dictionary
        ents_dict = self.createEntityDict()

        # setup faerie model
        self.createModel(ents_dict)

        # tokenize document
        doc_tokens = self.createDocumentTokens()

        # check and verify
        candidates = self.findCandidates(doc_tokens)
        self.verifyCandidates(candidates, ents_dict)

        return None

    def setupTokenizer(self) -> None:
        '''
        setup tokenizer
        create tokenizer generator without args
        '''

        self.tokenizer = nemex.Tokenizer(self.char, self.q, self.special_char, self.unique).tokenize
        return None

    def createEntityDict(self) -> dict:
        '''
        create entities dictionary from entity list
        '''

        return nemex.EntitiesDictionary.from_list(self.E, self.tokenizer)

    def createModel(self, ents_dict) -> None:
        '''
        setup model
        '''

        self.faerie = nemex.Faerie(ents_dict, self.similarity, self.t, self.q, self.pruner)
        return None

    def createDocumentTokens(self):
        '''
        tokenize document
        '''

        doc_tokens = self.tokenizer(self.D)
        return doc_tokens

    def findCandidates(self, doc_tokens):
        '''
        find candidates
        '''

        # candidates
        entity2candidates = collections.defaultdict(set)

        # run faerie on tokens
        for e, (i, j) in self.faerie(doc_tokens):

            #
            substring = doc_tokens[i:j + 1]

            #
            if self.char:
                substring = nemex.utils.qgrams_to_char(substring)
            else:
                substring = " ".join(substring)

            #
            entity2candidates[e].add(substring)

        return entity2candidates

    def verifyCandidates(self, entity2candidates, ents_dict) -> None:
        '''
        verify candidates
        '''

        # loop
        for e, candidates in entity2candidates.items():

            #
            if len(candidates) == 0:
                continue

            print("\nEntity:", ents_dict[e].entity)
            print("----------------------------")

            #
            if self.char:
                entity = nemex.utils.qgrams_to_char(ents_dict[e].tokens)
            else:
                entity = ents_dict[e].tokens

            #
            for candidate in candidates:

                #
                if not self.char:
                    substring = self.tokenizer(candidate)
                else:
                    substring = candidate

                #
                valid, score = nemex.Verify.check(substring, entity, self.similarity, self.t)

                #
                if self.verified_only:
                    if not valid:
                        continue

                #
                print("[{}] {} -- t_true={} {} {}=t_bounded".format(
                    valid, candidate, score, "<=" if self.similarity == "edit_dist" else ">=", self.t))

        return None

    def tearDown(self) -> None:
        return None


if __name__ == '__main__':
    unittest.main()
