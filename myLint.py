'''
Simple python Linter
original article: https://sadh.life/post/ast/
'''
import ast 
import os, sys
from typing import NamedTuple 

class Violation(NamedTuple):
    """
    Every rule violation contains a node that breaks the rule,
    and message that will be shownto the user.
    """
    node: ast.AST
    message: str

class Checker(ast.NodeVisitor):
    '''
    A checker is a visitor that defines a lint rule, and stors all the 
    nodes that violate that line rule.
    '''
    def __init__(self, issue_code):
        self.issue_code = issue_code
        self.violations = set()


class Linter:
    # Holds all the list rules, and runs them against a source file.

    def __init__(self):
        self.checkers = set()


    @staticmethod
    def print_violations(checker, file_name):
        for node, message in checker.violations:
            print(
                f"{file_name}:{node.lineno}:{node.col_offset}: "
                f"{checker.issue_code}: {message}"
            )

    def run(self, source_path):
        # runs all lints on a source file
        file_name = os.path.basename(source_path)

        with open(source_path) as source_file:
            source_file = source_file.read()

        tree = ast.parse(source_file)
        for checker in self.checkers:
            checker.visit(tree)
            self.print_violations(checker, file_name)


class SetDuplicateItemChecker(Checker):
    # checks if a set in your code has duplicate constants

    def visit_Set(self, node):
        # stores all the constants this set holds, and finds dubplicats
        seen_values = set()
        for element in node.elts:
            # we're only concerned about constant values like ints.
            if not isinstance(element, ast.Constant):
                continue

            # if its already in seem values, raise a lint violation.
            value = element.value
            if value in seen_values:
                violation = Violation(
                    node=element,
                    message = f"Set contains duplicate item: {value!r}",
                )
                self.violations.add(violation)
            else:
                seen_values.add(element.value)

class Unused_Variable_In_Scope_Checker(Checker):
    # checks if any variables are unused in a node's scope.

    def __init__(self, issue_code):
        super().__init__(issue_code)
        '''
        unused_name is a dictionary that stores variable names, and
        whether or not they've been found in a "Load" context yet.
        if thats found to be used, its value is turned to False.
        '''

        self.unused_names = {}

        # name_nodes holds the first occurences of variables.
        self.name_nodes = {}

    def visit_Name(self, node):
        # find all nodes that only exist in 'Store' context
        var_name = node.id

        if isinstance(node.ctx, ast.Store):
            # if its a new name, save the node for latter 
            if var_name not in self.name_nodes:
                self.name_nodes[var_name] = node
            
            # if we've never seen it before, ir is unused.
            if var_name not in self.unused_names:
                self.unused_names[var_name] = True

        else:
            # it's used somewhere
            self.unused_names[var_name] = False
            
class Unused_Variable_Checker(Checker):
    # find unused variables in  the local scope of this node.
    def check_for_unused_variables(self, node):
        visitor =Unused_Variable_In_Scope_Checker(self.issue_code)
        visitor.visit(node)

    # Now the visitor has collected data, and we can use that data
        for name, unused in visitor.unused_names.items():
            if unused:
                node = visitor.name_nodes[name]
                self.violations.add(Violation(node, f"Unused variable: {name}"))

    def visit_Modules(self, node):
        self.check_for_unused_variables(node)
        super().generic_visit(node)

    def visit_ClassDef(self, node):
        self.check_for_unused_variables(node)
        super().generic_visit(node)

    def visit_FunctionDef(self, node):
        self.check_for_unused_variables(node)
        super().generic_visit(node)


def main():
    source_path = sys.argv[1]

    linter = Linter()
    linter.checkers.add(SetDuplicateItemChecker(issue_code="W001"))
    linter.checkers.add(Unused_Variable_Checker(issue_code="W002"))

    linter.run(source_path)



if __name__ == "__main__":
    main()