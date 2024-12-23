#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import subprocess

from pyCmp.pyCmp import py_compile  # pylint: disable=all


def main() -> int:
    """
    _summary_ Main Function for Compiler
    """

    args = sys.argv
    mode = 4
    if len(args) < 2 or len(args) > 3:
        print(f"Usage: {args[0]} <C file> {{--lex|--parse|--codegen}}", file=sys.stderr)
        return 1

    if len(args) == 3:
        if args[2] == "--lex":
            mode = 0
        elif args[2] == "--parse":
            mode = 1
        elif args[2] == "--tacky":
            mode = 2
        elif args[2] == "--codegen":
            mode = 3
        else:
            print(
                f"Usage: {args[0]} <C file> {{--lex|--parse|--codegen}}",
                file=sys.stderr,
            )
            return 1

    file_name = args[1]
    if file_name[-2:] != ".c":
        print(f'Err: Invalid File Type "{file_name}"', file=sys.stderr)
        return 1
    file_prefix = file_name[:-2]

    result = subprocess.run(
        ["gcc", "-E", "-P", file_name, "-o", f"{file_prefix}.i"],
        capture_output=True,
        text=True,
        check=True,
    )

    if result.returncode != 0:
        print("Err: Unable to PreProcess", file=sys.stderr)
        print(result.stderr, file=sys.stderr, end="")
        return 1
    ## Compile time : )
    py_compile(f"{file_prefix}.i", f"{file_prefix}.s", mode)
    subprocess.run(["rm", f"{file_prefix}.i"], check=True)

    if mode < 4:
        return 0

    ## Assembling time : )
    result = subprocess.run(
        ["gcc", f"{file_prefix}.s", "-o", file_prefix],
        capture_output=True,
        text=True,
        check=True,
    )
    if result.returncode != 0:
        print("Err: Unable to PreProcess", file=sys.stderr)
        print(result.stderr, file=sys.stderr, end="")
        return 1

    subprocess.run(["rm", f"{file_prefix}.s"], check=True)

    return 0


if __name__ == "__main__":
    exitCode = main()
    sys.exit(exitCode)
