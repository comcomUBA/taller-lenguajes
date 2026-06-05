import sys

class Token():
    Let        = "Let"
    If         = "If"
    While      = "While"
    Not        = "Not"
    Define     = "Define"
    Equal      = "Equal"
    GT         = "GT"
    LT         = "LT"
    GTE        = "GTE"
    LTE        = "LTE"
    Add        = "Add"
    Subtract   = "Subtract"
    Multiply   = "Multiply"
    Divide     = "Divide"
    Pipe       = "Pipe"
    RoundBegin = "RoundBegin"
    RoundClose = "RoundClose"
    CurlyBegin = "CurlyBegin"
    CurlyClose = "CurlyClose"
    BlockBegin = "BlockBegin"
    BlockClose = "BlockClose"
    Comma      = "Comma"
    ColonSemi  = "ColonSemi"
    Identifier = "Identifier"
    String     = "String"
    Number     = "Number"
    Boolean    = "Boolean"

    def __init__(self, kind: str, data: any):
        self.kind = kind
        self.data = data

    def __str__(self):
        data = ""

        if self.data != None:
            data = str(self.data)

        return "Token::" + self.kind + "(" + data + ")"

def parse_file(path: str):
    list: [Token] = []

    for line in open(path).readlines():
        parse_line(line.strip(), list)

    for token in list:
        print(str(token))

def parse_line(line: str, list: [Token]):
    buffer = []
    string = False
    cursor = 0

    while True:
        if cursor >= len(line):
            break;

        character = line[cursor]

        match character:
            case '"':
                buffer.append(character)

                if string:
                    string = False

                    list.append(parse_text("".join(buffer)))
                    buffer.clear()
                else:
                    string = True
            case ' ':
                if string:
                    buffer.append(character)
                else:
                    if len(buffer) > 0:
                        list.append(parse_text("".join(buffer)))
                        buffer.clear()
            case _:
                if not string and character in ["=", ">", "<", "+", "-", "*", "/", "|", "(", ")", "{", "}", "[", "]", ",", ";"]:
                    if len(buffer) > 0:
                        list.append(parse_text("".join(buffer)))
                        buffer.clear()

                    if character in [">", "<", "="]:
                        if cursor < len(line) and line[cursor + 1] == "=":
                            list.append(parse_text(character + "="))
                            cursor += 1
                        else:
                            list.append(parse_text(character))
                    else:
                        list.append(parse_text(character))
                else:
                    buffer.append(character)

        cursor += 1

    if len(buffer) > 0:
        list.append(parse_text("".join(buffer)))
        buffer.clear()

def parse_text(text: str) -> Token:
    look_up = {
        "let"   : Token(Token.Let,        None),
        "if"    : Token(Token.If,         None),
        "while" : Token(Token.While,      None),
        "not"   : Token(Token.Not,        None),
        "true"  : Token(Token.Boolean,    True),
        "false" : Token(Token.Boolean,    False),
        "="     : Token(Token.Define,     None),
        "=="    : Token(Token.Equal,      None),
        ">"     : Token(Token.GT,         None),
        "<"     : Token(Token.LT,         None),
        ">="    : Token(Token.GTE,        None),
        "<="    : Token(Token.LTE,        None),
        "+"     : Token(Token.Add,        None),
        "-"     : Token(Token.Subtract,   None),
        "*"     : Token(Token.Multiply,   None),
        "/"     : Token(Token.Divide,     None),
        "|"     : Token(Token.Pipe,       None),
        "("     : Token(Token.RoundBegin, None),
        ")"     : Token(Token.RoundClose, None),
        "{"     : Token(Token.CurlyBegin, None),
        "}"     : Token(Token.CurlyClose, None),
        "["     : Token(Token.BlockBegin, None),
        "]"     : Token(Token.BlockClose, None),
        ","     : Token(Token.Comma,      None),
        ";"     : Token(Token.ColonSemi,  None),
    }

    if text in look_up:
        return look_up[text]
    else:
        if text[0] == '"':
            return Token(Token.String, text)
        else:
            if is_numeric(text):
                return Token(Token.Number, float(text))
            else:
                return Token(Token.Identifier, text)

def is_numeric(text: str) -> bool:
    dot = False

    for character in text:
        if not character.isnumeric():
            match character:
                case ".":
                    if dot:
                        return False
                    else:
                        dot = True
                case _:
                    return False

    return True

if len(sys.argv) > 1:
    path = sys.argv[1]
    parse_file("../snippets/javascriptese/" + path)
else:
    print("Example: lux.py bfs.tl")