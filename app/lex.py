import ast
import uuid

class CodeVisitor(ast.NodeVisitor):
    def __init__(self):
        self.items = []
        self.add_initial_blocks()

    def generate_id(self):
        return str(uuid.uuid4())

    def add_initial_blocks(self):
        self.items.append({
            'type': 'FUNCTION',
            'id': self.generate_id(),
            'name': None,
            'position': {"x": None, "y": None},
            'inputs': [],
            'outputs': [],
            'connections': [],
        })

        self.items.append({
            'type': 'INPUT',
            'id': self.generate_id(),
            'name': None,
            'valueType': 'unknown',
            'position': {"x": None, "y": None},
            'value': '',
            'functionId': None,
        })

        self.items.append({
            'type': 'OUTPUT',
            'id': self.generate_id(),
            'name': 'return',
            'valueType': 'output',
            'position': {"x": None, "y": None},
            'connections': [],
            'functionId': None,
            'value': '',
        })

    def visit_FunctionDef(self, node):
        func_id = self.generate_id()  
        func_item = {
            'type': 'FUNCTION',
            'id': func_id,
            'name': node.name,
            'position': {"x": None, "y": None},
            'inputs': [],  
            'outputs': [],
            'connections': [],
        }
        self.items.append(func_item)
        
        for subnode in ast.walk(node):
            if isinstance(subnode, ast.Assign):
                for target in subnode.targets:
                    if isinstance(target, ast.Name):
                        variable_item = {
                            'type': 'VARIABLE',
                            'id': self.generate_id(),
                            'name': target.id,
                            'valueType': 'unknown',
                            'position': {"x": None, "y": None},
                            'value': self.infer_literal_value(subnode.value),
                        }
                        self.items.append(variable_item)
            elif isinstance(subnode, ast.Return):
                value = self.infer_literal_value(subnode.value)
                if value is not None:
                    func_item['outputs'].append(value)
            elif isinstance(subnode, ast.Expr) and isinstance(subnode.value, ast.Call) and \
                    hasattr(subnode.value.func, 'id') and subnode.value.func.id == 'print':
                print_args = subnode.value.args
                if print_args:
                    print_value = self.infer_literal_value(print_args[0])
                    if print_value is not None:
                        func_item['outputs'].append(print_value)
        
        output_item = {
            'type': 'OUTPUT',
            'id': self.generate_id(),
            'name': 'return',
            'valueType': 'output',
            'position': {"x": None, "y": None},
            'connections': [],
            'functionId': func_id,  
        }
        if 'outputs' in func_item and func_item['outputs']:
            output_item['value'] = func_item['outputs'][0]
        
        self.items.append(output_item)
        
        for arg in node.args.args:
            input_item = {
                'type': 'INPUT',
                'id': self.generate_id(),
                'name': arg.arg,
                'valueType': 'unknown',
                'position': {"x": None, "y": None},
                'functionId': func_id,  
                'value': ''  
            }
            
            for default, param in zip(reversed(node.args.defaults), reversed(node.args.args)):
                if arg is param:
                    input_item['value'] = self.infer_literal_value(default)
                    break
            self.items.append(input_item)

    def infer_literal_value(self, value):
        
        if isinstance(value, (ast.Str, ast.Num)): 
            return value.s
        elif isinstance(value, ast.Constant): 
            return value.value
        return None

    def infer_return_type(self, node):
        return 'output'

def lex_code(code):
    tree = ast.parse(code)
    visitor = CodeVisitor()
    visitor.visit(tree)
    return {'blocks': visitor.items}

# hello_world_code = """
# def hello():
#     print('Hello world!')

# """
# print(lex_code(hello_world_code))
