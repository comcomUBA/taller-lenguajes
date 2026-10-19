from lexer  import *
from parser import *

#================================================================

import unittest

#================================================================

if __name__ == "__main__":
    if len(sys.argv) > 1:
        t_b = lexer(test_file("test/" + sys.argv[1]))

        if "ex_" in sys.argv[1]:
            print(Expression.parse(t_b).__buildstr__())
        else:
            print(parser(t_b).__buildstr__())
    else:
        class TestParser(unittest.TestCase):
            def test_ex_complejo(self):
                r_1 = Expression.parse((lexer(test_file("test/ex_complejo.txt"))))
                r_2 = Expression.__build__(
                  ExpressionKind.INFIX,
                  (
                    Token(TokenKind.MULTIPLY, None),
                    Expression.__build__(
                      ExpressionKind.INFIX,
                      (
                        Token(TokenKind.DIVIDE, None),
                        Expression.__build__(
                          ExpressionKind.INFIX,
                          (
                            Token(TokenKind.ADD, None),
                            Expression.__build__(
                              ExpressionKind.ATOM,
                              2.0
                            ),
                            Expression.__build__(
                              ExpressionKind.ATOM,
                              2.0
                            ),
                          )
                        ),
                        Expression.__build__(
                          ExpressionKind.ATOM,
                          4.0
                        ),
                      )
                    ),
                    Expression.__build__(
                      ExpressionKind.ATOM,
                      8.0
                    ),
                  )
                )

                self.assertEqual(r_1, r_2)

            def test_ex_infijo(self):
                r_1 = Expression.parse((lexer(test_file("test/ex_infijo.txt"))))
                r_2 = Expression.__build__(
                  ExpressionKind.INFIX,
                  (
                    Token(TokenKind.SUBTRACT, None),
                    Expression.__build__(
                      ExpressionKind.INFIX,
                      (
                        Token(TokenKind.ADD, None),
                        Expression.__build__(
                          ExpressionKind.ATOM,
                          2.0
                        ),
                        Expression.__build__(
                          ExpressionKind.ATOM,
                          2.0
                        ),
                      )
                    ),
                    Expression.__build__(
                      ExpressionKind.INFIX,
                      (
                        Token(TokenKind.DIVIDE, None),
                        Expression.__build__(
                          ExpressionKind.INFIX,
                          (
                            Token(TokenKind.MULTIPLY, None),
                            Expression.__build__(
                              ExpressionKind.ATOM,
                              4.0
                            ),
                            Expression.__build__(
                              ExpressionKind.ATOM,
                              8.0
                            ),
                          )
                        ),
                        Expression.__build__(
                          ExpressionKind.ATOM,
                          16.0
                        ),
                      )
                    ),
                  )
                )

                self.assertEqual(r_1, r_2)

            def test_ex_prefijo(self):
                r_1 = Expression.parse((lexer(test_file("test/ex_prefijo.txt"))))
                r_2 = Expression.__build__(
                  ExpressionKind.INFIX,
                  (
                    Token(TokenKind.SUBTRACT, None),
                    Expression.__build__(
                      ExpressionKind.PREFIX,
                      (
                        Token(TokenKind.SUBTRACT, None),
                        Expression.__build__(
                          ExpressionKind.ATOM,
                          2.0
                        ),
                      )
                    ),
                    Expression.__build__(
                      ExpressionKind.ATOM,
                      4.0
                    ),
                  )
                )

                self.assertEqual(r_1, r_2)

            def test_ex_posfijo(self):
                r_1 = Expression.parse((lexer(test_file("test/ex_posfijo.txt"))))
                r_2 = Expression.__build__(
                  ExpressionKind.POSTFIX,
                  (
                    Token(TokenKind.BLOCK_BEGIN, None),
                    Expression.__build__(
                      ExpressionKind.ATOM,
                      "foo"
                    ),
                    Expression.__build__(
                      ExpressionKind.ATOM,
                      1.0
                    ),
                  )
                )

                self.assertEqual(r_1, r_2)

            def test_aux_distancia(self):
                r_1 = parser(lexer(test_file("test/aux_distancia.txt")))
                r_2 = Auxiliary.__build__(
                  Token(TokenKind.IDENTIFIER, "distancia"),
                  [
                    Parameter.__build__(False, Token(TokenKind.IDENTIFIER, "a"), Token(TokenKind.IDENTIFIER, "Vector")),
                    Parameter.__build__(False, Token(TokenKind.IDENTIFIER, "b"), Token(TokenKind.IDENTIFIER, "Vector")),
                  ],
                  Token(TokenKind.IDENTIFIER, "Real"),
                  [
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
                  ],
                )

                self.assertEqual(r_1, r_2)

            def test_aux_interpolacion(self):
                r_1 = parser(lexer(test_file("test/aux_interpolacion.txt")))
                r_2 = Auxiliary.__build__(
                  Token(TokenKind.IDENTIFIER, "interpolacion"),
                  [
                    Parameter.__build__(False, Token(TokenKind.IDENTIFIER, "t"), Token(TokenKind.IDENTIFIER, "Real")),
                    Parameter.__build__(False, Token(TokenKind.IDENTIFIER, "a"), Token(TokenKind.IDENTIFIER, "Real")),
                    Parameter.__build__(False, Token(TokenKind.IDENTIFIER, "b"), Token(TokenKind.IDENTIFIER, "Real")),
                  ],
                  Token(TokenKind.IDENTIFIER, "Real"),
                  [
                    Token(TokenKind.IDENTIFIER, "a"),
                    Token(TokenKind.ADD, None),
                    Token(TokenKind.IDENTIFIER, "t"),
                    Token(TokenKind.MULTIPLY, None),
                    Token(TokenKind.ROUND_BEGIN, None),
                    Token(TokenKind.IDENTIFIER, "b"),
                    Token(TokenKind.SUBTRACT, None),
                    Token(TokenKind.IDENTIFIER, "a"),
                    Token(TokenKind.ROUND_CLOSE, None),
                  ],
                )

                self.assertEqual(r_1, r_2)

            def test_aux_valorEntre(self):
                r_1 = parser(lexer(test_file("test/aux_valorEntre.txt")))
                r_2 = Auxiliary.__build__(
                  Token(TokenKind.IDENTIFIER, "valorEntre"),
                  [
                    Parameter.__build__(False, Token(TokenKind.IDENTIFIER, "v"), Token(TokenKind.IDENTIFIER, "Entero")),
                    Parameter.__build__(False, Token(TokenKind.IDENTIFIER, "min"), Token(TokenKind.IDENTIFIER, "Entero")),
                    Parameter.__build__(False, Token(TokenKind.IDENTIFIER, "max"), Token(TokenKind.IDENTIFIER, "Entero")),
                  ],
                  Token(TokenKind.IDENTIFIER, "Entero"),
                  [
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
                  ],
                )

                self.assertEqual(r_1, r_2)

            def test_pred_divide(self):
                r_1 = parser(lexer(test_file("test/pred_divide.txt")))
                r_2 = Predicate.__build__(
                  Token(TokenKind.IDENTIFIER, "divide"),
                  [
                    Parameter.__build__(False, Token(TokenKind.IDENTIFIER, "x"), Token(TokenKind.IDENTIFIER, "Entero")),
                    Parameter.__build__(False, Token(TokenKind.IDENTIFIER, "y"), Token(TokenKind.IDENTIFIER, "Entero")),
                  ],
                  [
                    Token(TokenKind.IDENTIFIER, "y"),
                    Token(TokenKind.MODULO, None),
                    Token(TokenKind.IDENTIFIER, "x"),
                    Token(TokenKind.EQUAL, None),
                    Token(TokenKind.NUMBER, 0.0),
                  ],
                )

                self.assertEqual(r_1, r_2)

            def test_pred_divide(self):
                r_1 = parser(lexer(test_file("test/pred_mayorPrimoQueDivide.txt")))
                r_2 = Predicate.__build__(
                  Token(TokenKind.IDENTIFIER, "mayorPrimoQueDivide"),
                  [
                    Parameter.__build__(False, Token(TokenKind.IDENTIFIER, "x"), Token(TokenKind.IDENTIFIER, "Entero")),
                    Parameter.__build__(False, Token(TokenKind.IDENTIFIER, "y"), Token(TokenKind.IDENTIFIER, "Entero")),
                  ],
                  [
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
                  ],
                )

                self.assertEqual(r_1, r_2)

            def test_pred_divide(self):
                r_1 = parser(lexer(test_file("test/pred_sonCoprimos.txt")))
                r_2 = Predicate.__build__(
                  Token(TokenKind.IDENTIFIER, "sonCoprimos"),
                  [
                    Parameter.__build__(False, Token(TokenKind.IDENTIFIER, "x"), Token(TokenKind.IDENTIFIER, "Entero")),
                    Parameter.__build__(False, Token(TokenKind.IDENTIFIER, "y"), Token(TokenKind.IDENTIFIER, "Entero")),
                  ],
                  [
                    Token(TokenKind.IDENTIFIER, "MCD"),
                    Token(TokenKind.ROUND_BEGIN, None),
                    Token(TokenKind.IDENTIFIER, "x"),
                    Token(TokenKind.COMMA, None),
                    Token(TokenKind.IDENTIFIER, "y"),
                    Token(TokenKind.ROUND_CLOSE, None),
                    Token(TokenKind.EQUAL, None),
                    Token(TokenKind.NUMBER, 1.0),
                  ],
                )

                self.assertEqual(r_1, r_2)

            def test_proc_esMultiploDe(self):
                r_1 = parser(lexer(test_file("test/proc_esMultiploDe.txt")))
                r_2 = Procedure.__build__(
                  Token(TokenKind.IDENTIFIER, "esMultiploDe"),
                  [
                    Parameter.__build__(False, Token(TokenKind.IDENTIFIER, "x"), Token(TokenKind.IDENTIFIER, "Real")),
                    Parameter.__build__(False, Token(TokenKind.IDENTIFIER, "y"), Token(TokenKind.IDENTIFIER, "Real")),
                  ],
                  Token(TokenKind.IDENTIFIER, "bool"),
                  [
                    Token(TokenKind.IDENTIFIER, "y"),
                    Token(TokenKind.GT, None),
                    Token(TokenKind.NUMBER, 0.0),
                  ],
                  [
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
                  ],
                )

                self.assertEqual(r_1, r_2)

            def test_proc_minimo(self):
                r_1 = parser(lexer(test_file("test/proc_minimo.txt")))
                r_2 = Procedure.__build__(
                  Token(TokenKind.IDENTIFIER, "minimo"),
                  [
                    Parameter.__build__(False, Token(TokenKind.IDENTIFIER, "s"), Token(TokenKind.IDENTIFIER, "SeqEntero")),
                  ],
                  Token(TokenKind.IDENTIFIER, "Entero"),
                  [
                    Token(TokenKind.PIPE, None),
                    Token(TokenKind.IDENTIFIER, "s"),
                    Token(TokenKind.PIPE, None),
                    Token(TokenKind.GT, None),
                    Token(TokenKind.NUMBER, 0.0),
                  ],
                  [
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
                  ],
                )

                self.assertEqual(r_1, r_2)

            def test_proc_todosPares(self):
                r_1 = parser(lexer(test_file("test/proc_todosPares.txt")))
                r_2 = Procedure.__build__(
                  Token(TokenKind.IDENTIFIER, "todosPares"),
                  [
                    Parameter.__build__(False, Token(TokenKind.IDENTIFIER, "s"), Token(TokenKind.IDENTIFIER, "SeqEntero")),
                  ],
                  Token(TokenKind.IDENTIFIER, "bool"),
                  [
                    Token(TokenKind.TRUE, None),
                  ],
                  [
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
                  ],
                )

                self.assertEqual(r_1, r_2)

            def test_tad(self):
                r_1 = parser(lexer(test_file("test/tad.txt")))
                r_2 = ADT.__build__(
                  Token(TokenKind.IDENTIFIER, "Vector"),
                  [
                    Observer.__build__(Token(TokenKind.IDENTIFIER, "x"), Token(TokenKind.IDENTIFIER, "Real")),
                    Observer.__build__(Token(TokenKind.IDENTIFIER, "y"), Token(TokenKind.IDENTIFIER, "Real")),
                  ],
                  [
                    Procedure.__build__(
                      Token(TokenKind.IDENTIFIER, "nuevoVector"),
                      [
                        Parameter.__build__(True, Token(TokenKind.IDENTIFIER, "x"), Token(TokenKind.IDENTIFIER, "Real")),
                        Parameter.__build__(False, Token(TokenKind.IDENTIFIER, "y"), Token(TokenKind.IDENTIFIER, "Real")),
                      ],
                      Token(TokenKind.IDENTIFIER, "Vector"),
                      [
                        Token(TokenKind.TRUE, None),
                      ],
                      [
                        Token(TokenKind.RESULT, None),
                        Token(TokenKind.DOT, None),
                        Token(TokenKind.IDENTIFIER, "x"),
                        Token(TokenKind.EQUAL, None),
                        Token(TokenKind.IDENTIFIER, "x"),
                        Token(TokenKind.AND, None),
                        Token(TokenKind.RESULT, None),
                        Token(TokenKind.DOT, None),
                        Token(TokenKind.IDENTIFIER, "y"),
                        Token(TokenKind.EQUAL, None),
                        Token(TokenKind.IDENTIFIER, "y"),
                      ],
                    ),
                  ],
                  [
                    Predicate.__build__(
                      Token(TokenKind.IDENTIFIER, "esNulo"),
                      [
                        Parameter.__build__(False, Token(TokenKind.IDENTIFIER, "a"), Token(TokenKind.IDENTIFIER, "Vector")),
                      ],
                      [
                        Token(TokenKind.IDENTIFIER, "a"),
                        Token(TokenKind.DOT, None),
                        Token(TokenKind.IDENTIFIER, "x"),
                        Token(TokenKind.EQUAL, None),
                        Token(TokenKind.NUMBER, 0.0),
                        Token(TokenKind.AND, None),
                        Token(TokenKind.IDENTIFIER, "a"),
                        Token(TokenKind.DOT, None),
                        Token(TokenKind.IDENTIFIER, "y"),
                        Token(TokenKind.EQUAL, None),
                        Token(TokenKind.NUMBER, 0.0),
                      ],
                    ),
                  ],
                  [
                    Auxiliary.__build__(
                      Token(TokenKind.IDENTIFIER, "distancia"),
                      [
                        Parameter.__build__(False, Token(TokenKind.IDENTIFIER, "a"), Token(TokenKind.IDENTIFIER, "Vector")),
                        Parameter.__build__(False, Token(TokenKind.IDENTIFIER, "b"), Token(TokenKind.IDENTIFIER, "Vector")),
                      ],
                      Token(TokenKind.IDENTIFIER, "Real"),
                      [
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
                      ],
                    ),
                  ],
                )

                self.assertEqual(r_1, r_2)

        print(r""" ___________________
< Testing parser... >
 -------------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
----------------------------------------------------------------------""")
        unittest.main()