import unittest

from nemex import Sim, BucketCountPruning, Similarity


class TestPartitioning(unittest.TestCase):

    def setUp(self) -> None:
        self.sim = Similarity()
        self.span_new = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]
        self.span_old = [(1, 5)]
        return None

    def setArgs(self, sim, t, q, es, pc):
        self.t = t
        self.q = q
        self.es = es
        self.Pe = [1+i*pc for i in range(0, 5)]
        self.bound_args = ()

        if sim == Sim.EDIT_DIST:
            self.bound_args = (self.t, self.q)
        elif sim == Sim.EDIT_SIM:
            self.bound_args = (self.es, self.t, self.q)

        self.sim.similarity = sim
        self.T = self.sim.tighter_neighbor_bound(*self.bound_args)
        return

    '''EDIT DISTANCE'''

    def test_ED_T1_Q1_E1_P1(self):
        self.setArgs(Sim.EDIT_DIST, 1, 1, 1, 1)
        self.assertEqual(self.span_old, [(i, j) for i, j in BucketCountPruning.iter_bucket_spans(self.Pe, self.T)])
        return

    def test_ED_T1_Q1_E1_P2(self):
        self.setArgs(Sim.EDIT_DIST, 1, 1, 1, 2)
        self.assertEqual(self.span_old, [(i, j) for i, j in BucketCountPruning.iter_bucket_spans(self.Pe, self.T)])
        return

    def test_ED_T1_Q1_E1_P3(self):
        self.setArgs(Sim.EDIT_DIST, 1, 1, 1, 3)
        self.assertEqual(self.span_new, [(i, j) for i, j in BucketCountPruning.iter_bucket_spans(self.Pe, self.T)])
        return

    def test_ED_T1_Q2_E1_P1(self):
        self.setArgs(Sim.EDIT_DIST, 1, 2, 1, 1)
        self.assertEqual(self.span_old, [(i, j) for i, j in BucketCountPruning.iter_bucket_spans(self.Pe, self.T)])
        return

    def test_ED_T3_Q3_E1_P1(self):
        self.setArgs(Sim.EDIT_DIST, 3, 3, 1, 1)
        self.assertEqual(self.span_old, [(i, j) for i, j in BucketCountPruning.iter_bucket_spans(self.Pe, self.T)])
        return

    def test_ED_T5_Q4_E1_P1(self):
        self.setArgs(Sim.EDIT_DIST, 5, 4, 1, 1)
        self.assertEqual(self.span_old, [(i, j) for i, j in BucketCountPruning.iter_bucket_spans(self.Pe, self.T)])
        return

    def test_ED_T1_Q2_E1_P8(self):
        self.setArgs(Sim.EDIT_DIST, 1, 2, 1, 8)
        self.assertEqual(self.span_new, [(i, j) for i, j in BucketCountPruning.iter_bucket_spans(self.Pe, self.T)])
        return

    def test_ED_T3_Q3_E1_P8(self):
        self.setArgs(Sim.EDIT_DIST, 3, 3, 1, 8)
        self.assertEqual(self.span_old, [(i, j) for i, j in BucketCountPruning.iter_bucket_spans(self.Pe, self.T)])
        return

    def test_ED_T5_Q4_E1_P8(self):
        self.setArgs(Sim.EDIT_DIST, 5, 4, 1, 8)
        self.assertEqual(self.span_old, [(i, j) for i, j in BucketCountPruning.iter_bucket_spans(self.Pe, self.T)])
        return

    def test_ED_T1_Q2_E1_P16(self):
        self.setArgs(Sim.EDIT_DIST, 1, 2, 1, 16)
        self.assertEqual(self.span_new, [(i, j) for i, j in BucketCountPruning.iter_bucket_spans(self.Pe, self.T)])
        return

    def test_ED_T3_Q3_E1_P16(self):
        self.setArgs(Sim.EDIT_DIST, 3, 3, 1, 16)
        self.assertEqual(self.span_new, [(i, j) for i, j in BucketCountPruning.iter_bucket_spans(self.Pe, self.T)])
        return

    def test_ED_T5_Q4_E1_P16(self):
        self.setArgs(Sim.EDIT_DIST, 5, 4, 1, 16)
        self.assertEqual(self.span_old, [(i, j) for i, j in BucketCountPruning.iter_bucket_spans(self.Pe, self.T)])
        return

    def test_ED_T1_Q2_E1_P32(self):
        self.setArgs(Sim.EDIT_DIST, 1, 2, 1, 32)
        self.assertEqual(self.span_new, [(i, j) for i, j in BucketCountPruning.iter_bucket_spans(self.Pe, self.T)])
        return

    def test_ED_T3_Q3_E1_P32(self):
        self.setArgs(Sim.EDIT_DIST, 3, 3, 1, 32)
        self.assertEqual(self.span_new, [(i, j) for i, j in BucketCountPruning.iter_bucket_spans(self.Pe, self.T)])
        return

    def test_ED_T5_Q4_E1_P32(self):
        self.setArgs(Sim.EDIT_DIST, 5, 4, 1, 32)
        self.assertEqual(self.span_new, [(i, j) for i, j in BucketCountPruning.iter_bucket_spans(self.Pe, self.T)])
        return

    '''EDIT SIMILARITY'''

    def test_ES_T1_Q1_E3_P1(self):
        self.setArgs(Sim.EDIT_SIM, 0.9, 1, 3, 1)
        self.assertEqual(self.span_old, [(i, j) for i, j in BucketCountPruning.iter_bucket_spans(self.Pe, self.T)])
        return

    def test_ES_T1_Q1_E3_P2(self):
        self.setArgs(Sim.EDIT_SIM, 0.9, 1, 3, 2)
        self.assertEqual(self.span_new, [(i, j) for i, j in BucketCountPruning.iter_bucket_spans(self.Pe, self.T)])
        return

    def test_ES_T1_Q1_E3_P3(self):
        self.setArgs(Sim.EDIT_SIM, 0.9, 1, 3, 3)
        self.assertEqual(self.span_new, [(i, j) for i, j in BucketCountPruning.iter_bucket_spans(self.Pe, self.T)])
        return

    def test_ES_T1_Q2_E6_P1(self):
        self.setArgs(Sim.EDIT_SIM, 0.9, 2, 6, 1)
        self.assertEqual(self.span_old, [(i, j) for i, j in BucketCountPruning.iter_bucket_spans(self.Pe, self.T)])
        return

    def test_ES_T3_Q3_E6_P1(self):
        self.setArgs(Sim.EDIT_SIM, 0.7, 3, 6, 1)
        self.assertEqual(self.span_old, [(i, j) for i, j in BucketCountPruning.iter_bucket_spans(self.Pe, self.T)])
        return

    def test_ES_T5_Q4_E6_P1(self):
        self.setArgs(Sim.EDIT_SIM, 0.5, 4, 6, 1)
        self.assertEqual(self.span_old, [(i, j) for i, j in BucketCountPruning.iter_bucket_spans(self.Pe, self.T)])
        return

    def test_ES_T1_Q2_E9_P8(self):
        self.setArgs(Sim.EDIT_SIM, 0.9, 2, 9, 8)
        self.assertEqual(self.span_new, [(i, j) for i, j in BucketCountPruning.iter_bucket_spans(self.Pe, self.T)])
        return

    def test_ES_T3_Q3_E9_P8(self):
        self.setArgs(Sim.EDIT_SIM, 0.9, 3, 9, 8)
        self.assertEqual(self.span_new, [(i, j) for i, j in BucketCountPruning.iter_bucket_spans(self.Pe, self.T)])
        return

    def test_ES_T5_Q4_E9_P8(self):
        self.setArgs(Sim.EDIT_SIM, 0.9, 4, 9, 8)
        self.assertEqual(self.span_new, [(i, j) for i, j in BucketCountPruning.iter_bucket_spans(self.Pe, self.T)])
        return

    def test_ES_T1_Q2_E15_P16(self):
        self.setArgs(Sim.EDIT_SIM, 0.9, 2, 15, 16)
        self.assertEqual(self.span_new, [(i, j) for i, j in BucketCountPruning.iter_bucket_spans(self.Pe, self.T)])
        return

    def test_ES_T3_Q3_E15_P16(self):
        self.setArgs(Sim.EDIT_SIM, 0.7, 3, 15, 16)
        self.assertEqual(self.span_old, [(i, j) for i, j in BucketCountPruning.iter_bucket_spans(self.Pe, self.T)])
        return

    def test_ES_T5_Q4_E15_P16(self):
        self.setArgs(Sim.EDIT_SIM, 0.5, 4, 15, 16)
        self.assertEqual(self.span_old, [(i, j) for i, j in BucketCountPruning.iter_bucket_spans(self.Pe, self.T)])
        return

    def test_ES_T1_Q2_E24_P32(self):
        self.setArgs(Sim.EDIT_SIM, 0.9, 2, 24, 32)
        self.assertEqual(self.span_new, [(i, j) for i, j in BucketCountPruning.iter_bucket_spans(self.Pe, self.T)])
        return

    def test_ES_T3_Q3_E24_P32(self):
        self.setArgs(Sim.EDIT_SIM, 0.7, 3, 24, 32)
        self.assertEqual(self.span_old, [(i, j) for i, j in BucketCountPruning.iter_bucket_spans(self.Pe, self.T)])
        return

    def test_ES_T5_Q4_E24_P32(self):
        self.setArgs(Sim.EDIT_SIM, 0.5, 4, 24, 32)
        self.assertEqual(self.span_old, [(i, j) for i, j in BucketCountPruning.iter_bucket_spans(self.Pe, self.T)])
        return


if __name__ == '__main__':
    unittest.main()
