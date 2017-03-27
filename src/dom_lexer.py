##
## Domain lexer adapted from meth_lexer.py
##
import ply.lex as lex
import json                 
from pydoc import pager     

###############################
# Reserved words
###############################

reserved = {
    # variables
    'dock':            'DOCK',
    'robot':           'ROBOT',
    'cargo':           'CARGO',
    'pile' :	       'PILE',
    # relations
    'adjacent':        'ADJACENT',
    'on-dock':         'ONDECK',
    'on-robot':        'ONROBOT',
    'loc':             'LOC',    
    'in-pile':         'INPILE',
    # context
    'Variables':       'VARIABLES',
    'Rigid_Relations': 'RIGIDRELATIONS',
    'Ranges':          'RANGES',
    'Initial_State':   'INITIALSTATE',
    'Goal':            'GOAL'

}

###############################
# Tokens
###############################
# We might not need few of these -- needs to be revised
########################################################

tokens = list(set(reserved.values() + [
    # identifiers
    'ID',
    # data types
    'INT',
    'FLOAT',
    'STRING',
    # punctuation
    'LPAREN',
    'RPAREN',
    'COLON',
    'COMMA',
    'LBRACE',
    'RBRACE',
    # relational operators
    'EQUALS',
    'LTE',
    'GTE',
    'LT',
    'GT',
    # binary boolean operators
    'AND',
    'OR',
    # binary arithmetic operators
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDED',
    # unary boolean operator
    'NOT',
    # assignment operator
    'ASSIGN',
    # boolean primitives
    'TRUE',
    'FALSE',
    # Null
    'NIL'
]))

###############################
# Token Rules
###############################

# punctuation
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LBRACE  = r'\{'
t_RBRACE  = r'\}'
t_COLON =   r':'
t_COMMA =   r','


# relational operators
t_EQUALS =  r'=='
t_LTE =     r'<='
t_GTE =     r'>='
t_LT =      r'<'
t_GT =      r'>'

# binary arithmetic operators
t_PLUS =    r'\+'
t_MINUS =   r'-'
t_TIMES =   r'\*'
t_DIVIDED = r'/' 

# binary boolean operators
t_AND =     r'&&'
t_OR =      r'\|\|'

# unary boolean operator
t_NOT =     r'!'

# assignment operator
t_ASSIGN =  r'='

# boolean primitives
t_TRUE =    r'True'
t_FALSE =   r'False'

# This helper rule defines which lexemes we ignore
t_ignore = ' \t'

###############################
# Token Action Rules
###############################
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9-]*'
    t.type = reserved.get(t.value, 'ID') # if it's not a keyword, it's an ID
    return t

def t_INT(t):
    r'[-+]?0|([1-9]\d*)'
    t.value = int(t.value)
    return t

def t_FLOAT(t):
    r'([-+]?0?|([1-9]\d*))\.?\d+'
    t.value = float(t.value)
    return t

def t_STRING(t):
    r'["\'][^"\r\n]*["\']'
    t.value = t.value[1:-1]
    return t

def t_ONE_LINE_COMMENT(t):
    r'(\#.*$)|(//.*$)'
    pass

def t_MULTI_LINE_COMMENT(t):
    r'/\*(.|[\n\r])*?\*/'
    pass

def find_column(input,token):
    """
    This helper function computes the column at which the current token begins.
    This is super useful for error-handling. Here 'input' is the input text
    string and 'token' is a token instance.
    """
    last_cr = input.rfind('\n',0,token.lexpos)
    if last_cr < 0:
        last_cr = 0
        column = (token.lexpos - last_cr) + 1
    return column

'''
def t_NUMBER(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t
'''


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

def lex_print(filename, paged=True):
    """
    Attempts to open the file specified by the supplied path ('filename'),
    then reads the file in as a string, lexes it, and prints the lexed output
    in paged format (if paged is left True) -- or not (if paged is set to
    False).

    TODO: add error handling -- in particular against the case where the file-
    name is invalid or the specified file doesn't exist.
    """

    # try to read the supplied file
    input = ''
    with open(filename, 'r') as f:
        input = f.read()
    global_meth_lexer_instance.input(input)

    # lex the file and aggregate the output
    output = ''
    while True:
        tok = global_meth_lexer_instance.token()
        if not tok:
            break
        output += (tok.__repr__() + '\n')
    output += '\n'

    # print the output
    if paged:
        pager(output)
    else:
        print(output)



# some aliases for the above function, for Ruby-like happiness convenience:
print_token_stream = lex_print

"""
Create a global lexer instance.
Other modules should get their lexer from here, to avoid building
unnecessary finite automata.
"""
global_dom_lexer_instance = lex.lex(optimize=1,lextab="dom_test_tab")
# global_dom_lexer_instance = lex.lex()

def get_lexer():
    return global_dom_lexer_instance