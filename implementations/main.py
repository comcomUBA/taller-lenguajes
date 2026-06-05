import sys
import json
from parser_js import parse_file, ast_to_data
from visitor import ASTPrinter, ASTCompiler
from machine import VM, VMFunc

#================================================================

def main(argv: list[str]) -> int:
    if not argv:
        print("Usage: python tl_ply_parser.py FILE.tl [FILE.tl ...]", file=sys.stderr)
        return 2

    ok = True
    for filename in argv:
        print(f"== {filename} ==")
        try:
            tree = parse_file(filename)
        except Exception as exc:
            ok = False
            print(f"Syntax error: {exc}", file=sys.stderr)
            continue
        print(f"== {filename}: JSON ==")
        print(json.dumps(ast_to_data(tree), indent=2, ensure_ascii=False))

        print(f"== {filename}: AST ==")
        visitor = ASTPrinter()
        for statement in tree:
            statement.accept(visitor)

        visitor = ASTCompiler()
        for statement in tree:
            statement.accept(visitor)
        module_code = VMFunc(visitor.instructions)

        print(f"== {filename}: Bytecode ==")
        module_code.print_bytecode()

        print(f"== {filename}: Execution ==")
        VM(module_code).run()

    return 0 if ok else 1

if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))