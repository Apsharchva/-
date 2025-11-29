#!/usr/bin/env python3
import sys
from lexer import Lexer
from parser import Parser, Evaluator

def main():
    try:
        # Чтение из стандартного ввода
        input_text = sys.stdin.read()
        
        # Лексический анализ
        lexer = Lexer(input_text)
        
        # Синтаксический анализ
        parser = Parser(lexer.tokens)
        definitions = parser.parse()
        
        # Вычисление и преобразование в TOML
        evaluator = Evaluator(definitions)
        toml_output = evaluator.to_toml()
        
        # Вывод в стандартный вывод
        print(toml_output)
        
    except Exception as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()