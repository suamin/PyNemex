import unittest

from nemex import Verify


class TestVerify(unittest.TestCase):

    def setUp(self) -> None:
        self.verify = Verify()
        return None

    def test_jaccard(self):
        return self.assertEqual("", "")

    def test_cosine(self):
        return self.assertEqual("", "")

    def test_dice(self):
        return self.assertEqual("", "")

    def test_esim(self):
        return self.assertEqual("", "")

    def test_edist(self):
        return self.assertEqual("", "")

    def tearDown(self) -> None:
        return None


if __name__ == '__main__':
    unittest.main()
