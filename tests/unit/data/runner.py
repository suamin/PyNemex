import unittest

from .entities_dictionary import test_edict
from .entity import test_entity
from .faerie_data_structure import test_fds
from .inverted_index import test_index


# initialize the test suite
loader = unittest.TestLoader()
suite = unittest.TestSuite()

# add tests to the test suite
suite.addTests(loader.loadTestsFromModule(test_edict))
suite.addTests(loader.loadTestsFromModule(test_entity))
suite.addTests(loader.loadTestsFromModule(test_fds))
suite.addTests(loader.loadTestsFromModule(test_index))


if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=4)
    result = runner.run(suite)
