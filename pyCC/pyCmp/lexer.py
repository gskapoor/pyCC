from enum import Enum, auto
import re
from typing import List, Tuple


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
    PLUS = auto()
    ASTERISK = auto()
    FSLASH = auto()
    MODULUS = auto()
    DECREMENT = auto()
    NEGATE = auto()
    BITFLIP = auto()
    IDENTIFIER = auto()


TokenToRegex = {
    TokenType.CONSTINT: re.compile(r"[0-9]+\b"),
    TokenType.INT: re.compile(r"int\b"),
    TokenType.VOID: re.compile(r"void\b"),
    TokenType.RETURN: re.compile(r"return\b"),
    TokenType.POPEN: re.compile(r"\("),
    TokenType.PCLOSE: re.compile(r"\)"),
    TokenType.BOPEN: re.compile(r"\{"),
    TokenType.BCLOSE: re.compile(r"\}"),
    TokenType.SEMICOLON: re.compile(r";"),
    TokenType.PLUS: re.compile(r"\+"),
    TokenType.ASTERISK: re.compile(r"\*"),
    TokenType.FSLASH: re.compile(r"/"),
    TokenType.MODULUS: re.compile(r"%"),
    TokenType.DECREMENT: re.compile(r"--"),
    TokenType.NEGATE: re.compile(r"-"),
    TokenType.BITFLIP: re.compile(r"~"),
    TokenType.IDENTIFIER: re.compile(r"[a-zA-Z_]\w*\b"),
}


def lex(input_str: str) -> List[Tuple[TokenType, str]]:
    """Lexes input string into Tokens

    Args:
        input_str (str): The input string

    Raises:
        ValueError: Error parsing

    Returns:
        List[(TokenType, str)]: Tokens lexed
    """
    res = []

    input_str = input_str.strip()
    while input_str != "":
        found = False
        for token_type in TokenType:
            match = TokenToRegex[token_type].match(input_str)
            if match:
                if token_type == TokenType.DECREMENT:
                    raise NotImplementedError("Decrement isn't supported yet")
                found = True
                res.append((token_type, match[0]))
                input_str = input_str[len(match[0]) :]
                break
        if not found:
            raise ValueError("INVALID LEX")
        input_str = input_str.strip()
    return res
