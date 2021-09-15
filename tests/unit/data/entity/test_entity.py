import unittest

from nemex import Entity


class TestEntity(unittest.TestCase):

    def setUp(self) -> None:
        # TODO: Setup test.
        self.entity = Entity(0, "")
        return None

    def test_example(self):
        return self.assertEqual("", "")

    def tearDown(self) -> None:
        return None


if __name__ == '__main__':
    unittest.main()
