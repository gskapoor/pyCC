from enum import Enum, auto
from typing import List

from lexer import TokenType

class ASTNode:
    # Base Node Class
    pass

class IdentifierNode(ASTNode):
    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return self.name

class ConstantNode(ASTNode):
    ## TODO: add different types of 'values'
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return repr(self.value)

    def assemble(self):
        return ImmediateASM(self.value)
 

class ExpressionNode(ASTNode):
    def __init__(self, constant: ConstantNode):
        # This should be refactored to have the bottom (constant) inherit
        self.constant = constant

    def __repr__(self):
        return (f"ExprNode({repr(self.constant)})")
    
    def assemble(self):
        return self.constant.assemble()
 
class ReturnNode(ASTNode):
    def __init__(self, expression: ExpressionNode):
        self.expression = expression

    def __repr__(self):
        return (f"ReturnNode({repr(self.expression)})")
    
    def assemble(self):
        exprASM = self.expression.assemble()
        return [
            MoveASM(exprASM, RegisterASM(RegistersEnum.EAX)),
            ReturnASM()]
 
class FunctionNode(ASTNode):
    def __init__(self, identifier: IdentifierNode, statement: ReturnNode):
        self.identifier = identifier
        self.statement = statement

    def __repr__(self):
        return (f"FunctionNode({repr(self.identifier)}, {repr(self.statement)})")
    
    def assemble(self):
        funcName = repr(self.identifier)
        statementAsm = self.statement.assemble()
        return FunctionASM(funcName, statementAsm)

class ProgramNode(ASTNode):
    def __init__(self, function: FunctionNode):
        self.function = function

    def __repr__(self):
        return (f"ProgramNode({repr(self.function)})")
    
    def assemble(self):
        funcASM = self.function.assemble()
        return ProgramASM(funcASM)
   
class ASM():
    pass
   
class RegistersEnum(Enum):
    RAX = auto()
    EAX = auto()
    RBX = auto()
    EBX = auto()

class OperandASM(ASM):
    pass

class RegisterASM(OperandASM):
    def __init__(self, reg: RegistersEnum):
        self.val = reg

    def __repr__(self):
        return repr(self.val)

class ImmediateASM(OperandASM):
    def __init__(self, val):
        self.val = val
    
    def __repr__(self):
        return repr(self.val)

class InstructionASM(ASM):
    pass

class MoveASM(InstructionASM):
    # WE only have move rn
    def __init__(self, src: OperandASM, dst: OperandASM):
        self.src = src
        self.dst = dst
    
    def __repr__(self):
        return f"MOVE({repr(self.src)}, {repr(self.dst)})"

class ReturnASM(InstructionASM):
    def __repr__(self):
        return f"RET"

class FunctionASM(ASM):
    def __init__(self, name: str, instructions: List[InstructionASM]):
        self.name = name
        self.instructions = instructions

    def __repr__(self):
        return f"FUNC({self.name}, {repr(self.instructions)})"

class ProgramASM(ASM):
    def __init__(self, function: FunctionASM):
        self.function = function

    def __repr__(self):
        return f"PROG({repr(self.function)})"
 

class Parser():
    def __init__(self, tokens):
        self.tokens = tokens
        self.root = ProgramNode(None)
        self.pos = 0

    def verifyTokens(self, *expectedTokens):
        if self.pos + len(expectedTokens) > len(self.tokens):
            return False
        
        for index, token in enumerate(expectedTokens):
            if self.tokens[self.pos + index][0] != token:
                return False
        return True


    def parseProgram(self):
        ## Always start with a 'prog' 
        parsedFunc = self.parseFunction()
        if not parsedFunc:
            return None

        ## Should ensure that there isn't anything extra
        ## This may actually be unecessary
        if len(self.tokens) != self.pos:
            raise ValueError("Didn't quite parse everything")
            return None
        self.root.function = parsedFunc
        return self.root

    def parseFunction(self):
        ## TODO: figure this error handling out properly
        startingPos = self.pos

        if self.pos > len(self.tokens):
            self.pos = startingPos
            return None
        
        if not self.verifyTokens(TokenType.INT):
            self.pos = startingPos
            raise ValueError("Function did not start with Int")
            return None
        self.pos += 1

        parsedIdentifier = self.parseIdentifier()

        if not self.verifyTokens(TokenType.POPEN, TokenType.VOID, TokenType.PCLOSE, TokenType.BOPEN):
            self.pos = startingPos
            raise ValueError("Function did not start with '(){'")
            return None
        self.pos += 4

        parsedStatement = self.parseStatement()
        if not parsedStatement:
            return None


        if not self.verifyTokens(TokenType.BCLOSE):
            self.pos = startingPos
            raise ValueError("Can't parse Function")
            return None
        self.pos += 1
       
        return FunctionNode(parsedIdentifier, parsedStatement)

    def parseStatement(self):

        startingPos = self.pos
        if not self.verifyTokens(TokenType.RETURN):
            self.pos = startingPos
            return None
        self.pos += 1

        parsedExpr = self.parseExpression()
        if not parsedExpr:
            self.pos = startingPos
            raise ValueError("Can't parse Statement")
            return None

        if not self.verifyTokens(TokenType.SEMICOLON):
            self.pos = startingPos
            raise ValueError("Can't parse Statement")
            return None
        self.pos += 1

        return ReturnNode(parsedExpr)
    
    def parseExpression(self):

        if not self.verifyTokens(TokenType.CONSTINT):
            raise ValueError("Can't parse Expression")
            return None
        res = ExpressionNode(ConstantNode(self.tokens[self.pos][1]))
        self.pos += 1
        return res

    def parseIdentifier(self):
        if not self.verifyTokens(TokenType.IDENTIFIER):
            raise ValueError("Can't parse Identifier")
            return None
        
        name = self.tokens[self.pos][1]
        self.pos += 1
        return IdentifierNode(name)


def parse(input):
    myparser = Parser(input)
    res = myparser.parseProgram()
    print(res.assemble())
    return res;
