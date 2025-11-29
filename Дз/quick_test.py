from lexer import Lexer
from parser import Parser, Evaluator

input_text = "def CONFIG := ((0o1, 0o2), (0o3, 0o4))"
lexer = Lexer(input_text)
parser = Parser(lexer.tokens)
definitions = parser.parse()
evaluator = Evaluator(definitions)
print(evaluator.to_toml())