import unittest
from pyCC.pyCmp.ASTNode import (
    BinaryExpressionNode,
    BinaryOperatorNode,
    ConstIntNode,
    UnaryOperatorNode,
    UnaryExpressionNode,
    FunctionNode,
    IdentifierNode,
    ProgramNode,
    ReturnNode,
)
import pyCC.pyCmp.parser as parser
import pyCC.pyCmp.lexer as lexer


class TestParser(unittest.TestCase):
    def test_invalid_empty(self):
        with self.assertRaises(ValueError):
            parser.parse([])

    def test_basic_return(self):
        test_prog = """
                    int main(void){
                        return 1;
                    }
                    """
        output = parser.parse(lexer.lex(test_prog))
        expected = ProgramNode(
            FunctionNode(IdentifierNode("main"), ReturnNode(ConstIntNode(1)))
        )
        self.assertEqual(str(output), str(expected))

    def test_invalid_return(self):
        test_prog = """
                        int main(void){
                            return bajook;
                        }
                        """
        lexed_text = lexer.lex(test_prog)
        with self.assertRaises(ValueError):
            parser.parse(lexed_text)

    def test_unary_return(self):
        test_prog = """
                    int main(void){
                        return -1;
                    }
                    """
        output = parser.parse(lexer.lex(test_prog))
        expected = ProgramNode(
            FunctionNode(
                IdentifierNode("main"),
                ReturnNode(UnaryExpressionNode(UnaryOperatorNode.NEG, ConstIntNode(1))),
            )
        )
        self.assertEqual(str(output), str(expected))

    def test_paren_return(self):
        test_prog = """
                    int main(void){
                        return (1);
                    }
                    """
        output = parser.parse(lexer.lex(test_prog))
        expected = ProgramNode(
            FunctionNode(IdentifierNode("main"), ReturnNode(ConstIntNode(1)))
        )

        self.assertEqual(str(output), str(expected))

    def test_invalid_paren(self):
        test_prog = """
                        int main(void){
                            return (1;
                        }
                        """
        lexed_text = lexer.lex(test_prog)
        with self.assertRaises(ValueError):
            parser.parse(lexed_text)

    def test_basic_binary(self):
        test_prog = """
                    int main(void){
                        return (1 + 1);
                    }
                    """
        output = parser.parse(lexer.lex(test_prog))
        expected = ProgramNode(
            FunctionNode(
                IdentifierNode("main"),
                ReturnNode(
                    BinaryExpressionNode(
                        BinaryOperatorNode.ADD, ConstIntNode(1), ConstIntNode(1)
                    )
                ),
            )
        )

        self.assertEqual(str(output), str(expected))

    def test_precedent_binary(self):
        test_prog = """
                    int main(void){
                        return (1 + 1 * 2);
                    }
                    """
        output = parser.parse(lexer.lex(test_prog))
        expected = ProgramNode(
            FunctionNode(
                IdentifierNode("main"),
                ReturnNode(
                    BinaryExpressionNode(
                        BinaryOperatorNode.ADD,
                        ConstIntNode(1),
                        BinaryExpressionNode(
                            BinaryOperatorNode.MUL, ConstIntNode(1), ConstIntNode(2)
                        ),
                    )
                ),
            )
        )

        self.assertEqual(str(output), str(expected))

    def test_assoc_binary(self):
        test_prog = """
                    int main(void){
                        return (4 / 2 / 1);
                    }
                    """
        output = parser.parse(lexer.lex(test_prog))
        expected = ProgramNode(
            FunctionNode(
                IdentifierNode("main"),
                ReturnNode(
                    BinaryExpressionNode(
                        BinaryOperatorNode.DIV,
                        BinaryExpressionNode(
                            BinaryOperatorNode.DIV, ConstIntNode(4), ConstIntNode(2)
                        ),
                        ConstIntNode(1),
                    )
                ),
            )
        )
        self.assertEqual(str(output), str(expected))

    def test_unary_with_binary(self):
        test_prog = """
                    int main(void){
                        return -1 + 1 ;
                    }
                    """
        output = parser.parse(lexer.lex(test_prog))
        expected = ProgramNode(
            FunctionNode(
                IdentifierNode("main"),
                ReturnNode(
                    BinaryExpressionNode(
                        BinaryOperatorNode.ADD,
                        UnaryExpressionNode(
                            UnaryOperatorNode.NEG, ConstIntNode(1)),
                        ConstIntNode(1)
                    )
                ),
            )
        )
        self.assertEqual(str(output), str(expected))