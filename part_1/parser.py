from common import *
from lexer import lexer

#================================================================

from typing import Any
from textwrap import indent
import unittest

#================================================================

@dataclass
class Observer:
    name      : Token
    type      : Token

    def __init__(self, t_b: TokenBuffer):
        # ... código a completar ...!
        ...

    # Función de uso interno.
    def __repr__(self):
        return f"Observer({self.name} : {self.type})"

    # Función de uso interno.
    @classmethod
    def __build__(cls, name, type):
        this = cls.__new__(cls)
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
        ...

    # Función de uso interno.
    def __repr__(self):
        reference = "inOut" if self.reference else "in"

        return f"Parameter({reference} {self.name} : {self.type})"

    # Función de uso interno.
    @classmethod
    def __build__(cls, reference, name, type):
        this = cls.__new__(cls)
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
    parameter_list : list[Parameter]
    return_type    : Token
    expression_r   : list[Token]
    expression_a   : list[Token]

    def __init__(self, t_b: TokenBuffer):
        # ... código a completar ...!

        self.parameter_list = []
        self.expression_r   = []
        self.expression_a   = []

        # ... código a completar ...!
        ...

    # Función de uso interno.
    @classmethod
    def __build__(cls, name, p_l, return_type, e_r, e_a):
        this = cls.__new__(cls)
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
    parameter_list : list[Parameter]
    expression     : list[Token]

    def __init__(self, t_b: TokenBuffer):
        self.parameter_list = []
        self.expression     = []

        # ... código a completar ...!
        ...

    # Función de uso interno.
    @classmethod
    def __build__(cls, name, p_l, e):
        this = cls.__new__(cls)
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
    parameter_list : list[Parameter]
    return_type    : Token
    expression     : list[Token]

    def __init__(self, t_b: TokenBuffer):
        self.parameter_list = []
        self.expression     = []

        # ... código a completar ...!
        ...

    # Función de uso interno.
    @classmethod
    def __build__(cls, name, p_l, r_t, e):
        this = cls.__new__(cls)
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
    observer_list  : list[Observer]
    procedure_list : list[Procedure]
    predicate_list : list[Predicate]
    auxiliary_list : list[Auxiliary]

    def __init__(self, t_b: TokenBuffer):
        self.observer_list = []
        self.procedure_list = []
        self.predicate_list = []
        self.auxiliary_list = []

        # ... código a completar ...!
        ...

    # Función de uso interno.
    @classmethod
    def __build__(cls, name, o_l, p_l, e_l, a_l):
        this = cls.__new__(cls)
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
    data: Any

    @staticmethod
    def parse(token: TokenBuffer):
        return Expression.parse_recurse(token, 0)

    @staticmethod
    def parse_recurse(token: TokenBuffer, minimum_bind_power: int):
        ex_l = token.pop()

        # Caso: 1, 123, 67
        if Expression.is_atom(ex_l):
            # ... código a completar ...!
            ...
        # Caso: -
        elif Expression.is_operator(ex_l):
            # ... código a completar ...!
            ...
        else:
            raise ValueError(f"{ex_l} no es un valor válido (pre-fix).")

        #================================

        while True:
            operator = token.peek()

            # ... código a completar ...!
            ...

            #================================

            # Caso: !
            pf_bp = Expression.postfix_bind_power(operator)

            if pf_bp != None:
                # ... código a completar ...!
                ...

            #================================

            # Caso: +, -, *, /
            if_bp = Expression.infix_bind_power(operator)

            if if_bp != None:
                (bp_l, bp_r) = if_bp

                # ... código a completar ...!
                ...

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
                raise ValueError(f"{token} no es un operador válido.")

    @staticmethod
    def postfix_bind_power(token: Token) -> int | None:
        """
        Devuelve el poder de ligamiento de der. de un token asociado a un operador prefijo.
        """

        match token.kind:
            case TokenKind.EXCLAMATION:
                return 6
            case x:
                return None

    @staticmethod
    def infix_bind_power(token: Token) -> tuple[int, int] | None:
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
    def __build__(cls, kind, data):
        this = cls.__new__(cls)
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
    token = t_b.peek()

    if token != None:
        match token.kind:
            case TokenKind.PROCEDURE:
                value = Procedure(t_b)
            case TokenKind.PREDICATE:
                value = Predicate(t_b)
            case TokenKind.AUXILIARY:
                value = Auxiliary(t_b)
            case TokenKind.ADT:
                value = ADT(t_b)

    return value