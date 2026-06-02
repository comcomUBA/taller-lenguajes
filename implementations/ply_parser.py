from __future__ import annotations

from dataclasses import dataclass, fields, is_dataclass
import json
import sys
from typing import Any

import ply.yacc as yacc


# -----------------------------------------------------------------------------
# AST nodes
# -----------------------------------------------------------------------------


@dataclass
class Block:
    statements: list[Any]

    def accept(self, visitor):
        return visitor.visit_block(self)


@dataclass
class Let:
    name: str
    value: Any | None

    def accept(self, visitor):
        return visitor.visit_let(self)


@dataclass
class Return:
    value: Any | None

    def accept(self, visitor):
        return visitor.visit_return(self)


@dataclass
class ExprStmt:
    expr: Any

    def accept(self, visitor):
        return visitor.visit_expr_stmt(self)


@dataclass
class If:
    condition: Any
    then_body: Block
    elsif_parts: list[tuple[Any, Block]]
    else_body: Block | None

    def accept(self, visitor):
        return visitor.visit_if(self)


@dataclass
class While:
    condition: Any
    body: Block

    def accept(self, visitor):
        return visitor.visit_while(self)


@dataclass
class Assign:
    target: Any
    value: Any

    def accept(self, visitor):
        return visitor.visit_assign(self)


@dataclass
class Var:
    name: str

    def accept(self, visitor):
        return visitor.visit_var(self)


@dataclass
class Literal:
    value: Any

    def accept(self, visitor):
        return visitor.visit_literal(self)


@dataclass
class Array:
    elements: list[Any]

    def accept(self, visitor):
        return visitor.visit_array(self)


@dataclass
class Lambda:
    params: list[str]
    body: Block

    def accept(self, visitor):
        return visitor.visit_lambda(self)

@dataclass
class Call:
    func: Any
    args: list[Any]

    def accept(self, visitor):
        return visitor.visit_call(self)


@dataclass
class BinaryOp:
    op: str
    left: Any
    right: Any

    def accept(self, visitor):
        return visitor.visit_binary_op(self)

@dataclass
class UnaryOp:
    op: str
    expr: Any

    def accept(self, visitor):
        return visitor.visit_unary_op(self)


# -----------------------------------------------------------------------------
# Hand-written lexer with the PLY-compatible interface yacc needs.
# -----------------------------------------------------------------------------


@dataclass
class LexToken:
    type: str
    value: Any
    lineno: int
    lexpos: int


reserved = {
    "let": "LET",
    "if": "IF",
    "else": "ELSE",
    "elsif": "ELSIF",
    "while": "WHILE",
    "return": "RETURN",
    "true": "TRUE",
    "false": "FALSE",
    "nil": "NIL",
    "not": "NOT",
    "or": "OR",
    "and": "AND",
}


tokens = (
    "ID",
    "NUMBER",
    "STRING",
    "SEMI",
    "COMMA",
    "LPAREN",
    "RPAREN",
    "LBRACE",
    "RBRACE",
    "LBRACKET",
    "RBRACKET",
    "BAR",
    "PLUS",
    "MINUS",
    "TIMES",
    "DIVIDE",
    "MOD",
    "ASSIGN",
    "EQ",
    "NE",
    "LT",
    "LE",
    "GT",
    "GE",
    "ANDAND",
    "OROR",
    *reserved.values(),
)


class LexerError(SyntaxError):
    pass


class TLLexer:
    def input(self, text: str) -> None:
        self.text = text
        self.pos = 0
        self.lineno = 1

    def token(self) -> LexToken | None:
        text = self.text
        n = len(text)

        while self.pos < n:
            ch = text[self.pos]

            if ch in " \t\r":
                self.pos += 1
                continue

            if ch == "\n":
                self.lineno += 1
                self.pos += 1
                continue

            if ch == "#":
                while self.pos < n and text[self.pos] != "\n":
                    self.pos += 1
                continue

            break

        if self.pos >= n:
            return None

        start = self.pos
        ch = text[self.pos]

        two_char = {
            "==": "EQ",
            "!=": "NE",
            "<=": "LE",
            ">=": "GE",
            "&&": "ANDAND",
            "||": "OROR",
        }
        raw2 = text[self.pos : self.pos + 2]
        if raw2 in two_char:
            self.pos += 2
            return LexToken(two_char[raw2], raw2, self.lineno, start)

        one_char = {
            ";": "SEMI",
            ",": "COMMA",
            "(": "LPAREN",
            ")": "RPAREN",
            "{": "LBRACE",
            "}": "RBRACE",
            "[": "LBRACKET",
            "]": "RBRACKET",
            "|": "BAR",
            "+": "PLUS",
            "-": "MINUS",
            "*": "TIMES",
            "/": "DIVIDE",
            "%": "MOD",
            "=": "ASSIGN",
            "<": "LT",
            ">": "GT",
        }
        if ch in one_char:
            self.pos += 1
            return LexToken(one_char[ch], ch, self.lineno, start)

        if ch == '"':
            return self._read_string()

        if ch.isdigit():
            return self._read_number()

        if ch.isalpha() or ch == "_":
            return self._read_identifier()

        raise LexerError(f"Unexpected character {ch!r} at line {self.lineno}, position {self.pos}")

    def _read_identifier(self) -> LexToken:
        start = self.pos
        text = self.text

        while self.pos < len(text) and (text[self.pos].isalnum() or text[self.pos] == "_"):
            self.pos += 1

        raw = text[start : self.pos]
        typ = reserved.get(raw, "ID")

        if typ == "TRUE":
            value: Any = True
        elif typ == "FALSE":
            value = False
        elif typ == "NIL":
            value = None
        else:
            value = raw

        return LexToken(typ, value, self.lineno, start)

    def _read_number(self) -> LexToken:
        start = self.pos
        text = self.text

        while self.pos < len(text) and text[self.pos].isdigit():
            self.pos += 1

        is_float = False
        if self.pos < len(text) and text[self.pos] == ".":
            if self.pos + 1 < len(text) and text[self.pos + 1].isdigit():
                is_float = True
                self.pos += 1
                while self.pos < len(text) and text[self.pos].isdigit():
                    self.pos += 1

        raw = text[start : self.pos]
        return LexToken("NUMBER", float(raw) if is_float else int(raw), self.lineno, start)

    def _read_string(self) -> LexToken:
        start = self.pos
        self.pos += 1
        out: list[str] = []
        text = self.text

        escapes = {
            "n": "\n",
            "r": "\r",
            "t": "\t",
            '"': '"',
            "\\": "\\",
        }

        while self.pos < len(text):
            ch = text[self.pos]

            if ch == '"':
                self.pos += 1
                return LexToken("STRING", "".join(out), self.lineno, start)

            if ch == "\\":
                self.pos += 1
                if self.pos >= len(text):
                    raise LexerError(f"Unterminated escape at line {self.lineno}")
                esc = text[self.pos]
                out.append(escapes.get(esc, esc))
                self.pos += 1
                continue

            if ch == "\n":
                raise LexerError(f"Unterminated string at line {self.lineno}")

            out.append(ch)
            self.pos += 1

        raise LexerError(f"Unterminated string at line {self.lineno}")


# -----------------------------------------------------------------------------
# PLY yacc grammar
# -----------------------------------------------------------------------------


start = "stmt_list_opt"


def p_stmt_list_opt(p):
    """stmt_list_opt : stmt_list
                     | empty"""
    p[0] = p[1] or []


def p_stmt_list_single(p):
    """stmt_list : statement"""
    p[0] = [p[1]]


def p_stmt_list_many(p):
    """stmt_list : stmt_list statement"""
    p[0] = p[1] + [p[2]]


# The semicolon rule is enforced here: only block statements can omit ';'.


def p_statement_simple(p):
    """statement : simple_stmt SEMI"""
    p[0] = p[1]


def p_statement_block(p):
    """statement : if_stmt
                 | while_stmt"""
    p[0] = p[1]


def p_simple_stmt_let(p):
    """simple_stmt : LET ID
                   | LET ID ASSIGN expression"""
    p[0] = Let(p[2], p[4] if len(p) == 5 else None)


def p_simple_stmt_return(p):
    """simple_stmt : RETURN
                   | RETURN expression"""
    p[0] = Return(p[2] if len(p) == 3 else None)


def p_simple_stmt_expr(p):
    """simple_stmt : expression"""
    p[0] = ExprStmt(p[1])


def p_block(p):
    """block : LBRACE stmt_list_opt RBRACE"""
    p[0] = Block(p[2])


def p_while_stmt(p):
    """while_stmt : WHILE expression block"""
    p[0] = While(p[2], p[3])


def p_if_stmt(p):
    """if_stmt : IF expression block elsif_parts else_part"""
    p[0] = If(p[2], p[3], p[4], p[5])


def p_elsif_parts_empty(p):
    """elsif_parts : empty"""
    p[0] = []


def p_elsif_parts_many(p):
    """elsif_parts : elsif_parts ELSIF expression block"""
    p[0] = p[1] + [(p[3], p[4])]


def p_else_part_empty(p):
    """else_part : empty"""
    p[0] = None


def p_else_part_block(p):
    """else_part : ELSE block"""
    p[0] = p[2]


# Expressions, from lowest to highest precedence.


def p_expression(p):
    """expression : assignment"""
    p[0] = p[1]


def p_assignment_plain(p):
    """assignment : logic_or"""
    p[0] = p[1]


def p_assignment_assign(p):
    """assignment : lvalue ASSIGN assignment"""
    p[0] = Assign(p[1], p[3])


def p_lvalue_var(p):
    """lvalue : ID"""
    p[0] = Var(p[1])


def p_logic_or_plain(p):
    """logic_or : logic_and"""
    p[0] = p[1]


def p_logic_or_binary(p):
    """logic_or : logic_or OR logic_and
                | logic_or OROR logic_and"""
    p[0] = BinaryOp(p[2], p[1], p[3])


def p_logic_and_plain(p):
    """logic_and : equality"""
    p[0] = p[1]


def p_logic_and_binary(p):
    """logic_and : logic_and AND equality
                 | logic_and ANDAND equality"""
    p[0] = BinaryOp(p[2], p[1], p[3])


def p_equality_plain(p):
    """equality : comparison"""
    p[0] = p[1]


def p_equality_binary(p):
    """equality : equality EQ comparison
                | equality NE comparison"""
    p[0] = BinaryOp(p[2], p[1], p[3])


def p_comparison_plain(p):
    """comparison : term"""
    p[0] = p[1]


def p_comparison_binary(p):
    """comparison : comparison LT term
                  | comparison LE term
                  | comparison GT term
                  | comparison GE term"""
    p[0] = BinaryOp(p[2], p[1], p[3])


def p_term_plain(p):
    """term : factor"""
    p[0] = p[1]


def p_term_binary(p):
    """term : term PLUS factor
            | term MINUS factor"""
    p[0] = BinaryOp(p[2], p[1], p[3])


def p_factor_plain(p):
    """factor : unary"""
    p[0] = p[1]


def p_factor_binary(p):
    """factor : factor TIMES unary
              | factor DIVIDE unary
              | factor MOD unary"""
    p[0] = BinaryOp(p[2], p[1], p[3])


def p_unary_plain(p):
    """unary : postfix"""
    p[0] = p[1]


def p_unary_op(p):
    """unary : NOT unary
             | MINUS unary"""
    p[0] = UnaryOp(p[1], p[2])


def p_postfix_plain(p):
    """postfix : primary"""
    p[0] = p[1]


def p_postfix_call(p):
    """postfix : postfix LPAREN arg_list_opt RPAREN"""
    p[0] = Call(p[1], p[3])


def p_primary_id(p):
    """primary : ID"""
    p[0] = Var(p[1])


def p_primary_literal(p):
    """primary : NUMBER
               | STRING
               | TRUE
               | FALSE
               | NIL"""
    p[0] = Literal(p[1])


def p_primary_group(p):
    """primary : LPAREN expression RPAREN"""
    p[0] = p[2]


def p_primary_array(p):
    """primary : array"""
    p[0] = p[1]


def p_primary_lambda(p):
    """primary : lambda_literal"""
    p[0] = p[1]


def p_array(p):
    """array : LBRACKET arg_list_opt RBRACKET"""
    p[0] = Array(p[2])


def p_lambda_literal(p):
    """lambda_literal : BAR params_opt BAR block"""
    p[0] = Lambda(p[2], p[4])


def p_params_opt(p):
    """params_opt : param_list
                  | empty"""
    p[0] = p[1] or []


def p_param_list_single(p):
    """param_list : ID"""
    p[0] = [p[1]]


def p_param_list_many(p):
    """param_list : param_list COMMA ID"""
    p[0] = p[1] + [p[3]]


def p_arg_list_opt(p):
    """arg_list_opt : arg_list
                    | empty"""
    p[0] = p[1] or []


def p_arg_list_single(p):
    """arg_list : expression"""
    p[0] = [p[1]]


def p_arg_list_many(p):
    """arg_list : arg_list COMMA expression"""
    p[0] = p[1] + [p[3]]


def p_empty(p):
    """empty :"""
    p[0] = None


def p_error(p):
    if p is None:
        raise SyntaxError("Unexpected end of input. A statement may be missing a trailing ';'.")

    raise SyntaxError(
        f"Unexpected token {p.type}({p.value!r}) at line {getattr(p, 'lineno', '?')}, "
        f"position {getattr(p, 'lexpos', '?')}. "
        "Simple statements must end with ';'; only if/while blocks ending in '}' omit it."
    )


parser = yacc.yacc(debug=False, write_tables=False)


def parse(source: str) -> list[Any]:
    lexer = TLLexer()
    return parser.parse(source, lexer=lexer)


def parse_file(path: str) -> list[Any]:
    with open(path, "r", encoding="utf-8") as f:
        return parse(f.read())


def ast_to_data(node: Any) -> Any:
    if is_dataclass(node):
        return {
            "node": type(node).__name__,
            **{field.name: ast_to_data(getattr(node, field.name)) for field in fields(node)},
        }
    if isinstance(node, tuple):
        return [ast_to_data(x) for x in node]
    if isinstance(node, list):
        return [ast_to_data(x) for x in node]
    return node


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


@dataclass
class Frame:
    instructions: list[Any]
    pc: int
    parent: Frame
    local_scope: dict[str, Any]
    stack: list[Any]

    def push(self, value):
        self.stack.append(value)

    def pop(self):
        return self.stack.pop()

    def __repr__(self):
        return f'Frame(id={id(self)}, instructions={id(self.instructions)}, pc={self.pc!r}, parent={self.parent!r}, local_scope={self.local_scope!r}, stack={self.stack!r})'

@dataclass
class VMFunc:
    instructions: list[Any]

    def __repr__(self):
        return f'VMFunc(instructions={id(self.instructions)!r})'

    def print_bytecode(self):
        visited = set()
        queue = [self]
        while queue:
            func = queue.pop()
            if id(func) in visited:
                continue
            visited.add(id(func))

            print(f'{func}:')
            for i, (instr, *args) in enumerate(func.instructions):
                instr_args = ', '.join(repr(arg) for arg in args)
                print(f'{i:3} {instr} {instr_args}')

                for arg in args:
                    if isinstance(arg, VMFunc):
                        queue.append(arg)


@dataclass
class Print:
    def invoke(self, vm, *args):
        print(*args)
        vm.frame.push(None)


@dataclass
class IsEmpty:
    def invoke(self, vm, arr):
        vm.frame.push(len(arr) == 0)


@dataclass
class Pop:
    def invoke(self, vm, arr):
        vm.frame.push(arr.pop())


@dataclass
class Contains:
    def invoke(self, vm, arr, value):
        vm.frame.push(value in arr)


@dataclass
class Push:
    def invoke(self, vm, arr, value):
        arr.append(value)
        vm.frame.push(arr)


@dataclass
class Concat:
    def invoke(self, vm, arr, another_arr):
        arr.extend(another_arr)
        vm.frame.push(arr)


@dataclass
class Get:
    def invoke(self, vm, arr, idx):
        vm.frame.push(arr[idx])


@dataclass
class Set:
    def invoke(self, vm, arr, idx, value):
        arr[idx] = value
        vm.frame.push(value)


@dataclass
class ListOf:
    def invoke(self, vm, size):
        vm.frame.push([0] * size)


@dataclass
class Size:
    def invoke(self, vm, arr):
        vm.frame.push(len(arr))


@dataclass
class CoStart:
    yield_or_resume_to: Frame | CoStart | None
    running: bool

    def __repr__(self):
        if self.running:
            return f'CoStart(id={id(self)}, yield_to={id(self.yield_or_resume_to)})'
        else:
            return f'CoStart(id={id(self)}, resume_to={id(self.yield_or_resume_to)})'


@dataclass
class Start:
    def invoke(self, vm, func, args):
        assert isinstance(func, VMFunc), "start() only works for VM functions"
        co_start = CoStart(func, False)

        co_program = [
            ('DROP',),
            ('CALL', len(args)),
            ('CALL', 1)
        ]
        co_start.yield_or_resume_to = Frame(co_program, 0, co_start, {}, [Yield(), func, *args])
        vm.frame.push(co_start)


@dataclass
class Yield:
    def invoke(self, vm, value):
        co_frame = vm.frame
        while not isinstance(co_frame, CoStart) and co_frame is not None:
            co_frame = co_frame.parent

        assert co_frame is not None, "yield() could not find a running coroutine"
        assert co_frame.running, "yield() only works for running coroutines"

        yield_to = co_frame.yield_or_resume_to
        resume_to = vm.frame
        co_frame.yield_or_resume_to = resume_to
        co_frame.running = False

        vm.frame = yield_to
        vm.frame.push(value)


@dataclass
class Resume:
    def invoke(self, vm, co_frame, value):
        assert isinstance(co_frame, CoStart), "resume() only works for coroutines"
        assert not co_frame.running, "Cannot resume running coroutine"

        yield_to = vm.frame
        resume_to = co_frame.yield_or_resume_to

        assert resume_to.pc == 0 or resume_to.parent is not co_frame, "Cannot resume finished coroutine"

        co_frame.yield_or_resume_to = yield_to
        co_frame.running = True

        vm.frame = resume_to
        vm.frame.push(value)
        return value


class VM:
    def __init__(self, vm_func):
        self.global_scope = {
            'print': Print(),
            'is_empty': IsEmpty(),
            'pop': Pop(),
            'contains': Contains(),
            'push': Push(),
            'concat': Concat(),
            'get': Get(),
            'set': Set(),
            'list_of': ListOf(),
            'size': Size(),
            'start': Start(),
            'yield': Yield(),
            'resume': Resume(),
        }
        self.frame = Frame(vm_func.instructions, 0, None, self.global_scope, [])

    def run(self):
        while True:
            if self.frame.pc < 0 or len(self.frame.instructions) <= self.frame.pc:
                break

            ins = self.frame.instructions[self.frame.pc]
            self.frame.pc += 1

            #print(ins[0], self.frame)
            match ins:
                case ('JMP', Label(target=target)):
                    self.frame.pc = target
                case ('DEFINE', var_name):
                    value = self.frame.pop()
                    self.frame.local_scope[var_name] = value
                case ('LOAD', var_name):
                    if var_name in self.frame.local_scope:
                        value = self.frame.local_scope[var_name]
                    else:
                        value = self.global_scope[var_name]
                    self.frame.push(value)
                case ('PUSH', value):
                    self.frame.push(value)
                case ('CREATE_ARRAY', num_elems):
                    value = []
                    for i in range(num_elems):
                        value.insert(0, self.frame.pop())
                    self.frame.push(value)
                case ('CALL', num_args):
                    args = []
                    for i in range(num_args):
                        args.insert(0, self.frame.pop())
                    func = self.frame.pop()

                    if isinstance(func, VMFunc):
                        self.frame = Frame(func.instructions, 0, self.frame, {}, args)
                    else:
                        func.invoke(self, *args)
                case ('UNOP', 'not'):
                    self.frame.push(not self.frame.pop())
                case ('UNOP', '-'):
                    self.frame.push(-self.frame.pop())
                case ('JMP_IF_FALSE', Label(target=target)):
                    if self.frame.pop() == False:
                        self.frame.pc = target
                case ('JMP_IF_TRUE', Label(target=target)):
                    if self.frame.pop() == True:
                        self.frame.pc = target
                case ('DROP',):
                    self.frame.pop()
                case ('RETURN',):
                    result = self.frame.pop()
                    self.frame = self.frame.parent
                    self.frame.push(result)
                case ('BINOP', '>'):
                    rhs = self.frame.pop()
                    lhs = self.frame.pop()
                    self.frame.push(lhs > rhs)
                case ('BINOP', '<'):
                    rhs = self.frame.pop()
                    lhs = self.frame.pop()
                    self.frame.push(lhs < rhs)
                case ('BINOP', '+'):
                    rhs = self.frame.pop()
                    lhs = self.frame.pop()
                    self.frame.push(lhs + rhs)
                case ('BINOP', '-'):
                    rhs = self.frame.pop()
                    lhs = self.frame.pop()
                    self.frame.push(lhs - rhs)
                case ('BINOP', '=='):
                    rhs = self.frame.pop()
                    lhs = self.frame.pop()
                    self.frame.push(lhs == rhs)
                case ('BINOP', '%'):
                    rhs = self.frame.pop()
                    lhs = self.frame.pop()
                    self.frame.push(lhs % rhs)
                case ('ASSIGN', var_name):
                    value = self.frame.pop()
                    if var_name in self.frame.local_scope:
                        self.frame.local_scope[var_name] = value
                    elif var_name in self.global_scope:
                        self.global_scope[var_name] = value
                    else:
                        print("UNDEFINED", var_name)
                        break
                    self.frame.push(value)
                case ('DUP',):
                    value = self.frame.pop()
                    self.frame.push(value)
                    self.frame.push(value)
                case _:
                    print('UNKNOWN', ins)
                    break


def main(argv: list[str]) -> int:
    if not argv:
        print("Usage: python tl_ply_parser.py FILE.tl [FILE.tl ...]", file=sys.stderr)
        return 2

    ok = True
    for filename in argv:
        print(f"== {filename} ==")
        try:
            tree = parse_file(filename)
        except Exception as exc:
            ok = False
            print(f"Syntax error: {exc}", file=sys.stderr)
            continue
        print(f"== {filename}: JSON ==")
        print(json.dumps(ast_to_data(tree), indent=2, ensure_ascii=False))

        print(f"== {filename}: AST ==")
        visitor = ASTPrinter()
        for statement in tree:
            statement.accept(visitor)

        visitor = ASTCompiler()
        for statement in tree:
            statement.accept(visitor)
        module_code = VMFunc(visitor.instructions)

        print(f"== {filename}: Bytecode ==")
        module_code.print_bytecode()

        print(f"== {filename}: Execution ==")
        VM(module_code).run()

    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
