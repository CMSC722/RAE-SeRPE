"""
Date: Mon, 10 Apr 2017
Last updated: Mon, 10 Apr 2017
Author: Samuel Barham
Organization: University of Maryland, College Park (PhD student)

Project: RAE/SeRPE implementation
Component: Planning Problem Abstraction

This python files contains the class PlanningProblem, which provides an
abstraction over our planning problem description format. The user is meant
to initialize it with a path to a zip archive that contains the requisite
.meth, .dom, .act, and .cmd files. The class uses the various lexing and
parsing utilities we've written to read in the data in those files (and thus
provides other programmers with an abstraction over those utilities as well) and
stores the reulting Python representations of the planning domain, refinement
methods, action models, execution platform commands, and problem specification.
"""

import sys
import zipfile
import parsing.dom_parser as dom_parser
import parsing.meth_parser  as meth_parser
import parsing.action_parser as action_parser
import parsing.command_parser as command_parser

class PlanningProblem:
    def __init__(self, path_to_zip):
        (self.method_table, self.task_table, self.task_method_map) = ({},{},{})
        self.domain = {}
        self.action_models = {}
        self.commands = {}
        with zipfile.ZipFile(path_to_zip, 'r') as archive:
            for member in archive.namelist():
                if member.endswith('.meth'):
                    print("\n*******************************\n")
                    print("Processing .meth file: " + member + "\n\n")

                    (_method_table, _task_table, _task_method_map) = \
                        meth_parser.parse(member)
                    self.method_table.update(_method_table)
                    self.task_table.update(_task_table)
                    self.task_method_map.update(_task_method_map)

                    print("Completed processing .meth file: " + member)
                    print("\n*******************************\n")
                elif member.endswith('.dom'):
                    print("\n*******************************\n")
                    print("\nProcessing .dom_lex file: " + member + "\n\n")

                    self.domain = dom_parser.parse(filename=member)

                    print("\nCompleted processing .dom file: " + member)
                    print("\n*******************************\n")
                elif member.endswith('.act'):
                    print("\n*******************************\n")
                    print("Processing .act file: " + member + "\n\n")

                    self.action_models = action_parser.parse(member)
                    print("self.action_models isa " + repr(type(self.action_models)))

                    print("\nCompleted processing .act file: " + member)
                    print("\n*******************************\n")
                elif member.endswith('.cmd'):
                    print("\n*******************************\n")
                    print("Processing .cmd file: " + member + "\n\n")

                    self.commands = command_parser.parse(member)
                    print("self.commands isa " + repr(type(self.action_models)))

                    print("\nCompleted processing .cmd file: " + member)
                    print("\n*******************************\n")

    """
    Override the built-ins __str__ and __repr__
    """

    def __str__(self):
        res = self.dump(self.domain, 1, "DOMAIN:\n") + "\n" + \
        self.dump(self.task_table, 1, "TASKS:\n") + "\n" + \
        self.dump(self.method_table, 1, "METHODS:\n") + "\n" + \
        self.dump(self.task_method_map, 1, "TASK-METHOD MAPPING:\n") + "\n" + \
        self.dump(self.action_models, 1, "ACTION MODELS:\n") + "\n" + \
        self.dump(self.commands, 1, "COMMANDS:\n") + "\n"
        return res

    def __repr__(self):
        self.__str__()

    """
    UTILITY METHOD

    A generalized solution that is able to pretty-print arbitrarily-deeply
    nested dicts and lists -- a utility we've needed time and again in this
    project, but which library functions (like JSON.dump) cannot always
    provide with the generality that we'd like. This is also prettier and
    cleaner, because it doesn't involve converting a Python object to a
    JavaScript representation before dumping. This code was kindly provided
    to the world by StackOverflow user MrWonderful.
    """

    def dump(self, obj, nested_level=0, header=""):
        spacing = '   '
        string = header

        if type(obj) == dict:
            string = string + '%s{' % ((nested_level) * spacing) + '\n'
            for k, v in obj.items():
                if hasattr(v, '__iter__'):
                    string = string + '%s%s:' % ((nested_level + 1) * spacing, k) + '\n'
                    string = string + self.dump(v, nested_level + 1) + '\n'
                else:
                    string = string + '%s%s: %s' % ((nested_level + 1) * spacing, k, v) + '\n'
            string = string + '%s}' % (nested_level * spacing) + '\n'
        elif type(obj) == list:
            string = string + '%s[' % ((nested_level) * spacing) + '\n'
            for v in obj:
                if hasattr(v, '__iter__'):
                    string = string + self.dump(v, nested_level + 1) + '\n'
                else:
                    string = string + '%s%s' % ((nested_level + 1) * spacing, v) + '\n'
            string = string + '%s]' % ((nested_level) * spacing) + '\n'
        else:
            string = string + '%s%s' % (nested_level * spacing, obj) + '\n'

        return string
