#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from . import tackygen
from . import lexer
from . import parser
from . import asmgen


def py_compile(file_in_name: str, file_out_name: str, mode: int):
    """_summary_

    Args:
        file_in_name (str): Name of the input file
        file_out_name (str): name of the output file
        mode (int): Which level of compiling the compiler will run under,
                    (default is 4 (max level))

    Returns:
        _type_: _description_
    """
    with open(file_in_name, "r", encoding="utf-8") as file_in:
        lex_put = lexer.lex(file_in.read())
        if mode < 1:
            print(lex_put)
            return True

        parse_put = parser.parse(lex_put)
        if mode < 2:
            print(parse_put)
            return True

        tacky = tackygen.tackify(parse_put)
        if mode < 3:
            print(tacky)
            return True

        asm = asmgen.asmgenerate(tacky)

        with open(file_out_name, "w", encoding="utf-8") as file_out:
            file_out.write(asm)

    return True
