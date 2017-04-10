"""
Date: Mon, 10 Apr 2017
Last updated: Mon, 10 Apr 2017
Author: Samuel Barham
Organization: University of Maryland, College Park (PhD student)

Project: RAE/SeRPE implementation
Component: Action Model Parser

This component is only a parser in the loosest sense. It's primary purpose is
read in a file containing Python functions that encapsulate action models for
a particular planning domain, and from that file, compile a map of function
identifiers to function pointers. As you can see from the sparseness of the
module, it is merely a wrapper around fun_map, which is slightly more general.

It exposes a single function, parse() (the function new_module is meant to be
private to this module).
"""

import fun_map

def parse(filename):
     return fun_map.parse(filename)
