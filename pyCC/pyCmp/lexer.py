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

def lex(input_str: str):
    res = []

    input_str = input_str.strip()
    while input_str != "":
        found = False
        for token_type in TokenType:
            match = TokenToRegex[token_type].match(input_str)
            if match:
                found = True
                res.append((token_type, match[0]))
                input_str = input_str[len(match[0]):]
                break
        if not found:
            raise ValueError("INVALID LEX")
        input_str = input_str.strip()
    return res
