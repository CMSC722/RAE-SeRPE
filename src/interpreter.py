"""
Date: Thu, 9 Feb, 2017 -- ???
Author: Samuel Barham
Organization: University of Maryland, College Park (PhD student)

Project: RAE/SeRPE implementation
Component: Planning-DSL Interpreter

Description:
The interpreter exists to read in, parse, store, method files (whose content is
written in a simple domain-specific language) and to aid in executing the
tasks and methods they define. The first three functions mentioned (reading in,
parsing, and storing) is handled by the lexer/parser pair, which are built atop
the popular PLY (Pytnon Lex-Yacc). The Interpreter is written by hand, from
scratch, because it is simple and the resulting code transparent enough.
"""

# import statements here
import ply.lex as lex
from pydoc import pager # we'll be using this to produce less-like,
                        # paged output -- primarily for debugging purposes

"""
TOKENS

Following is the tokens list. This is used by both ply.lex and ply.yacc --
by ply.lex for validation purposes, by ply.yacc to identify valid terminals.
"""

reserved = {
    # statement delimiters
    'task':     'TASK',
    'pre':      'PRE',
    'body':     'BODY',
    # control structure keywords
    'if':       'IF',
    'then':     'THEN',
    'else':     'ELSE',
    'elsif':    'ELSIF',    # this makes lexing and parsing a bit easier
    'while':    'WHILE',
    #'for':      'FOR',
    #'in':       'IN',
    'end':      'END',
    # boolean operators
    'not':      'NOT',
    'and':      'AND',
    'or':       'OR',
}

# list(set()) is a common means of removing duplicates from a list
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
    # relational operators
    'EQUALS',
    'LTE',
    'GTE',
    'LT',
    'GT',
    # boolean operators
    'AND',
    'OR',
    # assignment operator
    'ASSIGN'
]))

"""
LEXER

The lexer provided by ply.lex returns lexemes, or tokens, in the form of
LexToken objects. A LexToken object has instance fields (attributes):
    tok.type
    tok.value [these two form the traditional Token-type/Token-value pair]
    tok.lineno
    tok.linepos [these are used for bookkeeping purposes -- and are handy
                 when, for instance, issuing parse errors. Note that
                 tok.linepos refers to the index of the token relative to the
                 start of the input text]

The lexer is provided with a token stream in the form of a string via the
lex.lex.input() method. It usses tokens one by one via the lex.lex.token()
method.

Lexer token rules can be specified as simple token rules -- i.e., ones that
merely return the token's value --, or as token action rules -- i.e., ones
that perform actions on the token's value(s) [for instance, aggregating a list].
In the former case, the rule is written as a simple assignment of a RE (qua raw
string) to a variable whose identifier begins with 't_' followed by the desired
name of the token (in all caps, to distinguish these rules from those that
include actions). In the latter case, the rules are written as regular Python
functions, each of which takes a paramter 't' which represents a LexToken
object, whose value field (.value) has already been set to the string that the
token represents. Here, the regular expression used to capture the token is
provided as the function's documentation string.
"""

# ########################## #
# Simple token rules follow: #
# ########################## #

# punctuation
t_LPAREN =  r'\('
t_RPAREN =  r'\)'
t_COLON =   r':'
t_COMMA =   r','

# relational operators
t_EQUALS =  r'=='
t_LTE =     r'<='
t_GTE =     r'>='
t_LT =      r'<'
t_GT =      r'>'

# boolean operators
t_AND =     r'&&'
t_OR =      r'\|\|'
t_NOT =     r'!'

# assignment operator
t_ASSIGN =    '='

# This helper rule defines which lexemes we ignore
t_ignore = ' \t'

# ########################## #
# Token action rules follow: #
# ########################## #


# This function identifies keywords and issues the appropriate
# tokens (e.g., 'body' => 'BODY', or ',' => 'COMMA') -- *or*, if
# no such keyword has been defined, assumes the token is an (e.g.,
# 'some_var' => 'ID').
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

# This allows us to track line numbers.
# Since it's not a rule -- but rather a kind of helper -- we do not capitalize
# it's identifier.
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)  # counts how many new lines and adds that
                                    # number to current lineno

# This helper rule defines what we do when we encounter a lexing error
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

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

# This, finally, builds the lexer:
lexer = lex.lex()

"""
TEST METHODS

These are some useful methods for sanity-checking basic aspects of the
lexer and parser. They can be run from the top-level (e.g., at the bottom
of this file) to get an idea at a glance of whether anything is horribly
broken.
"""

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
    lexer.input(input)

    # lex the file and aggregate the output
    output = ''
    while True:
        tok = lexer.token()
        if not tok:
            break
        output += (tok.__repr__() + '\n')
    output += '\n'

    # print the output
    if paged:
        pager(output)
    else:
        print(output)


"""
INTERPRETER API

The API defines exposes the interpreter's functionality to other components in
the RAE/SeRPE organism. Broadly speaking, it provides functions for loading
(registering) method files and for executing, line by line, the methods they
describe. Objects describing the domain (planning.Domain, which describes the
state space) and definitions of the actions available (planning.Actions) must
be provided to the interpreter prior to using it. Other functions are provided
to allow finer-grained configuration of the interpreter.
"""

def load_methods(filename):
    # 1) read in the file as a string
    # 2) feed the string to the lexer (lex.lex.input())
    # 3) feed the token stream to the parser
    # 4) save the resulting abstract syntax tree (AST)
    return None

def execute():
    # perhaps we keep track of where we are in the AST and what state
    # the world is in and resume from there?
    pass

"""
TOP-LEVEL CODE

By convention, we'll put top-level code here, at the bottom of the file (and
we'll use such code for debugging purposes, since this file is intended to
function as a module).
"""

lex_print("domains/test_domain1/test_domain1.meth")
