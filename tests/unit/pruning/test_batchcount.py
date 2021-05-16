import unittest
import nemex


class TestBatchCount(unittest.TestCase):

    def setUp(self) -> None:

        self.doc = "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, " \
            "sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. " \
            "At vero eos et accusam et justo duo dolores et ea rebum. " \
            "Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. " \
            "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, " \
            "sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. " \
            "At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, " \
            "no sea takimata sanctus est Lorem ipsum dolor sit amet."

        self.dict = [
            "lab",
            "elirt",
            "seddiam",
            "volupta",
            "ccusam",
            "dolore",
            "lit"
        ]

        #
        self.pruner = "batch_count"
        self.similarity = "edit_distance"
        self.t = 2
        self.q = 2
        self.special_char = "_"
        self.char = True
        self.unique = False

        #
        self.tokenizer = nemex.Tokenizer(self.char, self.q, self.special_char, self.unique).tokenize
        self.ents_dict = nemex.EntitiesDictionary.from_list(self.dict, self.tokenizer)

        #
        self.faerie = nemex.Faerie(self.ents_dict, self.similarity, self.t, self.q, self.pruner)

        self.doc_tokens = self.tokenizer(self.doc)

        #
        return None

    # full tokens
    def test_1_tokens_correct(self) -> None:
        self.dict = [
            "accusam",
            "takimata",
            "sanctus",
            "tempor",
            "voluptua"
            "ut"
        ]

        return

    # last character missing
    def test_last_missing_correct(self) -> None:
        self.dict = [
            "nonum",
            "dolor",
            "just",
            "labor",
            "e",
            "se"
        ]

        return

    # first character missing
    def test_first_missing_correct(self) -> None:
        self.dict = [
            "ed",
            "orem",
            "anctus",
            "tet",
            "t",
            "nvidunt"
        ]
        return

    # test 2 correct tokens
    def test_2_tokens_correct(self) -> None:
        self.dict = [
            "Lorem ipsum",
            "sed diam",
            "takimata sanctus",
            "Stet clita",
            "ea rebum"
        ]
        return

    # test 3 correct tokens
    def test_3_tokens_correct(self) -> None:
        self.dict = [
            "Lorem ipsum dolor",
            "sed diam voluptua",
            "justo duo dolores",
            "no sea takimata",
            "et ea rebum",
            "consetetur sadipscing elitr"
        ]
        return

    #
    def tearDown(self) -> None:
        return None

    # dummy
    def test_x(self) -> None:
        self.dict = [
            "",
            "",
            "",
            "",
            "",
            ""
        ]
        return None

