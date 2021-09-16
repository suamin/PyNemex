import unittest

from nemex import InvertedIndex


class TestInvertedIndex(unittest.TestCase):

    def setUp(self) -> None:
        # TODO: Setup test.
        self.inv_index = InvertedIndex({})
        return None

    def test_example(self):
        return self.assertEqual("", "")

    def tearDown(self) -> None:
        return None


if __name__ == '__main__':
    unittest.main()
