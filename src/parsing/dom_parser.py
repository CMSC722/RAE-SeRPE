"""
Date: Thu, Sat, 18 Feb, 2017
Last updated: Mon, 27 Mar, 2017
Author: Samuel Barham
Organization: University of Maryland, College Park (PhD student)

Project: RAE/SeRPE implementation
Component: Planning-DSL Interpreter

Description:
A parser is, for our purposes, a component which, given a token stream,
identifies syntactic relations between the lexemes in that token stream,
aggregating the tokens into larger structures. That is, to put it crudely,
where a lexer takes a stream of characters and groups them into "words", a
parser takes "words" and groups them into expressions and statements and blocks.
Thus, a lexer is built to understand lexical structure, and a parser is built
to understand grammatical structure (a higher level of organization). The
interpreter, then, attaches a semantics to the grammatical structure supplied
by the parser.

Just as it is rare to write a lexer by hand, it is even rarer to write a parser
by hand, and so we delegate the process of parser generation to special tools
built for that purpose. The UNIX tool that has traditionally been used to
generate parsers is called yacc, which stands for Yet Another Compiler Compiler.
PLY is a popular Python-implementation of the UNIX lex/yacc tools, and
this file defines the rules by which PLY will create the parser for our domain
file language -- i.e., the format in which we will describe our planning
domains. These planning domains consist of five types of data, divided into
five subsections by means of headers. Those headers (and the types of data des-
cribed in each subsection of the file) are as follows:
    Objects -- the sets of objects that exist in the planning domains, defined
        using a simple set notation
    Rigid relations -- the set of unchanging relationships between objects in
        the planning domain
    State-variable ranges -- the set of those relationships in the planning
        domain that change from state to state
    Initial state -- the initial state of the planning problem
    Goal -- the goal state of the planning problem
It may be seen that the first three subections describe a general planning
domain, whereas the last two describe a particular planning problem over that
domain.

More information on the PLY module and how it works can be found at the
following URL: http://www.dabeaz.com/ply/ply.html#ply_nn1
"""

import ply.yacc as yacc
from dom_lexer import tokens
from dom_lexer import get_dom_lexer
import json                     # a better way of getting a pretty print of a dict
                                # from interpreter.py import meth_parser
from pydoc import pager         # we'll be using this to produce less-like,
                                # paged output -- primarily for debugging purposes

"""
JSON EXTENSION

Here we do some magic in order to extend Python's JSON encoder
so that it can handle Python sets (which it can't otherwise). To wit,
we just convert the sets into lists, which can be serialized. Remember --
JSON has at its disposal only the built-in datatypes of JavaScript, which
are more limited than those of Python.
"""

class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)


"""
GLOBALS
"""

DEBUG = False
domain = dict()

"""
START SYMBOL
"""

def p_start(p):
    'start : obj rig s0 goal'
    domain['objects'] = p[1]
    domain['rigid_rels'] = p[2]
    domain['state_vars'] = p[3]
    domain['goal'] = p[4]
    p[0] = domain


"""
FILE HEADERS
"""

def p_obj(p):
    'obj : OBJ COLON obj_sets'
    p[0] = p[3]

def p_rig(p):
    'rig : RIG COLON rig_rels'
    p[0] = p[3]

'''
def p_svr(p):
    'svs : SVS state_var_ranges'
    p[0] = p[2]
'''

def p_s0(p):
    's0 : S0 COLON initial_state_atoms'
    p[0] = p[3]

def p_goal(p):
    'goal : GOAL COLON goal_state_atoms'
    p[0] = p[3]


"""
OBJECT SETS
"""

def p_obj_sets(p):
    '''obj_sets :
                | ID EQUALS obj_set obj_sets'''
    if len(p) == 1:
        p[0] = dict()
    else:
        p[0] = {
            p[1]: p[3]
        }
        p[0].update(p[4])

def p_obj_set(p):
    '''obj_set : LBRACK INT RBRACK
               | LBRACK FLOAT RBRACK
               | LBRACK BOOL RBRACK
               | LBRACK NIL RBRACK
               | LBRACK obj_atoms      '''
    if len(p) == 4:
        if p[2] == 'int':
            p[0] = {int}
        elif p[2] == 'float':
            p[0] = {float}
        elif p[2] == 'string':
            p[0] = {str}
        elif p[2] == 'bool':
            p[0] = {bool}
        elif p[2] == 'nil':
            p[0] = {None}
    else:
        p[0] = p[2]

def p_obj_atoms(p):
    '''obj_atoms : RBRACK
                | obj_atom RBRACK
                | obj_atom COMMA obj_atoms '''
    if len(p) == 2:
        p[0] = set()
    elif len(p) == 3:
        p[0] = {p[1]}
    else:
        p[0] = p[3]
        p[0].update({p[1]})

def p_obj_atom(p):
    '''obj_atom : ID
                | INT
                | FLOAT
                | TRUE
                | FALSE
                | NIL   '''
    if isinstance(p[1], (int, long)):
        p[0] = int(p[1])
    elif isinstance(p[1], (float)):
        p[0] = float(p[1])
    elif p[1] == "True":
        p[0] = True
    elif p[1] == "False":
        p[0] = False
    elif p[1] == "nil":
        p[0] = None
    else:
        p[0] = p[1]

"""
RIGID RELATIONSHIPS
"""

def p_rig_rels(p):
    '''rig_rels :
                | ID EQUALS rig_rel rig_rels '''
    if len(p) == 1:
        p[0] = dict()
    else:
        p[0] = {
            p[1]: p[3]
        }
        p[0].update(p[4])

def p_rig_rel(p):
    'rig_rel : LBRACK tuples'
    p[0] = p[2]

def p_tuples(p):
    '''tuples : RBRACK
              | tuple RBRACK
              | tuple COMMA tuples '''
    if len(p) == 2:
        p[0] = []
    elif len(p) == 3:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_tuple(p):
    'tuple : LPAREN ids'
    p[0] = p[2]

def p_ids(p):
    '''ids : RPAREN
           | ID RPAREN
           | ID COMMA ids '''
    if len(p) == 2:
        p[0] = tuple()
    elif len(p) == 3:
        p[0] = tuple([p[1]])
    else:
        p[0] = tuple([p[1]]) + p[3]

"""
STATE VARIABLE RANGES

NB: this is commented out at the moment, pending design decisions regarding
precisely how to use the ranges of state variables, and whether we really
need this information to implement RAE/SeRPE

def p_state_var_ranges(p):
    '''state_var_ranges : ID LPAREN ids RPAREN EQUALS  state_var_ranges
                |                                         '''
    if len(p) == 1:
        p[0] = dict()
    else:
        p[0] = {
            p[1]: p[3]
        }
        p[0].update(p[4])

def p_state_var_range(p):

"""

"""
INITIAL STATE ATOMS
"""

def p_initial_state_atoms(p):
    '''initial_state_atoms :
                           | ID LPAREN ids EQUALS obj_atom initial_state_atoms '''
    if len(p) == 1:
        p[0] = dict()
    else:
        p[0] = p[6]
        # temp = dict()
        # temp[p[1]] = dict()
        # temp[p[1]][p[3]] = p[5]
        if p[1] in p[0]:
            s_var = p[0][p[1]]
            s_var.update({p[3] : p[5]})
        else:
            p[0][p[1]] = dict()
            p[0][p[1]][p[3]] = p[5]
        # p[0].update(temp)

# def p_state_var_val(p):
#     '''state_var_val : ID
#                      | INT
#                      | FLOAT
#                      | TRUE
#                      | FALSE '''
#     if isinstance(p[1], (int, long)):
#         p[0] = int(p[1])
#     elif isinstance(p[1], (float)):
#         p[0] = float(p[1])
#     elif p[1] == "True":
#         p[0] = True
#     elif p[1] == "False":
#         p[0] = False
#     else:
#         p[0] = p[1]

"""
GOAL STATE ATOMS
"""

def p_goal_state_atoms(p):
    '''goal_state_atoms :
                        | ID LPAREN ids EQUALS ID goal_state_atoms '''
    if len(p) == 1:
        p[0] = dict()
    else:
        p[0] = p[6]
        temp = dict()
        temp[p[1]] = dict()
        temp[p[1]][p[3]] = p[5]
        p[0].update(temp)

"""
HELPER FUNCTIONS (AUXILIARY RULES)
"""

# the error-handling function:
def p_error(p):
    if p:
         print("Syntax error at token: ", p.type)
         print("\tline ", p.lineno)
         # nvm, the following is not good:
         # Just discard the token and tell the parser it's okay.
         # meth_parser.errok()
    else:
         print("Syntax error at EOF")


"""
PARSER API

These are some useful methods for sanity-checking basic aspects of the dom
parser. They can be run from the top-level (e.g., at the bottom of this file)
to get an idea at a glance of whether anything is horribly broken.
"""

def parse(filename='', file_text=''):
    """
    Attempts to open the file specified by the supplied path ('filename'),
    then reads the file in as a string, lexes it using the dom-file lexer,
    parses it, and then returns the resulting domain file

    TODO: add error handling -- in particular against the case where the file-
    name is invalid or the specified file doesn't exist.
    """
    # try to read the supplied file
    input = ''
    if not (filename == ''):
        with open(filename, 'r') as f:
            input = f.read()
    else:
        input = file_text

    # lex and parse the file text
    dom_parser_instance.parse(input, lexer=dom_lexer_instance, \
                                      tracking=True, debug=DEBUG)

    return domain

def parse_print(filename='', file_text='', paged=True):
    """
    Attempts to open the file specified by the supplied path ('filename'),
    then reads the file in as a string, lexes it using the dom-file lexer,
    parses it, and that prints the constructed AST in paged format (if paged
    is left set to True, as it is by default) -- or not (if paged is set to
    False).

    TODO: add error handling -- in particular against the case where the file-
    name is invalid or the specified file doesn't exist.
    """

    # try to read the supplied file
    if not (filename == ''):
        parse(filename)
    else:
        print("FILE TEXT : \n" + file_text + "\n")
        parse(file_text = file_text)

    # domain_string = json.dumps(domain, sort_keys=False,
    #                            indent=3, cls=SetEncoder)
    domain_string = repr(domain)

    # print the output
    if paged:
        pager(domain_string)
    else:
        print(domain_string)

# some aliases for the above function, for Ruby-like happiness and convenience:
print_dom_file = parse_print
parser_print = parse_print

"""
Create a global dom parser instance.
"""
dom_parser_instance = yacc.yacc()
dom_lexer_instance = get_dom_lexer()

"""
And here we test the thing ...
"""

test_file = """
Objects:
docks = {d1, d2}
robots = {r1, r2}
cargo = {c1, c2, c3}
piles = {p1, p2, p3, p4}

Rigid relations:
adjacent = {(d1, d2)}
on-dock = {(p1, d1), (p2, d1), (p3, d2), (p4, d2)}

/*
State-variable ranges:
on-robot(robots) = cargo + {nil}
loc(robots|cargo|piles) = docks
in-pile(cargo) = piles
*/

Initial state:
loc(r1) = d1
loc(r2) = d2
in-pile(c1) = p1
in-pile(c2) = p2
in-pile(c3) = p3
on-robot(r1) = nil
on-robot(r2) = nil

Goal:
in-pile(c3) = p4
"""

# print_dom_file(file_text = test_file)
