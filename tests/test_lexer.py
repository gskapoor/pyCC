import unittest
import pyCC.pyCmp.lexer as lexer


class TestLexer(unittest.TestCase):
    def test_int_parsing(self):
        result = lexer.lex("int")
        self.assertEqual(result, [(lexer.TokenType.INT, "int")])

    def test_neg_parsing(self):
        result = lexer.lex("-")
        self.assertEqual(result, [(lexer.TokenType.NEGATE, "-")])

    def test_bitflip_parsing(self):
        result = lexer.lex("~")
        self.assertEqual(result, [(lexer.TokenType.BITFLIP, "~")])

    def test_decr_parsing(self):
        ## For now, we want an "error"
        with self.assertRaises(NotImplementedError):
            lexer.lex("--")
        # self.assertEqual(result, [(lexer.TokenType.NEGATE, "-")])


if __name__ == "__main__":
    unittest.main()
