from dataclasses import dataclass
from enum import Enum

@dataclass
class LineBuffer:
    line  : str
    index : int

    def __init__(self, line: str):
        self.line  = line
        self.index = 0

    def next(self) -> str | None:
        if self.index < len(self.line):
            self.index += 1;
            return self.line[self.index - 1]

    def peek(self) -> str | None:
        if self.index < len(self.line):
            return self.line[self.index]

class TokenKind(Enum):
    IDENTIFIER    = 0
    NUMBER        = 1
    BRACKET_BEGIN = 2
    BRACKET_CLOSE = 3
    CURLY_BEGIN   = 4
    CURLY_CLOSE   = 5
    COLON_SEMI    = 6
    COLON         = 7
    EQUAL         = 8
    DOT           = 9
    ADD           = 10
    SUBTRACT      = 11
    MULTIPLY      = 12
    DIVIDE        = 13
    MODULO        = 14
    PROCEDURE     = 15
    PREDICATE     = 16
    AUXILIARY     = 17
    RESULT        = 18
    TRUE          = 19
    FALSE         = 20

@dataclass
class Token:
    kind : TokenKind
    data : any

def lex_character(text: str, list_token: list[Token]):
    match text:
        case '{':
            list_token.append(Token(TokenKind.BRACKET_BEGIN, None))
        case '}':
            list_token.append(Token(TokenKind.BRACKET_CLOSE, None))
        case '(':
            list_token.append(Token(TokenKind.CURLY_BEGIN, None))
        case ')':
            list_token.append(Token(TokenKind.CURLY_CLOSE, None))
        case ';':
            list_token.append(Token(TokenKind.COLON_SEMI, None))
        case ':':
            list_token.append(Token(TokenKind.COLON, None))
        case '=':
            list_token.append(Token(TokenKind.EQUAL, None))
        case '.':
            list_token.append(Token(TokenKind.DOT, None))
        case '+':
            list_token.append(Token(TokenKind.ADD, None))
        case '-':
            list_token.append(Token(TokenKind.SUBTRACT, None))
        case '*':
            list_token.append(Token(TokenKind.MULTIPLY, None))
        case '/':
            list_token.append(Token(TokenKind.DIVIDE, None))
        case "mod":
            list_token.append(Token(TokenKind.MODULO, None))
        case "proc":
            list_token.append(Token(TokenKind.PROCEDURE, None))
        case "pred":
            list_token.append(Token(TokenKind.PREDICATE, None))
        case "aux":
            list_token.append(Token(TokenKind.AUXILIARY, None))
        case "res":
            list_token.append(Token(TokenKind.RESULT, None))
        case "True":
            list_token.append(Token(TokenKind.TRUE, None))
        case "False":
            list_token.append(Token(TokenKind.FALSE, None))
        case x:
            list_token.append(Token(TokenKind.IDENTIFIER, x))

def lexer(text: str):
    list_token  = []
    list_string = ""

    for line in text:
        line = LineBuffer(line.strip())

        character = line.next()

        while character:
            match character:
                case '{' | '}' | '(' | ')' | ';' | ':' | '.' | '=' | '+' | '-' | '*' | '/':
                    if len(list_string) > 0:
                        lex_character(list_string, list_token)
                        list_string = ""

                    lex_character(character, list_token)
                case ' ':
                    if len(list_string) > 0:
                        lex_character(list_string, list_token)
                        list_string = ""
                case x:
                    list_string += x

            character = line.next()

        if len(list_string) > 0:
            lex_character(list_string, list_token)
            list_string = ""

    for t in list_token:
        print(t)

with open("aux.txt") as file:
    lexer(file.readlines())