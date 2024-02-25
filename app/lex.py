import ast
import uuid

class CodeVisitor(ast.NodeVisitor):
    def __init__(self):
        self.items = []
        self.context_stack = []

    def generate_id(self):
        return str(uuid.uuid4())

    def visit_FunctionDef(self, node):
        item = {
            'type': 'FUNCTION',
            'id': self.generate_id(),
            'name': node.name,
            'args': [arg.arg for arg in node.args.args],
            'returns': self.infer_return_type(node),
            'position': {"x": None, "y": None},
            'children': [],
        }
        self.context_stack.append(item)
        self.generic_visit(node)
        self.context_stack.pop()

        if self.context_stack:
            self.context_stack[-1]['children'].append(item)
        else:
            self.items.append(item)

    def visit_Assign(self, node):
        targets = [t.id for t in node.targets if isinstance(t, ast.Name)]
        value_type = self.infer_type(node.value)
        for target in targets:
            item = {
                'type': 'VARIABLE',
                'id': self.generate_id(),
                'name': target,
                'position': {"x": None, "y": None},
                'valueType': value_type,
            }
            if self.context_stack:
                self.context_stack[-1]['children'].append(item)
            else:
                self.items.append(item)
        self.generic_visit(node)

    def visit_If(self, node):
        item = {
            'type': 'CONDITIONAL',
            'id': self.generate_id(),
            'condition': ast.unparse(node.test),
            'position': {"x": None, "y": None},
            'children': [],
        }
        self.context_stack.append(item)
        self.generic_visit(node)
        self.context_stack.pop()

        if self.context_stack:
            self.context_stack[-1]['children'].append(item)
        else:
            self.items.append(item)

    def visit_For(self, node):
        item = {
            'type': 'LOOP',
            'id': self.generate_id(),
            'loopType': 'for',
            'iterator': ast.unparse(node.target),
            'iterable': ast.unparse(node.iter),
            'position': {"x": None, "y": None},
            'children': [],
        }
        self.context_stack.append(item)
        self.generic_visit(node)
        self.context_stack.pop()
        
        if self.context_stack:
            self.context_stack[-1]['children'].append(item)
        else:
            self.items.append(item)


    def visit_While(self, node):
        item = {
            'type': 'LOOP',
            'id': self.generate_id(),
            'loopType': 'while',
            'test': ast.unparse(node.test),
            'position': {"x": None, "y": None},
            'children': [],
        }
        self.context_stack.append(item)
        self.generic_visit(node)
        self.context_stack.pop()

        if self.context_stack:
            self.context_stack[-1]['children'].append(item)
        else:
            self.items.append(item)

    def infer_return_type(self, node):
        for body_item in node.body:
            if isinstance(body_item, ast.Return):
                return self.infer_type(body_item.value)
        return 'unknown'

    def infer_type(self, node):
        if isinstance(node, ast.Str):
            return 'str'
        elif isinstance(node, ast.Num):
            return type(node.n).__name__  
        elif isinstance(node, ast.List):
            return 'list'
        elif isinstance(node, ast.Dict):
            return 'dict'
        elif isinstance(node, ast.NameConstant):
            return str(node.value)  
        elif isinstance(node, ast.Call):
            
            return 'function result'
        elif isinstance(node, ast.BinOp):
            return 'result of binary operation'
        else:
            return 'unknown'

def lex_code(code):
    tree = ast.parse(code)
    visitor = CodeVisitor()
    visitor.visit(tree)
    return {'blocks': visitor.items}