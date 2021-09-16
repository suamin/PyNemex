import unittest

from nemex import Faerie, EntitiesDictionary, Default


class TestFaerie(unittest.TestCase):

    def setUp(self) -> None:
        # TODO: Setup test.
        self.edict = EntitiesDictionary(Default.TOKENIZER)
        self.faerie = Faerie(self.edict)
        return None

    def test_example(self):
        return self.assertEqual("", "")

    def tearDown(self) -> None:
        return None


if __name__ == '__main__':
    unittest.main()
