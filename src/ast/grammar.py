from lark import Lark, ast_utils
from lark.exceptions import UnexpectedToken
from lyra.ast.transformer import LyraTransformer, transformer_module

def lyra_grammar():
    with open("./lyra/ast/grammar.lark", "r") as fp:
        lyra_parser = Lark(fp.read(), start="module", parser='lalr')

    return lyra_parser

def parse_lyra_source(code, source=None):
    code = code + "\n"
    source = source if source else "<source>"
    err_msg = ""
    code_lines = code.split("\n")

    try:
        return lyra_grammar().parse(code)
    except UnexpectedToken as err:
        line = err.line
        column = err.column
        token = err.token
        err_msg = f"{source}:{line}:{column} "
        err_msg += f"Syntax error: Unexpected token {repr(token.value)}\n"
        err_msg += code_lines[line-1] + "\n"
        err_msg += " "*(column-1) + "^"
        print(err_msg)
        exit(1)

def parse_lyra_tree(code):
    transformer = ast_utils.create_transformer(transformer_module, LyraTransformer())
    return transformer.transform(parse_lyra_source(code))
