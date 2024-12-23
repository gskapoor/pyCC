from .ASMNode import (
    AllocateStack,
    FunctionASM,
    IntASM,
    PsuedoRegASM,
    RegisterASM,
    RegisterEnum,
    ReturnASM,
    StackASM,
    UnaryASM,
    MoveASM,
    ProgramASM,
    UnaryOpASM,
)
from .ASTNode import ProgramNode
from .tackyNode import (
    TackyNode,
    ConstIntTacky,
    VarTacky,
    ReturnTacky,
    UnaryTacky,
    FuncTacky,
    ProgramTacky,
    UnaryOpTacky,
)

OP_TABLE = {UnaryOpTacky.NEG: UnaryOpASM.NEG, UnaryOpTacky.BITFLIP: UnaryOpASM.BITFLIP}


def asmFromTacky(node: TackyNode):
    match node:
        case ConstIntTacky(val=val):
            return IntASM(val)
        case VarTacky(name=name):
            return PsuedoRegASM(name)
        case ReturnTacky(val=val):
            asm_val = asmFromTacky(val)
            return [MoveASM(asm_val, RegisterEnum.EAX), ReturnASM()]
        case UnaryTacky(op=op, src=src, dst=dst):
            return [
                MoveASM(asmFromTacky(src), asmFromTacky(dst)),
                UnaryASM(OP_TABLE[op], asmFromTacky(dst)),
            ]
        case FuncTacky(identifier=identifier, instructions=instructions):
            res = [AllocateStack(0)]
            # Number of bytes/int in our version of C
            sizeof_int = 4

            num_vars = 0
            found = {}
            for instruction in instructions:
                new_ins = asmFromTacky(instruction)
                for ins in new_ins:
                    match ins:
                        case MoveASM(
                            src=PsuedoRegASM(identifier=src_id),
                            dst=PsuedoRegASM(identifier=dst_id),
                        ):
                            if src_id not in found:
                                num_vars += 1
                                found[src_id] = num_vars
                            if dst_id not in found:
                                num_vars += 1
                                found[dst_id] = num_vars
                            new_src = StackASM(-1 * sizeof_int * found[src_id])
                            new_dst = StackASM(-1 * sizeof_int * found[dst_id])
                            res.append(MoveASM(new_src, RegisterASM(RegisterEnum.R10D)))
                            res.append(MoveASM(RegisterASM(RegisterEnum.R10D), new_dst))
                        case MoveASM(src=PsuedoRegASM(identifier=src_id), dst=cur_dst):
                            if src_id not in found:
                                num_vars += 1
                                found[src_id] = num_vars
                            new_src = StackASM(-1 * sizeof_int * found[src_id])
                            res.append(MoveASM(new_src, cur_dst))
                        case MoveASM(
                            src=cur_source, dst=PsuedoRegASM(identifier=dst_id)
                        ):
                            if dst_id not in found:
                                num_vars += 1
                                found[dst_id] = num_vars
                            new_dst = StackASM(-1 * sizeof_int * found[dst_id])
                            res.append(MoveASM(cur_source, new_dst))
                        case UnaryASM(op=cur_op, dst=PsuedoRegASM(identifier=dst_id)):
                            if dst_id not in found:
                                num_vars += 1
                                found[dst_id] = num_vars
                            new_dst = StackASM(-1 * sizeof_int * found[dst_id])
                            res.append(UnaryASM(cur_op, new_dst))

                        case _:
                            res.append(ins)
            res[0].num_vals = num_vars * sizeof_int

            return FunctionASM(identifier, res)

        case ProgramTacky(function=function):
            return ProgramASM(asmFromTacky(function))

        case _:
            raise ValueError("Invalid TACKY Expr")


def asmgenerate(ast: ProgramNode) -> str:
    """Generate Assembly from the ProgNode

    Args:
        ast (ProgramNode): The AST parsed from the code

    Returns:
        str: Assembly Code
    """

    asm_tree = ast.assemble()
    return asm_tree.codegen()
