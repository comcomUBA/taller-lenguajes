from common import *

#================================================================

from pprint import pprint

#================================================================

@dataclass
class Observer:
    name      : Token
    type      : Token

    def __init__(self, t_b: TokenBuffer):
        # ... código a completar ...!

        t_b.want(TokenKind.OBSERVER)

        self.name = t_b.want(TokenKind.IDENTIFIER)
        t_b.want(TokenKind.COLON)
        self.type = t_b.want(TokenKind.IDENTIFIER)

    def __repr__(self):
        return f"Observer({self.name} : {self.type})"

@dataclass
class Parameter:
    reference : bool
    name      : Token
    type      : Token

    def __init__(self, t_b: TokenBuffer, can_reference: bool):
        # ... código a completar ...!

        if can_reference:
            reference_in     = t_b.want_peek(TokenKind.IN)
            reference_in_out = t_b.want_peek(TokenKind.IN_OUT)

            if reference_in == None and reference_in_out == None:
                raise ValueError(f"Esperaba in/inOut, pero recibí: {t_b.peek()}")

            if reference_in != None:
                t_b.want(TokenKind.IN)
                self.reference = False

            if reference_in_out != None:
                t_b.want(TokenKind.IN_OUT)
                self.reference = True
        else:
            self.reference = False

        self.name = t_b.want(TokenKind.IDENTIFIER)
        t_b.want(TokenKind.COLON)
        self.type = t_b.want(TokenKind.IDENTIFIER)

    def __repr__(self):
        reference = "inOut" if self.reference else "in"

        return f"Parameter({reference} {self.name} : {self.type})"

@dataclass
class Procedure:
    name           : Token
    parameter_list : [Parameter]
    return_type    : Token
    expression_r   : [Token]
    expression_a   : [Token]

    def __init__(self, t_b: TokenBuffer):
        # ... código a completar ...!

        self.return_type    = None
        self.parameter_list = []
        self.expression_r   = []
        self.expression_a   = []

        t_b.want(TokenKind.PROCEDURE)

        self.name = t_b.want(TokenKind.IDENTIFIER)

        t_b.want(TokenKind.ROUND_BEGIN)

        while t_b.want_peek(TokenKind.ROUND_CLOSE) == None:
            self.parameter_list.append(Parameter(t_b, True))

            if t_b.want_peek(TokenKind.COMMA) != None:
                t_b.want(TokenKind.COMMA)

        t_b.want(TokenKind.ROUND_CLOSE)

        if t_b.want_peek(TokenKind.COLON):
            t_b.want(TokenKind.COLON)

            self.return_type = t_b.want(TokenKind.IDENTIFIER)

        t_b.want(TokenKind.BRACKET_BEGIN)

        #==== requiere ================

        t_b.want(TokenKind.REQUIRE)

        t_b.want(TokenKind.BRACKET_BEGIN)

        while t_b.want_peek(TokenKind.BRACKET_CLOSE) == None:
            self.expression_r.append(t_b.pop())

        t_b.want(TokenKind.BRACKET_CLOSE)

        #==== asegura =================

        t_b.want(TokenKind.ASSURE)

        t_b.want(TokenKind.BRACKET_BEGIN)

        while t_b.want_peek(TokenKind.BRACKET_CLOSE) == None:
            self.expression_a.append(t_b.pop())

        t_b.want(TokenKind.BRACKET_CLOSE)

        #==============================

        t_b.want(TokenKind.BRACKET_CLOSE)

@dataclass
class Predicate:
    name           : Token
    parameter_list : [Parameter]
    expression     : [Token]

    def __init__(self, t_b: TokenBuffer):
        # ... código a completar ...!

        self.parameter_list = []
        self.expression     = []

        t_b.want(TokenKind.PREDICATE)

        self.name = t_b.want(TokenKind.IDENTIFIER)

        t_b.want(TokenKind.ROUND_BEGIN)

        while t_b.want_peek(TokenKind.ROUND_CLOSE) == None:
            self.parameter_list.append(Parameter(t_b, False))

            if t_b.want_peek(TokenKind.COMMA) != None:
                t_b.want(TokenKind.COMMA)

        t_b.want(TokenKind.ROUND_CLOSE)

        t_b.want(TokenKind.BRACKET_BEGIN)

        while t_b.want_peek(TokenKind.BRACKET_CLOSE) == None:
            self.expression.append(t_b.pop())

        t_b.want(TokenKind.BRACKET_CLOSE)

@dataclass
class Auxiliary:
    name           : Token
    parameter_list : [Parameter]
    return_type    : Token
    expression     : [Token]

    def __init__(self, t_b: TokenBuffer):
        # ... código a completar ...!

        self.parameter_list = []
        self.expression     = []

        t_b.want(TokenKind.AUXILIARY)

        self.name = t_b.want(TokenKind.IDENTIFIER)

        t_b.want(TokenKind.ROUND_BEGIN)

        while t_b.want_peek(TokenKind.ROUND_CLOSE) == None:
            self.parameter_list.append(Parameter(t_b, False))

            if t_b.want_peek(TokenKind.COMMA) != None:
                t_b.want(TokenKind.COMMA)

        t_b.want(TokenKind.ROUND_CLOSE)

        t_b.want(TokenKind.COLON)

        self.return_type = t_b.want(TokenKind.IDENTIFIER)

        t_b.want(TokenKind.BRACKET_BEGIN)

        while t_b.want_peek(TokenKind.BRACKET_CLOSE) == None:
            self.expression.append(t_b.pop())

        t_b.want(TokenKind.BRACKET_CLOSE)

@dataclass
class ADT:
    name           : Token
    observer_list  : [Observer]
    procedure_list : [Procedure]
    predicate_list : [Predicate]
    auxiliary_list : [Auxiliary]

    def __init__(self, t_b: TokenBuffer):
        # ... código a completar ...!

        self.observer_list = []
        self.procedure_list = []
        self.predicate_list = []
        self.auxiliary_list = []

        t_b.want(TokenKind.ADT)

        self.name = t_b.want(TokenKind.IDENTIFIER)

        t_b.want(TokenKind.BRACKET_BEGIN)

        while t_b.want_peek(TokenKind.BRACKET_CLOSE) == None:
            match t_b.peek().kind:
                case TokenKind.OBSERVER:
                    self.observer_list.append(Observer(t_b))
                case TokenKind.PROCEDURE:
                    self.procedure_list.append(Procedure(t_b))
                case TokenKind.PREDICATE:
                    self.predicate_list.append(Predicate(t_b))
                case TokenKind.AUXILIARY:
                    self.auxiliary_list.append(Auxiliary(t_b))

        t_b.want(TokenKind.BRACKET_CLOSE)

def parser(t_b: TokenBuffer) -> Procedure | Predicate | Auxiliary | ADT:
    value = None

    match t_b.peek().kind:
        case TokenKind.PROCEDURE:
            value = Procedure(t_b)
        case TokenKind.PREDICATE:
            value = Predicate(t_b)
        case TokenKind.AUXILIARY:
            value = Auxiliary(t_b)
        case TokenKind.ADT:
            value = ADT(t_b)

    pprint(value, width=40)

    return value