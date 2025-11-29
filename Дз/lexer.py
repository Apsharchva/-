import re
from typing import List, Optional

class Token:
    def __init__(self, type: str, value: str, line: int, col: int):
        self.type = type
        self.value = value
        self.line = line
        self.col = col

class Lexer:
    patterns = [
        ('NUMBER', r'0[oO][0-7]+'),
        ('IDENT', r'[_A-Z][_a-zA-Z0-9]*'),
        ('DEF', r'def'),
        ('ASSIGN', r':='),
        ('BANG', r'!'),
        ('LBRACKET', r'\['),
        ('RBRACKET', r'\]'),
        ('LPAREN', r'\('),
        ('RPAREN', r'\)'),
        ('COMMA', r','),
        ('SKIP', r'[ \t]+'),
        ('NEWLINE', r'\n'),
    ]
    
    def __init__(self, text: str):
        self.tokens = []
        self.tokenize(text)
    
    def tokenize(self, text: str):
        pos = 0
        line = 1
        col = 1
        
        while pos < len(text):
            match = None
            for token_type, pattern in self.patterns:
                regex = re.compile(pattern)
                match = regex.match(text, pos)
                if match:
                    value = match.group(0)
                    if token_type == 'SKIP':
                        # Пропускаем пробелы и табы
                        pass
                    elif token_type == 'NEWLINE':
                        line += 1
                        col = 1
                    else:
                        self.tokens.append(Token(token_type, value, line, col))
                    
                    col += len(value)
                    pos = match.end()
                    break
            
            if not match:
                # Если не нашли совпадение - ошибка
                raise SyntaxError(f"Неизвестный символ '{text[pos]}' на позиции {line}:{col}")