#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import lexer
import parser
import asmgen

def compile(fileInName, fileOutName):
    with open(fileInName, "r") as fileIn:
        lexPut = lexer.lex(fileIn.read())
        parsePut = parser.parse(lexPut)
        asm = asmgen.asmgenerate(parsePut)
        with open(fileOutName, "w") as fileOut:
            fileOut.write(asm)
    return True
