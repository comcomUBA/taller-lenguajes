from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional
import ast as py_ast
import sys

import ply.yacc as yacc


# =============================================================================
# AST nodes
# =============================================================================

@dataclass(frozen=True)
class Let:
    name: str
    value: Optional[Any]


@dataclass(frozen=True)
class Assign:
    name: str
    value: Any


@dataclass(frozen=True)
class Return:
    value: Optional[Any]


@dataclass(frozen=True)
class If:
    condition: Any
    then_body: list[Any]
    elsif_parts: list[tuple[Any, list[Any]]]
    else_body: Optional[list[Any]]


@dataclass(frozen=True)
class While:
    condition: Any
    body: list[Any]


@dataclass(frozen=True)
class Block:
    statements: list[Any]


@dataclass(frozen=True)
class Lambda:
    params: list[str]
    body: Any


@dataclass(frozen=True)
class Binary:
    op: str
    left: Any
    right: Any


@dataclass(frozen=True)
class Unary:
    op: str
    value: Any


@dataclass(frozen=True)
class Call:
    func: Any
    args: list[Any]


@dataclass(frozen=True)
class Index:
    collection: Any
    index: Any


@dataclass(frozen=True)
class ArrayLiteral:
    items: list[Any]


@dataclass(frozen=True)
class Literal:
    value: Any


@dataclass(frozen=True)
class Name:
    value: str


# =============================================================================
# Hand-written lexer
# =============================================================================

reserved = {
    "let": "LET",
    "if": "IF",
    "then": "THEN",
    "elsif": "ELSIF",
    "else": "ELSE",
    "while": "WHILE",
    "do": "DO",
    "end": "END",
    "return": "RETURN",
    "true": "TRUE",
    "false": "FALSE",
    "nil": "NIL",
    "null": "NIL",
    "and": "AND",
    "or": "OR",
    "not": "NOT",
}

# PLY yacc needs this variable to know the terminal names.
tokens = [
    "ID",
    "NUMBER",
    "STRING",

    "EQ",
    "NE",
    "LE",
    "GE",
    "LT",
    "GT",

    "ASSIGN",
    "PLUS",
    "MINUS",
    "TIMES",
    "DIVIDE",
    "MOD",

    "LPAREN",
    "RPAREN",
    "LBRACKET",
    "RBRACKET",
    "COMMA",
    "SEMI",
    "BAR",
] + sorted(set(reserved.values()))


@dataclass
class LexToken:
    type: str
    value: Any
    lineno: int
    lexpos: int

    def __repr__(self) -> str:
        return f"LexToken({self.type},{self.value!r},{self.lineno},{self.lexpos})"


class TLLexer:
    single_char_tokens = {
        "=": "ASSIGN",
        "+": "PLUS",
        "-": "MINUS",
        "*": "TIMES",
        "/": "DIVIDE",
        "%": "MOD",
        "(": "LPAREN",
        ")": "RPAREN",
        "[": "LBRACKET",
        "]": "RBRACKET",
        ",": "COMMA",
        ";": "SEMI",
        "|": "BAR",
        "<": "LT",
        ">": "GT",
    }

    two_char_tokens = {
        "==": "EQ",
        "!=": "NE",
        "<=": "LE",
        ">=": "GE",
    }

    def input(self, text: str) -> None:
        self.text = text
        self.pos = 0
        self.lineno = 1

    def token(self) -> Optional[LexToken]:
        text = self.text
        n = len(text)

        while self.pos < n:
            ch = text[self.pos]

            if ch in " \t\r":
                self.pos += 1
                continue

            if ch == "\n":
                self.pos += 1
                self.lineno += 1
                continue

            if ch == "#":
                while self.pos < n and text[self.pos] != "\n":
                    self.pos += 1
                continue

            break

        if self.pos >= n:
            return None

        start = self.pos
        lineno = self.lineno

        # Strings: double quoted, Python-like escapes accepted.
        if text[start] == '"':
            self.pos += 1
            escaped = False
            while self.pos < n:
                ch = text[self.pos]
                if ch == "\n" and not escaped:
                    raise SyntaxError(f"Unterminated string at line {lineno}, lexpos {start}")
                if ch == '"' and not escaped:
                    self.pos += 1
                    raw = text[start:self.pos]
                    return LexToken("STRING", py_ast.literal_eval(raw), lineno, start)
                escaped = (ch == "\\" and not escaped)
                if ch != "\\":
                    escaped = False
                self.pos += 1
            raise SyntaxError(f"Unterminated string at line {lineno}, lexpos {start}")

        # Numbers: integers and decimal floats.
        ch = text[start]
        if ch.isdigit() or (ch == "." and start + 1 < n and text[start + 1].isdigit()):
            if ch == ".":
                self.pos += 1
                while self.pos < n and text[self.pos].isdigit():
                    self.pos += 1
                return LexToken("NUMBER", float(text[start:self.pos]), lineno, start)

            while self.pos < n and text[self.pos].isdigit():
                self.pos += 1

            if self.pos < n and text[self.pos] == ".":
                self.pos += 1
                while self.pos < n and text[self.pos].isdigit():
                    self.pos += 1
                return LexToken("NUMBER", float(text[start:self.pos]), lineno, start)

            return LexToken("NUMBER", int(text[start:self.pos]), lineno, start)

        # Identifiers and reserved words.
        if ch.isalpha() or ch == "_":
            self.pos += 1
            while self.pos < n and (text[self.pos].isalnum() or text[self.pos] == "_"):
                self.pos += 1
            value = text[start:self.pos]
            return LexToken(reserved.get(value, "ID"), value, lineno, start)

        # Operators and punctuation.
        two = text[start:start + 2]
        if two in self.two_char_tokens:
            self.pos += 2
            return LexToken(self.two_char_tokens[two], two, lineno, start)

        if ch in self.single_char_tokens:
            self.pos += 1
            return LexToken(self.single_char_tokens[ch], ch, lineno, start)

        raise SyntaxError(f"Illegal character {ch!r} at line {lineno}, lexpos {start}")


# =============================================================================
# Parser
# =============================================================================

#precedence = (
#    ("left", "OR"),
#    ("left", "AND"),
#    ("right", "NOT"),
#    ("nonassoc", "EQ", "NE", "LT", "LE", "GT", "GE"),
#    ("left", "PLUS", "MINUS"),
#    ("left", "TIMES", "DIVIDE", "MOD"),
#    ("right", "UMINUS"),
#)

start="p_program"

def p_program(p):
    """
    program : statement_list
    """
    p[0] = Program(p[1])


# -----------------------------------------------------------------------------
# Statement lists and the semicolon rule
# -----------------------------------------------------------------------------
#
# statement_list is right-recursive.
#
# After a simple statement, there are only two possibilities:
#   1. it is the final statement of the current list;
#   2. it is followed by ';' and then another statement list.
#
# Therefore this rejects:
#   print(1) print(2)
#
# but accepts:
#   print(1); print(2)
#   print(1)
#
# After a block statement, whose outer syntax ends in END, the following
# statement may appear with or without ';'.
# -----------------------------------------------------------------------------


def p_statement_list_empty(p):
    """
    statement_list :
    """
    p[0] = []


def p_statement_list_simple(p):
    """
    statement_list : simple_statement after_simple_statement
    """
    p[0] = [p[1]] + p[2]


def p_statement_list_block(p):
    """
    statement_list : block_statement after_block_statement
    """
    p[0] = [p[1]] + p[2]


def p_after_simple_statement_final(p):
    """
    after_simple_statement :
    """
    p[0] = []


def p_after_simple_statement_more(p):
    """
    after_simple_statement : SEMI statement_list
    """
    p[0] = p[2]


def p_after_block_statement_no_semi(p):
    """
    after_block_statement : statement_list
    """
    p[0] = p[1]


def p_after_block_statement_with_semi(p):
    """
    after_block_statement : SEMI statement_list
    """
    p[0] = p[2]


# -----------------------------------------------------------------------------
# Statements
# -----------------------------------------------------------------------------


def p_simple_statement_let_no_initializer(p):
    """
    simple_statement : LET ID
    """
    p[0] = Let(p[2], None)


def p_simple_statement_let_with_initializer(p):
    """
    simple_statement : LET ID ASSIGN expr
    """
    p[0] = Let(p[2], p[4])


def p_simple_statement_assignment(p):
    """
    simple_statement : ID ASSIGN expr
    """
    p[0] = Assign(p[1], p[3])


def p_simple_statement_return_empty(p):
    """
    simple_statement : RETURN
    """
    p[0] = Return(None)


def p_simple_statement_return_value(p):
    """
    simple_statement : RETURN expr
    """
    p[0] = Return(p[2])


def p_simple_statement_expr(p):
    """
    simple_statement : nonblock_expr
    """
    p[0] = p[1]


def p_block_statement_if(p):
    """
    block_statement : if_statement
    """
    p[0] = p[1]


def p_block_statement_while(p):
    """
    block_statement : while_statement
    """
    p[0] = p[1]


def p_block_statement_do(p):
    """
    block_statement : do_block
    """
    p[0] = p[1]


# -----------------------------------------------------------------------------
# Control flow and block expressions
# -----------------------------------------------------------------------------


def p_if_statement(p):
    """
    if_statement : IF expr THEN statement_list elsif_list else_part END
    """
    p[0] = If(p[2], p[4], p[5], p[6])


def p_elsif_list_empty(p):
    """
    elsif_list :
    """
    p[0] = []


def p_elsif_list_more(p):
    """
    elsif_list : elsif_list ELSIF expr THEN statement_list
    """
    p[0] = p[1] + [(p[3], p[5])]


def p_else_part_empty(p):
    """
    else_part :
    """
    p[0] = None


def p_else_part_some(p):
    """
    else_part : ELSE statement_list
    """
    p[0] = p[2]


def p_while_statement(p):
    """
    while_statement : WHILE expr DO statement_list END
    """
    p[0] = While(p[2], p[4])


def p_do_block(p):
    """
    do_block : DO statement_list END
    """
    p[0] = Block(p[2])


# -----------------------------------------------------------------------------
# Expressions
# -----------------------------------------------------------------------------


def p_expr_lambda(p):
    """
    expr : lambda_expr
    """
    p[0] = p[1]


def p_expr_do_block(p):
    """
    expr : do_block
    """
    p[0] = p[1]


def p_expr_nonblock(p):
    """
    expr : nonblock_expr
    """
    p[0] = p[1]


def p_lambda_expr(p):
    """
    lambda_expr : BAR param_list_opt BAR expr
    """
    p[0] = Lambda(p[2], p[4])


def p_param_list_opt_empty(p):
    """
    param_list_opt :
    """
    p[0] = []


def p_param_list_opt_some(p):
    """
    param_list_opt : param_list
    """
    p[0] = p[1]


def p_param_list_one(p):
    """
    param_list : ID
    """
    p[0] = [p[1]]


def p_param_list_more(p):
    """
    param_list : param_list COMMA ID
    """
    p[0] = p[1] + [p[3]]


def p_nonblock_expr_binary(p):
    """
    nonblock_expr : nonblock_expr OR nonblock_expr
                  | nonblock_expr AND nonblock_expr
                  | nonblock_expr EQ nonblock_expr
                  | nonblock_expr NE nonblock_expr
                  | nonblock_expr LT nonblock_expr
                  | nonblock_expr LE nonblock_expr
                  | nonblock_expr GT nonblock_expr
                  | nonblock_expr GE nonblock_expr
                  | nonblock_expr PLUS nonblock_expr
                  | nonblock_expr MINUS nonblock_expr
                  | nonblock_expr TIMES nonblock_expr
                  | nonblock_expr DIVIDE nonblock_expr
                  | nonblock_expr MOD nonblock_expr
    """
    p[0] = Binary(p[2], p[1], p[3])


def p_nonblock_expr_not(p):
    """
    nonblock_expr : NOT nonblock_expr
    """
    p[0] = Unary("not", p[2])


def p_nonblock_expr_uminus(p):
    """
    nonblock_expr : MINUS nonblock_expr %prec UMINUS
    """
    p[0] = Unary("-", p[2])


def p_nonblock_expr_postfix(p):
    """
    nonblock_expr : postfix_expr
    """
    p[0] = p[1]


def p_postfix_expr_primary(p):
    """
    postfix_expr : primary
    """
    p[0] = p[1]


def p_postfix_expr_call(p):
    """
    postfix_expr : postfix_expr LPAREN arg_list_opt RPAREN
    """
    p[0] = Call(p[1], p[3])


def p_postfix_expr_index(p):
    """
    postfix_expr : postfix_expr LBRACKET expr RBRACKET
    """
    p[0] = Index(p[1], p[3])


def p_arg_list_opt_empty(p):
    """
    arg_list_opt :
    """
    p[0] = []


def p_arg_list_opt_some(p):
    """
    arg_list_opt : arg_list
    """
    p[0] = p[1]


def p_arg_list_one(p):
    """
    arg_list : expr
    """
    p[0] = [p[1]]


def p_arg_list_more(p):
    """
    arg_list : arg_list COMMA expr
    """
    p[0] = p[1] + [p[3]]


def p_primary_number(p):
    """
    primary : NUMBER
    """
    p[0] = Literal(p[1])


def p_primary_string(p):
    """
    primary : STRING
    """
    p[0] = Literal(p[1])


def p_primary_true(p):
    """
    primary : TRUE
    """
    p[0] = Literal(True)


def p_primary_false(p):
    """
    primary : FALSE
    """
    p[0] = Literal(False)


def p_primary_nil(p):
    """
    primary : NIL
    """
    p[0] = Literal(None)


def p_primary_name(p):
    """
    primary : ID
    """
    p[0] = Name(p[1])


def p_primary_group(p):
    """
    primary : LPAREN expr RPAREN
    """
    p[0] = p[2]


def p_primary_array_literal(p):
    """
    primary : LBRACKET arg_list_opt RBRACKET
    """
    p[0] = ArrayLiteral(p[2])


# -----------------------------------------------------------------------------
# Errors and public API
# -----------------------------------------------------------------------------


def p_error(p):
    if p is None:
        raise SyntaxError("Unexpected end of input")

    raise SyntaxError(
        f"Unexpected token {p.type}({p.value!r}) at line "
        f"{getattr(p, 'lineno', '?')}, lexpos {getattr(p, 'lexpos', '?')}"
    )


parser = yacc.yacc(debug=False, write_tables=False)


def parse(text: str) -> Program:
    lexer = TLLexer()
    return parser.parse(text, lexer=lexer)


def parse_file(path: str) -> Program:
    with open(path, "r", encoding="utf-8") as f:
        return parse(f.read())


if __name__ == "__main__":
    from pprint import pprint

    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} file.tl", file=sys.stderr)
        raise SystemExit(2)

    pprint(parse_file(sys.argv[1]))
