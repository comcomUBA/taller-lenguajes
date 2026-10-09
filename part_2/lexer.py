from common import *
from parser import *

#================================================================

from dataclasses import dataclass
import sys
import unittest

#================================================================

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
    # ... código a completar ...!

    look_up = {
        '{'         : Token(TokenKind.BRACKET_BEGIN, None),
        '}'         : Token(TokenKind.BRACKET_CLOSE, None),
        '('         : Token(TokenKind.ROUND_BEGIN,   None),
        ')'         : Token(TokenKind.ROUND_CLOSE,   None),
        ';'         : Token(TokenKind.COLON_SEMI,    None),
        ","         : Token(TokenKind.COMMA,         None),
        '='         : Token(TokenKind.EQUAL,         None),
        '!='        : Token(TokenKind.EQUAL_NOT,     None),
        '>'         : Token(TokenKind.GT,            None),
        '>='        : Token(TokenKind.GTE,           None),
        '<'         : Token(TokenKind.LT,            None),
        '<='        : Token(TokenKind.LTE,           None),
        '+'         : Token(TokenKind.ADD,           None),
        '-'         : Token(TokenKind.SUBTRACT,      None),
        '*'         : Token(TokenKind.MULTIPLY,      None),
        '/'         : Token(TokenKind.DIVIDE,        None),
        "and"       : Token(TokenKind.AND,           None),
        "or"        : Token(TokenKind.OR,            None),
        "not"       : Token(TokenKind.NOT,           None),
        "if"        : Token(TokenKind.NOT,           None),
        "else"      : Token(TokenKind.NOT,           None),
        "while"     : Token(TokenKind.NOT,           None),
        "return"    : Token(TokenKind.NOT,           None),
    }

    if text in look_up:
        return look_up[text]
    else:
        if is_number(text):
            return Token(TokenKind.NUMBER, float(text))
        else:
            return Token(TokenKind.IDENTIFIER, text)

def lexer(text: str) -> TokenBuffer:
    t_b         = TokenBuffer()

    # ... código a completar ...!

    list_string = ""
    in_string   = False
    in_number   = False

    for line in text:
        line = LineBuffer(line.strip())

        character = line.next()

        while character:
            match character:
                case '{' | '}' | '(' | ')' | ';' | ':' | ',' | '.' | '!' | '=' | '>' | '<' | '+' | '-' | '*' | '/':
                    if in_number and character == '.':
                        list_string += character
                    else:

                        if len(list_string) > 0:
                            t_b.push(lex_string(list_string))
                            list_string = ""

                        list_string += character

                        if line.peek(0) == '=':
                            line.next()
                            list_string += '='

                        t_b.push(lex_string(list_string))
                        list_string = ""
                case ' ':
                    if len(list_string) > 0:
                        t_b.push(lex_string(list_string))
                        list_string = ""

                    in_number = False
                case x:
                    in_number = x.isnumeric()
                    list_string += x

            character = line.next()

        if len(list_string) > 0:
            t_b.push(lex_string(list_string))
            list_string = ""

    return t_b

#================================================================

class TestLexer(unittest.TestCase):
    def test_aux_es_par(self):
        t_b_1 = lexer(test_file("test/aux_1.txt"))
        t_b_2 = [
          Token(TokenKind.AUXILIARY, None),
          Token(TokenKind.IDENTIFIER, 'esPar'),
          Token(TokenKind.ROUND_BEGIN, None),
          Token(TokenKind.IDENTIFIER, 'x'),
          Token(TokenKind.COLON, None),
          Token(TokenKind.IDENTIFIER, 'Entero'),
          Token(TokenKind.COMMA, None),
          Token(TokenKind.IDENTIFIER, 'y'),
          Token(TokenKind.COLON, None),
          Token(TokenKind.IDENTIFIER, 'Entero'),
          Token(TokenKind.ROUND_CLOSE, None),
          Token(TokenKind.COLON, None),
          Token(TokenKind.IDENTIFIER, 'Booleano'),
          Token(TokenKind.BRACKET_BEGIN, None),
          Token(TokenKind.IDENTIFIER, 'x'),
          Token(TokenKind.MODULO, None),
          Token(TokenKind.IDENTIFIER, '2'),
          Token(TokenKind.DOT, None),
          Token(TokenKind.IDENTIFIER, '0'),
          Token(TokenKind.EQUAL, None),
          Token(TokenKind.IDENTIFIER, '0'),
          Token(TokenKind.BRACKET_CLOSE, None),
        ]

        self.assertEqual(t_b_1.token, t_b_2)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        t_b = lexer(test_file("test/" + sys.argv[1]))
        #print(t_b)
        parser(t_b)
    else:
        print(r""" ____________
< Testing... >
 ------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
----------------------------------------------------------------------""")
        unittest.main()