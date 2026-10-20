from common import *
from lexer import lexer

#================================================================

from textwrap import indent
import unittest

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

    # Función de uso interno.
    def __repr__(self):
        return f"Observer({self.name} : {self.type})"

    # Función de uso interno.
    @classmethod
    def __build__(self, name, type):
        this = self.__new__(self)
        this.name      = name
        this.type      = type
        return this

    # Función de uso interno.
    def __buildstr__(self):
        return f"Observer.__build__({self.name.__buildstr__()}, {self.type.__buildstr__()})"

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

    # Función de uso interno.
    def __repr__(self):
        reference = "inOut" if self.reference else "in"

        return f"Parameter({reference} {self.name} : {self.type})"

    # Función de uso interno.
    @classmethod
    def __build__(self, reference, name, type):
        this = self.__new__(self)
        this.reference = reference
        this.name      = name
        this.type      = type
        return this

    # Función de uso interno.
    def __buildstr__(self):
        return f"Parameter.__build__({self.reference}, {self.name.__buildstr__()}, {self.type.__buildstr__()})"

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

    # Función de uso interno.
    @classmethod
    def __build__(self, name, p_l, return_type, e_r, e_a):
        this = self.__new__(self)
        this.name           = name
        this.parameter_list = p_l
        this.return_type    = return_type
        this.expression_r   = e_r
        this.expression_a   = e_a
        return this

    # Función de uso interno.
    def __buildstr__(self):
        buffer = "Procedure.__build__(\n"

        buffer += f"  {self.name.__buildstr__()},\n"

        #================

        buffer += "  [\n"

        for p in self.parameter_list:
            buffer += f"    {p.__buildstr__()},\n"

        buffer += "  ],\n"

        #================

        buffer += f"  {self.return_type.__buildstr__()},\n"

        #================

        buffer += "  [\n"

        for p in self.expression_r:
            buffer += f"    {p.__buildstr__()},\n"

        buffer += "  ],\n"

        #================

        buffer += "  [\n"

        for p in self.expression_a:
            buffer += f"    {p.__buildstr__()},\n"

        buffer += "  ],\n)"

        return buffer

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

    # Función de uso interno.
    @classmethod
    def __build__(self, name, p_l, e):
        this = self.__new__(self)
        this.name           = name
        this.parameter_list = p_l
        this.expression     = e
        return this

    # Función de uso interno.
    def __buildstr__(self):
        buffer = "Predicate.__build__(\n"

        buffer += f"  {self.name.__buildstr__()},\n"

        #================

        buffer += "  [\n"

        for p in self.parameter_list:
            buffer += f"    {p.__buildstr__()},\n"

        buffer += "  ],\n"

        #================

        buffer += "  [\n"

        for p in self.expression:
            buffer += f"    {p.__buildstr__()},\n"

        buffer += "  ],\n)"

        return buffer

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

    # Función de uso interno.
    @classmethod
    def __build__(self, name, p_l, r_t, e):
        this = self.__new__(self)
        this.name           = name
        this.parameter_list = p_l
        this.return_type    = r_t
        this.expression     = e
        return this

    # Función de uso interno.
    def __buildstr__(self):
        buffer = "Auxiliary.__build__(\n"

        buffer += f"  {self.name.__buildstr__()},\n"

        #================

        buffer += "  [\n"

        for p in self.parameter_list:
            buffer += f"    {p.__buildstr__()},\n"

        buffer += "  ],\n"

        #================

        buffer += f"  {self.return_type.__buildstr__()},\n"

        #================

        buffer += "  [\n"

        for p in self.expression:
            buffer += f"    {p.__buildstr__()},\n"

        buffer += "  ],\n)"

        return buffer

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

    # Función de uso interno.
    @classmethod
    def __build__(self, name, o_l, p_l, e_l, a_l):
        this = self.__new__(self)
        this.name           = name
        this.observer_list  = o_l
        this.procedure_list = p_l
        this.predicate_list = e_l
        this.auxiliary_list = a_l
        return this

    # Función de uso interno.
    def __buildstr__(self):
        buffer = "ADT.__build__(\n"

        buffer += f"  {self.name.__buildstr__()},\n"

        #================

        buffer += "  [\n"

        for o in self.observer_list:
            buffer += f"    {o.__buildstr__()},\n"

        buffer += "  ],\n"

        #================

        buffer += "  [\n"

        for p in self.procedure_list:
            buffer += indent(f"{p.__buildstr__()},\n", "    ")

        buffer += "  ],\n"

        #================

        buffer += "  [\n"

        for p in self.predicate_list:
            buffer += indent(f"{p.__buildstr__()},\n", "    ")

        buffer += "  ],\n"

        #================

        buffer += "  [\n"

        for a in self.auxiliary_list:
            buffer += indent(f"{a.__buildstr__()},\n", "    ")

        buffer += "  ],\n)"

        return buffer

class ExpressionKind(Enum):
    ATOM    = auto() # a
    INFIX   = auto() # a + b
    PREFIX  = auto() # -a
    POSTFIX = auto() # a[i]

@dataclass
class Expression:
    kind: ExpressionKind
    data: any

    @staticmethod
    def parse(token: TokenBuffer):
        return Expression.parse_recurse(token, 0)

    @staticmethod
    def parse_recurse(token: TokenBuffer, minimum_bind_power: int):
        ex_l = token.pop()

        # Caso: 1, 123, 67
        if Expression.is_atom(ex_l):
            ex_l = Expression(ExpressionKind.ATOM, ex_l.data)
        # Caso: -
        elif Expression.is_operator(ex_l):
            bp_r = Expression.prefix_bind_power(ex_l)
            ex_r = Expression.parse_recurse(token, bp_r)
            ex_l = Expression(ExpressionKind.PREFIX, (ex_l, ex_r))
        else:
            raise ValueError(f"{ex_l} no es un valor válido (pre-fix).")

        #================================

        while True:
            operator = token.peek()

            if operator != None:
                if not Expression.is_operator(operator):
                    raise ValueError(f"{operator} no es un operador válido (post-fix).")
            else:
                break

            #================================

            # Caso: !
            pf_bp = Expression.postfix_bind_power(operator)

            if pf_bp != None:
                if pf_bp < minimum_bind_power:
                    break

                token.pop()
                ex_l = Expression(ExpressionKind.POSTFIX, (operator, ex_l))
                continue

            #================================

            # Caso: +, -, *, /
            if_bp = Expression.infix_bind_power(operator)

            if if_bp != None:
                (bp_l, bp_r) = if_bp

                if bp_l < minimum_bind_power:
                    break

                token.pop()
                ex_r = Expression.parse_recurse(token, bp_r)
                ex_l = Expression(ExpressionKind.INFIX, (operator, ex_l, ex_r))
                continue

            break

        return ex_l

    @staticmethod
    def is_atom(token: Token) -> bool:
        """
        Devuelve verdadero si el token es un token atómico (es decir, no es un operador, si no un valor indivisible)
        """

        match token.kind:
            case TokenKind.IDENTIFIER | TokenKind.NUMBER:
                return True
            case x:
                return False

    @staticmethod
    def is_operator(token: Token) -> bool:
        """
        Devuelve verdadero si el token es un token asociado a un operador.
        """

        look_up = [
            TokenKind.ADD,
            TokenKind.SUBTRACT,
            TokenKind.MULTIPLY,
            TokenKind.DIVIDE,
            TokenKind.EXCLAMATION
        ]

        if token.kind in look_up:
            return True
        else:
            return False

    @staticmethod
    def prefix_bind_power(token: Token) -> int:
        """
        Devuelve el poder de ligamiento de der. de un token asociado a un operador prefijo.
        """

        match token.kind:
            case TokenKind.SUBTRACT:
                return 5
            case x:
                return ValueError(f"{token} no es un operador válido.")

    @staticmethod
    def postfix_bind_power(token: Token) -> int:
        """
        Devuelve el poder de ligamiento de der. de un token asociado a un operador prefijo.
        """

        match token.kind:
            case TokenKind.EXCLAMATION:
                return 6
            case x:
                return None

    @staticmethod
    def infix_bind_power(token: Token) -> (int, int):
        """
        Devuelve el poder de ligamiento de izq./der. de un token asociado a un operador infijo.
        """

        match token.kind:
            case TokenKind.ADD | TokenKind.SUBTRACT:
                return (1, 2)
            case TokenKind.MULTIPLY | TokenKind.DIVIDE:
                return (3, 4)
            case x:
                return None

    # Función de uso interno.
    def __repr__(self):
        if self.data == None:
            return f"{self.kind}"
        else:
            if isinstance(self.data, str):
                return f"{self.kind}('{self.data}')"
            else:
                return f"{self.kind}({self.data})"


    # Función de uso interno.
    @classmethod
    def __build__(self, kind, data):
        this = self.__new__(self)
        this.kind = kind
        this.data = data
        return this

    # Función de uso interno.
    def __buildstr__(self, i=0):
        step = "  "
        name = "Expression.__build__"

        if self.kind == ExpressionKind.ATOM:
            buffer = f"{self.data}"
        else:
            data = [child.__buildstr__() for child in self.data]
            buffer = "(\n" + "\n".join(indent(d, step) + "," for d in data) + "\n)"

        text = f"{name}(\n{indent(f'{self.kind},', step)}\n{indent(buffer, step)}\n)"
        return indent(text, " " * i)

def parser(t_b: TokenBuffer) -> Procedure | Predicate | Auxiliary | ADT | None:
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

    return value