import unittest

from nemex import EntitiesDictionary, Default


class TestEntitiesDictionary(unittest.TestCase):

    def setUp(self) -> None:
        # TODO: Setup test.
        self.edict = EntitiesDictionary(Default.TOKENIZER)
        return None

    def test_example(self):
        return self.assertEqual("", "")

    def tearDown(self) -> None:
        return None


if __name__ == '__main__':
    unittest.main()
