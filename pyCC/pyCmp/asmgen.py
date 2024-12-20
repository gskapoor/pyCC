from .parser import *

def asmgenerate(ast: ProgramNode):
    asmTree = ast.assemble()
    return asmTree.codegen()
