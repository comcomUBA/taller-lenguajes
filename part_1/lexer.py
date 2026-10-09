from common import *
from parser import *

#================================================================

from dataclasses import dataclass
import sys
import unittest

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

"""
*************************
*     Pseudo-código     *
*************************

Reviso si texto está dentro de alguna estructura de datos donde podamos relacionar una clave con un valor...
    Si esta:
        Devuelvo el valor.
    Si no:
        Si es un valor numérico:
            Devuelvo un token numérico.
        Si no:
            Devuelvo un token identificador.
"""

def lex_string(text: str) -> Token:
    # ... código a completar ...!

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

"""
*************************
*     Pseudo-código     *
*************************

token    <- TokenBuffer()
string   <- ""
enNumero <- False

Por cada linea en el texto:
    buffer   <- LineBuffer(linea)
    caracter <- buffer.siguiente()

    Mientras que caracter sea no-nulo:
        Si el caracter es ' ':
            Si string es no-vacio:
                token.push(lex_string(string))
                string <- ""

            enNumero <- False
        Si no:
            Si el caracter es un simbolo:
                Si se esta dentro de un numero, y el caracter es '.':
                    string <- string + caracter
                Si no:
                    Si string es no-vacio:
                        token.push(lex_string(string))
                        string <- ""

                    string <- string + caracter

                    Si el siguiente caracter es '=':
                        buffer.siguiente()
                        string <- string + '='

                    token.push(lex_string(string))
                    string <- ""
            Si no:
                enNumero <- caracter.esNumerico()
                string   <- string + caracter

        caracter <- buffer.siguiente()

    Si string es no-vacio:
        token.push(lex_string(string))
        string <- ""
"""

def lexer(text: str) -> TokenBuffer:
    t_b         = TokenBuffer()

    # ... código a completar ...!

    list_string = ""
    in_number   = False

    for line in text:
        line = LineBuffer(line.strip())
        character = line.next()

        while character:
            match character:
                case ' ':
                    if len(list_string) > 0:
                        t_b.push(lex_string(list_string))
                        list_string = ""

                    in_number = False
                case x:
                    if is_symbol(x):
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
                    else:
                        in_number = x.isnumeric()
                        list_string += x

            character = line.next()

        if len(list_string) > 0:
            t_b.push(lex_string(list_string))
            list_string = ""

    return t_b

#================================================================

class TestLexer(unittest.TestCase):
    def test_aux_distancia(self):
        t_b_1 = lexer(test_file("test/aux_distancia.txt"))
        t_b_2 = [
          Token(TokenKind.AUXILIARY, None),
          Token(TokenKind.IDENTIFIER, "distancia"),
          Token(TokenKind.ROUND_BEGIN, None),
          Token(TokenKind.IDENTIFIER, "a"),
          Token(TokenKind.COLON, None),
          Token(TokenKind.IDENTIFIER, "Vector"),
          Token(TokenKind.COMMA, None),
          Token(TokenKind.IDENTIFIER, "b"),
          Token(TokenKind.COLON, None),
          Token(TokenKind.IDENTIFIER, "Vector"),
          Token(TokenKind.ROUND_CLOSE, None),
          Token(TokenKind.COLON, None),
          Token(TokenKind.IDENTIFIER, "Real"),
          Token(TokenKind.BRACKET_BEGIN, None),
          Token(TokenKind.PIPE, None),
          Token(TokenKind.ROUND_BEGIN, None),
          Token(TokenKind.IDENTIFIER, "a"),
          Token(TokenKind.DOT, None),
          Token(TokenKind.IDENTIFIER, "x"),
          Token(TokenKind.SUBTRACT, None),
          Token(TokenKind.IDENTIFIER, "b"),
          Token(TokenKind.DOT, None),
          Token(TokenKind.IDENTIFIER, "x"),
          Token(TokenKind.ROUND_CLOSE, None),
          Token(TokenKind.SUBTRACT, None),
          Token(TokenKind.ROUND_BEGIN, None),
          Token(TokenKind.IDENTIFIER, "a"),
          Token(TokenKind.DOT, None),
          Token(TokenKind.IDENTIFIER, "y"),
          Token(TokenKind.SUBTRACT, None),
          Token(TokenKind.IDENTIFIER, "b"),
          Token(TokenKind.DOT, None),
          Token(TokenKind.IDENTIFIER, "y"),
          Token(TokenKind.ROUND_CLOSE, None),
          Token(TokenKind.PIPE, None),
          Token(TokenKind.BRACKET_CLOSE, None),
        ]

        self.assertEqual(t_b_1.token, t_b_2)

    def test_aux_interpolacion(self):
        t_b_1 = lexer(test_file("test/aux_interpolacion.txt"))
        t_b_2 = [
          Token(TokenKind.AUXILIARY, None),
          Token(TokenKind.IDENTIFIER, "interpolacion"),
          Token(TokenKind.ROUND_BEGIN, None),
          Token(TokenKind.IDENTIFIER, "t"),
          Token(TokenKind.COLON, None),
          Token(TokenKind.IDENTIFIER, "Real"),
          Token(TokenKind.COMMA, None),
          Token(TokenKind.IDENTIFIER, "a"),
          Token(TokenKind.COLON, None),
          Token(TokenKind.IDENTIFIER, "Real"),
          Token(TokenKind.COMMA, None),
          Token(TokenKind.IDENTIFIER, "b"),
          Token(TokenKind.COLON, None),
          Token(TokenKind.IDENTIFIER, "Real"),
          Token(TokenKind.ROUND_CLOSE, None),
          Token(TokenKind.BRACKET_BEGIN, None),
          Token(TokenKind.IDENTIFIER, "a"),
          Token(TokenKind.ADD, None),
          Token(TokenKind.IDENTIFIER, "t"),
          Token(TokenKind.MULTIPLY, None),
          Token(TokenKind.ROUND_BEGIN, None),
          Token(TokenKind.IDENTIFIER, "b"),
          Token(TokenKind.SUBTRACT, None),
          Token(TokenKind.IDENTIFIER, "a"),
          Token(TokenKind.ROUND_CLOSE, None),
          Token(TokenKind.BRACKET_CLOSE, None),
        ]

        self.assertEqual(t_b_1.token, t_b_2)

    def test_aux_valorEntre(self):
        t_b_1 = lexer(test_file("test/aux_valorEntre.txt"))
        t_b_2 = [
          Token(TokenKind.AUXILIARY, None),
          Token(TokenKind.IDENTIFIER, "valorEntre"),
          Token(TokenKind.ROUND_BEGIN, None),
          Token(TokenKind.IDENTIFIER, "v"),
          Token(TokenKind.COLON, None),
          Token(TokenKind.IDENTIFIER, "Entero"),
          Token(TokenKind.COMMA, None),
          Token(TokenKind.IDENTIFIER, "min"),
          Token(TokenKind.COLON, None),
          Token(TokenKind.IDENTIFIER, "Entero"),
          Token(TokenKind.COMMA, None),
          Token(TokenKind.IDENTIFIER, "max"),
          Token(TokenKind.COLON, None),
          Token(TokenKind.IDENTIFIER, "Entero"),
          Token(TokenKind.ROUND_CLOSE, None),
          Token(TokenKind.BRACKET_BEGIN, None),
          Token(TokenKind.IDENTIFIER, "IfThenElse"),
          Token(TokenKind.ROUND_BEGIN, None),
          Token(TokenKind.IDENTIFIER, "v"),
          Token(TokenKind.GTE, None),
          Token(TokenKind.IDENTIFIER, "max"),
          Token(TokenKind.COMMA, None),
          Token(TokenKind.IDENTIFIER, "max"),
          Token(TokenKind.COMMA, None),
          Token(TokenKind.IDENTIFIER, "IfThenElse"),
          Token(TokenKind.ROUND_BEGIN, None),
          Token(TokenKind.IDENTIFIER, "v"),
          Token(TokenKind.LTE, None),
          Token(TokenKind.IDENTIFIER, "min"),
          Token(TokenKind.COMMA, None),
          Token(TokenKind.IDENTIFIER, "min"),
          Token(TokenKind.COMMA, None),
          Token(TokenKind.IDENTIFIER, "v"),
          Token(TokenKind.ROUND_CLOSE, None),
          Token(TokenKind.ROUND_CLOSE, None),
          Token(TokenKind.BRACKET_CLOSE, None),
        ]

        self.assertEqual(t_b_1.token, t_b_2)

    def test_pred_divide(self):
        t_b_1 = lexer(test_file("test/pred_divide.txt"))
        t_b_2 = [
          Token(TokenKind.PREDICATE, None),
          Token(TokenKind.IDENTIFIER, "divide"),
          Token(TokenKind.ROUND_BEGIN, None),
          Token(TokenKind.IDENTIFIER, "x"),
          Token(TokenKind.COLON, None),
          Token(TokenKind.IDENTIFIER, "Entero"),
          Token(TokenKind.COMMA, None),
          Token(TokenKind.IDENTIFIER, "y"),
          Token(TokenKind.COLON, None),
          Token(TokenKind.IDENTIFIER, "Entero"),
          Token(TokenKind.ROUND_CLOSE, None),
          Token(TokenKind.BRACKET_BEGIN, None),
          Token(TokenKind.IDENTIFIER, "y"),
          Token(TokenKind.MODULO, None),
          Token(TokenKind.IDENTIFIER, "x"),
          Token(TokenKind.EQUAL, None),
          Token(TokenKind.NUMBER, 0.0),
          Token(TokenKind.BRACKET_CLOSE, None),
        ]

        self.assertEqual(t_b_1.token, t_b_2)

    def test_pred_mayorPrimoQueDivide(self):
        t_b_1 = lexer(test_file("test/pred_mayorPrimoQueDivide.txt"))
        t_b_2 = [
          Token(TokenKind.PREDICATE, None),
          Token(TokenKind.IDENTIFIER, "mayorPrimoQueDivide"),
          Token(TokenKind.ROUND_BEGIN, None),
          Token(TokenKind.IDENTIFIER, "x"),
          Token(TokenKind.COLON, None),
          Token(TokenKind.IDENTIFIER, "Entero"),
          Token(TokenKind.COMMA, None),
          Token(TokenKind.IDENTIFIER, "y"),
          Token(TokenKind.COLON, None),
          Token(TokenKind.IDENTIFIER, "Entero"),
          Token(TokenKind.ROUND_CLOSE, None),
          Token(TokenKind.BRACKET_BEGIN, None),
          Token(TokenKind.IDENTIFIER, "esPrimo"),
          Token(TokenKind.ROUND_BEGIN, None),
          Token(TokenKind.IDENTIFIER, "y"),
          Token(TokenKind.ROUND_CLOSE, None),
          Token(TokenKind.AND, None),
          Token(TokenKind.IDENTIFIER, "divideA"),
          Token(TokenKind.ROUND_BEGIN, None),
          Token(TokenKind.IDENTIFIER, "x"),
          Token(TokenKind.COMMA, None),
          Token(TokenKind.IDENTIFIER, "y"),
          Token(TokenKind.ROUND_CLOSE, None),
          Token(TokenKind.AND, None),
          Token(TokenKind.NOT, None),
          Token(TokenKind.ROUND_BEGIN, None),
          Token(TokenKind.FOR_ONE, None),
          Token(TokenKind.IDENTIFIER, "p"),
          Token(TokenKind.COLON, None),
          Token(TokenKind.IDENTIFIER, "Entero"),
          Token(TokenKind.ROUND_CLOSE, None),
          Token(TokenKind.ROUND_BEGIN, None),
          Token(TokenKind.IDENTIFIER, "esPrimo"),
          Token(TokenKind.ROUND_BEGIN, None),
          Token(TokenKind.IDENTIFIER, "p"),
          Token(TokenKind.ROUND_CLOSE, None),
          Token(TokenKind.AND, None),
          Token(TokenKind.IDENTIFIER, "divideA"),
          Token(TokenKind.ROUND_BEGIN, None),
          Token(TokenKind.IDENTIFIER, "x"),
          Token(TokenKind.COMMA, None),
          Token(TokenKind.IDENTIFIER, "p"),
          Token(TokenKind.ROUND_CLOSE, None),
          Token(TokenKind.AND, None),
          Token(TokenKind.IDENTIFIER, "p"),
          Token(TokenKind.GT, None),
          Token(TokenKind.IDENTIFIER, "y"),
          Token(TokenKind.ROUND_CLOSE, None),
          Token(TokenKind.BRACKET_CLOSE, None),
        ]

        self.assertEqual(t_b_1.token, t_b_2)

    def test_pred_sonCoprimos(self):
        t_b_1 = lexer(test_file("test/pred_sonCoprimos.txt"))
        t_b_2 = [
          Token(TokenKind.PREDICATE, None),
          Token(TokenKind.IDENTIFIER, "sonCoprimos"),
          Token(TokenKind.ROUND_BEGIN, None),
          Token(TokenKind.IDENTIFIER, "x"),
          Token(TokenKind.COLON, None),
          Token(TokenKind.IDENTIFIER, "Entero"),
          Token(TokenKind.COMMA, None),
          Token(TokenKind.IDENTIFIER, "y"),
          Token(TokenKind.COLON, None),
          Token(TokenKind.IDENTIFIER, "Entero"),
          Token(TokenKind.ROUND_CLOSE, None),
          Token(TokenKind.BRACKET_BEGIN, None),
          Token(TokenKind.IDENTIFIER, "MCD"),
          Token(TokenKind.ROUND_BEGIN, None),
          Token(TokenKind.IDENTIFIER, "x"),
          Token(TokenKind.COMMA, None),
          Token(TokenKind.IDENTIFIER, "y"),
          Token(TokenKind.ROUND_CLOSE, None),
          Token(TokenKind.EQUAL, None),
          Token(TokenKind.NUMBER, 1.0),
          Token(TokenKind.BRACKET_CLOSE, None),
        ]

        self.assertEqual(t_b_1.token, t_b_2)

    def test_proc_esMultiploDe(self):
        t_b_1 = lexer(test_file("test/proc_esMultiploDe.txt"))
        t_b_2 = [
          Token(TokenKind.PROCEDURE, None),
          Token(TokenKind.IDENTIFIER, "esMultiploDe"),
          Token(TokenKind.ROUND_BEGIN, None),
          Token(TokenKind.IN, None),
          Token(TokenKind.IDENTIFIER, "x"),
          Token(TokenKind.COLON, None),
          Token(TokenKind.IDENTIFIER, "Real"),
          Token(TokenKind.COMMA, None),
          Token(TokenKind.IN, None),
          Token(TokenKind.IDENTIFIER, "y"),
          Token(TokenKind.COLON, None),
          Token(TokenKind.IDENTIFIER, "Real"),
          Token(TokenKind.ROUND_CLOSE, None),
          Token(TokenKind.COLON, None),
          Token(TokenKind.IDENTIFIER, "bool"),
          Token(TokenKind.BRACKET_BEGIN, None),
          Token(TokenKind.REQUIRE, None),
          Token(TokenKind.BRACKET_BEGIN, None),
          Token(TokenKind.IDENTIFIER, "y"),
          Token(TokenKind.GT, None),
          Token(TokenKind.NUMBER, 0.0),
          Token(TokenKind.BRACKET_CLOSE, None),
          Token(TokenKind.ASSURE, None),
          Token(TokenKind.BRACKET_BEGIN, None),
          Token(TokenKind.RESULT, None),
          Token(TokenKind.EQUAL, None),
          Token(TokenKind.TRUE, None),
          Token(TokenKind.IMPLICATION_DOUBLE, None),
          Token(TokenKind.ROUND_BEGIN, None),
          Token(TokenKind.IDENTIFIER, "x"),
          Token(TokenKind.MODULO, None),
          Token(TokenKind.NUMBER, 2.0),
          Token(TokenKind.EQUAL, None),
          Token(TokenKind.NUMBER, 0.0),
          Token(TokenKind.ROUND_CLOSE, None),
          Token(TokenKind.BRACKET_CLOSE, None),
          Token(TokenKind.BRACKET_CLOSE, None),
        ]

        self.assertEqual(t_b_1.token, t_b_2)

    def test_proc_minimo(self):
        t_b_1 = lexer(test_file("test/proc_minimo.txt"))
        t_b_2 = [
          Token(TokenKind.PROCEDURE, None),
          Token(TokenKind.IDENTIFIER, "minimo"),
          Token(TokenKind.ROUND_BEGIN, None),
          Token(TokenKind.IN, None),
          Token(TokenKind.IDENTIFIER, "s"),
          Token(TokenKind.COLON, None),
          Token(TokenKind.IDENTIFIER, "SeqEntero"),
          Token(TokenKind.ROUND_CLOSE, None),
          Token(TokenKind.COLON, None),
          Token(TokenKind.IDENTIFIER, "Entero"),
          Token(TokenKind.BRACKET_BEGIN, None),
          Token(TokenKind.REQUIRE, None),
          Token(TokenKind.BRACKET_BEGIN, None),
          Token(TokenKind.PIPE, None),
          Token(TokenKind.IDENTIFIER, "s"),
          Token(TokenKind.PIPE, None),
          Token(TokenKind.GT, None),
          Token(TokenKind.NUMBER, 0.0),
          Token(TokenKind.BRACKET_CLOSE, None),
          Token(TokenKind.ASSURE, None),
          Token(TokenKind.BRACKET_BEGIN, None),
          Token(TokenKind.RESULT, None),
          Token(TokenKind.IN, None),
          Token(TokenKind.IDENTIFIER, "s"),
          Token(TokenKind.AND, None),
          Token(TokenKind.NOT, None),
          Token(TokenKind.ROUND_BEGIN, None),
          Token(TokenKind.FOR_ONE, None),
          Token(TokenKind.IDENTIFIER, "i"),
          Token(TokenKind.COLON, None),
          Token(TokenKind.IDENTIFIER, "Entero"),
          Token(TokenKind.ROUND_CLOSE, None),
          Token(TokenKind.ROUND_BEGIN, None),
          Token(TokenKind.IDENTIFIER, "i"),
          Token(TokenKind.IN, None),
          Token(TokenKind.IDENTIFIER, "s"),
          Token(TokenKind.AND, None),
          Token(TokenKind.IDENTIFIER, "i"),
          Token(TokenKind.EQUAL_NOT, None),
          Token(TokenKind.RESULT, None),
          Token(TokenKind.AND, None),
          Token(TokenKind.IDENTIFIER, "i"),
          Token(TokenKind.LT, None),
          Token(TokenKind.RESULT, None),
          Token(TokenKind.ROUND_CLOSE, None),
          Token(TokenKind.BRACKET_CLOSE, None),
          Token(TokenKind.BRACKET_CLOSE, None),
        ]

        self.assertEqual(t_b_1.token, t_b_2)

    def test_proc_todosPares(self):
        t_b_1 = lexer(test_file("test/proc_todosPares.txt"))
        t_b_2 = [
          Token(TokenKind.PROCEDURE, None),
          Token(TokenKind.IDENTIFIER, "todosPares"),
          Token(TokenKind.ROUND_BEGIN, None),
          Token(TokenKind.IN, None),
          Token(TokenKind.IDENTIFIER, "s"),
          Token(TokenKind.COLON, None),
          Token(TokenKind.IDENTIFIER, "SeqEntero"),
          Token(TokenKind.ROUND_CLOSE, None),
          Token(TokenKind.COLON, None),
          Token(TokenKind.IDENTIFIER, "bool"),
          Token(TokenKind.BRACKET_BEGIN, None),
          Token(TokenKind.REQUIRE, None),
          Token(TokenKind.BRACKET_BEGIN, None),
          Token(TokenKind.TRUE, None),
          Token(TokenKind.BRACKET_CLOSE, None),
          Token(TokenKind.ASSURE, None),
          Token(TokenKind.BRACKET_BEGIN, None),
          Token(TokenKind.RESULT, None),
          Token(TokenKind.EQUAL, None),
          Token(TokenKind.TRUE, None),
          Token(TokenKind.IMPLICATION_DOUBLE, None),
          Token(TokenKind.ROUND_BEGIN, None),
          Token(TokenKind.FOR_ALL, None),
          Token(TokenKind.IDENTIFIER, "i"),
          Token(TokenKind.COLON, None),
          Token(TokenKind.IDENTIFIER, "Entero"),
          Token(TokenKind.ROUND_CLOSE, None),
          Token(TokenKind.ROUND_BEGIN, None),
          Token(TokenKind.NUMBER, 0.0),
          Token(TokenKind.LTE, None),
          Token(TokenKind.IDENTIFIER, "i"),
          Token(TokenKind.LT, None),
          Token(TokenKind.PIPE, None),
          Token(TokenKind.IDENTIFIER, "s"),
          Token(TokenKind.PIPE, None),
          Token(TokenKind.IMPLICATION, None),
          Token(TokenKind.IDENTIFIER, "esPar"),
          Token(TokenKind.ROUND_BEGIN, None),
          Token(TokenKind.IDENTIFIER, "s"),
          Token(TokenKind.BLOCK_BEGIN, None),
          Token(TokenKind.IDENTIFIER, "i"),
          Token(TokenKind.BLOCK_CLOSE, None),
          Token(TokenKind.ROUND_CLOSE, None),
          Token(TokenKind.ROUND_CLOSE, None),
          Token(TokenKind.BRACKET_CLOSE, None),
          Token(TokenKind.BRACKET_CLOSE, None),
        ]

        self.assertEqual(t_b_1.token, t_b_2)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        t_b = lexer(test_file("test/" + sys.argv[1]))
        print(parser(t_b))
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