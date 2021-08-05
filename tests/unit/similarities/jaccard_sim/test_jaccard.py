import unittest

from nemex.similarities import JaccardSimilarity


class TestJaccardSimilarity(unittest.TestCase):

    def setUp(self) -> None:
        self.sim = JaccardSimilarity()
        return None

    def test_OST(self):
        self.assertEqual(1, self.sim.find_tau_min_overlap(1, 1, 0.2))
        self.assertEqual(1, self.sim.find_tau_min_overlap(1, 1, 0.7))
        self.assertEqual(1, self.sim.find_tau_min_overlap(2, 2, 0.2))
        self.assertEqual(2, self.sim.find_tau_min_overlap(2, 2, 0.7))
        self.assertEqual(1, self.sim.find_tau_min_overlap(3, 3, 0.2))
        self.assertEqual(3, self.sim.find_tau_min_overlap(3, 3, 0.7))
        self.assertEqual(2, self.sim.find_tau_min_overlap(4, 4, 0.2))
        self.assertEqual(4, self.sim.find_tau_min_overlap(4, 4, 0.7))
        self.assertEqual(2, self.sim.find_tau_min_overlap(5, 5, 0.2))
        self.assertEqual(5, self.sim.find_tau_min_overlap(5, 5, 0.7))
        return

    def test_LTS(self):
        self.assertEqual(1, self.sim.find_min_size(1, 0.2))
        self.assertEqual(1, self.sim.find_min_size(1, 0.7))
        self.assertEqual(1, self.sim.find_min_size(2, 0.2))
        self.assertEqual(2, self.sim.find_min_size(2, 0.7))
        self.assertEqual(1, self.sim.find_min_size(3, 0.2))
        self.assertEqual(3, self.sim.find_min_size(3, 0.7))
        self.assertEqual(1, self.sim.find_min_size(4, 0.2))
        self.assertEqual(3, self.sim.find_min_size(4, 0.7))
        self.assertEqual(1, self.sim.find_min_size(5, 0.2))
        self.assertEqual(4, self.sim.find_min_size(5, 0.7))
        return

    def test_UTS(self):
        self.assertEqual(5, self.sim.find_max_size(1, 0.2))
        self.assertEqual(1, self.sim.find_max_size(1, 0.7))
        self.assertEqual(10, self.sim.find_max_size(2, 0.2))
        self.assertEqual(2, self.sim.find_max_size(2, 0.7))
        self.assertEqual(15, self.sim.find_max_size(3, 0.2))
        self.assertEqual(4, self.sim.find_max_size(3, 0.7))
        self.assertEqual(20, self.sim.find_max_size(4, 0.2))
        self.assertEqual(5, self.sim.find_max_size(4, 0.7))
        self.assertEqual(25, self.sim.find_max_size(5, 0.2))
        self.assertEqual(7, self.sim.find_max_size(5, 0.7))
        return

    def test_LOST(self):
        self.assertEqual(1, self.sim.find_lower_bound_of_entity(1, 0.2))
        self.assertEqual(1, self.sim.find_lower_bound_of_entity(1, 0.7))
        self.assertEqual(1, self.sim.find_lower_bound_of_entity(2, 0.2))
        self.assertEqual(2, self.sim.find_lower_bound_of_entity(2, 0.7))
        self.assertEqual(1, self.sim.find_lower_bound_of_entity(3, 0.2))
        self.assertEqual(3, self.sim.find_lower_bound_of_entity(3, 0.7))
        self.assertEqual(1, self.sim.find_lower_bound_of_entity(4, 0.2))
        self.assertEqual(3, self.sim.find_lower_bound_of_entity(4, 0.7))
        self.assertEqual(1, self.sim.find_lower_bound_of_entity(5, 0.2))
        self.assertEqual(4, self.sim.find_lower_bound_of_entity(5, 0.7))
        return

    def test_TUWS(self):
        self.assertEqual(5, self.sim.tighter_upper_window_size(1, 1, 0.2))
        self.assertEqual(1, self.sim.tighter_upper_window_size(1, 2, 0.7))
        self.assertEqual(10, self.sim.tighter_upper_window_size(2, 3, 0.2))
        self.assertEqual(2, self.sim.tighter_upper_window_size(2, 4, 0.7))
        self.assertEqual(15, self.sim.tighter_upper_window_size(3, 5, 0.2))
        self.assertEqual(1, self.sim.tighter_upper_window_size(3, 1, 0.7))
        self.assertEqual(10, self.sim.tighter_upper_window_size(4, 2, 0.2))
        self.assertEqual(4, self.sim.tighter_upper_window_size(4, 3, 0.7))
        self.assertEqual(20, self.sim.tighter_upper_window_size(5, 4, 0.2))
        self.assertEqual(7, self.sim.tighter_upper_window_size(5, 5, 0.7))
        return

    def tearDown(self) -> None:
        return None


if __name__ == '__main__':
    unittest.main()