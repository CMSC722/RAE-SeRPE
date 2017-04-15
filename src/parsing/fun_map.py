"""
Date: Mon, 10 Apr 2017
Last updated: Mon, 10 Apr 2017
Author: Samuel Barham
Organization: University of Maryland, College Park (PhD student)

Project: RAE/SeRPE implementation
Component purpose: Dynamic Module Generation and Function Mapping

This component's purpose is to read in a file containing Python functions,
dynmically generate a module from that file, and inspect the resultant module
with the purpose of compiling a table of the module's functions. That table
should map function identifiers to function pointers.

It exposes a single function, parse() (the function new_module is meant to be
private to this module).
"""

def parse(filename, name):
    """
    filename is the path to the module that we're trying to load
    name is the name we'd like the module, once created, to have --
    it should be either:
        actions
    or
        commands
    """
    import inspect

    # try to read the supplied file
    input = ''
    with open(filename, 'r') as f:
        input = f.read()

    module = _new_module(input, name, True)
    functions = inspect.getmembers(module, inspect.isfunction)

    return functions


def _new_module(code, name, add_to_sys_modules=False):
    """
    Import dynamically generated code as a module.

    The parameter 'code' is some object containing the module's code (a string,
    a file handle or an actual compiled code object -- which are the same Python
    types accepted by an exec statement).

    The parameter 'name' is the name to give to the module,

    The parameter 'add_to_sys_modules' is a boolean that indicates wheter or no
    to add the dynmically-generated module to sys.modules. If it is added, a
    subsequent import statement using 'name' will return this module. If it
    is not added to sys.modules, import will try to load it in the normal
    fashion.

    Returns a newly generated module.
    """
    import sys, imp

    module = imp.new_module(name)

    exec code in module.__dict__
    if add_to_sys_modules:
        sys.modules[name] = module

    return module
