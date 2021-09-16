import unittest

from nemex import Nemex, Pruner, Sim


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

        self.edict = [
            "lab",
            "elirt",
            "seddiam",
            "volupta",
            "ccusam",
            "dolore",
            "lit"
        ]

        self.nemex = None

        return None

    # full tokens
    def test_single_token_correct(self) -> None:
        self.edict = [
            "accusam",
            "takimata",
            "sanctus",
            "tempor",
            "voluptua"
            "ut"
        ]

        self.nemex = Nemex(list_or_file_entities=self.edict, pruner=Pruner.BATCH_COUNT, similarity=Sim.EDIT_DIST)

        matches = self.nemex(self.doc)
        print(matches)

        return

    # last character missing
    def test_last_missing_correct(self) -> None:
        self.edict = [
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
        self.edict = [
            "ed",
            "orem",
            "anctus",
            "tet",
            "t",
            "nvidunt"
        ]
        return

    # test 2 correct tokens
    def test_two_tokens_correct(self) -> None:
        self.edict = [
            "Lorem ipsum",
            "sed diam",
            "takimata sanctus",
            "Stet clita",
            "ea rebum"
        ]
        return

    # test 3 correct tokens
    def test_three_tokens_correct(self) -> None:
        self.edict = [
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
        self.edict = [
            "",
            "",
            "",
            "",
            "",
            ""
        ]
        return None


if __name__ == '__main__':
    unittest.main()
