import unittest

from pyCC.pyCmp.ASTNode import ReturnNode, ConstIntNode, IdentifierNode
from pyCC.pyCmp.tackyNode import (
    ConstIntTacky,
    FuncTacky,
    ProgramTacky,
    ReturnTacky,
    UnaryTacky,
    VarTacky,
    UnaryOpTacky,
)
import pyCC.pyCmp.tackygen as tackygen
import pyCC.pyCmp.parser as parser
import pyCC.pyCmp.lexer as lexer


class TestTackygen(unittest.TestCase):

    def test_identifier_tackygen(self):
        identifier_ast = IdentifierNode("main")
        res = tackygen.tackify(identifier_ast)
        self.assertEqual(res, "main")

    def test_return_tackygen(self):
        return_ast = ReturnNode(ConstIntNode(1))
        res = tackygen.tackify(return_ast)
        expected = [ReturnTacky(ConstIntTacky(1))]
        self.assertEqual(str(res), str(expected))

    def test_invalid_emit(self):
        tacky_generator = tackygen.TackyGen()
        with self.assertRaises(TypeError):
            tacky_generator.emit_tacky(ReturnNode(ConstIntNode(1)))

    def test_basic_prog(self):
        ## this requires parsing tests to pass as well
        test_prog = """
                    int main(void){
                        return 1;
                    }
                    """
        output = str(tackygen.tackify(parser.parse(lexer.lex(test_prog))))
        expected = str(ProgramTacky(FuncTacky("main", [ReturnTacky(ConstIntTacky(1))])))
        self.assertEqual(output, expected)

    def test_unary_prog0(self):
        ## this requires parsing tests to pass as well
        test_prog = """
                    int main(void){
                        return (-1);
                    }
                    """
        output = str(tackygen.tackify(parser.parse(lexer.lex(test_prog))))
        expected = str(
            ProgramTacky(
                FuncTacky(
                    "main",
                    [
                        UnaryTacky(
                            UnaryOpTacky.NEG, ConstIntTacky(1), VarTacky(".tmp0")
                        ),
                        ReturnTacky(VarTacky(".tmp0")),
                    ],
                )
            )
        )
        self.assertEqual(output, expected)

    def test_unary_prog1(self):
        ## this requires parsing tests to pass as well
        test_prog = """
                    int main(void){
                        return ~(-1);
                    }
                    """
        output = str(tackygen.tackify(parser.parse(lexer.lex(test_prog))))
        expected = str(
            ProgramTacky(
                FuncTacky(
                    "main",
                    [
                        UnaryTacky(
                            UnaryOpTacky.NEG, ConstIntTacky(1), VarTacky(".tmp0")
                        ),
                        UnaryTacky(
                            UnaryOpTacky.BITFLIP, VarTacky(".tmp0"), VarTacky(".tmp1")
                        ),
                        ReturnTacky(VarTacky(".tmp1")),
                    ],
                )
            )
        )
        self.assertEqual(output, expected)
