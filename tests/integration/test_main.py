import unittest
from main import Main


class TestMain(unittest.TestCase):
    """Main Test class.

    """

    def setUp(self) -> None:
        """Setup test.

        """

        # entity dictionary
        self.E = [
            "lab",
            "elirt",
            "seddiam",
            "volupta",
            "ccusam",
            "dolore",
            "lit"
        ]

        # document
        self.D = "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, " \
            "sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. " \
            "At vero eos et accusam et justo duo dolores et ea rebum. " \
            "Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. " \
            "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, " \
            "sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. " \
            "At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, " \
            "no sea takimata sanctus est Lorem ipsum dolor sit amet."

        return None

    def test_main(self):
        """Run main test.

        """

        main = Main(doc=self.D, entity_dict=self.E)
        main.run()

        return

    def tearDown(self) -> None:
        """Cleanup test.

        """
        return None


if __name__ == '__main__':
    unittest.main()
