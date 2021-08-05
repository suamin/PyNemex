import unittest

from nemex.similarities import EditSimilarity


class TestEditSimilarity(unittest.TestCase):

    def setUp(self) -> None:
        self.sim = EditSimilarity()
        return None

    def test_OST(self):
        self.assertEqual(-2, self.sim.find_tau_min_overlap(1, 1, 0.2, 2))
        self.assertEqual(0, self.sim.find_tau_min_overlap(1, 1, 0.7, 2))
        self.assertEqual(-7, self.sim.find_tau_min_overlap(2, 2, 0.2, 3))
        self.assertEqual(-1, self.sim.find_tau_min_overlap(2, 2, 0.7, 3))
        self.assertEqual(-16, self.sim.find_tau_min_overlap(3, 3, 0.2, 4))
        self.assertEqual(-4, self.sim.find_tau_min_overlap(3, 3, 0.7, 4))
        self.assertEqual(-28, self.sim.find_tau_min_overlap(4, 4, 0.2, 5))
        self.assertEqual(-8, self.sim.find_tau_min_overlap(4, 4, 0.7, 5))
        self.assertEqual(-43, self.sim.find_tau_min_overlap(5, 5, 0.2, 6))
        self.assertEqual(-13, self.sim.find_tau_min_overlap(5, 5, 0.7, 6))
        return

    def test_LTS(self):
        self.assertEqual(0, self.sim.find_min_size(1, 0.2, 2))
        self.assertEqual(1, self.sim.find_min_size(1, 0.7, 2))
        self.assertEqual(-1, self.sim.find_min_size(2, 0.2, 3))
        self.assertEqual(1, self.sim.find_min_size(2, 0.7, 3))
        self.assertEqual(-1, self.sim.find_min_size(3, 0.2, 4))
        self.assertEqual(2, self.sim.find_min_size(3, 0.7, 4))
        self.assertEqual(-2, self.sim.find_min_size(4, 0.2, 5))
        self.assertEqual(2, self.sim.find_min_size(4, 0.7, 5))
        self.assertEqual(-3, self.sim.find_min_size(5, 0.2, 6))
        self.assertEqual(2, self.sim.find_min_size(5, 0.7, 6))
        return

    def test_UTS(self):
        self.assertEqual(9, self.sim.find_max_size(1, 0.2, 2))
        self.assertEqual(1, self.sim.find_max_size(1, 0.7, 2))
        self.assertEqual(18, self.sim.find_max_size(2, 0.2, 3))
        self.assertEqual(3, self.sim.find_max_size(2, 0.7, 3))
        self.assertEqual(27, self.sim.find_max_size(3, 0.2, 4))
        self.assertEqual(5, self.sim.find_max_size(3, 0.7, 4))
        self.assertEqual(36, self.sim.find_max_size(4, 0.2, 5))
        self.assertEqual(7, self.sim.find_max_size(4, 0.7, 5))
        self.assertEqual(45, self.sim.find_max_size(5, 0.2, 6))
        self.assertEqual(9, self.sim.find_max_size(5, 0.7, 6))
        return

    def test_LOST(self):
        self.assertEqual(-15, self.sim.find_lower_bound_of_entity(1, 0.2, 2))
        self.assertEqual(0, self.sim.find_lower_bound_of_entity(1, 0.7, 2))
        self.assertEqual(-46, self.sim.find_lower_bound_of_entity(2, 0.2, 3))
        self.assertEqual(-3, self.sim.find_lower_bound_of_entity(2, 0.7, 3))
        self.assertEqual(-93, self.sim.find_lower_bound_of_entity(3, 0.2, 4))
        self.assertEqual(-7, self.sim.find_lower_bound_of_entity(3, 0.7, 4))
        self.assertEqual(-156, self.sim.find_lower_bound_of_entity(4, 0.2, 5))
        self.assertEqual(-13, self.sim.find_lower_bound_of_entity(4, 0.7, 5))
        self.assertEqual(-235, self.sim.find_lower_bound_of_entity(5, 0.2, 6))
        self.assertEqual(-20, self.sim.find_lower_bound_of_entity(5, 0.7, 6))
        return

    def test_TNB(self):
        self.assertEqual(16, self.sim.tighter_neighbor_bound(1, 0.2, 2))
        self.assertEqual(1, self.sim.tighter_neighbor_bound(1, 0.7, 2))
        self.assertEqual(48, self.sim.tighter_neighbor_bound(2, 0.2, 3))
        self.assertEqual(5, self.sim.tighter_neighbor_bound(2, 0.7, 3))
        self.assertEqual(96, self.sim.tighter_neighbor_bound(3, 0.2, 4))
        self.assertEqual(10, self.sim.tighter_neighbor_bound(3, 0.7, 4))
        self.assertEqual(160, self.sim.tighter_neighbor_bound(4, 0.2, 5))
        self.assertEqual(17, self.sim.tighter_neighbor_bound(4, 0.7, 5))
        self.assertEqual(240, self.sim.tighter_neighbor_bound(5, 0.2, 6))
        self.assertEqual(25, self.sim.tighter_neighbor_bound(5, 0.7, 6))
        return

    def tearDown(self) -> None:
        return None


if __name__ == '__main__':
    unittest.main()
