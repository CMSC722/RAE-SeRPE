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

"""
TOKENS

Following is the tokens list. This is used by both ply.lex and ply.yacc --
by ply.lex for validation purposes, by ply.yacc to identify valid terminals.
"""

reserved = {
    'if':       'IF',
    'then':     'THEN',
    'else':     'ELSE',
    'elsif':    'ELSIF',    # this makes lexing and parsing a bit easier
    'while':    'WHILE',
    'end':      'END',
    'not':      'NOT',
    'and':      'AND',
    '&&':       'AND',
    'or':       'OR',
    '||':       'OR'
}

tokens = list(reserved.values()) + [
    'NUMBER',
    'PLUS'
]

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

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID') # if it's not a keyword, it's an ID
    return t

# This allows us to track line numbers.
# Since it's not a rule -- but rather a kind of helper -- we do not capitalize
# it's identifier.
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)  # counts how many new lines and adds that
                                    # number to current lineno

# This helper rule defines which lexemes we ignore
t_ignore(t) = ' \t'

# This helper rule defines what we do when we encounter a lexing error
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# This, finally, builds the lexer:
lexer = lex.lex()


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
