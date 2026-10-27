from common import *

#================================================================

from dataclasses import dataclass
import sys

#================================================================

def is_symbol(text: str) -> bool:
    look_up = ['{', '}', '(', ')', '[', ']', ';', ':', ',', '.', '|', '!', '=', '>', '<', '+', '-', '*', '/']

    return text in look_up

def is_number(text: str) -> bool:
    d = False

    for character in text:
        match character:
            case '.':
                if d == False:
                    d = True
                else:
                    return False
            case x:
                if not x.isnumeric():
                    return False

    return True

def lex_string(text: str) -> Token:
    look_up = {
        '{'         : Token(TokenKind.BRACKET_BEGIN,      None),
        '}'         : Token(TokenKind.BRACKET_CLOSE,      None),
        '('         : Token(TokenKind.ROUND_BEGIN,        None),
        ')'         : Token(TokenKind.ROUND_CLOSE,        None),
        '['         : Token(TokenKind.BLOCK_BEGIN,        None),
        ']'         : Token(TokenKind.BLOCK_CLOSE,        None),
        ';'         : Token(TokenKind.COLON_SEMI,         None),
        ':'         : Token(TokenKind.COLON,              None),
        ","         : Token(TokenKind.COMMA,              None),
        '.'         : Token(TokenKind.DOT,                None),
        '|'         : Token(TokenKind.PIPE,               None),
        '!'         : Token(TokenKind.EXCLAMATION,        None),
        '='         : Token(TokenKind.EQUAL,              None),
        '!='        : Token(TokenKind.EQUAL_NOT,          None),
        '>'         : Token(TokenKind.GT,                 None),
        '>='        : Token(TokenKind.GTE,                None),
        '<'         : Token(TokenKind.LT,                 None),
        '<='        : Token(TokenKind.LTE,                None),
        '+'         : Token(TokenKind.ADD,                None),
        '-'         : Token(TokenKind.SUBTRACT,           None),
        '*'         : Token(TokenKind.MULTIPLY,           None),
        '/'         : Token(TokenKind.DIVIDE,             None),
        "mod"       : Token(TokenKind.MODULO,             None),
        "obs"       : Token(TokenKind.OBSERVER,           None),
        "proc"      : Token(TokenKind.PROCEDURE,          None),
        "pred"      : Token(TokenKind.PREDICATE,          None),
        "aux"       : Token(TokenKind.AUXILIARY,          None),
        "TAD"       : Token(TokenKind.ADT,                None),
        "res"       : Token(TokenKind.RESULT,             None),
        "Verdadero" : Token(TokenKind.TRUE,               None),
        "Falso"     : Token(TokenKind.FALSE,              None),
        "in"        : Token(TokenKind.IN,                 None),
        "inOut"     : Token(TokenKind.IN_OUT,             None),
        "and"       : Token(TokenKind.AND,                None),
        "or"        : Token(TokenKind.OR,                 None),
        "not"       : Token(TokenKind.NOT,                None),
        "entonces"  : Token(TokenKind.IMPLICATION,        None),
        "sii"       : Token(TokenKind.IMPLICATION_DOUBLE, None),
        "requiere"  : Token(TokenKind.REQUIRE,            None),
        "asegura"   : Token(TokenKind.ASSURE,             None),
        "existe"    : Token(TokenKind.FOR_ONE,            None),
        "paraTodo"  : Token(TokenKind.FOR_ALL,            None),
    }

    if text in look_up:
        return look_up[text]
    else:
        if is_number(text):
            return Token(TokenKind.NUMBER, float(text))
        else:
            return Token(TokenKind.IDENTIFIER, text)

def lexer(text: list[str]) -> TokenBuffer:
    t_b         = TokenBuffer()

    # ... código a completar ...!

    return t_b