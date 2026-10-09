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

    def peek(self, index: int) -> str | None:
        """
        Devuelve, sin eliminar, el carácter en el índice dado. Devuelve None si no hay.
        """

        if index >= 0 and index < len(self.line):
            return self.line[index]

class TokenKind(Enum):
    IDENTIFIER    = auto() # foo
    NUMBER        = auto() # 1
    BRACKET_BEGIN = auto() # {
    BRACKET_CLOSE = auto() # }
    ROUND_BEGIN   = auto() # (
    ROUND_CLOSE   = auto() # )
    COLON_SEMI    = auto() # ;
    COLON         = auto() # :
    COMMA         = auto() # ,
    DOT           = auto() # .
    PIPE          = auto() # |
    EQUAL         = auto() # =
    EQUAL_NOT     = auto() # !=
    GT            = auto() # >
    GTE           = auto() # >=
    LT            = auto() # <
    LTE           = auto() # <=
    ADD           = auto() # +
    SUBTRACT      = auto() # -
    MULTIPLY      = auto() # *
    DIVIDE        = auto() # /
    MODULO        = auto() # mod
    OBSERVER      = auto() # obs
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
    REQUIRE       = auto() # requiere
    ASSURE        = auto() # asegura

    def __repr__(self):
        look_up = {
            TokenKind.IDENTIFIER    : "Identifier",
            TokenKind.NUMBER        : "Number",
            TokenKind.BRACKET_BEGIN : "'{'",
            TokenKind.BRACKET_CLOSE : "'}'",
            TokenKind.ROUND_BEGIN   : "'('",
            TokenKind.ROUND_CLOSE   : "')'",
            TokenKind.COLON_SEMI    : "';'",
            TokenKind.COLON         : "':'",
            TokenKind.COMMA         : "','",
            TokenKind.DOT           : "'.'",
            TokenKind.PIPE          : "'|'",
            TokenKind.EQUAL         : "'='",
            TokenKind.EQUAL_NOT     : "'!='",
            TokenKind.GT            : "'>'",
            TokenKind.GTE           : "'>='",
            TokenKind.LT            : "'<'",
            TokenKind.LTE           : "'<='",
            TokenKind.ADD           : "'+'",
            TokenKind.SUBTRACT      : "'-'",
            TokenKind.MULTIPLY      : "'*'",
            TokenKind.DIVIDE        : "'/'",
            TokenKind.MODULO        : "'mod'",
            TokenKind.OBSERVER      : "'obs'",
            TokenKind.PROCEDURE     : "'proc'",
            TokenKind.PREDICATE     : "'pred'",
            TokenKind.AUXILIARY     : "'aux'",
            TokenKind.ADT           : "'TAD'",
            TokenKind.RESULT        : "'res'",
            TokenKind.TRUE          : "'Verdadero'",
            TokenKind.FALSE         : "'Falso'",
            TokenKind.IN            : "'in'",
            TokenKind.IN_OUT        : "'inOut'",
            TokenKind.AND           : "'and'",
            TokenKind.OR            : "'or'",
            TokenKind.NOT           : "'not'",
            TokenKind.IMPLICATION   : "'then'",
            TokenKind.REQUIRE       : "'require'",
            TokenKind.ASSURE        : "'assure'",
        }

        return look_up[self]

@dataclass
class Token:
    kind : TokenKind
    data : any

    def __repr__(self):
        if self.data == None:
            return f"{self.kind}"
        else:
            if isinstance(self.data, str):
                return f"{self.kind}('{self.data}')"
            else:
                return f"{self.kind}({self.data})"

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

        t = self.pop()

        if t.kind == kind:
            return t
        else:
            raise ValueError(f"Esperaba un token de tipo: {kind} pero recibí: {t.kind}")

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

    def __repr__(self):
        """
        Imprime por pantalla la lista actual de tokens.
        """

        buffer = ""

        buffer = buffer + '[' + '\n'

        for t in self.token:
            buffer = buffer + f"  Token({t}),\n"

        buffer = buffer + ']'

        return buffer