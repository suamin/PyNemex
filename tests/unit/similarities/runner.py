import unittest

from .cosine_sim import test_cosine
from .dice_sim import test_dice
from .edit_dist import test_edist
from .edit_sim import test_esim
from .jaccard_sim import test_jaccard
from .similarity import test_sim
from .verify import test_verify


# initialize the test suite
loader = unittest.TestLoader()
suite = unittest.TestSuite()

# add tests to the test suite
suite.addTests(loader.loadTestsFromModule(test_cosine))
suite.addTests(loader.loadTestsFromModule(test_dice))
suite.addTests(loader.loadTestsFromModule(test_edist))
suite.addTests(loader.loadTestsFromModule(test_esim))
suite.addTests(loader.loadTestsFromModule(test_jaccard))
suite.addTests(loader.loadTestsFromModule(test_sim))
suite.addTests(loader.loadTestsFromModule(test_verify))


if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=7)
    result = runner.run(suite)
