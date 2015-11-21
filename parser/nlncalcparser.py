# module: nlncalcparser.py
# vim: set fileencoding: utf-8 :

# This file provides the parser and lexer rules for the natural language
# number calculator. A lexer rule can either be expressed as a variable
# that directly defines the regular expression for matching a specif token,
# or it can be a function. In either way the variables and functions have
# to have the name of the token to be matched prefixed with a 't_'. If a
# function is used for matching a token the corresponding regular expression
# has to bedefined in the doc-string of that function.
# The production rules of the parser are defined as regular python functions
# whos names have to begin with 'p_'. The production rule itself is defined
# in the doc-string of that function and is notated in EBNF format.
# For further informations on the syntax refer to http://www.dabeaz.com/ply/ply.html.


#---------------------------------------------------------------------
#   Lexer token defintions
#---------------------------------------------------------------------

tokens = (
    "ZERO",
    "ONE",
    "ONE_PREFIX",
    "ONE_PREFIX_2",
    "ONES",
    "TENS",
    "TEN_TO_NINETEEN",
    "HUNDRED",
    "THOUSAND",
    "MILLION",
    "MILLION_SUFFIX",
    "SEPARATOR",
    "NUMBER",
    "MINUS_PREFIX",
    "MINUS",
    "PLUS",
    "TIMES",
    "DIVIDE"
)

def t_TEN_TO_NINETEEN(t): 
    r'(zehn|elf|zwölf|dreizehn|vierzehn|fünfzehn|sechzehn|siebzehn|achtzehn|neunzehn)'
    if t.value == 'zehn':
        t.value = 10.0
    elif t.value == 'elf':
        t.value = 11.0
    elif t.value == 'zwölf':
        t.value = 12.0
    elif t.value == 'dreizehn':
        t.value = 13.0
    elif t.value == 'vierzehn':
        t.value = 14.0
    elif t.value == 'fünfzehn':
        t.value = 15.0
    elif t.value == 'sechzehn':
        t.value = 16.0
    elif t.value == 'siebzehn':
        t.value = 17.0
    elif t.value == 'achtzehn':
        t.value = 18.0
    elif t.value == 'neunzehn':
        t.value = 19.0
    return t

def t_TENS(t):
    r'(zwanzig|dreißig|vierzig|fünfzig|sechzig|siebzig|achtzig|neunzig)'
    if t.value == 'zwanzig':
        t.value = 20.0
    elif t.value == 'dreißig':
        t.value = 30.0
    elif t.value == 'vierzig':
        t.value = 40.0
    elif t.value == 'fünfzig':
        t.value = 50.0
    elif t.value == 'sechzig':
        t.value = 60.0
    elif t.value == 'siebzig':
        t.value = 70.0
    elif t.value == 'achtzig':
        t.value = 80.0
    elif t.value == 'neunzig':
        t.value = 90.0
    return t

def t_ONES(t):
    r'(zwei|drei|vier|fünf|sechs|sieben|acht|neun)'
    if t.value == 'zwei':
        t.value = 2.0
    elif t.value == 'drei':
        t.value = 3.0
    elif t.value == 'vier':
        t.value = 4.0
    elif t.value == 'fünf':
        t.value = 5.0
    elif t.value == 'sechs':
        t.value = 6.0
    elif t.value == 'sieben':
        t.value = 7.0
    elif t.value == 'acht':
        t.value = 8.0
    elif t.value == 'neun':
        t.value = 9.0
    return t

def t_ZERO(t):
    r'(null)'
    t.value = 0
    return t

def t_ONE(t):
    r'(eins)'
    t.value = 1.0
    return t

def t_ONE_PREFIX_2(t):
    r'(eine)'
    t.value = 1.0
    return t

def t_ONE_PREFIX(t):
    r'(ein)'
    t.value = 1
    return t

def t_HUNDRED(t):
    r'(hundert)'
    t.value = 100.0
    return t

def t_THOUSAND(t):
    r'(tausend)'
    t.value = 1000.0
    return t

def t_MILLION(t):
    r'(million)'
    t.value = 1000000.0
    return t


def t_NUMBER(t): 
    r'\d+'
    t.value = float(t.value)
    return t


t_MILLION_SUFFIX = r'(en)'
t_MINUS_PREFIX = r'(minus|-)'
t_MINUS = r'\s+(minus|-)\s+'
t_PLUS = r'\s+(plus|\+)\s+'
t_TIMES = r'\s+(mal|\*)\s+'
t_DIVIDE = r'\s+(durch|/)\s+'

t_SEPARATOR = r"(und)"

def t_error(t):
    raise SyntaxError("Syntax error: Unknown text '{0}'".format(t.value))

#---------------------------------------------------------------------
#   Parser production rules
#---------------------------------------------------------------------

def p_expression_plus(p):
    'expression         : expression PLUS term'
    p[0] = p[1] + p[3]

def p_expression_minus(p):
    'expression         : expression MINUS term'
    p[0] = p[1] - p[3]

def p_expression_term(p):
    'expression         : term'
    p[0] = p[1]

def p_term_times(p):
    'term               : term TIMES factor'
    p[0] = p[1] * p[3]

def p_term_div(p):
    'term               : term DIVIDE factor'
    p[0] = p[1] / p[3]

def p_term_factor(p):
    'term               : factor'
    p[0] = p[1]

def p_factor_num(p):
    'factor             : number'
    p[0] = p[1]

def p_number(p):
    '''number           : positive_number
                        | ZERO
                        | negative_number'''
    p[0] = p[1]

def p_positive_number(p):
    '''positive_number  : NUMBER
                        | nl_number'''
    p[0] = p[1]

def p_negative_number(p):
    '''negative_number  : MINUS_PREFIX positive_number'''
    p[0] = -1 * p[2]

def p_nl_number(p):
    '''nl_number        : nl_decimals
                        | nl_hundreds
                        | nl_thousands
                        | nl_millions'''
    p[0] = p[1]

def p_num_decimals(p):
    '''nl_decimals      : ONE
                        | num2_99'''
    p[0] = p[1]

def p_num2_99(p):
    '''num2_99          : num2_19
                        | num20_99'''
    p[0] = p[1]

def p_num2_19(p):
    '''num2_19          : ONES 
                        | TEN_TO_NINETEEN'''
    p[0] = p[1]

def p_num20_99(p):
    '''num20_99         : ONE_PREFIX SEPARATOR TENS
                        | ONES SEPARATOR TENS
                        | TENS'''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = p[1] + p[3]

def p_hundreds(p):
    '''hundreds         : ONE_PREFIX HUNDRED
                        | ONES HUNDRED
                        | HUNDRED'''
    if len(p) == 3:
        p[0] = p[1] * p[2]
    else:
        p[0] = p[1]


def p_hundred_common(p):
    '''hundred_common    : hundreds
                         | hundreds num2_99
                         | hundreds SEPARATOR num2_99'''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = p[1] + p[2]
    elif len(p) == 4:
        p[0] = p[1] + p[3]

def p_nl_hudreds(p):
    '''nl_hundreds      : hundred_common
                        | hundreds ONE
                        | hundreds SEPARATOR ONE'''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = p[1] + p[2]
    elif len(p) == 4:
        p[0] = p[1] + p[3]


def p_thousands(p):
    '''thousands        : hundred_common THOUSAND
                        | num2_99 THOUSAND
                        | ONE_PREFIX THOUSAND
                        | hundreds ONE_PREFIX THOUSAND
                        | hundreds SEPARATOR ONE_PREFIX THOUSAND
                        | THOUSAND'''
    if len(p) == 5:
        p[0] = (p[1] + p[3]) * p[4]
    if len(p) == 4:
        p[0] = (p[1] + p[2]) * p[3]
    elif len(p) == 3:
        p[0] = p[1] * p[2]
    elif len(p) == 2:
        p[0] = p[1]

def p_nl_thousands(p):
    '''nl_thousands     : thousands
                        | thousands nl_decimals
                        | thousands nl_hundreds
                        | thousands SEPARATOR nl_hundreds'''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = p[1] + p[2]
    elif len(p) == 4:
        p[0] = p[1] + p[3]

def p_millions(p):
    '''millions         : ONE_PREFIX_2 MILLION
                        | ONES MILLION MILLION_SUFFIX'''
    p[0] = p[1] * p[2]

def p_nl_millions(p):
    '''nl_millions      : millions
                        | millions nl_decimals
                        | millions nl_hundreds
                        | millions nl_thousands
                        | millions SEPARATOR nl_thousands'''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = p[1] + p[2]
    elif len(p) == 4:
        p[0] = p[1] + p[3]


def p_error(p):
    raise SyntaxError('Syntax error on input: Unexpected token {0}'.format(p.type))
