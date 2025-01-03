from enum import Enum, auto
from typing import List


class ASM:
    pass


class RegisterEnum(Enum):
    RAX = auto()
    EAX = auto()
    RDX = auto()
    EDX = auto()
    R10D = auto()
    R11D = auto()


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
            case RegisterEnum.RDX:
                return "%rdx"
            case RegisterEnum.EDX:
                return "%edx"
            case RegisterEnum.R10D:
                return "%r10d"
            case RegisterEnum.R11D:
                return "%r11d"
            case _:
                raise TypeError("Invalid Register: ", self.val)


class IntASM(OperandASM):
    # Right now it's just immediate ints
    def __init__(self, val: int):
        self.val = val

    def __repr__(self):
        return f"INT({self.val})"

    def codegen(self):
        return f"${self.val}"


class PsuedoRegASM(OperandASM):
    def __init__(self, identifier: str):
        self.identifier = identifier

    def __repr__(self):
        return f"PsuedoReg({self.identifier})"


class StackASM(OperandASM):
    def __init__(self, num_vals: int):
        self.index = num_vals

    def __repr__(self):
        return f"Stack({self.index})"

    def codegen(self):
        return f"{self.index}(%rbp)"


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


class BinaryOpASM(Enum):
    ADD = auto()
    SUB = auto()
    MUL = auto()

    def codegen(self):
        if self == BinaryOpASM.ADD:
            return "addl"
        if self == BinaryOpASM.SUB:
            return "subl"
        if self == BinaryOpASM.MUL:
            return "imull"
        

class BinaryASM(InstructionASM):

    def __init__(self, op:BinaryOpASM, r_src: OperandASM, dst: OperandASM):
        self.op = op
        self.r_src = r_src
        self.dst = dst

    def __repr__(self):
        return f"Binary({self.op}, {repr(self.r_src)}, {repr(self.dst)})"
    
    def codegen(self):
        return f"{self.op.codegen()} {self.r_src.codegen()}, {self.dst.codegen()}"



class UnaryOpASM(Enum):
    NEG = auto()
    BITFLIP = auto()

    def codegen(self):
        if self == UnaryOpASM.NEG:
            return "negl"
        return "notl"

class UnaryASM(InstructionASM):

    def __init__(self, op: UnaryOpASM, dst: OperandASM):
        self.op = op
        self.dst = dst

    def __repr__(self):
        return f"Unary({self.op}, {repr(self.dst)})"
    
    def codegen(self):
        return f"{self.op.codegen()} {self.dst.codegen()}"
    
class IDivASM(InstructionASM):
    def __init__(self, src: OperandASM):
        self.src = src
    
    def __repr__(self):
        return f"IDiv({repr(self.src)})"
    
    def codegen(self):
        return f"idivl {self.src.codegen()}"
    

class CdqASM(InstructionASM):
    def __repr__(self):
        return "CDQ"
    
    def codegen(self):
        return "cdq"


class AllocateStack(InstructionASM):

    def __init__(self, num_vals: int):
        self.num_vals = num_vals

    def __repr__(self):
        return f"AllocateStack({self.num_vals})"
    
    def codegen(self):
        return f"subq ${self.num_vals}, %rsp"


class ReturnASM(InstructionASM):
    def __repr__(self):
        return "RET"

    def codegen(self):
        res = "movq %rbp, %rsp\n"
        res += "popq %rbp\n"
        res += "ret"
        return res


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
        res += "pushq %rbp\n"
        res += "movq %rsp, %rbp\n"
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
