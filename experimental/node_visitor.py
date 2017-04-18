import inspect
import ast
import symtable
from tokenize import generate_tokens, untokenize, INDENT
from cStringIO import StringIO

class NodeVisitor(ast.NodeVisitor):
    def __init__(self, SymbolTable):
        self.symtable = SymbolTable
        for child in SymbolTable.get_children():
            self.symtable = child
            print(child.get_symbols())

    def _visit_children(self, node):
        """Determine if the node has children and visit"""
        for _, value in ast.iter_fields(node):
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, ast.AST):
                        print('  visit item %s' % (type(item).__name__))
                        self.visit(item)

            elif isinstance(value, ast.AST):
                print('  visit value %s' % (type(value).__name__))
                self.visit(value)

    def generic_visit(self, node):
        print(type(node).__name__)
        self._visit_children(node)

    def visit_Attribute(self, node):
        print('  attribute %s' % node.attr)
        self._visit_children(node)

    def visit_Name(self, node):
        print('  variable %s type %s' % (node.id,
                                         self.symtable.lookup(node.id)))
        print(dir(self.symtable.lookup(node.id)))

# _dedent borrowed from the myhdl package (www.myhdl.org)
def _dedent(s):
    """Dedent python code string."""

    result = [t[:2] for t in generate_tokens(StringIO(s).readline)]
    # set initial indent to 0 if any
    if result[0][0] == INDENT:
        result[0] = (INDENT, '')
    return untokenize(result)


class MyObj(object):
    def __init__(self):
        self.val = None

class MyObjFloat(object):
    def __init__(self):
        self.x = 1.

class MyObjInt(object):
    def __init__(self):
        self.x = 1

class MyObjObj(object):
    def __init__(self):
        self.xi = MyObjInt()
        self.xf = MyObjFloat()


def testFunc(x,y,xo,z):

    def eval_types():
        z.val = x + y + xo.xi.x + xo.xf.x

    return eval_types


if __name__ == '__main__':
    z = MyObj()
    print(z.val)
    f = testFunc(1, 2, MyObjObj(), z)
    f()
    print(z.val)
    s = inspect.getsource(f)
    s = _dedent(s)
    print(type(s))
    print(s)

    SymbolTable = symtable.symtable(s,'string','exec')
    tree = ast.parse(s)
    v = NodeVisitor(SymbolTable)
    v.visit(tree)
