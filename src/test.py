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

import unittest
import interpreter
import meth_parser
import json

"""
TEST SETUP
"""
empty_interpreter_instance = interpreter.Interpreter()

"""
TEST CASES

Here is where we define the test cases, organized by project component and then
component functionality.
"""


""" INTERPRETER EVAL TESTS """

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
        arg1 = "x"
    )

    id_instr_env = dict(
        x = "I'm a variable!"
    )

    def test_eval_int(self):
        self.assertEqual(empty_interpreter_instance.eval(self.int_instr, {}, {}, {}),
                                                         (dict(
                                                            v_type = 'val_num',
                                                            val = 3
                                                          ), {}, {}))

    def test_eval_float(self):
        self.assertEqual(empty_interpreter_instance.eval(self.float_instr, {}, {}, {}),
                                                         (dict(
                                                            v_type = 'val_num',
                                                            val = 3.1415926
                                                          ), {}, {}))

    def test_eval_str(self):
        self.assertEqual(empty_interpreter_instance.eval(self.str_instr, {}, {}, {}),
                                                         (dict(
                                                            v_type = 'val_str',
                                                            val = "Hello, world!"
                                                          ), {}, {}))

    def test_eval_id(self):
        self.assertEqual(empty_interpreter_instance.eval(self.id_instr, self.id_instr_env, {}, {}),
                                                         (dict(
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
        self.assertEqual(empty_interpreter_instance.eval(self.add_instr, {}, {}, {}),
                                                         (dict(
                                                            v_type = 'val_num',
                                                            val = 45
                                                          ), {}, {}))

    def test_eval_minus(self):
        self.assertEqual(empty_interpreter_instance.eval(self.sub_instr, {}, {}, {}),
                                                         (dict(
                                                            v_type = 'val_num',
                                                            val = -5
                                                          ), {}, {}))

    def test_eval_times(self):
        self.assertEqual(empty_interpreter_instance.eval(self.mult_instr, {}, {}, {}),
                                                         (dict(
                                                            v_type = 'val_num',
                                                            val = 500
                                                          ), {}, {}))

    def test_eval_div_int_coerce(self):
        self.assertEqual(empty_interpreter_instance.eval(self.div_instr_coerce, {}, {}, {}),
                                                         (dict(
                                                            v_type = 'val_num',
                                                            val = 2
                                                          ), {}, {}))

    def test_eval_div_float(self):
        self.assertEqual(empty_interpreter_instance.eval(self.div_instr_float, {}, {}, {}),
                                                         (dict(
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
        self.assertEqual(empty_interpreter_instance.eval(self.true_instr, {}, {}, {}),
                                                         (self.val_true, {}, {}))

        self.assertEqual(empty_interpreter_instance.eval(self.false_instr, {}, {}, {}),
                                                         (self.val_false, {}, {}))

    def test_equals(self):
        self.assertEqual(empty_interpreter_instance.eval(self.equals_instr_bool, {}, {}, {}),
                                                         (self.val_true, {}, {}))

        self.assertEqual(empty_interpreter_instance.eval(self.not_equals_instr_bool, {}, {}, {}),
                                                         (self.val_false, {}, {}))

        self.assertEqual(empty_interpreter_instance.eval(self.equals_instr_int, {}, {}, {}),
                                                         (self.val_true, {}, {}))

        self.assertEqual(empty_interpreter_instance.eval(self.not_equals_instr_int, {}, {}, {}),
                                                         (self.val_false, {}, {}))

        self.assertEqual(empty_interpreter_instance.eval(self.equals_instr_float, {}, {}, {}),
                                                         (self.val_true, {}, {}))

        self.assertEqual(empty_interpreter_instance.eval(self.not_equals_instr_float, {}, {}, {}),
                                                         (self.val_false, {}, {}))

        self.assertEqual(empty_interpreter_instance.eval(self.equals_instr_str, {}, {}, {}),
                                                         (self.val_true, {}, {}))

        self.assertEqual(empty_interpreter_instance.eval(self.not_equals_instr_str, {}, {}, {}),
                                                         (self.val_false, {}, {}))

    def test_gt(self):
        self.assertEqual(empty_interpreter_instance.eval(self.gt_instr, {}, {}, {}),
                                                         (self.val_true, {}, {}))

        self.assertEqual(empty_interpreter_instance.eval(self.not_gt_instr, {}, {}, {}),
                                                         (self.val_false, {}, {}))

    def test_lt(self):
        self.assertEqual(empty_interpreter_instance.eval(self.lt_instr, {}, {}, {}),
                                                         (self.val_true, {}, {}))

        self.assertEqual(empty_interpreter_instance.eval(self.not_lt_instr, {}, {}, {}),
                                                         (self.val_false, {}, {}))

    def test_gte(self):
        self.assertEqual(empty_interpreter_instance.eval(self.gte_instr, {}, {}, {}),
                                                         (self.val_true, {}, {}))

        self.assertEqual(empty_interpreter_instance.eval(self.not_gte_instr, {}, {}, {}),
                                                         (self.val_false, {}, {}))

    def test_lte(self):
        self.assertEqual(empty_interpreter_instance.eval(self.lte_instr, {}, {}, {}),
                                                         (self.val_true, {}, {}))

        self.assertEqual(empty_interpreter_instance.eval(self.not_lte_instr, {}, {}, {}),
                                                         (self.val_false, {}, {}))

    def test_and(self):
        self.assertEqual(empty_interpreter_instance.eval(self.and_instr_simple_true, {}, {}, {}),
                                                         (self.val_true, {}, {}))

        self.assertEqual(empty_interpreter_instance.eval(self.and_instr_simple_false_1, {}, {}, {}),
                                                         (self.val_false, {}, {}))

        self.assertEqual(empty_interpreter_instance.eval(self.and_instr_simple_false_2, {}, {}, {}),
                                                         (self.val_false, {}, {}))

        self.assertEqual(empty_interpreter_instance.eval(self.and_instr_complex_true, {}, {}, {}),
                                                         (self.val_true, {}, {}))

        self.assertEqual(empty_interpreter_instance.eval(self.and_instr_complex_false, {}, {}, {}),
                                                         (self.val_false, {}, {}))

    def test_or(self):
        self.assertEqual(empty_interpreter_instance.eval(self.or_instr_simple_true_1, {}, {}, {}),
                                                         (self.val_true, {}, {}))

        self.assertEqual(empty_interpreter_instance.eval(self.or_instr_simple_true_2, {}, {}, {}),
                                                         (self.val_true, {}, {}))

        self.assertEqual(empty_interpreter_instance.eval(self.or_instr_simple_false, {}, {}, {}),
                                                         (self.val_false, {}, {}))

        self.assertEqual(empty_interpreter_instance.eval(self.or_instr_complex_true, {}, {}, {}),
                                                         (self.val_true, {}, {}))

        self.assertEqual(empty_interpreter_instance.eval(self.or_instr_complex_false, {}, {}, {}),
                                                         (self.val_false, {}, {}))

    def test_not(self):
        self.assertEqual(empty_interpreter_instance.eval(self.not_instr_simple_false, {}, {}, {}),
                                                         (self.val_false, {}, {}))

        self.assertEqual(empty_interpreter_instance.eval(self.not_instr_simple_true, {}, {}, {}),
                                                         (self.val_true, {}, {}))

        self.assertEqual(empty_interpreter_instance.eval(self.not_instr_complex_false, {}, {}, {}),
                                                         (self.val_false, {}, {}))

        self.assertEqual(empty_interpreter_instance.eval(self.not_instr_complex_true, {}, {}, {}),
                                                         (self.val_true, {}, {}))

class EvalSimpleMethod(unittest.TestCase):
    def test_eval_expr_meth(self):
        (method_table, _, _) = meth_parser.parse("tests.meth")
        simple_method = method_table['test_meth1']
        environment = dict(
            x = 10,
            y = 4,
            pi = 3.1415952
        )
        simple_method_interpreter = \
                interpreter.Interpreter(simple_method, environment, {}, {})

        # we'll round the interpreter's answer to three decimal places
        # so that we're actually testing the interpreter's functionality, and
        # not Python's floating point precision
        unrounded_val = simple_method_interpreter.res[0]['val']
        rounded_val = float("{0:.3f}".format(unrounded_val))
        simple_method_interpreter.res[0]['val'] = rounded_val

        self.assertEqual(simple_method_interpreter.res, (dict(
                                                            v_type = 'val_num',
                                                            val = 15.283
                                                         ), environment, {}))

    #TODO: write a test that exercises the interpreter's semantics for
    #TODO: *statements* -- that is, syntactic constructs that *could* alter
    #TODO: the environment, or that traditionally don't return a value -- as
    #TODO: 'if', 'while', 'seq', 'assign', 'loc/state_var_rd/wr'
    def test_eval_stmt_meth(self):
        True


if __name__ == '__main__':
    unittest.main()
