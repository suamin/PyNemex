import unittest

from nemex import FaerieDataStructure, EntitiesDictionary, Default


class TestFaerieDataStructure(unittest.TestCase):

    def setUp(self) -> None:
        # TODO: Setup test.
        self.edict = EntitiesDictionary(Default.TOKENIZER)
        self.fds = FaerieDataStructure(self.edict)
        return None

    def test_example(self):
        return self.assertEqual("", "")

    def tearDown(self) -> None:
        return None


if __name__ == '__main__':
    unittest.main()
