import unittest

from nemex import LazyCountPruning


class TestLazyCount(unittest.TestCase):

    def setUp(self) -> None:
        # TODO: Setup test.
        self.doc = "Lorem ipsum."
        self.Pe = None
        self.Le = None
        self.Te = None
        self.Tl = None
        return None

    def tearDown(self) -> None:
        LazyCountPruning.filter(self.Pe, self.Le, self.Te, self.Tl)
        return None


if __name__ == '__main__':
    unittest.main()
