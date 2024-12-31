import unittest

from pyCC.pyCmp.ASTNode import (
    BinaryExpressionNode,
    ReturnNode,
    ConstIntNode,
    IdentifierNode,
    BinaryOperatorNode,
)
from pyCC.pyCmp.tackyNode import (
    BinaryOpTacky,
    BinaryTacky,
    ConstIntTacky,
    CopyTacky,
    FuncTacky,
    JumpIfNotZero,
    JumpIfZero,
    JumpTacky,
    Label,
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

    def test_binary_tackygen(self):
        test_expr = BinaryExpressionNode(
            BinaryOperatorNode.ADD, ConstIntNode(1), ConstIntNode(1)
        )
        gen = tackygen.TackyGen()
        _, output = gen.emit_tacky(test_expr)
        expected = [
            BinaryTacky(
                BinaryOpTacky.ADD, ConstIntTacky(1), ConstIntTacky(1), VarTacky(".tmp0")
            )
        ]
        self.assertEqual(str(output), str(expected))

    def test_binary_prog0(self):
        test_prog = """
                    int main(void){
                        return 1 + 2 + 3;
                    }
                    """
        output = str(tackygen.tackify(parser.parse(lexer.lex(test_prog))))
        expected = str(
            ProgramTacky(
                FuncTacky(
                    "main",
                    [
                        BinaryTacky(
                            BinaryOpTacky.ADD,
                            ConstIntTacky(1),
                            ConstIntTacky(2),
                            VarTacky(".tmp0"),
                        ),
                        BinaryTacky(
                            BinaryOpTacky.ADD,
                            VarTacky(".tmp0"),
                            ConstIntTacky(3),
                            VarTacky(".tmp1"),
                        ),
                        ReturnTacky(VarTacky(".tmp1")),
                    ],
                )
            )
        )
        self.assertEqual(output, expected)

    def test_mixed_binary_0(self):
        test_prog = """
                    int main(void) {
                        return 
                            1 + 3  % (1 + 2);
                    }
                    """
        output = str(tackygen.tackify(parser.parse(lexer.lex(test_prog))))
        expected = str(
            ProgramTacky(
                FuncTacky(
                    "main",
                    [
                        BinaryTacky(
                            BinaryOpTacky.ADD,
                            ConstIntTacky(1),
                            ConstIntTacky(2),
                            VarTacky(".tmp0"),
                        ),
                        BinaryTacky(
                            BinaryOpTacky.MOD,
                            ConstIntTacky(3),
                            VarTacky(".tmp0"),
                            VarTacky(".tmp1"),
                        ),
                        BinaryTacky(
                            BinaryOpTacky.ADD,
                            ConstIntTacky(1),
                            VarTacky(".tmp1"),
                            VarTacky(".tmp2"),
                        ),
                        ReturnTacky(VarTacky(".tmp2")),
                    ],
                )
            )
        )
        self.assertEqual(output, expected)

    def test_bitop_binary(self):
        test_prog = """
                    int main(void) {
                        return 
                            1 << 2;
                    }
                    """
        output = str(tackygen.tackify(parser.parse(lexer.lex(test_prog))))
        expected = str(
            ProgramTacky(
                FuncTacky(
                    "main",
                    [
                        BinaryTacky(
                            BinaryOpTacky.LSHIFT,
                            ConstIntTacky(1),
                            ConstIntTacky(2),
                            VarTacky(".tmp0"),
                        ),
                        ReturnTacky(VarTacky(".tmp0")),
                    ],
                )
            )
        )
        self.assertEqual(output, expected)

    def test_land_eval(self):
        return_ast = BinaryExpressionNode(
            BinaryOperatorNode.LAND, ConstIntNode(1), ConstIntNode(2)
        )
        gen = tackygen.TackyGen()
        _, res = gen.emit_tacky(return_ast)
        expected = [
            JumpIfZero(ConstIntTacky(1), Label("and_false(0)")),
            JumpIfZero(ConstIntTacky(2), Label("and_false(0)")),
            CopyTacky(ConstIntTacky(1), VarTacky(".tmp0")),
            JumpTacky(Label("and_end(0)")),
            Label("and_false(0)"),
            CopyTacky(ConstIntTacky(0), VarTacky(".tmp0")),
            Label("and_end(0)")
        ]

        self.assertEqual(str(res), str(expected))

    def test_lor_eval(self):
        return_ast = BinaryExpressionNode(
            BinaryOperatorNode.LOR, ConstIntNode(1), ConstIntNode(2)
        )
        gen = tackygen.TackyGen()
        _, res = gen.emit_tacky(return_ast)
        expected = [
            JumpIfNotZero(ConstIntTacky(1), Label("or_true(0)")),
            JumpIfNotZero(ConstIntTacky(2), Label("or_true(0)")),
            CopyTacky(ConstIntTacky(0), VarTacky(".tmp0")),
            JumpTacky(Label("or_end(0)")),
            Label("or_true(0)"),
            CopyTacky(ConstIntTacky(1), VarTacky(".tmp0")),
            Label("or_end(0)")
        ]

        self.assertEqual(str(res), str(expected))

    def test_logic_short_circuit(self):
        self.maxDiff=None
        return_ast = BinaryExpressionNode(
            BinaryOperatorNode.LOR, BinaryExpressionNode(
                BinaryOperatorNode.EQ,
                ConstIntNode(1),
                ConstIntNode(2)
            ), ConstIntNode(3)
        )
        gen = tackygen.TackyGen()
        _, res = gen.emit_tacky(return_ast)
        expected = [
            BinaryTacky(BinaryOpTacky.EQ, ConstIntTacky(1), ConstIntTacky(2), VarTacky(".tmp1")),
            JumpIfNotZero(VarTacky(".tmp1"), Label("or_true(0)")),
            JumpIfNotZero(ConstIntTacky(3), Label("or_true(0)")),
            CopyTacky(ConstIntTacky(0), VarTacky(".tmp0")),
            JumpTacky(Label("or_end(0)")),
            Label("or_true(0)"),
            CopyTacky(ConstIntTacky(1), VarTacky(".tmp0")),
            Label("or_end(0)")
        ]

        self.assertEqual(str(res), str(expected))


