from .parser import ProgramNode

def asmgenerate(ast: ProgramNode) -> str:
    """ Generate Assembly from the ProgNode 

    Args:
        ast (ProgramNode): The AST parsed from the code

    Returns:
        str: Assembly Code
    """

    asm_tree = ast.assemble()
    return asm_tree.codegen()
