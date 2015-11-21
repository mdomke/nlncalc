#!/usr/bin/env python
# vim: set fileencoding: utf-8 :

# This is a simple script for testing the capabilities of the 
# natural number parser.

from __future__ import print_function

import re
import nlncalcparser
from ply import lex, yacc

if __name__ == '__main__':

    lexer = lex.lex(module=nlncalcparser, reflags=re.UNICODE)
    parser = yacc.yacc(module=nlncalcparser)

    while True:
        try:
            input_string = raw_input('> ')
        except EOFError:
            break

        try:
            result = parser.parse(input_string)
        except SyntaxError as e:
            print(str(e))
            continue 

        print(result)
