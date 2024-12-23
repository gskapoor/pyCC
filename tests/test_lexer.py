import unittest
import pyCC.pyCmp.lexer as lexer


class TestLexer(unittest.TestCase):
    def test_int_lexing(self):
        result = lexer.lex("int")
        self.assertEqual(result, [(lexer.TokenType.INT, "int")])

    def test_neg_lexing(self):
        result = lexer.lex("-")
        self.assertEqual(result, [(lexer.TokenType.NEGATE, "-")])

    def test_bitflip_lexing(self):
        result = lexer.lex("~")
        self.assertEqual(result, [(lexer.TokenType.BITFLIP, "~")])

    def test_decr_lexing(self):
        ## For now, we want an "error"
        with self.assertRaises(NotImplementedError):
            lexer.lex("--")
        # self.assertEqual(result, [(lexer.TokenType.NEGATE, "-")])

    def test_plus_lexing(self):
        result = lexer.lex("+")
        self.assertEqual(result, [(lexer.TokenType.PLUS, "+")])

    def test_ast_lexing(self):
        result = lexer.lex("*")
        self.assertEqual(result, [(lexer.TokenType.ASTERISK, "*")])

    def test_fslash_parsing(self):
        result = lexer.lex("/")
        self.assertEqual(result, [(lexer.TokenType.FSLASH, "/")])

    def test_mod_parsing(self):
        result = lexer.lex("%")
        self.assertEqual(result, [(lexer.TokenType.MODULUS, "%")])


if __name__ == "__main__":
    unittest.main()
