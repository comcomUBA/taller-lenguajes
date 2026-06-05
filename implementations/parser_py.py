from dataclasses import dataclass, fields, is_dataclass
from typing import Any
import ply.yacc as yacc
from node import *

#================================================================

# -----------------------------------------------------------------------------
# Hand-written lexer with the PLY-compatible interface yacc needs.
# -----------------------------------------------------------------------------

@dataclass
class LexToken:
    type: str
    value: Any
    lineno: int
    lexpos: int


reserved = {
    "let": "LET",
    "if": "IF",
    "then": "THEN",
    "else": "ELSE",
    "elsif": "ELSIF",
    "while": "WHILE",
    "return": "RETURN",
    "true": "TRUE",
    "false": "FALSE",
    "nil": "NIL",
    "not": "NOT",
    "or": "OR",
    "and": "AND",
    "do": "DO",
    "end": "END",
}


tokens = (
    "ID",
    "NUMBER",
    "STRING",
    "SEMI",
    "COMMA",
    "LPAREN",
    "RPAREN",
    "LBRACKET",
    "RBRACKET",
    "BAR",
    "PLUS",
    "MINUS",
    "TIMES",
    "DIVIDE",
    "MOD",
    "ASSIGN",
    "EQ",
    "NE",
    "LT",
    "LE",
    "GT",
    "GE",
    *reserved.values(),
)


class LexerError(SyntaxError):
    pass


class TLLexer:
    def input(self, text: str) -> None:
        self.text = text
        self.pos = 0
        self.lineno = 1

    def token(self) -> LexToken | None:
        text = self.text
        n = len(text)

        while self.pos < n:
            ch = text[self.pos]

            if ch in " \t\r":
                self.pos += 1
                continue

            if ch == "\n":
                self.lineno += 1
                self.pos += 1
                continue

            if ch == "#":
                while self.pos < n and text[self.pos] != "\n":
                    self.pos += 1
                continue

            break

        if self.pos >= n:
            return None

        start = self.pos
        ch = text[self.pos]

        two_char = {
            "==": "EQ",
            "!=": "NE",
            "<=": "LE",
            ">=": "GE",
        }
        raw2 = text[self.pos : self.pos + 2]
        if raw2 in two_char:
            self.pos += 2
            return LexToken(two_char[raw2], raw2, self.lineno, start)

        one_char = {
            ";": "SEMI",
            ",": "COMMA",
            "(": "LPAREN",
            ")": "RPAREN",
            "[": "LBRACKET",
            "]": "RBRACKET",
            "|": "BAR",
            "+": "PLUS",
            "-": "MINUS",
            "*": "TIMES",
            "/": "DIVIDE",
            "%": "MOD",
            "=": "ASSIGN",
            "<": "LT",
            ">": "GT",
        }
        if ch in one_char:
            self.pos += 1
            return LexToken(one_char[ch], ch, self.lineno, start)

        if ch == '"':
            return self._read_string()

        if ch.isdigit():
            return self._read_number()

        if ch.isalpha() or ch == "_":
            return self._read_identifier()

        raise LexerError(f"Unexpected character {ch!r} at line {self.lineno}, position {self.pos}")

    def _read_identifier(self) -> LexToken:
        start = self.pos
        text = self.text

        while self.pos < len(text) and (text[self.pos].isalnum() or text[self.pos] == "_"):
            self.pos += 1

        raw = text[start : self.pos]
        typ = reserved.get(raw, "ID")

        if typ == "TRUE":
            value: Any = True
        elif typ == "FALSE":
            value = False
        elif typ == "NIL":
            value = None
        else:
            value = raw

        return LexToken(typ, value, self.lineno, start)

    def _read_number(self) -> LexToken:
        start = self.pos
        text = self.text

        while self.pos < len(text) and text[self.pos].isdigit():
            self.pos += 1

        is_float = False
        if self.pos < len(text) and text[self.pos] == ".":
            if self.pos + 1 < len(text) and text[self.pos + 1].isdigit():
                is_float = True
                self.pos += 1
                while self.pos < len(text) and text[self.pos].isdigit():
                    self.pos += 1

        raw = text[start : self.pos]
        return LexToken("NUMBER", float(raw) if is_float else int(raw), self.lineno, start)

    def _read_string(self) -> LexToken:
        start = self.pos
        self.pos += 1
        out: list[str] = []
        text = self.text

        escapes = {
            "n": "\n",
            "r": "\r",
            "t": "\t",
            '"': '"',
            "\\": "\\",
        }

        while self.pos < len(text):
            ch = text[self.pos]

            if ch == '"':
                self.pos += 1
                return LexToken("STRING", "".join(out), self.lineno, start)

            if ch == "\\":
                self.pos += 1
                if self.pos >= len(text):
                    raise LexerError(f"Unterminated escape at line {self.lineno}")
                esc = text[self.pos]
                out.append(escapes.get(esc, esc))
                self.pos += 1
                continue

            if ch == "\n":
                raise LexerError(f"Unterminated string at line {self.lineno}")

            out.append(ch)
            self.pos += 1

        raise LexerError(f"Unterminated string at line {self.lineno}")


# -----------------------------------------------------------------------------
# PLY yacc grammar
# -----------------------------------------------------------------------------


start = "stmt_list_opt"


def p_stmt_list_opt(p):
    """stmt_list_opt : stmt_list
                     | empty"""
    p[0] = p[1] or []


def p_stmt_list_single(p):
    """stmt_list : statement"""
    p[0] = [p[1]]


def p_stmt_list_many(p):
    """stmt_list : stmt_list statement"""
    p[0] = p[1] + [p[2]]


# The semicolon rule is enforced here: only block statements can omit ';'.


def p_statement_simple(p):
    """statement : simple_stmt SEMI"""
    p[0] = p[1]


def p_statement_block(p):
    """statement : if_stmt
                 | while_stmt"""
    p[0] = p[1]


def p_simple_stmt_let(p):
    """simple_stmt : LET ID
                   | LET ID ASSIGN expression"""
    p[0] = Let(p[2], p[4] if len(p) == 5 else None)


def p_simple_stmt_return(p):
    """simple_stmt : RETURN
                   | RETURN expression"""
    p[0] = Return(p[2] if len(p) == 3 else None)


def p_simple_stmt_expr(p):
    """simple_stmt : expression"""
    p[0] = ExprStmt(p[1])


def p_block(p):
    """block : DO stmt_list_opt END"""
    p[0] = Block(p[2])


def p_while_stmt(p):
    """while_stmt : WHILE expression block"""
    p[0] = While(p[2], p[3])


def p_if_stmt(p):
    """if_stmt : IF expression THEN stmt_list_opt elsif_parts else_part END"""
    p[0] = If(p[2], Block(p[4]), p[5], p[6])


def p_elsif_parts_empty(p):
    """elsif_parts : empty"""
    p[0] = []


def p_elsif_parts_many(p):
    """elsif_parts : elsif_parts ELSIF expression THEN stmt_list_opt"""
    p[0] = p[1] + [(p[3], Block(p[5]))]


def p_else_part_empty(p):
    """else_part : empty"""
    p[0] = None


def p_else_part_stmts(p):
    """else_part : ELSE stmt_list_opt"""
    p[0] = Block(p[2])


# Expressions, from lowest to highest precedence.


def p_expression(p):
    """expression : assignment"""
    p[0] = p[1]


def p_assignment_plain(p):
    """assignment : logic_or"""
    p[0] = p[1]


def p_assignment_assign(p):
    """assignment : lvalue ASSIGN assignment"""
    p[0] = Assign(p[1], p[3])


def p_lvalue_var(p):
    """lvalue : ID"""
    p[0] = Var(p[1])


def p_logic_or_plain(p):
    """logic_or : logic_and"""
    p[0] = p[1]


def p_logic_or_binary(p):
    """logic_or : logic_or OR logic_and"""
    p[0] = BinaryOp(p[2], p[1], p[3])


def p_logic_and_plain(p):
    """logic_and : equality"""
    p[0] = p[1]


def p_logic_and_binary(p):
    """logic_and : logic_and AND equality"""
    p[0] = BinaryOp(p[2], p[1], p[3])


def p_equality_plain(p):
    """equality : comparison"""
    p[0] = p[1]


def p_equality_binary(p):
    """equality : equality EQ comparison
                | equality NE comparison"""
    p[0] = BinaryOp(p[2], p[1], p[3])


def p_comparison_plain(p):
    """comparison : term"""
    p[0] = p[1]


def p_comparison_binary(p):
    """comparison : comparison LT term
                  | comparison LE term
                  | comparison GT term
                  | comparison GE term"""
    p[0] = BinaryOp(p[2], p[1], p[3])


def p_term_plain(p):
    """term : factor"""
    p[0] = p[1]


def p_term_binary(p):
    """term : term PLUS factor
            | term MINUS factor"""
    p[0] = BinaryOp(p[2], p[1], p[3])


def p_factor_plain(p):
    """factor : unary"""
    p[0] = p[1]


def p_factor_binary(p):
    """factor : factor TIMES unary
              | factor DIVIDE unary
              | factor MOD unary"""
    p[0] = BinaryOp(p[2], p[1], p[3])


def p_unary_plain(p):
    """unary : postfix"""
    p[0] = p[1]


def p_unary_op(p):
    """unary : NOT unary
             | MINUS unary"""
    p[0] = UnaryOp(p[1], p[2])


def p_postfix_plain(p):
    """postfix : primary"""
    p[0] = p[1]


def p_postfix_call(p):
    """postfix : postfix LPAREN arg_list_opt RPAREN"""
    p[0] = Call(p[1], p[3])


def p_primary_id(p):
    """primary : ID"""
    p[0] = Var(p[1])


def p_primary_literal(p):
    """primary : NUMBER
               | STRING
               | TRUE
               | FALSE
               | NIL"""
    p[0] = Literal(p[1])


def p_primary_group(p):
    """primary : LPAREN expression RPAREN"""
    p[0] = p[2]


def p_primary_array(p):
    """primary : array"""
    p[0] = p[1]


def p_primary_lambda(p):
    """primary : lambda_literal"""
    p[0] = p[1]


def p_array(p):
    """array : LBRACKET arg_list_opt RBRACKET"""
    p[0] = Array(p[2])


def p_lambda_literal(p):
    """lambda_literal : BAR params_opt BAR block"""
    p[0] = Lambda(p[2], p[4])


def p_params_opt(p):
    """params_opt : param_list
                  | empty"""
    p[0] = p[1] or []


def p_param_list_single(p):
    """param_list : ID"""
    p[0] = [p[1]]


def p_param_list_many(p):
    """param_list : param_list COMMA ID"""
    p[0] = p[1] + [p[3]]


def p_arg_list_opt(p):
    """arg_list_opt : arg_list
                    | empty"""
    p[0] = p[1] or []


def p_arg_list_single(p):
    """arg_list : expression"""
    p[0] = [p[1]]


def p_arg_list_many(p):
    """arg_list : arg_list COMMA expression"""
    p[0] = p[1] + [p[3]]


def p_empty(p):
    """empty :"""
    p[0] = None


def p_error(p):
    if p is None:
        raise SyntaxError("Unexpected end of input. A statement may be missing a trailing ';'.")

    raise SyntaxError(
        f"Unexpected token {p.type}({p.value!r}) at line {getattr(p, 'lineno', '?')}, "
        f"position {getattr(p, 'lexpos', '?')}. "
        "Simple statements must end with ';'; only if/while blocks ending in '}' omit it."
    )


parser = yacc.yacc(debug=False, write_tables=False)


def parse(source: str) -> list[Any]:
    lexer = TLLexer()
    return parser.parse(source, lexer=lexer)


def parse_file(path: str) -> list[Any]:
    with open(path, "r", encoding="utf-8") as f:
        return parse(f.read())


def ast_to_data(node: Any) -> Any:
    if is_dataclass(node):
        return {
            "node": type(node).__name__,
            **{field.name: ast_to_data(getattr(node, field.name)) for field in fields(node)},
        }
    if isinstance(node, tuple):
        return [ast_to_data(x) for x in node]
    if isinstance(node, list):
        return [ast_to_data(x) for x in node]
    return node