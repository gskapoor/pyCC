import unittest

from pyCC.pyCmp.ASMNode import (
    AllocateStack,
    BinaryASM,
    BinaryOpASM,
    CmpASM,
    CondFlags,
    FunctionASM,
    JumpCCASM,
    PsuedoRegASM,
    IntASM,
    RegisterASM,
    RegisterEnum,
    MoveASM,
    ReturnASM,
    UnaryASM,
    UnaryOpASM,
    StackASM
)
from pyCC.pyCmp.tackyNode import (
    BinaryOpTacky,
    BinaryTacky,
    FuncTacky,
    JumpIfZero,
    ReturnTacky,
    UnaryOpTacky,
    UnaryTacky,
    VarTacky,
    ConstIntTacky,
)
import pyCC.pyCmp.asmgen as asmgen
import pyCC.pyCmp.tackygen as tackygen
import pyCC.pyCmp.parser as parser
import pyCC.pyCmp.lexer as lexer


class AsmgenTest(unittest.TestCase):
    def test_var(self):
        test_input = VarTacky("obama")
        output = asmgen.asmFromTacky(test_input)
        expected_output = PsuedoRegASM("obama")
        self.assertEqual(str(output), str(expected_output))

    def test_constint(self):
        test_input = ConstIntTacky(21)
        output = asmgen.asmFromTacky(test_input)
        expected_output = IntASM(21)
        self.assertEqual(str(output), str(expected_output))

    def test_return(self):
        test_input = ReturnTacky(ConstIntTacky(1))
        output = asmgen.asmFromTacky(test_input)
        expected_output = [MoveASM(IntASM(1), RegisterEnum.EAX), ReturnASM()]
        self.assertEqual(str(output), str(expected_output))

    def test_unary(self):
        test_input = UnaryTacky(
            UnaryOpTacky.BITFLIP, ConstIntTacky(0), VarTacky("obama")
        )
        output = asmgen.asmFromTacky(test_input)
        expected_output = [
            MoveASM(IntASM(0), PsuedoRegASM("obama")),
            UnaryASM(UnaryOpASM.BITFLIP, PsuedoRegASM("obama")),
        ]
        self.assertEqual(str(output), str(expected_output))

    def test_function_oneunary(self):
        test_input = FuncTacky("main", [UnaryTacky(
            UnaryOpTacky.BITFLIP, ConstIntTacky(0), VarTacky("obama")
        )])
        output = asmgen.asmFromTacky(test_input)
        expected_output = FunctionASM("main", [
            AllocateStack(4),
            MoveASM(IntASM(0), StackASM(-4)),
            UnaryASM(UnaryOpASM.BITFLIP, StackASM(-4)),
        ])
        self.assertEqual(str(output), str(expected_output))

    def test_function_multivar(self):
        test_input = FuncTacky("main", [UnaryTacky(
            UnaryOpTacky.BITFLIP, ConstIntTacky(0), VarTacky("obama")
        ),
        UnaryTacky(
            UnaryOpTacky.NEG, VarTacky("obama"), VarTacky("newbama")
        )
        ])
        output = asmgen.asmFromTacky(test_input)
        expected_output = FunctionASM("main", [
            AllocateStack(8),
            MoveASM(IntASM(0), StackASM(-4)),
            UnaryASM(UnaryOpASM.BITFLIP, StackASM(-4)),
            MoveASM(StackASM(-4), RegisterASM(RegisterEnum.R10D)),
            MoveASM(RegisterASM(RegisterEnum.R10D), StackASM(-8)),
            UnaryASM(UnaryOpASM.NEG, StackASM(-8)),
        ])
        self.assertEqual(str(output), str(expected_output))

    def test_function_binary_op(self):
        test_input = FuncTacky("main", [
            BinaryTacky(
                BinaryOpTacky.ADD, VarTacky("obama"), VarTacky("obama"), VarTacky("jobama")
            )
        ])
        output = asmgen.asmFromTacky(test_input)
        expected_output = FunctionASM("main", [
            AllocateStack(8),
            MoveASM(StackASM(-4), RegisterASM(RegisterEnum.R10D)),
            MoveASM(RegisterASM(RegisterEnum.R10D), StackASM(-8)),
            MoveASM(StackASM(-4), RegisterASM(RegisterEnum.R10D)),
            BinaryASM(BinaryOpASM.ADD, RegisterASM(RegisterEnum.R10D), StackASM(-8))
        ])
        self.assertEqual(str(output), str(expected_output))

    def test_jz(self):
        test_input = JumpIfZero(ConstIntTacky(0), "obama")
        output = asmgen.asmFromTacky(test_input)
        expected_output = [
            CmpASM(IntASM(0), IntASM(0)),
            JumpCCASM(CondFlags.E, "obama")
        ]
        self.assertEqual(str(output), str(expected_output))

if __name__ == "__main__":
    unittest.main()
