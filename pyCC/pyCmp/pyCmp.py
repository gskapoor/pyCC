#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from . import lexer
from . import parser
from . import asmgen

def compile(fileInName, fileOutName, mode):
    with open(fileInName, "r") as fileIn:
        lexPut = lexer.lex(fileIn.read())
        parsePut = parser.parse(lexPut)
        asm = asmgen.asmgenerate(parsePut)
        # for now, use this dummy value:
        with open(fileOutName, "w") as fileOut:
            fileOut.write(asm)
    return True
