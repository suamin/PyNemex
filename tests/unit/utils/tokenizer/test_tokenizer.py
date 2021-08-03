import unittest

from nemex import Tokenizer


class TestTokenizer(unittest.TestCase):

    def setUp(self) -> None:
        self.char = True
        self.q = 2
        self.special_char = "_"
        self.unique = False
        self.lower = True

        self.doc = "Lorem ipsum."

        self.tokenizer = Tokenizer(
            char=self.char,
            q=self.q,
            special_char=self.special_char,
            unique=self.unique,
            lower=self.lower
        )

        return None

    def test_tokenize_1(self):
        self.tokenizer.q = 1
        tokens = self.tokenizer.tokenize(self.doc)
        self.assertEqual(tokens, ["l", "o", "r", "e", "m", "_", "i", "p", "s", "u", "m", "."])

    def test_tokenize_2(self):
        self.tokenizer.q = 2
        tokens = self.tokenizer.tokenize(self.doc)
        self.assertEqual(tokens, ["lo", "or", "re", "em", "m_", "_i", "ip", "ps", "su", "um", "m."])

    def test_tokenize_3(self):
        self.tokenizer.q = 3
        tokens = self.tokenizer.tokenize(self.doc)
        self.assertEqual(tokens, ["lor", "ore", "rem", "em_", "m_i", "_ip", "ips", "psu", "sum", "um."])

    def test_tokenize_4(self):
        self.tokenizer.q = 4
        tokens = self.tokenizer.tokenize(self.doc)
        self.assertEqual(tokens, ["lore", "orem", "rem_", "em_i", "m_ip", "_ips", "ipsu", "psum", "sum."])

    def test_tokenize_5(self):
        self.tokenizer.q = 5
        tokens = self.tokenizer.tokenize(self.doc)
        self.assertEqual(tokens, ["lorem", "orem_", "rem_i", "em_ip", "m_ips", "_ipsu", "ipsum", "psum."])

    def tearDown(self) -> None:
        return None


if __name__ == '__main__':
    unittest.main()
