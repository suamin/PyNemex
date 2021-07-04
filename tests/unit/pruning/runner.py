import unittest

from .batch_count import test_batchcount
from .bucket_count import test_bucketcount
from .lazy_count import test_lazycount

# initialize the test suite
loader = unittest.TestLoader()
suite = unittest.TestSuite()

# add tests to the test suite
suite.addTests(loader.loadTestsFromModule(test_batchcount))
suite.addTests(loader.loadTestsFromModule(test_bucketcount))
suite.addTests(loader.loadTestsFromModule(test_lazycount))

if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=3)
    result = runner.run(suite)
