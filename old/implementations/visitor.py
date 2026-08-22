from dataclasses import dataclass, fields, is_dataclass

#================================================================

class ASTPrinter:
    def __init__(self, tab='  '):
        self.tab = tab
        self.ident = 0

    def print(self, *args):
        print(f'{self.tab * self.ident}{' '.join(str(arg) for arg in args)}')

    def visit(self, node):
        self.ident += 1
        node.accept(self)
        self.ident -= 1

    def visit_let(self, let):
        self.print('Let', let.name)
        if let.value is not None:
            self.visit(let.value)

    def visit_lambda(self, _lambda):
        self.print('Lambda', *_lambda.params)
        self.visit(_lambda.body)

    def visit_block(self, block):
        self.print('Block')
        for statement in block.statements:
            self.visit(statement)

    def visit_literal(self, literal):
        self.print('Literal', repr(literal.value))

    def visit_if(self, _if):
        self.print('If')
        self.ident += 1
        self.print('#condition')
        self.visit(_if.condition)
        self.print('#then')
        self.visit(_if.then_body)
        for (cond, block) in _if.elsif_parts:
            self.print('#elsif_condition')
            self.visit(cond)
            self.print('#elsif_then')
            self.visit(block)
        if _if.else_body is not None:
            self.print('#else')
            self.visit(_if.else_body)
        self.ident -= 1

    def visit_while(self, _while):
        self.print('While')
        self.ident += 1
        self.print('#condition')
        self.visit(_while.condition)
        self.print('#body')
        self.visit(_while.body)
        self.ident -= 1

    def visit_assign(self, assign):
        self.print('Assign')
        self.ident += 1
        self.print('#target')
        self.visit(assign.target)
        self.print('#value')
        self.visit(assign.value)
        self.ident -= 1

    def visit_var(self, var):
        self.print('Var', var.name)

    def visit_call(self, call):
        self.print('Call')
        self.ident += 1
        self.print('#func')
        self.visit(call.func)
        self.print('#args')
        for arg in call.args:
            self.visit(arg)

    def visit_binary_op(self, binary_op):
        self.print('BinaryOp', binary_op.op)
        self.ident += 1
        self.print('#left')
        self.visit(binary_op.left)
        self.print('#right')
        self.visit(binary_op.right)
        self.ident -= 1

    def visit_array(self, array):
        self.print('Array')
        for elem in array.elements:
            self.visit(elem)

    def visit_unary_op(self, unary_op):
        self.print('UnaryOp', unary_op.op)
        self.visit(unary_op.expr)

    def visit_return(self, _return):
        self.print('Return')
        if _return.value is not None:
            self.visit(_return.value)

    def visit_expr_stmt(self, expr_stmt):
        self.print('ExprStmt')
        self.visit(expr_stmt.expr)

@dataclass
class Label:
    target: int | None


class ASTCompiler:
    def __init__(self):
        self.labels = []
        self.instructions = []

    def new_label(self):
        result = Label(None)
        self.labels.append(result)
        return result

    def resolve(self, label):
        assert label.target is None, "Cannot resolve an already resolved label"
        label.target = len(self.instructions)

    def do(self, *args):
        self.instructions.append(tuple(args))

    def visit(self, node):
        node.accept(self)

    def visit_let(self, let):
        if let.value is not None:
            self.visit(let.value)
        else:
            self.do('PUSH', None)
        self.do('DEFINE', let.name)

    def visit_lambda(self, _lambda):
        lambda_visitor = ASTCompiler()
        for param in reversed(_lambda.params):
            lambda_visitor.do('DEFINE', param)
        lambda_visitor.visit(_lambda.body)
        lambda_visitor.do('PUSH', None)
        lambda_visitor.do('RETURN')

        # HACK
        from machine import VMFunc

        self.do('PUSH', VMFunc(lambda_visitor.instructions))

    def visit_block(self, block):
        for statement in block.statements:
            self.visit(statement)

    def visit_literal(self, literal):
        self.do('PUSH', literal.value)

    def visit_if(self, _if):
        after_if = self.new_label()
        self.visit(_if.condition)

        condition_failed = self.new_label()
        self.do('JMP_IF_FALSE', condition_failed)
        self.visit(_if.then_body)
        self.do('JMP', after_if)

        for (cond, block) in _if.elsif_parts:
            self.resolve(condition_failed)
            self.visit(cond)

            condition_failed = self.new_label()
            self.do('JMP_IF_FALSE', condition_failed)
            self.visit(block)
            self.do('JMP', after_if)

        self.resolve(condition_failed)
        if _if.else_body is not None:
            self.visit(_if.else_body)
        self.resolve(after_if)

    def visit_while(self, _while):
        after_loop = self.new_label()
        guard = self.new_label()
        self.resolve(guard)
        self.visit(_while.condition)
        self.do('JMP_IF_FALSE', after_loop)
        self.visit(_while.body)
        self.do('JMP', guard)
        self.resolve(after_loop)

    def visit_assign(self, assign):
        self.visit(assign.value)
        self.do('ASSIGN', assign.target.name)

    def visit_var(self, var):
        self.do('LOAD', var.name)

    def visit_call(self, call):
        self.visit(call.func)
        for arg in call.args:
            self.visit(arg)
        self.do('CALL', len(call.args))

    def visit_binary_op(self, binary_op):
        if binary_op.op == 'or':
            after_right = self.new_label()
            self.visit(binary_op.left)
            self.do('DUP')
            self.do('JMP_IF_TRUE', after_right)
            self.do('DROP')
            self.visit(binary_op.right)
            self.resolve(after_right)
        elif binary_op.op == 'and':
            after_right = self.new_label()
            self.visit(binary_op.left)
            self.do('DUP')
            self.do('JMP_IF_FALSE', after_right)
            self.do('DROP')
            self.visit(binary_op.right)
            self.resolve(after_right)
        else:
            self.visit(binary_op.left)
            self.visit(binary_op.right)
            #FIXME
            self.do('BINOP', binary_op.op)

    def visit_array(self, array):
        for elem in array.elements:
            self.visit(elem)
        self.do('CREATE_ARRAY', len(array.elements))

    def visit_unary_op(self, unary_op):
        self.visit(unary_op.expr)
        #FIXME
        self.do('UNOP', unary_op.op)

    def visit_return(self, _return):
        if _return.value is not None:
            self.visit(_return.value)
        else:
            self.do('PUSH', None)
        self.do('RETURN')

    def visit_expr_stmt(self, expr_stmt):
        self.visit(expr_stmt.expr)
        self.do('DROP')