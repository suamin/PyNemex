import unittest

from nemex.similarities import EditDistance


class TestEditDistance(unittest.TestCase):

    def setUp(self) -> None:
        self.sim = EditDistance()
        return None

    def test_OST(self):
        self.assertEqual(-1, self.sim.find_tau_min_overlap(1, 1, 1, 2))
        self.assertEqual(-3, self.sim.find_tau_min_overlap(1, 1, 2, 2))
        self.assertEqual(-1, self.sim.find_tau_min_overlap(2, 2, 1, 3))
        self.assertEqual(-4, self.sim.find_tau_min_overlap(2, 2, 2, 3))
        self.assertEqual(-5, self.sim.find_tau_min_overlap(3, 3, 2, 4))
        self.assertEqual(-9, self.sim.find_tau_min_overlap(3, 3, 3, 4))
        self.assertEqual(-6, self.sim.find_tau_min_overlap(4, 4, 2, 5))
        self.assertEqual(-11, self.sim.find_tau_min_overlap(4, 4, 3, 5))
        self.assertEqual(-13, self.sim.find_tau_min_overlap(5, 5, 3, 6))
        self.assertEqual(-19, self.sim.find_tau_min_overlap(5, 5, 4, 6))
        return

    def test_LTS(self):
        self.assertEqual(0, self.sim.find_min_size(1, 1))
        self.assertEqual(-1, self.sim.find_min_size(1, 2))
        self.assertEqual(1, self.sim.find_min_size(2, 1))
        self.assertEqual(0, self.sim.find_min_size(2, 2))
        self.assertEqual(1, self.sim.find_min_size(3, 2))
        self.assertEqual(0, self.sim.find_min_size(3, 3))
        self.assertEqual(2, self.sim.find_min_size(4, 2))
        self.assertEqual(1, self.sim.find_min_size(4, 3))
        self.assertEqual(2, self.sim.find_min_size(5, 3))
        self.assertEqual(1, self.sim.find_min_size(5, 4))
        return

    def test_UTS(self):
        self.assertEqual(2, self.sim.find_max_size(1, 1))
        self.assertEqual(3, self.sim.find_max_size(1, 2))
        self.assertEqual(3, self.sim.find_max_size(2, 1))
        self.assertEqual(4, self.sim.find_max_size(2, 2))
        self.assertEqual(5, self.sim.find_max_size(3, 2))
        self.assertEqual(6, self.sim.find_max_size(3, 3))
        self.assertEqual(6, self.sim.find_max_size(4, 2))
        self.assertEqual(7, self.sim.find_max_size(4, 3))
        self.assertEqual(8, self.sim.find_max_size(5, 3))
        self.assertEqual(9, self.sim.find_max_size(5, 4))
        return

    def test_LOST(self):
        self.assertEqual(-1, self.sim.find_lower_bound_of_entity(1, 1, 2))
        self.assertEqual(-3, self.sim.find_lower_bound_of_entity(1, 2, 2))
        self.assertEqual(-1, self.sim.find_lower_bound_of_entity(2, 1, 3))
        self.assertEqual(-4, self.sim.find_lower_bound_of_entity(2, 2, 3))
        self.assertEqual(-5, self.sim.find_lower_bound_of_entity(3, 2, 4))
        self.assertEqual(-9, self.sim.find_lower_bound_of_entity(3, 3, 4))
        self.assertEqual(-6, self.sim.find_lower_bound_of_entity(4, 2, 5))
        self.assertEqual(-11, self.sim.find_lower_bound_of_entity(4, 3, 5))
        self.assertEqual(-13, self.sim.find_lower_bound_of_entity(5, 3, 6))
        self.assertEqual(-19, self.sim.find_lower_bound_of_entity(5, 4, 6))
        return

    def test_TNB(self):
        self.assertEqual(2, self.sim.tighter_neighbor_bound(1, 2))
        self.assertEqual(4, self.sim.tighter_neighbor_bound(2, 2))
        self.assertEqual(3, self.sim.tighter_neighbor_bound(1, 3))
        self.assertEqual(6, self.sim.tighter_neighbor_bound(2, 3))
        self.assertEqual(8, self.sim.tighter_neighbor_bound(2, 4))
        self.assertEqual(12, self.sim.tighter_neighbor_bound(3, 4))
        self.assertEqual(10, self.sim.tighter_neighbor_bound(2, 5))
        self.assertEqual(15, self.sim.tighter_neighbor_bound(3, 5))
        self.assertEqual(18, self.sim.tighter_neighbor_bound(3, 6))
        self.assertEqual(24, self.sim.tighter_neighbor_bound(4, 6))
        return

    def tearDown(self) -> None:
        return None


if __name__ == '__main__':
    unittest.main()
