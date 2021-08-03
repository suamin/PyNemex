import unittest

from nemex import Nemex, Pruner
from nemex.defaults import Default


class TestNemex(unittest.TestCase):

    def setUp(self) -> None:

        # data
        self.document = None
        self.entities = None

        self.q = Default.TOKEN_THRESH
        self.sim = Default.SIMILARITY
        self.t = Default.SIM_THRESH
        self.pruner = Default.PRUNER

        self.nemex = None

        return None

    def setArgs(self, document, entities, q, sim, t, pruner):

        self.document = document
        self.entities = entities

        self.q = q
        self.sim = sim
        self.t = t
        self.pruner = pruner

        self.nemex = Nemex(
            list_or_file_entities=self.entities,
            char=Default.CHAR,
            q=self.q,
            special_char=Default.SPECIAL_CHAR,
            unique=Default.UNIQUE,
            lower=Default.LOWER,
            similarity=self.sim,
            t=self.t,
            pruner=self.pruner,
            verify=Default.VERIFY
        )

        return

    @staticmethod
    def get_matches(output):
        matches = []

        for mdict in output['matches']:
            matches.append(mdict['match'])

        return matches

    def example_data_1(self, pruner, t):

        self.setArgs(
            document="Lorem ipsum dolo sit amet.",
            entities=['dolor'],
            q=Default.TOKEN_THRESH,
            sim=Default.SIMILARITY,
            t=t,
            pruner=pruner
        )

        expected = []

        if t >= 0:
            expected += ['dolor']
        if t >= 1:
            expected += ['dolo', 'olor', ' dolor', 'dolor ']
        if t >= 2:
            expected += ['dol', 'lor', 'olo',  'm dolor', 'dolor s', ' dolor ', ' dolo', 'olor ']
        if t >= 3:
            expected += ['do', 'or', 'ol', 'lo', 'lor ', ' dol', 'm dolo', 'olor s']

        output = self.nemex(document=self.document, valid_only=Default.VALID_ONLY)
        computed = self.get_matches(output)

        return set(expected), set(computed)

    def example_data_2(self, pruner, t):

        self.setArgs(
            document="At vero eos et accusam et justo duo dolores et ea rebum.",
            entities=['gusta'],
            q=Default.TOKEN_THRESH,
            sim=Default.SIMILARITY,
            t=t,
            pruner=pruner
        )

        expected = []

        if t >= 0:
            expected += []
        if t >= 1:
            expected += []
        if t >= 2:
            expected += ['ust', 'just', 'usto', 'cusa', 'usa', 'justo']
        if t >= 3:
            expected += ['sto', ' just', 'usto ']

        output = self.nemex(document=self.document, valid_only=Default.VALID_ONLY)
        computed = self.get_matches(output)

        return set(expected), set(computed)

    def example_data_3(self, pruner, t):

        self.setArgs(
            document="How much wood would a woodchuck chuck if a woodchuck could chuck wood?",
            entities=['wood', 'chuck'],
            q=Default.TOKEN_THRESH,
            sim=Default.SIMILARITY,
            t=t,
            pruner=pruner
        )

        # TODO
        expected = []

        if t >= 0:
            expected += []
        if t >= 1:
            expected += []
        if t >= 2:
            expected += []
        if t >= 3:
            expected += []

        output = self.nemex(document=self.document, valid_only=Default.VALID_ONLY)
        computed = self.get_matches(output)

        return set(expected), set(computed)

    def example_data_4(self, pruner, t):

        self.setArgs(
            document="She sells seashells by the seashore.",
            entities=['sea', 'shells'],
            q=Default.TOKEN_THRESH,
            sim=Default.SIMILARITY,
            t=t,
            pruner=pruner
        )

        # TODO
        expected = []

        if t >= 0:
            expected += []
        if t >= 1:
            expected += []
        if t >= 2:
            expected += []
        if t >= 3:
            expected += []

        output = self.nemex(document=self.document, valid_only=Default.VALID_ONLY)
        computed = self.get_matches(output)

        return set(expected), set(computed)

    def example_data_5(self, pruner, t):

        self.setArgs(
            document="Betty Botter bought some butter, but she said the butter’s bitter.",
            entities=['bitter', 'butter'],
            q=Default.TOKEN_THRESH,
            sim=Default.SIMILARITY,
            t=t,
            pruner=pruner
        )

        # TODO
        expected = []

        if t >= 0:
            expected += []
        if t >= 1:
            expected += []
        if t >= 2:
            expected += []
        if t >= 3:
            expected += []

        output = self.nemex(document=self.document, valid_only=Default.VALID_ONLY)
        computed = self.get_matches(output)

        return set(expected), set(computed)

    def example_data_6(self, pruner, t):

        self.setArgs(
            document="A big bug bit the little beetle but the little beetle bit the bug back.",
            entities=['bug', 'beetle'],
            q=Default.TOKEN_THRESH,
            sim=Default.SIMILARITY,
            t=t,
            pruner=pruner
        )

        # TODO
        expected = []

        if t >= 0:
            expected += []
        if t >= 1:
            expected += []
        if t >= 2:
            expected += []
        if t >= 3:
            expected += []

        output = self.nemex(document=self.document, valid_only=Default.VALID_ONLY)
        computed = self.get_matches(output)

        return set(expected), set(computed)

    def example_data_7(self, pruner, t):

        self.setArgs(
            document="Ed Nott was shot and Sam Shott was not. So it is better to be Shott than Nott. "
                     "Some say Nott was not shot. But Shott says he shot Nott. Either the shot Shott shot "
                     "at Nott was not shot, or Nott was shot. If the shot Shott shot shot Nott, Nott was shot. "
                     "But if the shot Shott shot shot Shott, the shot was Shott, not Nott. However, the shot "
                     "Shott shot shot not Shott – but Nott. So, Ed Nott was shot and that’s hot! Is it not?",
            entities=['not', 'shot'],
            q=Default.TOKEN_THRESH,
            sim=Default.SIMILARITY,
            t=t,
            pruner=pruner
        )

        # TODO
        expected = []

        if t >= 0:
            expected += []
        if t >= 1:
            expected += []
        if t >= 2:
            expected += []
        if t >= 3:
            expected += []

        output = self.nemex(document=self.document, valid_only=Default.VALID_ONLY)
        computed = self.get_matches(output)

        return set(expected), set(computed)

    def example_data_8(self, pruner, t):

        self.setArgs(
            document="Peter Piper picked a peck of pickled peppers. A peck of pickled peppers Peter Piper picked. "
                     "If Peter Piper picked a peck of pickled peppers, Where’s the peck of pickled peppers Peter Piper "
                     "picked?",
            entities=['pickled', 'peppers'],
            q=Default.TOKEN_THRESH,
            sim=Default.SIMILARITY,
            t=t,
            pruner=pruner
        )

        # TODO
        expected = []

        if t >= 0:
            expected += []
        if t >= 1:
            expected += []
        if t >= 2:
            expected += []
        if t >= 3:
            expected += []

        output = self.nemex(document=self.document, valid_only=Default.VALID_ONLY)
        computed = self.get_matches(output)

        return set(expected), set(computed)

    ''' Data 1 '''

    def test_nemex_bucket_t1_data_1(self):
        expected, computed = self.example_data_1(Pruner.BUCKET_COUNT, 1)
        self.assertEqual(expected, computed)
        return

    def test_nemex_bucket_t2_data_1(self):
        expected, computed = self.example_data_1(Pruner.BUCKET_COUNT, 2)
        self.assertEqual(expected, computed)
        return

    def test_nemex_bucket_t3_data_1(self):
        expected, computed = self.example_data_1(Pruner.BUCKET_COUNT, 3)
        self.assertEqual(expected, computed)
        return

    ''' Data 2 '''

    def test_nemex_bucket_t1_data_2(self):
        expected, computed = self.example_data_2(Pruner.BUCKET_COUNT, 1)
        self.assertEqual(expected, computed)
        return

    def test_nemex_bucket_t2_data_2(self):
        expected, computed = self.example_data_2(Pruner.BUCKET_COUNT, 2)
        self.assertEqual(expected, computed)
        return

    def test_nemex_bucket_t3_data_2(self):
        expected, computed = self.example_data_2(Pruner.BUCKET_COUNT, 3)
        self.assertEqual(expected, computed)
        return

    def tearDown(self) -> None:
        return None

    # TODO: data 3-8
    ''' Data 3 '''
    ''' Data 4 '''
    ''' Data 5 '''
    ''' Data 6 '''
    ''' Data 7 '''
    ''' Data 8 '''


if __name__ == '__main__':
    unittest.main()
