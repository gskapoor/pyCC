from .ASTNode import (
    ConstantNode,
    ExpressionNode,
    FunctionNode,
    ProgramNode,
    ReturnNode,
    IdentifierNode,
    ASTNode,
)
from .lexer import TokenType


class Parser:
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
        self.root.function = parsedFunc
        return self.root

    def parseFunction(self):
        startingPos = self.pos

        if self.pos > len(self.tokens):
            self.pos = startingPos
            return None

        if not self.verifyTokens(TokenType.INT):
            self.pos = startingPos
            raise ValueError("Function did not start with Int")

        self.pos += 1

        parsed_identifier = self.parseIdentifier()

        if not self.verifyTokens(
            TokenType.POPEN, TokenType.VOID, TokenType.PCLOSE, TokenType.BOPEN
        ):
            self.pos = startingPos
            raise ValueError("Function did not start with '(){'")

        self.pos += 4

        parsed_statement = self.parseStatement()
        if not parsed_statement:
            return None

        if not self.verifyTokens(TokenType.BCLOSE):
            self.pos = startingPos
            raise ValueError("Can't parse Function")

        self.pos += 1

        return FunctionNode(parsed_identifier, parsed_statement)

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

        if not self.verifyTokens(TokenType.SEMICOLON):
            self.pos = startingPos
            raise ValueError("Can't parse Statement")

        self.pos += 1

        return ReturnNode(parsedExpr)

    def parseExpression(self):

        if not self.verifyTokens(TokenType.CONSTINT):
            raise ValueError("Can't parse Expression")

        res = ExpressionNode(ConstantNode(self.tokens[self.pos][1]))
        self.pos += 1
        return res

    def parseIdentifier(self):
        if not self.verifyTokens(TokenType.IDENTIFIER):
            raise ValueError("Can't parse Identifier")

        name = self.tokens[self.pos][1]
        self.pos += 1
        return IdentifierNode(name)


def parse(lexed_input) -> ASTNode:
    myparser = Parser(lexed_input)
    res = myparser.parseProgram()
    return res
