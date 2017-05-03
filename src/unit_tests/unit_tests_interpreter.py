"""
Date: Thu, 7 Mar, 2017
Last updated: Sat, 7 Mar, 2017
Author: Samuel Barham
Organization: University of Maryland, College Park (PhD student)

Project: RAE/SeRPE implementation
Component: Unit Testing Apparatus

Description:
This file contains unit tests and associated infrastructure for testing , organized into
*test fixtures*, *test suites*, and *test cases*. Test fixtures perform
necessary test preparation and cleanup; test suites are collections or
aggregations of related test cases; test cases are collections or aggregations
of unit tests that test related functionality. These testing constructs
are defined by and implemented in the Python unittest module.

For more information on the Python 2.7-2.x unittest framework, see the doc-
umentation at the following url:
https://docs.python.org/2/library/unittest.html.

____________________________________________________________________________

Current debugging hit list (change '-' to 'x' as completed):
- get dom lexer done and test that thoroughly
- use the symbol table the dom lexer produces to disambiguate
  state-variable read / task invocation in the parser
- test short-circuiting evaluation of:
-       and
-       or
- test dereferencing of:
-       local variables
-       state variables
- test assignment of:
-       local variables
-       state variables
- test control structures:
-       if
-       while
-       seq
- fix reduce-reduce conflicts in grammar
- fix shift-reduce conflicts in grammar
- add arrays and dictionaries
- add power function
- add print function (THIS WILL BE HUGELY IMPORTANT)
"""

import sys
sys.path.insert(0, '../')
sys.path.insert(0, '../parsing')

import interpreter
import meth_parser

import unittest
import json
import copy

"""
TEST SETUP
"""
empty_interpreter_instance = interpreter.Interpreter()

"""
TEST CASES

Here is where we define the test cases, organized by project component and then
component functionality.
"""


"""
INTERPRETER SEMANTICS: EXPRESSIONS

The following four test cases exercise the interpreter's semantics for
*expressions* -- that is, those syntactic constructions that do not alter the
environment, but which do produce (reduce to) a value. Within the context
of our domain-specific language for methods, expressions can reduce to one of
four value types: Int(eger), Float(ing point number), (Character) String, or
Boolean. There is, additionally, a fifth type of value which we call, after
Python, the None type. In our Python implementation of the language, these
five types are represented, respectively, by the strings:
    'val_int',
    'val_float',
    'val_str',
    'val_bool',
    'val_none'

In fact, in our language, which is represented with an expression grammar,
even statements reduce to values -- specifically, control statements reduce
to the None type, and variable reads and writes reduce to the value being read
from or written to the variable (whether that be a local variable or a state
variable). However, the values produced by statements are typically thrown
away, and it is their effect on execution flow and program state (through
modification of the environment) that is most important.
"""

class EvalPrimitives(unittest.TestCase):
    int_instr = dict(
        e_type = "E_INT",
        val = 3
    )

    float_instr = dict(
        e_type = "E_FLOAT",
        val = 3.1415926
    )

    str_instr = dict(
        e_type = "E_STRING",
        val = "Hello, world!"
    )

    id_instr = dict(
        e_type = "E_LOC_VAR_RD",
        arg1 = 'x'
    )

    id_instr_env = dict(
        x = "I'm a variable!"
    )

    def test_eval_int(self):
        empty_interpreter_instance.eval(self.int_instr, {}, {})
        self.assertEqual(empty_interpreter_instance.ret, (dict(
                                                            v_type = 'val_num',
                                                            val = 3
                                                          ), {}, {}))

    def test_eval_float(self):
        empty_interpreter_instance.eval(self.float_instr, {}, {})
        self.assertEqual(empty_interpreter_instance.ret, (dict(
                                                            v_type = 'val_num',
                                                            val = 3.1415926
                                                          ), {}, {}))

    def test_eval_str(self):
        empty_interpreter_instance.eval(self.str_instr, {}, {})
        self.assertEqual(empty_interpreter_instance.ret, (dict(
                                                            v_type = 'val_str',
                                                            val = "Hello, world!"
                                                          ), {}, {}))

    def test_eval_id(self):
        empty_interpreter_instance.eval(self.id_instr, self.id_instr_env, {})
        self.assertEqual(empty_interpreter_instance.ret, (dict(
                                                            v_type = 'val_str',
                                                            val = "I'm a variable!"
                                                          ), self.id_instr_env, {}))

class EvalArithmeticExpressions(unittest.TestCase):
    add_instr = dict(
        e_type = "E_ADD",
        arg1 = dict(
            e_type = "E_INT",
            val = 20
        ),
        arg2 = dict(
            e_type = "E_INT",
            val = 25
        )
    )

    sub_instr = dict(
        e_type = "E_SUB",
        arg1 = dict(
            e_type = "E_INT",
            val = 20
        ),
        arg2 = dict(
            e_type = "E_INT",
            val = 25
        )
    )

    mult_instr = dict(
        e_type = "E_MUL",
        arg1 = dict(
            e_type = "E_INT",
            val = 20
        ),
        arg2 = dict(
            e_type = "E_INT",
            val = 25
        )
    )

    div_instr_coerce = dict(
        e_type = "E_DIV",
        arg1 = dict(
            e_type = "E_INT",
            val = 5
        ),
        arg2 = dict(
            e_type = "E_INT",
            val = 2
        )
    )

    div_instr_float = dict(
        e_type = "E_DIV",
        arg1 = dict(
            e_type = "E_FLOAT",
            val = 5.0
        ),
        arg2 = dict(
            e_type = "E_FLOAT",
            val = 2.0
        )
    )

    def test_eval_add(self):
        empty_interpreter_instance.eval(self.add_instr, {}, {})
        self.assertEqual(empty_interpreter_instance.ret, (dict(
                                                            v_type = 'val_num',
                                                            val = 45
                                                          ), {}, {}))

    def test_eval_minus(self):
        empty_interpreter_instance.eval(self.sub_instr, {}, {})
        self.assertEqual(empty_interpreter_instance.ret, (dict(
                                                            v_type = 'val_num',
                                                            val = -5
                                                          ), {}, {}))

    def test_eval_times(self):
        empty_interpreter_instance.eval(self.mult_instr, {}, {})
        self.assertEqual(empty_interpreter_instance.ret, (dict(
                                                            v_type = 'val_num',
                                                            val = 500
                                                          ), {}, {}))

    def test_eval_div_int_coerce(self):
        empty_interpreter_instance.eval(self.div_instr_coerce, {}, {})
        self.assertEqual(empty_interpreter_instance.ret, (dict(
                                                            v_type = 'val_num',
                                                            val = 2
                                                          ), {}, {}))

    def test_eval_div_float(self):
        empty_interpreter_instance.eval(self.div_instr_float, {}, {})
        self.assertEqual(empty_interpreter_instance.ret, (dict(
                                                            v_type = 'val_num',
                                                            val = 2.5
                                                          ), {}, {}))


#TODO: test the short-circuiting nature of the two operators -- i.e.,
#TODO: evaluation of constituent expressions should stop immediately upon
#TODO: encountering a tell-tale value (false for &&, true for ||), and
#TODO: potential run-time errors in further, non-evaluated operand expressions
#TODO: should never arise
class EvalBooleanExpressions(unittest.TestCase):
    # here are the values the boolean expressions can return
    val_true = dict(
        v_type = "val_bool",
        val = True
    )

    val_false = dict(
        v_type = "val_bool",
        val = False
    )

    # here are simple primitive instructions to help build up the complex
    # boolean instructions below
    int_instr_1 = dict(
        e_type = "E_INT",
        val = 1
    )

    int_instr_2 = dict(
        e_type = "E_INT",
        val = 2
    )

    float_instr_1 = dict(
        e_type = "E_INT",
        val = 1.5
    )

    float_instr_2 = dict(
        e_type = "E_INT",
        val = 2.5
    )

    str_instr_1 = dict(
        e_type = "E_STRING",
        val = "string1"
    )

    str_instr_2 = dict(
        e_type = "E_STRING",
        val = "string2"
    )

    # here are the instructions to test
    true_instr = dict(
        e_type = "E_TRUE",
        val = True
    )

    false_instr = dict(
        e_type = "E_FALSE",
        val = False
    )

    equals_instr_bool = dict(
        e_type = "E_EQUALS",
        arg1 = dict(
            e_type = "E_EQUALS",
            arg1 = true_instr,
            arg2 = true_instr
        ),
        arg2 = dict(
            e_type = "E_EQUALS",
            arg1 = false_instr,
            arg2 = false_instr
        )
    )

    not_equals_instr_bool = dict(
        e_type = "E_EQUALS",
        arg1 = true_instr,
        arg2 = false_instr
    )

    equals_instr_int = dict(
        e_type = "E_EQUALS",
        arg1 = int_instr_1,
        arg2 = int_instr_1
    )

    not_equals_instr_int = dict(
        e_type = "E_EQUALS",
        arg1 = int_instr_1,
        arg2 = int_instr_2
    )

    equals_instr_float = dict(
        e_type = "E_EQUALS",
        arg1 = float_instr_1,
        arg2 = float_instr_1
    )

    not_equals_instr_float = dict(
        e_type = "E_EQUALS",
        arg1 = float_instr_1,
        arg2 = float_instr_2
    )

    equals_instr_str = dict(
        e_type = "E_EQUALS",
        arg1 = str_instr_1,
        arg2 = str_instr_1
    )

    not_equals_instr_str = dict(
        e_type = "E_EQUALS",
        arg1 = str_instr_1,
        arg2 = str_instr_2
    )

    gt_instr = dict(
        e_type = "E_GT",
        arg1 = int_instr_2,
        arg2 = int_instr_1
    )

    not_gt_instr = dict(
        e_type = "E_GT",
        arg1 = int_instr_1,
        arg2 = int_instr_2
    )

    lt_instr = dict(
        e_type = "E_LT",
        arg1 = float_instr_1,
        arg2 = float_instr_2
    )

    not_lt_instr = dict(
        e_type = "E_LT",
        arg1 = float_instr_2,
        arg2 = float_instr_1
    )

    gte_instr = dict(
        e_type = "E_GTE",
        arg1 = float_instr_2,
        arg2 = int_instr_1
    )

    not_gte_instr = dict(
        e_type = "E_GTE",
        arg1 = int_instr_1,
        arg2 = float_instr_2
    )

    lte_instr = dict(
        e_type = "E_LTE",
        arg1 = int_instr_1,
        arg2 = float_instr_2
    )

    not_lte_instr = dict(
        e_type = "E_LTE",
        arg1 = float_instr_2,
        arg2 = int_instr_1
    )

    and_instr_simple_true = dict(
        e_type = "E_AND",
        arg1 = true_instr,
        arg2 = true_instr
    )

    and_instr_simple_false_1 = dict(
        e_type = "E_AND",
        arg1 = true_instr,
        arg2 = false_instr
    )

    and_instr_simple_false_2 = dict(
        e_type = "E_AND",
        arg1 = false_instr,
        arg2 = false_instr
    )

    and_instr_complex_true = dict(
        e_type = "E_AND",
        arg1 = gte_instr,
        arg2 = lte_instr
    )

    and_instr_complex_false = dict(
        e_type = "E_AND",
        arg1 = gte_instr,
        arg2 = not_gte_instr
    )

    or_instr_simple_true_1 = dict(
        e_type = "E_OR",
        arg1 = true_instr,
        arg2 = true_instr
    )

    or_instr_simple_true_2 = dict(
        e_type = "E_OR",
        arg1 = true_instr,
        arg2 = false_instr
    )

    or_instr_simple_false = dict(
        e_type = "E_OR",
        arg1 = false_instr,
        arg2 = false_instr
    )

    or_instr_complex_true = dict(
        e_type = "E_OR",
        arg1 = gt_instr,
        arg2 = not_lt_instr
    )

    or_instr_complex_false = dict(
        e_type = "E_OR",
        arg1 = not_gt_instr,
        arg2 = not_lt_instr
    )

    not_instr_simple_false = dict(
        e_type = "E_NOT",
        arg1 = true_instr
    )

    not_instr_simple_true = dict(
        e_type = "E_NOT",
        arg1 = false_instr
    )

    not_instr_complex_false = dict(
        e_type = "E_NOT",
        arg1 = or_instr_complex_true
    )

    not_instr_complex_true = dict(
        e_type = "E_NOT",
        arg1 = and_instr_complex_false
    )

    # here are the tests themselves
    def test_boolean_primitives(self):
        empty_interpreter_instance.eval(self.true_instr, {}, {})
        self.assertEqual(empty_interpreter_instance.ret, (self.val_true, {}, {}))

        empty_interpreter_instance.eval(self.false_instr, {}, {})
        self.assertEqual(empty_interpreter_instance.ret, (self.val_false, {}, {}))

    def test_equals(self):
        empty_interpreter_instance.eval(self.equals_instr_bool, {}, {})
        self.assertEqual(empty_interpreter_instance.ret, (self.val_true, {}, {}))

        empty_interpreter_instance.eval(self.not_equals_instr_bool, {}, {})
        self.assertEqual(empty_interpreter_instance.ret, (self.val_false, {}, {}))

        empty_interpreter_instance.eval(self.equals_instr_int, {}, {})
        self.assertEqual(empty_interpreter_instance.ret, (self.val_true, {}, {}))

        empty_interpreter_instance.eval(self.not_equals_instr_int, {}, {})
        self.assertEqual(empty_interpreter_instance.ret, (self.val_false, {}, {}))

        empty_interpreter_instance.eval(self.equals_instr_float, {}, {})
        self.assertEqual(empty_interpreter_instance.ret, (self.val_true, {}, {}))

        empty_interpreter_instance.eval(self.not_equals_instr_float, {}, {})
        self.assertEqual(empty_interpreter_instance.ret, (self.val_false, {}, {}))

        empty_interpreter_instance.eval(self.equals_instr_str, {}, {})
        self.assertEqual(empty_interpreter_instance.ret, (self.val_true, {}, {}))

        empty_interpreter_instance.eval(self.not_equals_instr_str, {}, {})
        self.assertEqual(empty_interpreter_instance.ret, (self.val_false, {}, {}))

    def test_gt(self):
        empty_interpreter_instance.eval(self.gt_instr, {}, {})
        self.assertEqual(empty_interpreter_instance.ret, (self.val_true, {}, {}))

        empty_interpreter_instance.eval(self.not_gt_instr, {}, {})
        self.assertEqual(empty_interpreter_instance.ret, (self.val_false, {}, {}))

    def test_lt(self):
        empty_interpreter_instance.eval(self.lt_instr, {}, {})
        self.assertEqual(empty_interpreter_instance.ret, (self.val_true, {}, {}))

        empty_interpreter_instance.eval(self.not_lt_instr, {}, {})
        self.assertEqual(empty_interpreter_instance.ret, (self.val_false, {}, {}))

    def test_gte(self):
        empty_interpreter_instance.eval(self.gte_instr, {}, {})
        self.assertEqual(empty_interpreter_instance.ret, (self.val_true, {}, {}))

        empty_interpreter_instance.eval(self.not_gte_instr, {}, {})
        self.assertEqual(empty_interpreter_instance.ret, (self.val_false, {}, {}))

    def test_lte(self):
        empty_interpreter_instance.eval(self.lte_instr, {}, {})
        self.assertEqual(empty_interpreter_instance.ret, (self.val_true, {}, {}))

        empty_interpreter_instance.eval(self.not_lte_instr, {}, {})
        self.assertEqual(empty_interpreter_instance.ret, (self.val_false, {}, {}))

    def test_and(self):
        empty_interpreter_instance.eval(self.and_instr_simple_true, {}, {})
        self.assertEqual(empty_interpreter_instance.ret, (self.val_true, {}, {}))

        empty_interpreter_instance.eval(self.and_instr_simple_false_1, {}, {})
        self.assertEqual(empty_interpreter_instance.ret, (self.val_false, {}, {}))

        empty_interpreter_instance.eval(self.and_instr_simple_false_2, {}, {})
        self.assertEqual(empty_interpreter_instance.ret, (self.val_false, {}, {}))

        empty_interpreter_instance.eval(self.and_instr_complex_true, {}, {})
        self.assertEqual(empty_interpreter_instance.ret, (self.val_true, {}, {}))

        empty_interpreter_instance.eval(self.and_instr_complex_false, {}, {})
        self.assertEqual(empty_interpreter_instance.ret, (self.val_false, {}, {}))

    def test_or(self):
        empty_interpreter_instance.eval(self.or_instr_simple_true_1, {}, {})
        self.assertEqual(empty_interpreter_instance.ret, (self.val_true, {}, {}))

        empty_interpreter_instance.eval(self.or_instr_simple_true_2, {}, {})
        self.assertEqual(empty_interpreter_instance.ret, (self.val_true, {}, {}))

        empty_interpreter_instance.eval(self.or_instr_simple_false, {}, {})
        self.assertEqual(empty_interpreter_instance.ret, (self.val_false, {}, {}))

        empty_interpreter_instance.eval(self.or_instr_complex_true, {}, {})
        self.assertEqual(empty_interpreter_instance.ret, (self.val_true, {}, {}))

        empty_interpreter_instance.eval(self.or_instr_complex_false, {}, {})
        self.assertEqual(empty_interpreter_instance.ret, (self.val_false, {}, {}))

    def test_not(self):
        empty_interpreter_instance.eval(self.not_instr_simple_false, {}, {})
        self.assertEqual(empty_interpreter_instance.ret, (self.val_false, {}, {}))

        empty_interpreter_instance.eval(self.not_instr_simple_true, {}, {})
        self.assertEqual(empty_interpreter_instance.ret, (self.val_true, {}, {}))

        empty_interpreter_instance.eval(self.not_instr_complex_false, {}, {})
        self.assertEqual(empty_interpreter_instance.ret, (self.val_false, {}, {}))

        empty_interpreter_instance.eval(self.not_instr_complex_true, {}, {})
        self.assertEqual(empty_interpreter_instance.ret, (self.val_true, {}, {}))

# class EvalSimpleMethod(unittest.TestCase):
#     def test_eval_expr_meth(self):
#         (method_table, _, _) = meth_parser.parse("tests.meth")
#         simple_method = method_table['test_meth1']
#         environment = dict(
#             x = 10,
#             y = 4,
#             pi = 3.1415952
#         )
#         simple_method_interpreter = \
#                 interpreter.Interpreter(simple_method, environment, {})
#
#         # we'll round the interpreter's answer to three decimal places
#         # so that we're actually testing the interpreter's functionality, and
#         # not Python's floating point precision
#         for node in simple_method_interpreter:
#             print node
#         unrounded_val = simple_method_interpreter.ret[0]['val']
#         rounded_val = float("{0:.3f}".format(unrounded_val))
#         simple_method_interpreter.ret[0]['val'] = rounded_val
#
#         self.assertEqual(simple_method_interpreter.ret, (dict(
#                                                             v_type = 'val_num',
#                                                             val = 15.283
#                                                          ), environment, {}))

"""
INTERPRETER SEMANTICS: STATEMENTS

The following three test cases exercise the interpreter's semantics for
*statements* -- that is, those syntactic constructs that *could* alter the
environment, or that traditionally don't return a value -- as 'if', 'while',
'seq', 'assign', 'loc_var_rd/wr' and 'state_var_rd/wr.'

As noted in the overall documentation for the expression-semantic unit tests
(which see above), in our language (as in Ruby) even statements reduce to
values, though the values produced by statements are typically thrown
away, and it is their effect on execution flow and program state (through
modification of the environment) that is their most important characteristic.

However, it is generally worth noting that, in our language, control statements
reduce to the None type, and variable reads and writes reduce to the value being
read from or written to the variable (whether that be a local variable or a
state variable).
"""

class EvalControlStatements(unittest.TestCase):
    # environments (they correspond by number to the conditions below --
    # an environment and a condition with a corresponding number are such that
    # the environment makes the condition true or false, according as the name
    # of the condition indicates that it ought to evaluate to true or false)
    env_1 = dict(
        i = 5,
        j = 10,
        t = True,
        f = False
    )
    env_2 = dict(
        s1 = "string1",
        s1_copy = "string1",
        s2 = "string2",
        t = True,
        f = False
    )
    env_3 = dict(
        i = 5,
        j = 10,
        x = 5.5,
        y = 10.5,
        s1 = "string1",
        s1_copy = "string1",
        s2 = "string2",
        t = True,
        f = False
    )

    # a method to construct local variable primitives
    def make_loc_var_instr(self, id):
        dict(
            e_type = "E_LOC_VAR_RD",
            arg1 = id
        )

    # conditions, to be used in testing control statements
    simple_cond_true = dict(
        e_type = "E_TRUE",
        val = True
    )
    simple_cond_false = dict(
        e_type = "E_FALSE",
        val = False
    )
    simple_cond_true_1 = dict(
        e_type = "E_GT",
        arg1 = dict(
            e_type = "E_LOC_VAR_RD",
            arg1 = 'j'
        ),
        arg2 = dict(
            e_type = "E_LOC_VAR_RD",
            arg1 = 'i'
        )
    )
    simple_cond_false_1 = dict(
        e_type = "E_LTE",
        arg1 = dict(
            e_type = "E_LOC_VAR_RD",
            arg1 = 'j'
        ),
        arg2 = dict(
            e_type = "E_LOC_VAR_RD",
            arg1 = 'i'
        )
    )
    simple_cond_true_2 = dict(
        e_type = "E_EQUALS",
        arg1 = dict(
            e_type = "E_LOC_VAR_RD",
            arg1 = 's1'
        ),
        arg2 = dict(
            e_type = "E_LOC_VAR_RD",
            arg1 = 's1_copy'
        )
    )
    simple_cond_false_2 = dict(
        e_type = "E_EQUALS",
        arg1 = dict(
            e_type = "E_LOC_VAR_RD",
            arg1 = 's1'
        ),
        arg2 = dict(
            e_type = "E_LOC_VAR_RD",
            arg1 = 's2'
        )
    )
    simple_cond_true_3 = dict(
        e_type = "E_OR",
        arg1 = dict(
            e_type = "E_LTE",
            arg1 = dict(
                e_type = "E_LOC_VAR_RD",
                arg1 = 'x'
            ),
            arg2 = dict(
                e_type = "E_LOC_VAR_RD",
                arg1 = 'y'
            )
        ),
        arg2 = simple_cond_false_2
    )
    simple_cond_false_3 = dict(
        e_type = "E_OR",
        arg1 = dict(
            e_type = "E_GTE",
            arg1 = dict(
                e_type = "E_LOC_VAR_RD",
                arg1 = 'x'
            ),
            arg2 = dict(
                e_type = "E_LOC_VAR_RD",
                arg1 = 'y'
            )
        ),
        arg2 = simple_cond_false_2
    )

    complex_cond_true = dict(
        e_type = "E_AND",
        arg1 = dict(
            e_type = "E_NOT",
            arg1 = simple_cond_false_3
        ),
        arg2 = simple_cond_true_3
    )
    complex_cond_false = dict(
        e_type = "E_AND",
        arg1 = dict(
            e_type = "E_NOT",
            arg1 = simple_cond_true_3
        ),
        arg2 = dict(
            e_type = "E_AND",
            arg1 = simple_cond_false_1,
            arg2 = dict(
                e_type = "E_AND",
                arg1 = simple_cond_false_2,
                arg2 = simple_cond_false_3
            )
        )
    )

    # blocks
    block_1 = dict(
        e_type = "E_LOC_VAR_WR",
        arg1 = 'i',
        arg2 = dict(
            e_type = "E_SUB",
            arg1 = dict(
                e_type = "E_LOC_VAR_RD",
                arg1 = 'i'
            ),
            arg2 = dict(
                e_type = "E_INT",
                val = 1
            )
        )
    )

    # a function for building if-statements out of conditions and blocks
    def make_if_instr(self, conds, blocks):
        if len(conds) != len(blocks):
            raise ValueError("The number of conditions does not match the \
                              number of blocks")
        return dict(
            e_type = "E_IF",
            conds = conds,
            blocks = blocks
        )

    # code blocks -- they all change the environment in various ways, which is
    # how we'll determine whether or not the control statements are directing
    # execution flow correctly

    # finally, the tests:
    def test_if(self):
        # first make local copies of the environments before we mutate them
        _env_1 = copy.copy(self.env_1)

        '''first a simple (true) if with no alternate branches'''
        old_env = copy.copy(_env_1)
        new_env = copy.copy(old_env)
        new_env['i'] = old_env['i'] - 1

        if_instr_1 = self.make_if_instr([self.simple_cond_true_1], [self.block_1])
        empty_interpreter_instance.eval(if_instr_1, _env_1, {})
        (res, test_env, _) = empty_interpreter_instance.ret

        # print("\n\nres = " + res.__repr__())
        # print("test_env = " + test_env.__repr__() + "\n\n")

        self.assertEqual(res['val'], None) # test the stmt returns the
                                                   # correct value as result
        self.assertEqual(test_env, new_env) # test that the stmt correctly
                                            # modified the environment

        # restore the environment
        _env_1 = old_env

        '''now a simple (false) if with no alternate branches'''
        if_instr_2 = self.make_if_instr([self.simple_cond_false_1], [self.block_1])
        empty_interpreter_instance.eval(if_instr_2, _env_1, {})
        (res, test_env, _) = empty_interpreter_instance.ret

        self.assertEqual(res['val'], None) # test the stmt returns the
                                                   # correct value as result
        self.assertEqual(test_env, old_env) # test that the stmt correctly (didn't)
                                            # modify the environment

        # restore the environment
        _env_1 = old_env

    def test_if_else(self):
        pass

    def test_if_elif(self):
        pass

    def test_if_elif_else(self):
        pass

    def test_while_false(self):
        pass

    def test_while_true(self):
        pass

# class EvalLocalVariableStatements(unittest.TestCase):

# class EvalStateVariableStatements(unittest.TestCase):

"""
INTERPRETER API: DECISION NODES

The following three test cases exercise the interpreter's semantics for
*statements* -- that is, those syntactic constructs that *could* alter the
environment, or that traditionally don't return a value -- as 'if', 'while',
'seq', 'assign', 'loc_var_rd/wr' and 'state_var_rd/wr.'

As noted in the overall documentation for the expression-semantic unit tests
(which see above), in our language (as in Ruby) even statements reduce to
values, though the values produced by statements are typically thrown
away, and it is their effect on execution flow and program state (through
modification of the environment) that is their most important characteristic.

However, it is generally worth noting that, in our language, control statements
reduce to the None type, and variable reads and writes reduce to the value being
read from or written to the variable (whether that be a local variable or a
state variable).
"""

# class EvalDecisionNodeProduction(unittest.TestCase):


if __name__ == '__main__':
    unittest.main()
