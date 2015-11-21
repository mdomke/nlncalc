#!/usr/bin/env python

import re
import sys

# The bottle python web framework is used for serving the contents of the natural
# language numbers calcultor. 
# For more informations see http://bottle.paws.de/docs/dev/index.html
try: from bottle import route, run, request, template
except ImportError:
    print("Unable to import required WSGI module 'bottle'")
    sys.exit(-1)

try: from ply import lex, yacc
except ImportError:
    print("Unable to import required parser module 'ply'")
    sys.exit(-1)

# Add the 'parser'-directory to the path, so that the parser
# module can be found.
sys.path.insert(0, 'parser')
try: import nlncalcparser
except ImportError:
    print("Unable to import module 'nlncalcparser'.")
    sys.exit(-1)

# Build lexer and parser for the natural language calculator. The token definitions
# and parser rules are defined in the 'nlncalcparser' module.
lexer = lex.lex(module=nlncalcparser, reflags=re.UNICODE)
parser = yacc.yacc(module=nlncalcparser, outputdir='parser', debug=0)


@route('/')
def send_index_page():
    '''This function is called when the user navigates to the server root URL.
    It will generate an input form where the user can input a list of calculations.
    Each calculation can be expressed in natural language, arabic numbers ore a
    mixed form.'''
    return template('index')


@route('/result', method='POST')
def send_result_page():
    ''' This function is called when the user submits the input from and the '/result'-URL 
    is requested. It will calculate the result of each input line and hand over the result 
    list to the bottle template engine.'''
    input_text = request.forms.get('calcinput')

    result_list = list()
    for line in input_text.splitlines():
        try:
            calc_result = parser.parse(line)
        except (SyntaxError, ZeroDivisionError) as e:
            result_list = [str(e)]
            break

        result_list.append(calc_result)

    return template('result', result=result_list)


if __name__ == '__main__':
    # Start the webserver at port 8080
    run(host='localhost', port=8080)
