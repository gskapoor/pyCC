from .ASMNode import (
    AllocateStack,
    BinaryASM,
    BinaryOpASM,
    CdqASM,
    CmpASM,
    CondFlags,
    FunctionASM,
    IDivASM,
    IntASM,
    JumpASM,
    JumpCCASM,
    LabelASM,
    PsuedoRegASM,
    RegisterASM,
    RegisterEnum,
    ReturnASM,
    SetCCASM,
    StackASM,
    UnaryASM,
    MoveASM,
    ProgramASM,
    UnaryOpASM,
)
from .tackyNode import (
    BinaryOpTacky,
    BinaryTacky,
    CopyTacky,
    JumpIfNotZero,
    JumpIfZero,
    JumpTacky,
    LabelTacky,
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
    BinaryOpTacky.LSHIFT: BinaryOpASM.LSHIFT,
    BinaryOpTacky.RSHIFT: BinaryOpASM.RSHIFT,
    BinaryOpTacky.BAND: BinaryOpASM.BAND,
    BinaryOpTacky.BOR: BinaryOpASM.BOR,
    BinaryOpTacky.BXOR: BinaryOpASM.BXOR,
}

REL_TO_FLAGS = {
    BinaryOpTacky.GE: CondFlags.G,
    BinaryOpTacky.GEQ: CondFlags.GE,
    BinaryOpTacky.LE: CondFlags.L,
    BinaryOpTacky.LEQ: CondFlags.LE,
    BinaryOpTacky.EQ: CondFlags.E,
    BinaryOpTacky.NEQ: CondFlags.NE,
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
        case CopyTacky(src=src, dst=dst):
            return [MoveASM(asmFromTacky(src), asmFromTacky(dst))]
        case UnaryTacky(op=op, src=src, dst=dst) if op == UnaryOpTacky.NOT:
            return [
                CmpASM(IntASM(0), asmFromTacky(src)),
                MoveASM(IntASM(0), asmFromTacky(dst)),
                SetCCASM(CondFlags.E, asmFromTacky(dst))
            ]
        case UnaryTacky(op=op, src=src, dst=dst):
            return [
                MoveASM(asmFromTacky(src), asmFromTacky(dst)),
                UnaryASM(OP_TABLE[op], asmFromTacky(dst)),
            ]
        case BinaryTacky(
            op=op, left_val=left_val, right_val=right_val, dst=dst
        ) if op in REL_TO_FLAGS:
            return [
                CmpASM(asmFromTacky(left_val), asmFromTacky(right_val)),
                MoveASM(IntASM(0), asmFromTacky(dst)),
                SetCCASM(REL_TO_FLAGS[op], asmFromTacky(dst)),
            ]
        case BinaryTacky(op=op, left_val=left_val, right_val=right_val, dst=dst):
            if op == BinaryOpTacky.DIV or op == BinaryOpTacky.MOD:
                dst = RegisterEnum.EAX
                if op == BinaryOpTacky.MOD:
                    dst = RegisterEnum.EDX

                return [
                    MoveASM(asmFromTacky(left_val), RegisterASM(RegisterEnum.EAX)),
                    CdqASM(),
                    IDivASM(asmFromTacky(right_val)),
                    MoveASM(RegisterASM(dst), asmFromTacky(dst)),
                ]
            return [
                MoveASM(asmFromTacky(left_val), asmFromTacky(dst)),
                BinaryASM(OP_TABLE[op], asmFromTacky(right_val), asmFromTacky(dst)),
            ]
        case JumpTacky(target=LabelTacky(name=name)):
            return [
                JumpASM(f".L{name}")
            ]
        case JumpIfZero(condition=condition, target=LabelTacky(name=name)):
            return [
                CmpASM(IntASM(0), asmFromTacky(condition)),
                JumpCCASM(CondFlags.E, f".L{name}"),
            ]
        case JumpIfNotZero(condition=condition, target=LabelTacky(name=name)):
            return [
                CmpASM(IntASM(0), asmFromTacky(condition)),
                JumpCCASM(CondFlags.NE, f".L{name}"),
            ]
        case LabelTacky(name=name):
            return [LabelASM(name)]
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

                        case CmpASM(left_operand=left_operand, right_operand=IntASM(val=x)):
                            res.append(MoveASM(IntASM(x), RegisterASM(RegisterEnum.R11D)))
                            res.append(CmpASM(left_operand, RegisterASM(RegisterEnum.R11D)))

                        case CmpASM(left_operand=PsuedoRegASM(identifier=l_name), right_operand=PsuedoRegASM(identifier=r_name)):
                            if l_name not in found:
                                num_vars += 1
                                found[l_name] = num_vars
                            if r_name not in found:
                                num_vars += 1
                                found[r_name] = num_vars

                            new_left = StackASM(-1 * sizeof_int * found[l_name])
                            new_right = StackASM(-1 * sizeof_int * found[r_name])
                            res.append(MoveASM(new_left, RegisterASM(RegisterEnum.R10D)))
                            res.append(CmpASM(RegisterASM(RegisterEnum.R10D), new_right))

                        case CmpASM(left_operand=PsuedoRegASM(identifier=l_name), right_operand=right_operand):
                            if l_name not in found:
                                num_vars += 1
                                found[l_name] = num_vars
                            new_left = StackASM(-1 * sizeof_int * found[l_name])
                            res.append(CmpASM(new_left, right_operand))

                        case CmpASM(left_operand=left_operand, right_operand=PsuedoRegASM(identifier=r_name)):
                            if r_name not in found:
                                num_vars += 1
                                found[r_name] = num_vars

                            new_right = StackASM(-1 * sizeof_int * found[r_name])
                            res.append(CmpASM(left_operand, new_right))

                        case SetCCASM(cond_code=cond_code, src=PsuedoRegASM(identifier=name)):
                            if name not in found:
                                num_vars += 1
                                found[name] = num_vars
                            new_src = StackASM(-1 * sizeof_int * found[name])
                            res.append(SetCCASM(cond_code, new_src))


                        case UnaryASM(op=cur_op, dst=PsuedoRegASM(identifier=dst_id)):
                            if dst_id not in found:
                                num_vars += 1
                                found[dst_id] = num_vars
                            new_dst = StackASM(-1 * sizeof_int * found[dst_id])
                            res.append(UnaryASM(cur_op, new_dst))

                        case BinaryASM(
                            op=cur_op,
                            r_src=PsuedoRegASM(identifier=r_src_id),
                            dst=PsuedoRegASM(identifier=dst_id),
                        ):
                            if r_src_id not in found:
                                num_vars += 1
                                found[r_src_id] = num_vars
                            if dst_id not in found:
                                num_vars += 1
                                found[dst] = num_vars
                            new_r_src = StackASM(-1 * sizeof_int * found[r_src_id])
                            new_dst = StackASM(-1 * sizeof_int * found[dst_id])

                            res.append(
                                MoveASM(new_r_src, RegisterASM(RegisterEnum.R10D))
                            )
                            if cur_op == BinaryOpASM.MUL:
                                ## TODO: rename the src/dst parameters
                                res.append(
                                    MoveASM(new_dst, RegisterASM(RegisterEnum.R11D))
                                )
                                res.append(
                                    BinaryASM(
                                        cur_op,
                                        RegisterASM(RegisterEnum.R10D),
                                        RegisterASM(RegisterEnum.R11D),
                                    )
                                )
                                res.append(
                                    MoveASM(RegisterASM(RegisterEnum.R11D), new_dst)
                                )
                            elif cur_op in {BinaryOpASM.LSHIFT, BinaryOpASM.RSHIFT}:
                                res.append(
                                    MoveASM(new_r_src, RegisterASM(RegisterEnum.ECX))
                                )
                                res.append(
                                    BinaryASM(
                                        cur_op, RegisterASM(RegisterEnum.CL), new_dst
                                    )
                                )
                            else:
                                res.append(
                                    BinaryASM(
                                        cur_op, RegisterASM(RegisterEnum.R10D), new_dst
                                    )
                                )
                        case BinaryASM(
                            op=cur_op, r_src=r_src, dst=PsuedoRegASM(identifier=dst_id)
                        ):
                            if dst_id not in found:
                                num_vars += 1
                                found[dst] = num_vars
                            new_dst = StackASM(-1 * sizeof_int * found[dst_id])
                            if cur_op == BinaryOpASM.MUL:
                                res.append(
                                    MoveASM(new_dst, RegisterASM(RegisterEnum.R11D))
                                )
                                res.append(
                                    BinaryASM(
                                        cur_op, r_src, RegisterASM(RegisterEnum.R11D)
                                    )
                                )
                                res.append(
                                    MoveASM(RegisterASM(RegisterEnum.R11D), new_dst)
                                )
                            elif cur_op in {BinaryOpASM.LSHIFT, BinaryOpASM.RSHIFT}:
                                res.append(
                                    MoveASM(r_src, RegisterASM(RegisterEnum.ECX))
                                )
                                res.append(
                                    BinaryASM(
                                        cur_op, RegisterASM(RegisterEnum.CL), new_dst
                                    )
                                )
                            else:
                                res.append(BinaryASM(cur_op, r_src, new_dst))

                        case BinaryASM(
                            op=cur_op,
                            r_src=PsuedoRegASM(identifier=r_src_id),
                            dst=dst,
                        ):
                            if r_src_id not in found:
                                num_vars += 1
                                found[r_src_id] = num_vars
                            new_r_src = StackASM(-1 * sizeof_int * found[r_src_id])

                            res.append(BinaryASM(cur_op, new_r_src, dst))

                        case IDivASM(src=PsuedoRegASM(identifier=id)):
                            if id not in found:
                                num_vars += 1
                                found[id] = num_vars
                            res.append(IDivASM(StackASM(-1 * sizeof_int * found[id])))

                        case IDivASM(src=IntASM(val=val)):
                            res.append(
                                MoveASM(IntASM(val), RegisterASM(RegisterEnum.R10D))
                            )
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
