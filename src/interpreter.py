"""
Date: Thu, 9 Feb, 2017
Last updated: Sat, 27 Feb, 2017
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
lexer.py and parser.py, respectively. Whereas a lexer is built to
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

__________________
TODO:
0) finish the seq/control statement instrs
1) write the dom-lexer and dom-parser that generate the state-variable tables
    and domain descriptions used by the interpreter and other planning components.
2) do num 3 above
3) add parens to exprs in the parser meth grammar
4) have interpreter disambiguate between state-vars and tasks using the task
    table
5) add arithmetic in ints and floats to the parser grammar
6) make environment/state variables a global object, so that planning domain
    state is preserved after recursive method calls
"""

# import statements here
from __future__ import print_function   # this is so that print() will be a
                                        # a function, rather than a statement --
                                        # in Pytnon 2.x, print() is merely a
                                        # statement; in Pytnon 3.x, it is an
                                        # actual function -- which allows us
                                        # to use it in lambdas, which expect
                                        # expressions, not statements
import ply.lex as lex
import ply.yacc as yacc
from pydoc import pager     # we'll be using this to produce less-like,
                            # paged output -- primarily for debugging purposes
import dom_lexer            # this is the module where we've specified the method-file lexer rules
import dom_parser           # this is the module where we've specified the method-file lexer rules
import meth_lexer           # this is the module where we've specified the method-file lexer rules
import meth_parser          # this is the module where we've specified the method-file parser rules
# import pprint             # python's pretty-printer for arbitrary data
import json                 # a better way of getting a pretty print of a dict
import cPickle as pickle    # for serializing objects to file -- in our case,
                            # we'll want to be persisting our method tables


"""
GLOBALS

The following are variables used across the interpreter module -- namely,
the lexers and parsers, and the current method-table.
"""

# First we build the lexer and the parser, using the lexing and parsing rules
# defined in our lexer.py and parser.py files:
meth_lexer_instance = lex.lex(module=meth_lexer)
meth_parser_instance = yacc.yacc(module=meth_parser)

# The method table
method_table = {}

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
    e_if =      'IF',       # conds (expr list), blocks (list of lists of exprs)
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
    e_false =   'FALSE',    # arg1 (False)
    # variable expressions
    e_state_var_rd =    'STATE_VAR_RD',     # arg1 (id string),
                                            # arg2 (list of parameter ids)
    e_state_var_wr =    'STATE_VAR_WR',     # arg1 (id string),
                                            # arg2 (list of parameter ids)
                                            # arg3 (expr)
    e_loc_var_rd =      'LOC_VAR_RD',       # arg1 (id string)
    e_loc_var_wr =      'LOC_VAR_WR'        # arg1 (id string), arg2 (expr)
)


"""
AUXILIARY CLASSES

For now, we'll just put errors here that the interpreter needs to raise.
Perhaps, at a later date, we may wish to factor these out into a separate
file.
"""

class NoMethodTable(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class MethodNotFound(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class SemanticError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

"""
OPERATIONAL SEMANTICS

The following functions define the semantics of the interpreter's instruction
set. Generally, the semantics reduces expressions in the method-file language's
expression grammar to values (represented as native Python values).
"""

    # noop
def e_noop(instr, **dom_args):      # [no arguments]
    return (None, dom_args['environment']. dom_args['state_vars'])


"""
IMPORTANT NOTE
"""
# NOTE: the following three have yet to be implemented

    # sequence and control statement instructions
def e_seq(instr, **dom_args):       # local_variables (list), exprs (list)

    return (val, dom_args['environment'], dom_args['state_vars'])

def e_while(instr, **dom_args):     # cond (expr), exprs (list)

    return (val, dom_args['environment'], dom_args['state_vars'])

def e_if(instr, **dom_args):        # conds (expr list), blocks (list of lists of exprs)

    return (val, dom_args['environment'], dom_args['state_vars'])

    # binary (here only boolean) operators
def e_and(instr, **dom_args):       # arg1 (expr), arg2 (expr)
    l_expr = instr['arg1']
    r_expr = instr['arg2']
    (l_operand, _, dom_args['state_vars']) = execute_method_helper(l_expr, **dom_args)
    (r_operand, _, dom_args['state_vars']) = execute_method_helper(r_expr, **dom_args)
    return (l_operand and r_operand, dom_args['environment'], dom_args['state_vars'])

def e_or(instr, **dom_args):        # "    "       "    "
    l_expr = instr['arg1']
    r_expr = instr['arg2']
    (l_operand, _, dom_args['state_vars']) = execute_method_helper(l_expr, **dom_args)
    (r_operand, _, dom_args['state_vars']) = execute_method_helper(r_expr, **dom_args)
    return (l_operand or r_operand, dom_args['environment'], dom_args['state_vars'])

def e_equals(instr, **dom_args):    # "    "       "    "
    l_expr = instr['arg1']
    r_expr = instr['arg2']
    (l_operand, _, dom_args['state_vars']) = execute_method_helper(l_expr, **dom_args)
    (r_operand, _, dom_args['state_vars']) = execute_method_helper(r_expr, **dom_args)
    return (l_operand == r_operand, dom_args['environment'], dom_args['state_vars'])

def e_lt(instr, **dom_args):        # "    "       "    "
    l_expr = instr['arg1']
    r_expr = instr['arg2']
    (l_operand, _, dom_args['state_vars']) = execute_method_helper(l_expr, **dom_args)
    (r_operand, _, dom_args['state_vars']) = execute_method_helper(r_expr, **dom_args)
    return (l_operand < r_operand, dom_args['environment'], dom_args['state_vars'])

def e_gt(instr, **dom_args):        # "    "       "    "
    l_expr = instr['arg1']
    r_expr = instr['arg2']
    (l_operand, _, dom_args['state_vars']) = execute_method_helper(l_expr, **dom_args)
    (r_operand, _, dom_args['state_vars']) = execute_method_helper(r_expr, **dom_args)
    return (l_operand > r_operand, dom_args['environment'], dom_args['state_vars'])

def e_lte(instr, **dom_args):       # "    "       "    "
    l_expr = instr['arg1']
    r_expr = instr['arg2']
    (l_operand, _, dom_args['state_vars']) = execute_method_helper(l_expr, **dom_args)
    (r_operand, _, dom_args['state_vars']) = execute_method_helper(r_expr, **dom_args)
    return (l_operand <= r_operand, dom_args['environment'], dom_args['state_vars'])

def e_gte(instr, **dom_args):       # "    "       "    "
    l_expr = instr['arg1']
    r_expr = instr['arg2']
    (l_operand, _) = execute_method_helper(l_expr, **dom_args)
    (r_operand, _) = execute_method_helper(r_expr, **dom_args)
    return (l_operand >= r_operand, dom_args['environment'], dom_args['state_vars'])

    # unary operators
def e_not(instr, **dom_args):       # arg1 (expr)
    expr = instr['arg1']
    (val, _) = execute_method_helper(expr, **dom_args)
    return (not val, dom_args['environment'], dom_args['state_vars'])

    # primitive values
def e_true(instr, **dom_args):      # arg1 (True)
    return (True, dom_args['environment'], dom_args['state_vars'])

def e_false(instr, **dom_args):     # arg1 (False)
    return (False, dom_args['environment'], dom_args['state_vars'])

    # variable expressions

"""
THE FOLLOWING COMMENT IS IMPORTANT AND CONTAINS AN IMPLICIT TODO
"""
# NOTE: we disambiguate between a state-variable read and a task invocation
# within the body of this method -- this is a bit kludgie, and we may wish
# to later rely on a symbol-table constructed by the dom-lexer (which doesn't
# yet exist) to disambiguate this within the parser and issue separate byte-code
# instructions; but for now, this will at least work.
# ALSO: note the task_node dictionary format -- we'll want to confirm that this
# is the way we want to represent a task-node, and then apply a similar format
# to the action-nodes if and once we begin to generate them
def e_state_var_rd(instr, **dom_args):  # arg1 (id string), arg2 (list of parameter ids)
    id = instr['arg1']
    arguments = instr['arg2']

    task_table = meth_parser.get_task_table()
    task = task_table.get(id, None)

    if task:
        if not arguments.size == task['params'].size:
            raise SemanticError("Task {0} invoked with improper number of \
                                 arguments ({1} rather than {2})".format(id,
                                    arguments.size, task['params'].size))
        task_node = dict(
            node_type =   'task_node',
            task_id =     id,
            args =        arguments,
            task =        task
        )

        yield (task_node, dom_args['environment'], dom_args['state_vars'])

    else:
        state_var = dom_args['state_vars'][id]
        val = state_var[arg2]
        yield (val, dom_args['environment'], dom_args['state_vars'])

def e_state_var_wr(instr, **dom_args):  # arg1 (id string), arg2 (list of parameter ids), arg3 (expr)
    id = instr['arg1']
    arguments = instr['arg2']
    (val, _, state_vars) = execute_method_helper(instr['arg3'], **dom_args)
    dom_args['state_vars'] = state_vars
    dom_args['state_vars'][id][arguments] = val
    return (val, dom_args['environment'], dom_args['state_vars'])

def e_loc_var_rd(instr, **dom_args):    # arg1 (id string)
    id = instr['arg1']
    env = dom_args['environment']
    return (env[id], env, dom_args['state_vars'])

def e_loc_var_wr(instr, **dom_args):    # arg1 (id string), arg2 (expr)
    id = instr['arg1']
    (val, _) = execute_method_helper(instr['arg2'], **dom_args)
    env = dom_args['environment']
    env[id] = val
    return (val, env, dom_args['state_vars'])


"""
IMPORTANT NOTE
"""
# NOTE: these have yet to be implemented
    # the equivalent of function invocation
def e_task_invocation(instr, **dom_args):
    pass

    # native python function invocation (interface with agent/environment)
def e_action_invocation(instr, **dom_args):
    pass

"""
INTERPRETER API

The following functions provide an API for the interpreter module. In general,
to invoke the interpreter, one must either first ensure that a method file has
been loaded into memory (the load_methods(<filename>) function handles this),
which generates a method-table; or one must already
"""

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
    # 1) read in the file as a string
    input = ''
    with open(filename, 'r') as f:
        input = f.read()
    # 2) feed the string and the lexer to the parser
    meth_parser_instance.parse(input, lexer=meth_lexer)
    # 3) possibly overwrite the old table with this new one -- or not
    if overwrite:
        method_table = meth_parser.get_method_table()
    # 3) grab the resulting method table from the parser and return it
    return meth_parser.get_method_table()

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

def execute_method(meth_name, environment,
                   method_table = meth_parser.get_method_table(),
                   action_model = None):
    """
    Looks up the supplied method name in the method table and attempts to
    execute the corresponding byte-code sequence. If the method is not found,
    execute_method() raises a MethodNotFound error. If the method table is not
    supplied, execute_method() attempts to get the most recently compiled
    method table from the parser module. If this fails, the method raises
    a NoMethodTable error.

    By default, execution begins at the first instruction in the body of
    the method.

    (* Note -- the following is currently not supported: If necessary, the
    invoking function can pass in an instruction index to begin execution at any
    arbitrary point in the method body -- as, for instance, when resuming
    execution after backtracking. *)

    When execution reaches the end of the method, a tuple is returned
    containing, as the first component, the environment at the end of
    method execution, and, as the second component, the return value of the
    method -- which, for void methods, is None.

    During execution of the method, the interpreter executes the byte-code
    instructions found in the method table one by one, in sequence, until
    it encounters a decision point, which we define for now as a task-
    invocation. At that point, the interpreter should yield to the invoking
    function a tuple containing the current task-node, the current domain
    state (i.e., the set of all state variable assignments), and the current
    environment state (i.e., the set of all local variable assignments).

    In the future, we may wish to support planning over non-deterministic
    action outcomes, in which case we will also wish to yield action-nodes
    as decision points in the planning tree.
    """
    # no method table yet
    if not method_table:
        raise NoMethodTable("Either the method table you supplied is empty, "
                             "or it is nil, or no .meth file has been parsed yet")

    # no such method
    meth = method_table.get(meth_name)
    if not meth:
        raise MethodNotFound("No such method exists: '{0}'".format(meth_name))

    # method table and method exist -- execute method
    return execute_method_helper(meth.exprs, meth, environment,
                                 method_table, action_model)

def execute_method_helper(curr_instr, meth, environment, method_table, action_model):
    """
    See documentation for execute_method()
    """
    instr_table = {
        'NOOP':         e_noop,
        'SEQ':          e_seq,
        'WHILE':        e_while,
        'IF':           e_if,
        'AND':          e_and,
        'OR':           e_or,
        'EQUALS':       e_equals,
        'LT':           e_lt,
        'GT':           e_gt,
        'LTE':          e_lte,
        'GTE':          e_gte,
        'NOT':          e_not,
        'TRUE':         e_true,
        'FALSE':        e_false,
        'STATE_VAR_RD': e_state_var_rd,
        'STATE_VAR_WR': e_state_var_wr,
        'LOC_VAR_RD':   e_loc_var_rd,
        'LOC_VAR_WR':   e_loc_var_wr,
        'TASK_INVOCATION':  e_task_invocation
    }

    # op_sem = instr_table.get(curr_instr.e_type,
    #   lambda *args: raise NoSuchInstruction("instruction '{0}' does not exist". \
    #                                     format(curr_instr['e_type']))

    op_sem = lambda *args: print("I'm an instruction")
    return op_sem(curr_instr, meth, environment, method_table, action_model)


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
    meth_lexer_instance.input(input)

    # lex the file and aggregate the output
    output = ''
    while True:
        tok = meth_lexer_instance.token()
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

    # try to read the supplied file
    input = ''
    with open(filename, 'r') as f:
        input = f.read()
    meth_parser_instance.parse(input, lexer=meth_lexer_instance, tracking=True, debug=debug)

    method_table = meth_parser.get_method_table()
    asts_string = json.dumps(method_table, sort_keys=False, indent=4)

    # print the output
    if paged:
        pager(asts_string)
    else:
        print(asts_string)

# some aliases for the above function, for Ruby-like happiness and convenience:
print_asts = parse_print
parser_print = parse_print


"""
TOP-LEVEL CODE

By convention, we'll put top-level code here, at the bottom of the file (and
we'll use such code for debugging purposes, since this file is intended to
function as a module).
"""

print_token_stream("../domains/test_domain1/test_domain1.meth")
print_asts("../domains/test_domain1/test_domain1.meth", paged = False, debug=False)
