from dataclasses import dataclass
from enum import Enum, auto
import sys

#================================================================

def test_file(name: str) -> str:
    with open(name) as file:
        return file.readlines()

@dataclass
class LineBuffer:
    line  : str

    def __init__(self, line: str):
        self.line = line

    def next(self) -> str | None:
        """
        Devuelve, eliminando, el próximo carácter en la línea. Devuelve None si no hay.
        """

        if len(self.line) > 0:
            p = self.line[0]; self.line = self.line[1:]
            return p

    def peek(self) -> str | None:
        """
        Devuelve, sin eliminar, el próximo carácter en la línea. Devuelve None si no hay.
        """

        if len(self.line) > 0:
            return self.line[0]

class TokenKind(Enum):
    IDENTIFIER    = auto() # foo
    NUMBER        = auto() # 1
    BRACKET_BEGIN = auto() # {
    BRACKET_CLOSE = auto() # }
    CURLY_BEGIN   = auto() # (
    CURLY_CLOSE   = auto() # )
    COLON_SEMI    = auto() # ;
    COLON         = auto() # :
    COMMA         = auto() # ,
    DOT           = auto() # .
    EQUAL         = auto() # =
    ADD           = auto() # +
    SUBTRACT      = auto() # -
    MULTIPLY      = auto() # *
    DIVIDE        = auto() # /
    MODULO        = auto() # mod
    PROCEDURE     = auto() # proc
    PREDICATE     = auto() # pred
    AUXILIARY     = auto() # aux
    ADT           = auto() # TAD
    RESULT        = auto() # res
    TRUE          = auto() # Verdadero
    FALSE         = auto() # Falso
    IN            = auto() # in
    IN_OUT        = auto() # inOut
    AND           = auto() # and
    OR            = auto() # or
    NOT           = auto() # not
    IMPLICATION   = auto() # then

    def __str__(self):
        look_up = {
            TokenKind.IDENTIFIER    : "Identifier",
            TokenKind.NUMBER        : "Number",
            TokenKind.BRACKET_BEGIN : "{",
            TokenKind.BRACKET_CLOSE : "}",
            TokenKind.CURLY_BEGIN   : "(",
            TokenKind.CURLY_CLOSE   : ")",
            TokenKind.COLON_SEMI    : ";",
            TokenKind.COLON         : ":",
            TokenKind.COMMA         : ",",
            TokenKind.DOT           : ".",
            TokenKind.EQUAL         : "=",
            TokenKind.ADD           : "+",
            TokenKind.SUBTRACT      : "-",
            TokenKind.MULTIPLY      : "*",
            TokenKind.DIVIDE        : "/",
            TokenKind.MODULO        : "mod",
            TokenKind.PROCEDURE     : "proc",
            TokenKind.PREDICATE     : "pred",
            TokenKind.AUXILIARY     : "aux",
            TokenKind.ADT           : "TAD",
            TokenKind.RESULT        : "res",
            TokenKind.TRUE          : "Verdadero",
            TokenKind.FALSE         : "Falso",
            TokenKind.IN            : "in",
            TokenKind.IN_OUT        : "inOut",
            TokenKind.AND           : "and",
            TokenKind.OR            : "or",
            TokenKind.NOT           : "not",
            TokenKind.IMPLICATION   : "then",
        }

        return f"'{look_up[self]}'"

@dataclass
class Token:
    kind : TokenKind
    data : any

@dataclass
class TokenBuffer:
    token: [Token]

    def __init__(self):
        self.token = []

    def push(self, token: Token):
        """
        Agrega un token al final de la lista de tokens.
        """

        self.token.append(token)

    def pop(self) -> Token:
        """
        Devuelve, eliminando, el próximo token en la lista.
        """

        if len(self.token) > 0:
            return self.token.pop(0)
        else:
            raise ValueError(f"No hay más tokens en la lista de tokens.")

    def want(self, kind: TokenKind) -> Token:
        """
        Devuelve, eliminando, el próximo token en la lista, sí es el tipo de token deseado (kind).
        """

        t = self.token.pop()

        if t.kind == kind:
            return t
        else:
            raise ValueError(f"Esperaba un token de tipo: '{kind}' pero recibí: '{t.kind}'")

    def want_peek(self, kind: TokenKind) -> Token | None:
        """
        Devuelve, sin eliminar, el próximo token en la lista, sí es el tipo de token deseado (kind). Devuelve None si no hay.
        """

        t = self.peek()

        if t != None and t.kind == kind:
            return t

        return None

    def peek(self) -> Token | None:
        """
        Devuelve, sin eliminar, el próximo token en la lista. Devuelve None si no hay.
        """

        if len(self.token) > 0:
            return self.token[0]
        else:
            return None

    def print(self):
        """
        Imprime por pantalla la lista actual de tokens.
        """

        print("[")

        for t in self.token:
            if t.data == None:
                print(f"  Token({t.kind}),")
            else:
                if isinstance(t.data, str):
                    print(f"  Token({t.kind}, '{t.data}'),")
                else:
                    print(f"  Token({t.kind}, {t.data}),")

        print("]")