import ast
import uuid

class CodeVisitor(ast.NodeVisitor):
    def __init__(self):
        self.items = []

    def generate_id(self):
        return str(uuid.uuid4())

    def visit_FunctionDef(self, node):
        func_id = self.generate_id()  # Unique identifier for the function block.
        func_item = {
            'type': 'FUNCTION',
            'id': func_id,
            'name': node.name,
            'position': {"x": None, "y": None},
            'inputs': [],  # Will be updated with argument info.
            'outputs': [],
            'connections': [],
        }
        self.items.append(func_item)
        
        # Generate OUTPUT block for function's return value.
        output_item = {
            'type': 'OUTPUT',
            'id': self.generate_id(),
            'name': 'return',
            'valueType': self.infer_return_type(node),
            'position': {"x": None, "y": None},
            'connections': [],
            'functionId': func_id,  # Reference to the function block.
        }
        self.items.append(output_item)
        
        # Generate INPUT blocks for function arguments.
        for arg in node.args.args:
            input_item = {
                'type': 'INPUT',
                'id': self.generate_id(),
                'name': arg.arg,
                'valueType': 'unknown',  # Placeholder, as inferring type from arg alone is complex.
                'position': {"x": None, "y": None},
                'functionId': func_id,  # Linking this input to its function.
            }
            self.items.append(input_item)

    def visit_Assign(self, node):
        # Handling assignment statements to create variable blocks.
        # ... (same as before)
        self.generic_visit(node)

    def infer_return_type(self, node):
        # Placeholder for return type inference.
        return 'output'

    def infer_type(self, node):
        # Placeholder for value type inference.
        if isinstance(node, (ast.Num, ast.Constant)):  # ast.Constant for Python 3.8+
            return 'int'
        return 'unknown'

def lex_code(code):
    tree = ast.parse(code)
    visitor = CodeVisitor()
    visitor.visit(tree)
    return {'blocks': visitor.items}


two_sums_code = """
def two_sums(nums, target):
    prev_map = {}  # to store visited numbers and their indices
    
    for i, num in enumerate(nums):
        diff = target - num
        if diff in prev_map:
            return [prev_map[diff], i]
        prev_map[num] = i
    return []
"""

hello_world_code = """
def hello():
    print('Hello, World!')
"""
print(lex_code(two_sums_code))

print(lex_code(hello_world_code))
