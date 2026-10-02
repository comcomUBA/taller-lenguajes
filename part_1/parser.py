from common import *

#================================================================

from pprint import pprint

#================================================================

def parser(t_b: TokenBuffer) -> [any]:
    construct_list = []

    for t in t_b.token:
        match t.kind:
            case TokenKind.PROCEDURE:
                value = Procedure(t_b)
                pprint(value, width=40)
            case TokenKind.PREDICATE:
                value = Predicate(t_b)
                pprint(value, width=40)
            case TokenKind.AUXILIARY:
                value = Auxiliary(t_b)
                pprint(value, width=40)
            case TokenKind.ADT:
                value = ADT(t_b)
                pprint(value, width=40)

    return construct_list

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
                raise ValueError("expected in/inOut, got: " + str(t_b.peek()))

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

@dataclass
class Procedure:
    name           : Token
    parameter_list : [Parameter]
    return_type    : Token
    expression_r   : [Token]
    expression_a   : [Token]

    def __init__(self, t_b: TokenBuffer):
        # ... código a completar ...!
        ...

@dataclass
class Predicate:
    name           : Token
    parameter_list : [Parameter]
    expression     : [Token]

    def __init__(self, t_b: TokenBuffer):
        # ... código a completar ...!
        ...

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

        identifier = t_b.want(TokenKind.IDENTIFIER)

        t_b.want(TokenKind.CURLY_BEGIN)

        while t_b.want_peek(TokenKind.CURLY_CLOSE) == None:
            self.parameter_list.append(Parameter(False))

            if t_b.want_peek(TokenKind.COMMA) != None:
                t_b.want(TokenKind.COMMA)

        t_b.want(TokenKind.CURLY_CLOSE)

        t_b.want(TokenKind.COLON)

        self.return_type = t_b.want(TokenKind.IDENTIFIER)

        t_b.want(TokenKind.BRACKET_BEGIN)

        while t_b.want_peek(TokenKind.BRACKET_CLOSE) == None:
            self.expression.append(pop(list_token))

        t_b.want(TokenKind.BRACKET_CLOSE)

@dataclass
class ADT:
    name           : Token
    observer_list  : [Parameter]
    procedure_list : [Procedure]
    predicate_list : [Predicate]
    auxiliary_list : [Auxiliary]

    def __init__(self, t_b: TokenBuffer):
        # ... código a completar ...!
        ...