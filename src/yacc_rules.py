"""
Date: Thu, Sat, 18 Feb, 2017
Last updated: Sat, 18 Feb, 2017
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
this file defines the rules by which PLY will create the parser for our method-
definition language (i.e., the domain-specific language in which we will define
the methods in a given planning domain).

More information on the PLY module and how it works can be found at the
following URL: http://www.dabeaz.com/ply/ply.html#ply_nn1

_________________

TODO:
1) have the lexer build a symbol table of tasks, so that we can disambiguate
    between task invocations and local variable reads
"""

import ply.yacc as yacc
from lex_rules import tokens
# from interpreter.py import meth_parser

"""
METHODS, TASKS, PRECONDITIONS, and INSTRUCTIONS: REPRESENTATION

The code following this doc-string initializes the method/task-tables and the
task-method-map. The method-table maps method id's (as strings) onto methods
(as dicts). The task-table is precisely analogous, only for tasks (as dicts).
The task_method_map, on the other hand, maps each task (as a dict) onto
a list of methods (as dicts) that implement it. These two tables are used by
the interpreter. The following makes their form a bit more comprehensible by
representing them visually:

    method_table = {
        ...
        'some_meth_id'       :  { ... some method dict ... },
        'some_other_meth_id' :  { ... some other method dict ... },
        ...
    }

    task_table = {
        ...
        'some_task_id'       :  { ... some task dict ... },
        'some_other_task_id' :  { ... some other task dict ... },
        ...
    }

    task_method_map = {
        ...
        'some_task_id'       :  {
                                    ...
                                    'meth_n' : { meth1 dict },
                                    'meth_n+1' : { meth2 dict},
                                    ...
                                },
        ...
    }

Methods are represented by the parser and interpreter as dicts. They have
the following attributes (as keys):
    'id':               the name of the method as a string
    'task':             the task this method implements, as a task dict (see below)
    'parameters':       the parameters the method takes, as a list of strings
    'preconditions':    the preconditions the method stipulates, as a list of
                        precondition dicts (see below)
    'exprs':            the expr/statement sequence the method encapsulates, as a
                        list of expr dicts
    'local_variables'   # a list of local variable id's as strings

Tasks are represented by the parser and interpreter as dicts as well. They have
the following attributes (as keys):
    'id':               the name of the task as a string
    'parameters':       the parameters the task takes

Preconditions are represented by the parser and interpreter as dicts as well.
They have the following attributes:

...

Instructions, finally, are also represented by the parser and interpreter as
dicts. They have the following form:

...

"""
# initialize the method table and the task table:
method_table = {}       # table mapping method ids to methods (as dicts)
task_method_map = {}    # table mapping each task to a list of methods that
                        # implement it
task_table = {}         # table mapping task ids to tasks (as dicts)

# initialize the singleton primitives
e_true = dict(
    e_type = 'TRUE',
    arg1 = True
)

e_false = dict(
    e_type = 'FALSE',
    arg1 = False
)

"""
PRECEDENCE
"""

precedence = (
    ('left', 'AND', 'OR'),
    ('left', 'EQUALS', 'LT', 'GT', 'LTE', 'GTE')
)


"""
RULES

The grammar's rules are, as the lexing rules, provided within Python functions.
By analogy with the PLY lexer, the actual CFG productions are given within the
functions' docstrings, in a kind of simplified BNF (Backus-Naur form). The
principle here is that of syntax-directed translation, where the functions that
embody the CFG productions return Python dicts which, in this case, are the
byte-code-like instructions that the interpreter will execute. The exception is
the set of rules that represent the method-block- and program-level structures,
which, naturally, are used to build up a hash of methods, along with their
signatures, preconditions, and local-variable lists.
"""

# productions for methods
def p_methods(p):
    '''methods : method methods
               | empty         '''
    if len(p) == 2:
        # we've reached the end of the method file
        return method_table
    else:
        # we have more methods to parse, so parse the first one:
        method_id = p[1].id
        method_table[method_id] = p[1]
        # and then return the result of parsing the rest:
        return p[2]

def p_method(p):
    'method : ID LPAREN params RPAREN COLON task pre body'
    # create a dictionary representing the 'method' nonterminal's value
    p[0] = dict(
        id = p[1],
        parameters = p[2],
        task = p[5],
        preconditions = p[6],
        local_variables = p[7]['local_variables'],
        exprs = p[7]['exprs']
    )
    # now add this method to the relevant task's method list in the
    # task-method-map:
    task_method_map[p[5]['id']].append(p[0])

# productions for parameter lists
def p_params(p):
    '''params : ID COMMA params
              | ID
              |             '''
    if len(p) == 4:
        p[0] = list(p[1]) + p[3]
    elif len(p) == 2:
        p[0] = list(p[1])
    else:
        p[0] = []


'''
PRODUCTION FOR TASKS
'''

def p_task(p):
    'task : TASK COLON ID LPAREN params RPAREN'
    p[0] = dict(
        id = p[3],
        parameters = p[5]
    )
    # now add entries in the task-table and the task-method-map as appropriate:
    task_table[p[0]['id']] = p[0]
    if not p[0]['id'] in task_method_map:
        task_method_map[p[0]['id']] = list()


'''
PRODUCTIONS FOR PRECONDITIONS
'''

def p_pre(p):
    '''pre : PRE COLON preconditions
           | PRE COLON              '''
    if len(p) == 4:
        p[0] = p[3]
    else:
        p[0] = list()

def p_precon_list(p):
    '''preconditions : bexpr COMMA preconditions
                     | bexpr                    '''
    if len(p) == 4:
        p[0] = list(p[1]) + p[3]
    else:
        p[0] = list(p[1])


'''
PRODUCTION FOR METHOD BODIES
'''

def p_body(p):
    'body : BODY COLON exprs'
    p[0] = dict(
        local_variables = p[3]['local_variables'], # list
        exprs = p[3]['exprs']                      # list
    )


'''
PRODUCTIONS FOR STATEMENTS AND STATEMENT SEQUENCES
'''

def p_exprs(p):
    '''exprs : expr exprs
             | empty     '''
    if len(p) == 3:
        p[0] = dict(
            e_type = 'SEQ',
            local_variables = p[1]['local_variables'] + p[2]['local_variables'],
            exprs = list(p[1]) + p[2]['exprs']
        )
    else:
        p[0] = dict(
            e_type = None,
            local_variables = [],
            exprs = []
        )

# We divide the production for exprs up just for sanity's sake ...
def p_expr(p):
    '''expr : control_structure
            | state_var_rd
            | state_var_wr     '''
    #        | task_invocation
    #        | loc_var_rd
    #        | loc_var_wr        '''
    p[0] = p[1]

# ... nd the same here -- once again for readibility
def p_control_structure(p):
    '''control_structure : while_loop
                         | if_statement'''
    p[0] = p[1]

def p_while_loop(p):
    'while_loop : WHILE bexpr DO exprs END'
    p[0] = dict(
        e_type = p[1],
        cond = p[2],
        exprs = p[4]
    )

def p_if_statement(p):
    'if_statement : IF bexpr DO exprs elsif_block'
    p[0] = dict(
        e_type = p[1],
        conds = list(p[2]) + p[6]['conds'],
        blocks = list(p[5]) + p[6]['blocks']
    )

def p_elsif_block(p):
    '''elsif_block : ELSIF bexpr DO exprs elsif_block
                   | ELSE exprs END
                   | END                              '''
    if len(p) == 6:
        p[0] = dict(
            e_type = None,
            conds = list(p[2]) + p[5]['conds'],
            blocks = list(p[4]) + p[5]['blocks']
        )
    elif len(p) == 4:
        p[0] = dict(
            e_type = None,
            conds = list(e_true),
            blocks = list(p[2])
        )
    else:
        p[0] = dict(
            e_type = None,
            conds = list(),
            blocks = list()
        )

'''
def p_task_invocation(p):
    'task_invocation : empty'
    pass
'''

'''
PRODUCTIONS FOR EXPRESSIONS
'''

# boolean expressions:
def p_bexpr(p):
    '''bexpr : bexpr AND bexpr
             | bexpr OR bexpr
             | expr EQUALS expr
             | expr LT expr
             | expr GT expr
             | expr LTE expr
             | expr GTE expr
             | NOT bexpr
             | expr             '''
    if len(p) == 4:
        p[0] = dict(
            e_type = p[2],
            arg1 = p[1],
            arg2 = p[3]
        )
    else:
        p[0] = dict(
            e_type = p[1],
            arg1 = p[2]
        )

# var read/write:
def p_state_var_rd(p):
    'state_var_rd : ID LPAREN params RPAREN'
    p[0] = dict(
        e_type = 'STATE_VAR_RD',
        arg1 = p[1],
        arg2 = p[3]
    )

def p_state_var_wr(p):
    'state_var_wr : ID LPAREN params RPAREN ASSIGN expr'
    p[0] = dict(
        e_type = 'STATE_VAR_RD',
        arg1 = p[1],
        arg2 = p[3]
    )

"""
def p_loc_var_rd(p):
    'loc_var_rd : empty'
    pass

def p_loc_var_wr(p):
    'loc_var_wr : empty'
    pass
"""

# numerical expressions:


# the error-handling function:
def p_error(p):
    if p:
         print("Syntax error at token", p.type)
         # Just discard the token and tell the parser it's okay.
         # meth_parser.errok()
    else:
         print("Syntax error at EOF")

# an empty production representing, for our purposes, the end of the file
def p_empty(p):
    'empty :'
    pass
