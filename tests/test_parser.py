import unittest
from pyCC.pyCmp.ASTNode import (
    ConstantNode,
    ExpressionNode,
    FunctionNode,
    IdentifierNode,
    ProgramNode,
    ReturnNode,
)
import pyCC.pyCmp.parser as parser
import pyCC.pyCmp.lexer as lexer
from pyCC.pyCmp.ASMNode import *


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
            FunctionNode(
                IdentifierNode("main"), ReturnNode(ExpressionNode(ConstantNode(1)))
            )
        )
        self.assertEqual(str(output), str(expected))
