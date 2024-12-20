from enum import Enum, auto
from typing import List


class ASM:
    pass


class RegisterEnum(Enum):
    RAX = auto()
    EAX = auto()
    RBX = auto()
    EBX = auto()


class OperandASM(ASM):
    pass


class RegisterASM(OperandASM):
    def __init__(self, reg: RegisterEnum):
        self.val = reg

    def __repr__(self):
        return repr(self.val)

    def codegen(self):
        match self.val:
            case RegisterEnum.RAX:
                return "%rax"
            case RegisterEnum.EAX:
                return "%eax"
            case RegisterEnum.RBX:
                return "%rbx"
            case RegisterEnum.EBX:
                return "%ebx"
            case _:
                raise TypeError("Invalid Register: ", self.val)


class ImmediateASM(OperandASM):
    # Right now it's just immediate ints
    def __init__(self, val):
        self.val = val

    def __repr__(self):
        return repr(self.val)

    def codegen(self):
        return f"${self.val}"


class InstructionASM(ASM):
    pass


class MoveASM(InstructionASM):
    # WE only have move rn
    def __init__(self, src: OperandASM, dst: OperandASM):
        self.src = src
        self.dst = dst

    def __repr__(self):
        return f"MOVE({repr(self.src)}, {repr(self.dst)})"

    def codegen(self):
        return f"movl {self.src.codegen()}, {self.dst.codegen()}"


class ReturnASM(InstructionASM):
    def __repr__(self):
        return "RET"

    def codegen(self):
        return "ret"


class FunctionASM(ASM):
    def __init__(self, name: str, instructions: List[InstructionASM]):
        self.name = name
        self.instructions = instructions

    def __repr__(self):
        return f"FUNC({self.name}, {repr(self.instructions)})"

    def codegen(self):
        ## Note: this makes this compiler arch dependent
        ## This is made for linux at the moment
        res = ""
        res += f"\t.globl {self.name}\n"
        res += f"{self.name}:\n"
        for instruction in self.instructions:
            res += f"\t{instruction.codegen()}\n"
        if res == None:
            raise ValueError("Invalid Instruction")
        return res


class ProgramASM(ASM):
    def __init__(self, function: FunctionASM):
        self.function = function

    def __repr__(self):
        return f"PROG({repr(self.function)})"

    def codegen(self):
        res = self.function.codegen()
        res += '\n.section .note.GNU-stack,"",@progbits\n'
        return res