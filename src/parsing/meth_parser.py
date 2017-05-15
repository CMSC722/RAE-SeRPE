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
this file defines the rules by which PLY will create the parser for our method-
definition language (i.e., the domain-specific language in which we will define
the methods in a given planning domain).

More information on the PLY module and how it works can be found at the
following URL: http://www.dabeaz.com/ply/ply.html#ply_nn1

_________________

TODO:
0) generate the task-method-map
1) build a symbol table of tasks using the dom-lexer, so we can issue task-invocation
    instructions
2) build a symbol table of actions using the dom-lexer, so we can issue action-
    invocation instructions
3) create task-invocation productions in this, the method-parser
4) create action-invocation productions in this, the method-parser
5) allow state-variables to contain arbitrary nested terms -- i.e., arguments
    can be other state variables, as in top(pile(c))
6) allow assignment of state-variables to local variables, as in:
    d = top(pile(c))
"""

import ply.yacc as yacc
from meth_lexer import tokens
from meth_lexer import get_lexer
from meth_lexer import print_token_stream
import json                     # a better way of getting a pretty print of a dict
                                # from interpreter.py import meth_parser
from pydoc import pager         # we'll be using this to produce less-like,
                                # paged output -- primarily for debugging purposes

DEBUG = True

"""
METHODS, TASKS, PRECONDITIONS, and INSTRUCTIONS: REPRESENTATION

The code following this doc-string initializes the method/task-tables and the
task-method-map. The method-table maps method id's (as strings) onto methods
(as dicts). The task-table is precisely analogous, only for tasks (as dicts).
The task_method_map, on the other hand, maps each task id onto a list of method ids
belonging to those method that implement it. These three tables are exposed by
the interpreter API. The following makes their form a bit more comprehensible by
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
                                    'meth_n',
                                    'meth_n+1',
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
(The following attribute was deprecated because it seemed unnecessary:
    'local_variables'   a list of local variable id's as strings)

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
method_table = dict()       # table mapping method ids to methods (as dicts)
task_method_map = dict()    # table mapping each task to a list of methods that
                        # implement it
task_table = dict()         # table mapping task ids to tasks (as dicts)

# initialize the singleton primitives
e_true = dict(
    e_type = 'E_TRUE',
    val = True
)

e_false = dict(
    e_type = 'E_FALSE',
    val = False
)

"""
PRECEDENCE
"""

precedence = (
    ('left', 'AND', 'OR'),
    ('left', 'EQUALS'),
    ('left', 'NOT'),
    ('left', 'LT', 'GT', 'LTE', 'GTE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDED_BY')
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

def p_start(p):
    'start : methods'
    method_table = dict()

# productions for methods
def p_methods(p):
    '''methods : method methods
               |               '''

    if len(p) == 3:
        method_id = p[1]['id']
        method_table_addition = dict()
        method_table_addition[method_id] = p[1]
        # print("method_table before:\t" + json.dumps(method_table, sort_keys=False, indent=3))
        method_table[method_id] = p[1]
        # print("method_table after:\t" + json.dumps(method_table, sort_keys=False, indent=3))

        # print("p[2] = " + repr(p[2]))
        # print("p[0] = " + repr(p[0]))

        p[2].update(method_table_addition)
        p[0] = p[2]
        # method_table = p[0]
    else:
        p[0] = dict()
        # method_table = p[0]

def p_method(p):
    'method : METHOD ID LPAREN params RPAREN COLON task pre body'
    # create a dictionary representing the 'method' nonterminal's value
    p[0] = dict(
        id = p[2],
        parameters = p[4],
        task = p[7],
        preconditions = p[8],
        # local_variables = p[8]['local_variables'],
        exprs = p[9]['exprs']
    )
    # now add this method to the relevant task's method list in the
    # task-method-map:
    # task_method_map[p[7]['id']].append(p[1])

# productions for parameter lists
def p_params(p):
    '''params : ID COMMA params
              | ID
              |             '''
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    elif len(p) == 2:
        p[0] = [p[1]]
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
    # print("\n\nadding task " + p[0]['id'] + " to task-table\n")
    task_table[p[0]['id']] = p[0]
    # print("now task-table = " + task_table.__repr__() + "\n\n")
    # if not p[0]['id'] in task_method_map:
    #    task_method_map[p[3]] = list()

'''
PRODUCTIONS FOR PRECONDITIONS
'''

def p_pre(p):
    'pre : PRE COLON PYTHON_CODE'
    p[0] = dict(
        pre_code = p[3]
    )
    try:
        exec p[3] in p[0]
    except:
        error_fun = "def preconditions(state_variables): raise Exception(\"The provided precondition code " + \
                    "failed to compile, likely due to a syntax error. Please find the " + \
                    "problematic code listed below:\\n\" + pre_code)"
        exec error_fun in p[0]

# NB: the bexpr2prec utility is defined at the bottom of the file
# def p_precon_list(p):
#     '''preconditions : bexpr AND preconditions
#                      | bexpr
#                      |                        '''
#     if len(p) == 4:
#         p[0] = [bexpr2prec(p[1])] + p[3]
#     elif len(p) == 2:
#         p[0] = [bexpr2prec(p[1])]
#     else:
#         p[0] = list()


'''
PRODUCTION FOR METHOD BODIES
'''

def p_body(p):
    'body : BODY COLON exprs'
    p[0] = dict(
        # local_variables = p[3]['local_variables'], # list
        exprs = p[3]#['exprs']
    )


'''
PRODUCTIONS FOR STATEMENTS AND STATEMENT SEQUENCES
'''

def p_exprs(p):
    '''exprs : LPAREN exprs RPAREN
             | expr exprs
             |                    '''
    if len(p) == 4:
        p[0] = p[2]
    elif len(p) == 3:
        p[0] = dict(
            e_type = 'E_SEQ',
            # local_variables = p[1].get('local_variables', []) + p[2]['local_variables'],
            arg1 = p[1],
            arg2 = p[2]
        )
    else:
        p[0] = dict(
            e_type = 'E_NOOP',
            # local_variables = [],
            # exprs = []
        )

# We divide the production for exprs up just for sanity's sake ...
def p_expr(p):
    # used to have as first production: LPAREN expr RPAREN
    '''expr : fail
            | control_structure
            | bexpr
            | aexpr
            | string
            | state_var_rd
            | state_var_wr
            | loc_var_rd
            | loc_var_wr        '''
    #        | task_invocation
    if len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = p[1]

# ... and the same here -- once again for readibility
def p_control_structure(p):
    '''control_structure : while_loop
                         | if_statement'''
    p[0] = p[1]

def p_while_loop(p):
    'while_loop : WHILE bexpr DO exprs END'
    p[0] = dict(
        e_type = 'E_WHILE',
        cond = p[2],
        block = p[4]
    )

def p_if_statement(p):
    '''if_statement : IF bexpr THEN exprs END
                    | IF bexpr THEN exprs elsif_blocks END
                    | IF bexpr THEN exprs ELSE exprs END
                    | IF bexpr THEN exprs elsif_blocks ELSE exprs END'''
    if len(p) == 6:
        p[0] = dict(
            e_type = 'E_IF',
            conds = [p[2]],
            blocks = [p[4]]
        )
    elif len(p) == 7:
        p[0] = dict(
            e_type = 'E_IF',
            conds = [p[2]] + p[5]['conds'],
            blocks = [p[4]] + p[5]['blocks']
        )
    elif len(p) == 8:
        e_else = dict(
            e_type = None,
            conds = [e_true],
            blocks = [p[6]]
        )
        p[0] = dict(
            e_type = 'E_IF',
            conds = [p[2]] + e_else['conds'],
            blocks = [p[4]] + e_else['blocks']
        )
    elif len(p) == 9:
        e_else = dict(
            e_type = None,
            conds = [e_true],
            blocks = [p[7]]
        )
        p[0] = dict(
            e_type = 'E_IF',
            conds = [p[2]] + p[5]['conds'] + e_else['conds'],
            blocks = [p[5]] + p[5]['blocks'] + e_else['blocks']
        )

def p_elsif_blocks(p):
    '''elsif_blocks : elsif_blocks elsif_block
                    | elsif_block             '''
    if len(p) == 3:
        p[0] = dict(
            e_type = None,
            conds = p[1]['conds'] + p[2]['conds'],
            blocks = p[1]['blocks'] + p[2]['blocks'],
        )
    else:
        p[0] = p[1]

def p_elsif_block(p):
    'elsif_block : ELSIF bexpr THEN exprs'
    p[0] = dict(
        e_type = None,
        conds = [p[2]],
        blocks = [p[4]]
    )

'''
def p_task_invocation(p):
    'task_invocation : empty'
    pass
'''

'''
PRODUCTIONS FOR EXPRESSIONS
'''

# failure
def p_fail(p):
    'fail : FAIL'
    p[0] = dict(
        e_type = 'E_FAIL'
    )

# arithmetic expressions:
def p_aexpr(p):
    '''aexpr : LPAREN aexpr RPAREN
             | aexpr PLUS aexpr
             | aexpr MINUS aexpr
             | aexpr TIMES aexpr
             | aexpr DIVIDED_BY aexpr
             | INT
             | FLOAT
             | ID                    '''
    if len(p) == 4:
        p[0] = dict(
            e_type = {
                '+': 'E_ADD',
                '-': 'E_SUB',
                '*': 'E_MUL',
                '/': 'E_DIV'
            }.get(p[2]),
            arg1 = p[1],
            arg2 = p[3]
        )
    else:
        if isinstance(p[1], (int, long)):
            p[0] = dict(
                e_type = "E_INT",
                val = int(p[1])
            )
        elif isinstance(p[1], (float)):
            p[0] = dict(
                e_type = "E_FLOAT",
                val = float(p[1])
            )
        else:
            p[0] = dict(
                e_type = "E_LOC_VAR_RD",
                arg1 = p[1]
            )

# boolean expressions:
def p_bexpr(p):
    '''bexpr : LPAREN bexpr RPAREN
             | bexpr AND bexpr
             | bexpr OR bexpr
             | expr EQUALS expr
             | expr LT expr
             | expr GT expr
             | expr LTE expr
             | expr GTE expr
             | NOT bexpr
             | true
             | false
             | loc_var_rd
             | state_var_rd     '''
             # | expr             '''
    if len(p) == 4:
        try:
            p[0] = dict(
                e_type = {
                    '&&':   'E_AND',
                    '||':   'E_OR',
                    '==':   'E_EQUALS',
                    '<':    'E_LT',
                    '>':    'E_GT',
                    '<=':   'E_LTE',
                    '>=':   'E_GTE'
                }.get(p[2]),
                arg1 = p[1],
                arg2 = p[3]
            )
        except TypeError: # this is the LPAREN bexpr RPAREN case, if you can believe it
            p[0] = p[2]
    elif len(p) == 3:
        p[0] = dict(
            e_type = 'E_NOT',
            arg1 = p[2]
        )
    else:
        p[0] = p[1]

def p_true(p):
    'true : TRUE'
    p[0] = dict(
        e_type = 'E_TRUE',
        val = True
    )

def p_false(p):
    'false : FALSE'
    p[0] = dict(
        e_type = 'E_FALSE',
        val = False
    )

def p_string(p):
    'string : STRING'
    p[0] = dict(
        e_type = 'E_STRING',
        val = p[1]
    )

# var read/write:
# NOTE: the comma_exprs here and below (in the state_var_wr production) is
# a list of expressions that need to be evaluated
def p_state_var_rd(p):
    'state_var_rd : ID LPAREN state_var_args RPAREN'
    p[0] = dict(
        e_type = 'E_STATE_VAR_RD',
        arg1 = p[1],
        arg2 = p[3]
    )

def p_state_var_wr(p):
    'state_var_wr : ID LPAREN state_var_args RPAREN ASSIGN expr'
    p[0] = dict(
        e_type = 'E_STATE_VAR_WR',
        arg1 = p[1],
        arg2 = p[3]
    )

def p_state_var_args(p):
    '''state_var_args : state_var_arg COMMA state_var_args
                      | state_var_arg'''
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]

def p_state_var_arg(p):
    '''state_var_arg : state_var_rd
                     | loc_var_rd
                     | string
                     | INT
                     | FLOAT'''
    p[0] = p[1]

def p_loc_var_rd(p):
    'loc_var_rd : ID'
    p[0] = dict(
        e_type = 'E_LOC_VAR_RD',
        arg1 = p[1]
    )

def p_loc_var_wr(p):
    'loc_var_wr : ID ASSIGN expr'
    p[0] = dict(
        e_type = 'E_LOC_VAR_WR',
        arg1 = p[1],
        arg2 = p[3]
    )

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

# an empty production representing, for our purposes, the end of the file
# def p_empty(p):
#    'empty :'
#    pass

"""
UTILITY FUNCTIONS
"""

def bexpr2prec(bexpr):
    '''recall that this is what a bexpr looks like:
        bexpr : bexpr AND bexpr
              | bexpr OR bexpr
              | expr EQUALS expr
              | expr LT expr
              | expr GT expr
              | expr LTE expr
              | expr GTE expr
              | NOT bexpr
              | true
              | false
              | state_var_rd
       and that an expr looks like this
        expr : LPAREN expr RPAREN
             | control_structure
             | bexpr
             | aexpr
             | string
             | state_var_rd
             | state_var_wr
             | loc_var_rd
             | loc_var_wr        '''
    pass

"""
PARSER API

These are some useful methods for sanity-checking basic aspects of the
parser. They can be run from the top-level (e.g., at the bottom of this file)
to get an idea at a glance of whether anything is horribly broken.
"""

def get_method_table():
    return method_table

def set_method_table(new_method_table):
    method_table = new_method_table

def get_task_table():
    return task_table

def get_task_method_map():
    return {} # task_method_map

def parse_print(filename, paged=True, debug=True):
    """
    Attempts to open the file specified by the supplied path ('filename'),
    then reads the file in as a string, lexes it using the method-file lexer,
    parses it, and that prints the constructed AST in paged format (if paged
    is left set to True, as it is by default) -- or not (if paged is set to
    False).

    TODO: add error handling -- in particular against the case where the file-
    name is invalid or the specified file doesn't exist.
    """
    parse(filename)
    asts_string = json.dumps(get_method_table(), sort_keys=False, indent=3)

    # print the output
    if paged:
        pager(asts_string)
    else:
        print(asts_string)

# some aliases for the above function, for Ruby-like happiness and convenience:
print_asts = parse_print
parser_print = parse_print

def load_methods(filename, overwrite=True):
    """
    This method, given a path to a .meth file, reads it in, parses it,
    constructs a method table in METH Bytecode, and finally *returns* the method
    table, which is of the type used by the interpreter.

    By default, this method overwrites any previously generated method-table
    stored in memory. If one wishes to generate a new method-table without
    overwriting the old one (that is, allowing it to persist in memory), one
    should call the function with the 'overwrite' parameter set to False. Under
    this setting, the load_methods() function merely returns the newly generated
    table without affecting the old one.

    On the other hand, if one wishes to load a new method-file and *add* its
    methods to those already stored in the in-memory method-table, one should
    use the add_methods() function, which behaves similarly, but returns the
    union of the old method-table and the newly generated one, and also updates
    the in-memory method-table.
    """
    # 1) instantiate a placeholder for the extant method table
    old_table = get_method_table()
    new_table = dict()
    # 2) feed the string and the lexer to the parser
    parse(filename)
    new_table = get_method_table() # create the new table from the parser output
    # 3) possibly overwrite the old table with this new one -- or not
    if overwrite:
        del old_table
    else:
        set_method_table(old_table) # restore the older method table
    # 3) in either case return the new method table
    return new_table

def add_methods(filename):
    table_addition = load_methods(filename, overwrite=False)
    method_table.update(table_addition)
    return method_table

def save_method_table():
    """
    This function writes the in-memory method-table to file, so that it
    needn't be re-generated next time. This may be useful for large and com-
    plicated method files, which take time to parse.
    """
    with open('method_table.pkl', 'wb') as output:
        pickle.dump(meth_table, output, pickle.HIGHEST_PROTOCOL)

def load_method_table():
    """
    This function reads the in-memory method-table from file, so that it
    needn't be re-generated. This may be useful for large and com-
    plicated method files, which take time to parse.
    """
    with open('method_table.pkl', 'rb') as input:
        meth_table = pickle.load(input)

def parse(filename):
    """
    Attempts to open the file specified by the supplied path ('filename'),
    then reads the file in as a string, lexes it using the method-file lexer,
    parses it, and then returns a tuple containing the resulting method_table,
    task_table, and task_method_map.

    TODO: add error handling -- in particular against the case where the file-
    name is invalid or the specified file doesn't exist.
    """
    # try to read the supplied file
    input = ''
    with open(filename, 'r') as f:
        input = f.read()

    # lex and parse the file text
    # print_token_stream(filename)
    meth_parser_instance.parse(input, lexer=meth_lexer_instance, \
                                      tracking=True, debug=DEBUG)

    # print("\n\nreturning task_table = " + task_table.__repr__())
    return (method_table, task_table, {}) #task_method_map)

"""
Create a global parser instance.
"""
meth_parser_instance = yacc.yacc()
meth_lexer_instance = get_lexer()
