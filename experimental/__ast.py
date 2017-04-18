
import ast

class Visitor(ast.NodeVisitor):
     def __init__(self):
            self._names_seen = set()
     def visit_Name(self, node):
            self._names_seen.add(node.id)

node = ast.parse("all(package.name not in ['plainbox', 'tuxracer'])")

v = Visitor()
v.visit(node)

print(v._names_seen)