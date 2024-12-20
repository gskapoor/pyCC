from enum import Enum, auto
import re

class TokenType(Enum):
    CONSTINT = auto()
    INT = auto()
    VOID = auto()
    RETURN = auto()
    POPEN = auto()
    PCLOSE = auto()
    BOPEN = auto()
    BCLOSE = auto()
    SEMICOLON = auto()
    IDENTIFIER = auto()

TokenToRegex = {
    TokenType.CONSTINT   : re.compile(r'[0-9]+\b'), 
    TokenType.INT        : re.compile(r'int\b'), 
    TokenType.VOID       : re.compile(r'void\b'), 
    TokenType.RETURN     : re.compile(r'return\b'), 
    TokenType.POPEN      : re.compile(r'\('), 
    TokenType.PCLOSE     : re.compile(r'\)'), 
    TokenType.BOPEN      : re.compile(r'\{'), 
    TokenType.BCLOSE     : re.compile(r'\}'), 
    TokenType.SEMICOLON  : re.compile(r';'), 
    TokenType.IDENTIFIER : re.compile(r'[a-zA-Z_]\w*\b'), 
}

class Token:
    def __init__(self, token_type, regexStr):
        self.token_type = token_type
        pattern = re.compile


def lex(inputStr):
    res = []

    inputStr = inputStr.strip()
    while (inputStr != ""):
        found = False
        for type in TokenType:
            match = TokenToRegex[type].match(inputStr)
            if (match):
                found = True
                res.append((type, match[0]))
                inputStr = inputStr[len(match[0]):]
                break
        if not found:
            raise Exception("INVALID LEX")
            return res
        inputStr = inputStr.strip()
    return res

test = """
int main(void) {
    return 100;
}
"""

# print(lex(test))
