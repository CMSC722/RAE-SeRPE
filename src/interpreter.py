"""
Date: Thu, 9 Feb, 2017
Last updated: Sat, 18 Feb, 2017
Author: Samuel Barham
Organization: University of Maryland, College Park (PhD student)

Project: RAE/SeRPE implementation
Component: Planning-DSL Interpreter

Description:
The interpreter exists to read in, parse, store, method files (whose content is
written in a simple domain-specific language) and to aid in executing the
tasks and methods they define. The first three functions mentioned (reading in,
parsing, and storing) are handled by the lexer/parser pair, which are built atop
the popular PLY (Pytnon Lex-Yacc). Their rules are defined in the files
lex_rules.py and yacc_rules.py, respectively. Whereas a lexer is built to
understand the lexical structure of a language, and a parser is built to under-
stand its grammatical structure (a higher level of organization), the
interpreter exists to attach a semantics to the grammatical structure captured
by the parser. The interpreter is written by hand, from scratch, unlike the
lexer and parser, because it is simple and the resulting is transparent
enough -- and this gives us a greater degree of control over the interpreter's
semantics and operation.

More information on the PLY module used to build the the lexer and the parser
can be found at the following URL:
http://www.dabeaz.com/ply/ply.html#ply_nn1

_________________

Finally, some ideas that we might consider future TODO's:
1) finish implementing local variable read/write for method bodies
2) write a lexer for domain description files, and design the lexer to
    construct a symbol table that it then passes to the method-file parser,
    so that we can check at compile-time that state variables are accessed
    with the proper number of arguments
3) enhance the domain description files and the dom-parser to construct a typed
    symbol table that is then supplied to the method-file parser, so that we can
    check at compile-time for type-consistency in the use of state variables
    (e.g., predicates appear only in boolean expressions, int/float-state vars
    only appear in numerical operations, etc.)
"""

# import statements here
import ply.lex as lex
import ply.yacc as yacc
from pydoc import pager # we'll be using this to produce less-like,
                        # paged output -- primarily for debugging purposes
import lex_rules        # this is the module where we've specified the lexer rules
import yacc_rules       # this is the module where we've specified the parser rules



# First we build the lexer and the parser, using the lexing and parsing rules
# defined in our lex_rules.py and yacc_rules.py files:
meth_lexer = lex.lex(module=lex_rules)
meth_parser = yacc.yacc(module=yacc_rules)

"""
EXPRESSION TYPES

The following hash defines the types of expressions in the byte-code used
by the intrepeter. The comments after each expression type lists their
arguments, and the types of those arguments, for the developer's convenience.
For now, we only list the types that have been actually implemented in the
parser, so as not to confuse:
"""

e_types = dict(
    # misc
    e_noop =    'NOOP',     # [no arguments]
    # statements
    e_seq =     'SEQ',      # local_variables (list), exprs (list)
    e_while =   'WHILE',    # cond (expr), exprs (list)
    e_if =      'IF',        # conds (expr list), blocks (list of lists of exprs)
    # binary operators
    e_and =     'AND',      # arg1 (expr), arg2 (expr)
    e_or =      'OR',       # "    "       "    "
    e_equals =  'EQUALS',   # "    "       "    "
    e_lt =      'LT',       # "    "       "    "
    e_gt =      'GT',       # "    "       "    "
    e_lte =     'LTE',      # "    "       "    "
    e_gte =     'GTE',      # "    "       "    "
    # unary operators
    e_not =     'NOT',      # arg1 (expr)
    # primitive values
    e_true =    'TRUE',     # arg1 (True)
    e_false =   'FALSE'     # arg1 (False)

)


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
    meth_lexer.input(input)

    # lex the file and aggregate the output
    output = ''
    while True:
        tok = meth_lexer.token()
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

def parse_print(filename, paged=True):
    """
    Attempts to open the file specified by the supplied path ('filename'),
    then reads the file in as a string, lexes it using the method-file lexer,
    parses it, and that prints the constructed AST in paged format (if paged
    is left set to True, as it is by default) -- or not (if paged is set to
    False).

    TODO: add error handling -- in particular against the case where the file-
    name is invalid or the specified file doesn't exist.
    """

    # try to read the supplied file
    input = ''
    with open(filename, 'r') as f:
        input = f.read()
    ast = meth_parser.parse(input, lexer=meth_lexer)

    print(type(ast))

    # print the output
    # if paged:
    #     pager(ast)
    # else:
    #     print(ast)

# some aliases for the above function, for Ruby-like happiness and convenience:
print_ast = parse_print
parser_print = parse_print


"""
TOP-LEVEL CODE

By convention, we'll put top-level code here, at the bottom of the file (and
we'll use such code for debugging purposes, since this file is intended to
function as a module).
"""

print_ast("domains/test_domain1/test_domain1.meth")
