import unittest

from nemex import Similarity
from nemex import similarities as sims


class TestSimilarity(unittest.TestCase):

    def setUp(self) -> None:
        self.sim = Similarity()
        self.r_tokens = []
        self.s_tokens = []
        self.r_string = []
        self.s_string = []
        return None

    def test_jaccard(self):
        self.assertEqual(0, sims.jaccard(self.r_tokens[0], self.s_tokens[0]))
        self.assertEqual(0, sims.jaccard(self.r_tokens[0], self.s_tokens[0]))
        self.assertEqual(0, sims.jaccard(self.r_tokens[0], self.s_tokens[0]))
        self.assertEqual(0, sims.jaccard(self.r_tokens[0], self.s_tokens[0]))
        self.assertEqual(0, sims.jaccard(self.r_tokens[0], self.s_tokens[0]))
        self.assertEqual(0, sims.jaccard(self.r_tokens[0], self.s_tokens[0]))
        self.assertEqual(0, sims.jaccard(self.r_tokens[0], self.s_tokens[0]))
        self.assertEqual(0, sims.jaccard(self.r_tokens[0], self.s_tokens[0]))
        self.assertEqual(0, sims.jaccard(self.r_tokens[0], self.s_tokens[0]))
        self.assertEqual(0, sims.jaccard(self.r_tokens[0], self.s_tokens[0]))
        return

    def test_cosine(self):
        self.assertEqual(0, sims.cosine(self.r_tokens[0], self.s_tokens[0]))
        self.assertEqual(0, sims.cosine(self.r_tokens[0], self.s_tokens[0]))
        self.assertEqual(0, sims.cosine(self.r_tokens[0], self.s_tokens[0]))
        self.assertEqual(0, sims.cosine(self.r_tokens[0], self.s_tokens[0]))
        self.assertEqual(0, sims.cosine(self.r_tokens[0], self.s_tokens[0]))
        self.assertEqual(0, sims.cosine(self.r_tokens[0], self.s_tokens[0]))
        self.assertEqual(0, sims.cosine(self.r_tokens[0], self.s_tokens[0]))
        self.assertEqual(0, sims.cosine(self.r_tokens[0], self.s_tokens[0]))
        self.assertEqual(0, sims.cosine(self.r_tokens[0], self.s_tokens[0]))
        self.assertEqual(0, sims.cosine(self.r_tokens[0], self.s_tokens[0]))
        return

    def test_dice(self):
        self.assertEqual(0, sims.dice(self.r_tokens[0], self.s_tokens[0]))
        self.assertEqual(0, sims.dice(self.r_tokens[0], self.s_tokens[0]))
        self.assertEqual(0, sims.dice(self.r_tokens[0], self.s_tokens[0]))
        self.assertEqual(0, sims.dice(self.r_tokens[0], self.s_tokens[0]))
        self.assertEqual(0, sims.dice(self.r_tokens[0], self.s_tokens[0]))
        self.assertEqual(0, sims.dice(self.r_tokens[0], self.s_tokens[0]))
        self.assertEqual(0, sims.dice(self.r_tokens[0], self.s_tokens[0]))
        self.assertEqual(0, sims.dice(self.r_tokens[0], self.s_tokens[0]))
        self.assertEqual(0, sims.dice(self.r_tokens[0], self.s_tokens[0]))
        self.assertEqual(0, sims.dice(self.r_tokens[0], self.s_tokens[0]))
        return

    def test_esim(self):
        self.assertEqual(0, sims.edit_sim(self.r_string[0]))
        self.assertEqual(0, sims.edit_sim(self.r_string[0]))
        self.assertEqual(0, sims.edit_sim(self.r_string[0]))
        self.assertEqual(0, sims.edit_sim(self.r_string[0]))
        self.assertEqual(0, sims.edit_sim(self.r_string[0]))
        self.assertEqual(0, sims.edit_sim(self.r_string[0]))
        self.assertEqual(0, sims.edit_sim(self.r_string[0]))
        self.assertEqual(0, sims.edit_sim(self.r_string[0]))
        self.assertEqual(0, sims.edit_sim(self.r_string[0]))
        self.assertEqual(0, sims.edit_sim(self.r_string[0]))
        return

    def test_edist(self):
        self.assertEqual(0, sims.edit_dist(self.r_string[0]))
        self.assertEqual(0, sims.edit_dist(self.r_string[0]))
        self.assertEqual(0, sims.edit_dist(self.r_string[0]))
        self.assertEqual(0, sims.edit_dist(self.r_string[0]))
        self.assertEqual(0, sims.edit_dist(self.r_string[0]))
        self.assertEqual(0, sims.edit_dist(self.r_string[0]))
        self.assertEqual(0, sims.edit_dist(self.r_string[0]))
        self.assertEqual(0, sims.edit_dist(self.r_string[0]))
        self.assertEqual(0, sims.edit_dist(self.r_string[0]))
        self.assertEqual(0, sims.edit_dist(self.r_string[0]))
        return

    def tearDown(self) -> None:
        return None


if __name__ == '__main__':
    unittest.main()
