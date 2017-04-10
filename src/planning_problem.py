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

import zipfile
# import dom_lexer            # this is the module where we've specified the dom-file lexer rules
import dom_parser           # this is the module where we've specified the dom-file parser rules
# import meth_lexer           # this is the module where we've specified the method-file lexer rules
import meth_parser          # this is the module where we've specified the method-file parser rules
import action_parser
import command_parser

class PlanningProblem:
    def __init__(path_to_zip):
        with ZipFile(path_to_zip, 'r') as archive:
            for member in archive.namelist():
                if member.endswith('.meth'):
                    (self.method_table, self.task_table, self.task_method_map) = \
                        meth_parser.parse(member)
                elif member.endswith('.dom'):
                    self.domain = dom_parser.parse(filename=member)
                elif member.endswith('.act'):
                    self.action_models = action_parser.parse(member)
                elif member.endswith('.cmd'):
                    self.commands = command_parser.parse(member)
