import ast

module = ast.parse("""
class A():
    # pass
    def __init__(self, melf):
        print("smth")
        self.zero = 0

    # def take_zero(self):
    #     return self.zero

    # class_variable = 2

a = A(23)
""")

class_definitions = [node for node in module.body
                     if isinstance(node, ast.ClassDef)]
method_definitions = []

for class_def in class_definitions:
    for node in class_def.body:
        if isinstance(node, ast.FunctionDef):
            method_definitions.append(node.name)


for node in ast.walk(module):
    if isinstance(node, ast.Name):
        print(node.id)


print(method_definitions)
