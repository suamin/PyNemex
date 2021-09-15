import unittest

from nemex import Faerie, Pruner, BucketCountPruning, EntitiesDictionary, Default


class TestBucketCount(unittest.TestCase):

    def setUp(self) -> None:
        self.document = "Lorem ipsum dolor sit amet."
        self.entities = ["dolor"]
        self.doc_tokens = []
        self.Pe = []
        self.Te = 0
        self.Tl = 0
        self.tighter_neighbor_bound = None
        self.bound_args = ()
        self.entity_len = 0
        self.edict = None
        self.faerie = None
        return None

    def setArgs(self):
        self.edict = EntitiesDictionary.from_list(self.entities, Default.TOKENIZER)
        self.faerie = Faerie(self.edict, Default.SIMILARITY, Default.SIM_THRESH_CHAR, Default.TOKEN_THRESH, Pruner.BUCKET_COUNT)
        self.doc_tokens = Default.TOKENIZER(self.document)
        return

    def test_1(self):

        self.entities = ["dolor"]
        self.setArgs()

        pruner_args = ()

        inv_lists = self.faerie.inv_index[self.doc_tokens]
        self.faerie.init_from_inv_lists(inv_lists)

        BucketCountPruning.filter(*self.pruner_args)

        return

    def tearDown(self) -> None:
        return None


if __name__ == '__main__':
    unittest.main()
