#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pyCC.pyCmp import lexer
from pyCC.pyCmp import parser
from pyCC.pyCmp import asmgen


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
            return True

        parse_put = parser.parse(lex_put)
        if mode < 2:
            return True

        asm = asmgen.asmgenerate(parse_put)
        if mode < 3:
            return True

        with open(file_out_name, "w", encoding="utf-8") as file_out:
            file_out.write(asm)

    return True
