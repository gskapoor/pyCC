import unittest
from pyCC.pyCmp.ASTNode import (
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
        print(output)
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
        print(output)
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
        print(output)
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