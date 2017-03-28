import ast

module = ast.parse("""
class A():
    def __init__(self):
        print("smth")
        self.zero = 0

    def take_zero(self):
        return self.zero
""")

class_definitions = [node for node in module.body if isinstance(node, ast.ClassDef)]
method_definitions = []

for class_def in class_definitions:
    method_definitions.append([node.name for node in class_def.body if isinstance(node, ast.FunctionDef)])

print(method_definitions)