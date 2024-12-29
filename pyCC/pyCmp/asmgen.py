from .ASMNode import (
    AllocateStack,
    BinaryASM,
    BinaryOpASM,
    CdqASM,
    FunctionASM,
    IDivASM,
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
from .tackyNode import (
    BinaryOpTacky,
    BinaryTacky,
    TackyNode,
    ConstIntTacky,
    VarTacky,
    ReturnTacky,
    UnaryTacky,
    FuncTacky,
    ProgramTacky,
    UnaryOpTacky,
)

OP_TABLE = {
    UnaryOpTacky.NEG: UnaryOpASM.NEG,
    UnaryOpTacky.BITFLIP: UnaryOpASM.BITFLIP,
    BinaryOpTacky.ADD: BinaryOpASM.ADD,
    BinaryOpTacky.SUB: BinaryOpASM.SUB,
    BinaryOpTacky.MUL: BinaryOpASM.MUL,
    }


def asmFromTacky(node: TackyNode):
    match node:
        case ConstIntTacky(val=val):
            return IntASM(val)
        case VarTacky(name=name):
            return PsuedoRegASM(name)
        case ReturnTacky(val=val):
            asm_val = asmFromTacky(val)
            return [MoveASM(asm_val, RegisterASM(RegisterEnum.EAX)), ReturnASM()]
        case UnaryTacky(op=op, src=src, dst=dst_reg):
            return [
                MoveASM(asmFromTacky(src), asmFromTacky(dst_reg)),
                UnaryASM(OP_TABLE[op], asmFromTacky(dst_reg)),
            ]
        case BinaryTacky(op=op, left_val=left_val, right_val=right_val, dst=dst):
            if op == BinaryOpTacky.DIV or op == BinaryOpTacky.MOD:
                dst_reg = RegisterEnum.EAX
                if op == BinaryOpTacky.MOD:
                    dst_reg = RegisterEnum.EDX

                print("Here's the right vals: ")
                print(right_val)
                print(asmFromTacky(right_val))
                return [
                    MoveASM(asmFromTacky(left_val), RegisterASM(RegisterEnum.EAX)),
                    CdqASM(),
                    IDivASM(asmFromTacky(right_val)),
                    MoveASM(RegisterASM(dst_reg), asmFromTacky(dst))
                ]
            return [
                MoveASM(asmFromTacky(left_val), asmFromTacky(dst)),
                BinaryASM(OP_TABLE[op], asmFromTacky(right_val), asmFromTacky(dst))
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

                        case BinaryASM(op=cur_op, r_src=PsuedoRegASM(identifier=r_src_id),dst=PsuedoRegASM(identifier=dst_id)):
                            if r_src_id not in found:
                                num_vars += 1
                                found[r_src_id] = num_vars
                            if dst_id not in found:
                                num_vars += 1
                                found[dst_reg] = num_vars
                            new_r_src = StackASM(-1 * sizeof_int * found[r_src_id])
                            new_dst = StackASM(-1 * sizeof_int * found[dst_id])

                            res.append(MoveASM(new_r_src, RegisterASM(RegisterEnum.R10D)))
                            if cur_op == BinaryOpASM.MUL:
                                res.append(MoveASM(new_dst, RegisterASM(RegisterEnum.R11D)))
                                res.append(BinaryASM(cur_op, RegisterASM(RegisterEnum.R10D), RegisterASM(RegisterEnum.R11D)))
                                res.append(MoveASM(RegisterASM(RegisterEnum.R11D), new_dst))
                            else:
                                res.append(BinaryASM(cur_op, RegisterASM(RegisterEnum.R10D), new_dst))
                        case BinaryASM(op=cur_op, r_src=r_src, dst=PsuedoRegASM(identifier=dst_id)):
                            if dst_id not in found:
                                num_vars += 1
                                found[dst_reg] = num_vars
                            new_dst = StackASM(-1 * sizeof_int * found[dst_id])
                            if cur_op == BinaryOpASM.MUL:
                                res.append(MoveASM(new_dst, RegisterASM(RegisterEnum.R11D)))
                                res.append(BinaryASM(cur_op, r_src, RegisterASM(RegisterEnum.R11D)))
                                res.append(MoveASM(RegisterASM(RegisterEnum.R11D), new_dst))
                            else:
                                res.append(BinaryASM(cur_op, r_src, new_dst))

                        case BinaryASM(op=cur_op, r_src=PsuedoRegASM(identifier=r_src_id),dst=dst_reg):
                            if r_src_id not in found:
                                num_vars += 1
                                found[r_src_id] = num_vars
                            new_r_src = StackASM(-1 * sizeof_int * found[r_src_id])

                            res.append(BinaryASM(cur_op, new_r_src, dst_reg))

                        case IDivASM(src=PsuedoRegASM(identifier=id)):
                            if id not in found:
                                num_vars += 1
                                found[id] = num_vars
                            res.append(IDivASM(StackASM(-1 * sizeof_int * found[id])))

                        case IDivASM(src=IntASM(val=val)):
                            res.append(MoveASM(IntASM(val), RegisterASM(RegisterEnum.R10D)))
                            res.append(IDivASM(RegisterASM(RegisterEnum.R10D)))



                        case _:
                            res.append(ins)
            res[0].num_vals = num_vars * sizeof_int

            return FunctionASM(identifier, res)

        case ProgramTacky(func=func):
            return ProgramASM(asmFromTacky(func))

        case _:
            raise ValueError("Invalid TACKY Expr: ", node)


def asmgenerate(tacky: TackyNode) -> str:
    """Generate Assembly from the ProgNode

    Args:
        ast (ProgramNode): The AST parsed from the code

    Returns:
        str: Assembly Code
    """
    asm = asmFromTacky(tacky)
    return asm.codegen()
