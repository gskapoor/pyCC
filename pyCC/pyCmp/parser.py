from enum import verify
from .ASTNode import (
    ConstIntNode,
    FunctionNode,
    ProgramNode,
    ReturnNode,
    IdentifierNode,
    ASTNode,
    UnaryExpressionNode,
    UnaryOperatorNode,
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

    def consumeTokens(self, *expectedTokens):
        if self.verifyTokens(*expectedTokens):
            self.pos += len(expectedTokens)
            return True
        return False

    def peek(self, num_tokens=1):
        if self.pos + num_tokens > len(self.tokens):
            return []
        res = []
        for i in range(num_tokens):
            res.append(self.tokens[self.pos + i][0])

        return res

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

        if not self.consumeTokens(TokenType.INT):
            self.pos = startingPos
            raise ValueError("Function did not start with Int")

        parsed_identifier = self.parseIdentifier()

        if not self.consumeTokens(
            TokenType.POPEN, TokenType.VOID, TokenType.PCLOSE, TokenType.BOPEN
        ):
            self.pos = startingPos
            raise ValueError("Function did not start with '(){'")

        parsed_statement = self.parseStatement()
        if not parsed_statement:
            return None

        if not self.consumeTokens(TokenType.BCLOSE):
            self.pos = startingPos
            raise ValueError("Can't parse Function")

        return FunctionNode(parsed_identifier, parsed_statement)

    def parseStatement(self):

        startingPos = self.pos
        if not self.consumeTokens(TokenType.RETURN):
            self.pos = startingPos
            return None

        parsedExpr = self.parseExpression()
        if not parsedExpr:
            self.pos = startingPos
            raise ValueError("Can't parse Statement")

        if not self.consumeTokens(TokenType.SEMICOLON):
            self.pos = startingPos
            raise ValueError("Can't parse Statement")

        return ReturnNode(parsedExpr)

    def parseExpression(self):

        if self.consumeTokens(TokenType.CONSTINT):
            res = ConstIntNode(int(self.tokens[self.pos - 1][1]))
            return res
        elif self.consumeTokens(TokenType.NEGATE):
            ## Unary time
            expr = self.parseExpression()
            return UnaryExpressionNode(UnaryOperatorNode.NEG, expr)
        elif self.consumeTokens(TokenType.BITFLIP):
            ## Unary time
            expr = self.parseExpression()
            return UnaryExpressionNode(UnaryOperatorNode.BITFLIP, expr)
        elif self.consumeTokens(TokenType.POPEN):
            expr = self.parseExpression()
            if not self.consumeTokens(TokenType.PCLOSE):
                raise ValueError("Can't parse Expression: Invalid Paranthesis Closure")
            return expr

        raise ValueError("Can't parse Expression")

    def parseIdentifier(self):

        if not self.consumeTokens(TokenType.IDENTIFIER):
            raise ValueError("Can't parse Identifier")

        name = self.tokens[self.pos - 1][1]
        return IdentifierNode(name)


def parse(lexed_input) -> ASTNode:
    myparser = Parser(lexed_input)
    res = myparser.parseProgram()
    return res
