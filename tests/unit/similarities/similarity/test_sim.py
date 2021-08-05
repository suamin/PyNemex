import unittest

from nemex import Similarity
from nemex import similarities as sims


class TestSimilarity(unittest.TestCase):
    """
    # Test Cases
    1. Diff start
    2. Diff end
    3. Diff middle
    4. Diff start+end
    5. Diff with special chars '-', ' ', '_'
    """

    def setUp(self) -> None:
        self.sim = Similarity()
        self.tokens1 = [
            [],
            [],
            []
        ]
        self.tokens2 = [
            [],
            [],
            []
        ]
        self.tokens3 = [
            [],
            [],
            []
        ]
        self.tokens4 = [
            [],
            [],
            []
        ]
        self.tokens5 = [
            [],
            [],
            []
        ]
        self.strings = [
            "AAA",
            "AAB",
            "ABA",
            "BAA",
            "BBB"
        ]
        return None

    def test_jaccard(self):
        self.assertEqual(0, sims.jaccard(self.tokens1[0], self.tokens1[1]))
        self.assertEqual(0, sims.jaccard(self.tokens1[1], self.tokens1[2]))
        self.assertEqual(0, sims.jaccard(self.tokens1[2], self.tokens1[0]))
        self.assertEqual(0, sims.jaccard(self.tokens2[0], self.tokens2[1]))
        self.assertEqual(0, sims.jaccard(self.tokens2[1], self.tokens2[2]))
        self.assertEqual(0, sims.jaccard(self.tokens2[2], self.tokens2[0]))
        self.assertEqual(0, sims.jaccard(self.tokens3[0], self.tokens3[1]))
        self.assertEqual(0, sims.jaccard(self.tokens3[1], self.tokens3[2]))
        self.assertEqual(0, sims.jaccard(self.tokens3[2], self.tokens3[0]))
        self.assertEqual(0, sims.jaccard(self.tokens4[0], self.tokens4[1]))
        self.assertEqual(0, sims.jaccard(self.tokens4[1], self.tokens4[2]))
        self.assertEqual(0, sims.jaccard(self.tokens4[2], self.tokens4[0]))
        return

    def test_cosine(self):
        self.assertEqual(0, sims.cosine(self.tokens1[0], self.tokens1[1]))
        self.assertEqual(0, sims.cosine(self.tokens1[1], self.tokens1[2]))
        self.assertEqual(0, sims.cosine(self.tokens1[2], self.tokens1[0]))
        self.assertEqual(0, sims.cosine(self.tokens2[0], self.tokens2[1]))
        self.assertEqual(0, sims.cosine(self.tokens2[1], self.tokens2[2]))
        self.assertEqual(0, sims.cosine(self.tokens2[2], self.tokens2[0]))
        self.assertEqual(0, sims.cosine(self.tokens3[0], self.tokens3[1]))
        self.assertEqual(0, sims.cosine(self.tokens3[1], self.tokens3[2]))
        self.assertEqual(0, sims.cosine(self.tokens3[2], self.tokens3[0]))
        self.assertEqual(0, sims.cosine(self.tokens4[0], self.tokens4[1]))
        self.assertEqual(0, sims.cosine(self.tokens4[1], self.tokens4[2]))
        self.assertEqual(0, sims.cosine(self.tokens4[2], self.tokens4[0]))
        return

    def test_dice(self):
        self.assertEqual(0, sims.dice(self.tokens1[0], self.tokens1[1]))
        self.assertEqual(0, sims.dice(self.tokens1[1], self.tokens1[2]))
        self.assertEqual(0, sims.dice(self.tokens1[2], self.tokens1[0]))
        self.assertEqual(0, sims.dice(self.tokens2[0], self.tokens2[1]))
        self.assertEqual(0, sims.dice(self.tokens2[1], self.tokens2[2]))
        self.assertEqual(0, sims.dice(self.tokens2[2], self.tokens2[0]))
        self.assertEqual(0, sims.dice(self.tokens3[0], self.tokens3[1]))
        self.assertEqual(0, sims.dice(self.tokens3[1], self.tokens3[2]))
        self.assertEqual(0, sims.dice(self.tokens3[2], self.tokens3[0]))
        self.assertEqual(0, sims.dice(self.tokens4[0], self.tokens4[1]))
        self.assertEqual(0, sims.dice(self.tokens4[1], self.tokens4[2]))
        self.assertEqual(0, sims.dice(self.tokens4[2], self.tokens4[0]))
        return

    def test_esim(self):
        self.assertEqual(0.667, sims.edit_sim(self.strings[0], self.strings[1]))
        self.assertEqual(0.333, sims.edit_sim(self.strings[1], self.strings[2]))
        self.assertEqual(0.333, sims.edit_sim(self.strings[2], self.strings[3]))
        self.assertEqual(0.333, sims.edit_sim(self.strings[3], self.strings[4]))
        self.assertEqual(0.000, sims.edit_sim(self.strings[4], self.strings[0]))
        self.assertEqual(0.667, sims.edit_sim(self.strings[0], self.strings[2]))
        self.assertEqual(0.333, sims.edit_sim(self.strings[1], self.strings[3]))
        self.assertEqual(0.333, sims.edit_sim(self.strings[2], self.strings[4]))
        self.assertEqual(0.667, sims.edit_sim(self.strings[3], self.strings[0]))
        return

    def test_edist(self):
        self.assertEqual(1, sims.edit_dist(self.strings[0], self.strings[1]))
        self.assertEqual(2, sims.edit_dist(self.strings[1], self.strings[2]))
        self.assertEqual(2, sims.edit_dist(self.strings[2], self.strings[3]))
        self.assertEqual(2, sims.edit_dist(self.strings[3], self.strings[4]))
        self.assertEqual(3, sims.edit_dist(self.strings[4], self.strings[0]))
        self.assertEqual(1, sims.edit_dist(self.strings[0], self.strings[2]))
        self.assertEqual(2, sims.edit_dist(self.strings[1], self.strings[3]))
        self.assertEqual(2, sims.edit_dist(self.strings[2], self.strings[4]))
        self.assertEqual(1, sims.edit_dist(self.strings[3], self.strings[0]))
        return

    def tearDown(self) -> None:
        return None


if __name__ == '__main__':
    unittest.main()
