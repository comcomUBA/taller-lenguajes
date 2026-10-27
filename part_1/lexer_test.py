from lexer import *

#================================================================

import unittest

#================================================================

if __name__ == "__main__":
    if len(sys.argv) > 1:
        t_b = lexer(test_file("test/" + sys.argv[1]))
        print(t_b)
    else:
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
                    Token(TokenKind.MULTIPLY, None),
                    Token(TokenKind.ROUND_BEGIN, None),
                    Token(TokenKind.IDENTIFIER, "a"),
                    Token(TokenKind.DOT, None),
                    Token(TokenKind.IDENTIFIER, "x"),
                    Token(TokenKind.SUBTRACT, None),
                    Token(TokenKind.IDENTIFIER, "b"),
                    Token(TokenKind.DOT, None),
                    Token(TokenKind.IDENTIFIER, "x"),
                    Token(TokenKind.ROUND_CLOSE, None),
                    Token(TokenKind.ADD, None),
                    Token(TokenKind.ROUND_BEGIN, None),
                    Token(TokenKind.IDENTIFIER, "a"),
                    Token(TokenKind.DOT, None),
                    Token(TokenKind.IDENTIFIER, "y"),
                    Token(TokenKind.SUBTRACT, None),
                    Token(TokenKind.IDENTIFIER, "b"),
                    Token(TokenKind.DOT, None),
                    Token(TokenKind.IDENTIFIER, "y"),
                    Token(TokenKind.ROUND_CLOSE, None),
                    Token(TokenKind.MULTIPLY, None),
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
                    Token(TokenKind.COLON, None),
                    Token(TokenKind.IDENTIFIER, "Real"),
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
                    Token(TokenKind.COLON, None),
                    Token(TokenKind.IDENTIFIER, "Entero"),
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

        print(r""" __________________
< Testing lexer... >
 ------------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
----------------------------------------------------------------------""")
        unittest.main()