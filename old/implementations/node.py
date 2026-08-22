from dataclasses import dataclass, fields, is_dataclass

#================================================================

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