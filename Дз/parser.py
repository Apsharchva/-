from typing import List, Optional
from lexer import Token

class ASTNode:
    pass

class Number(ASTNode):
    def __init__(self, value: int):
        self.value = value

class Array(ASTNode):
    def __init__(self, elements: List[ASTNode]):
        self.elements = elements

class Constant(ASTNode):
    def __init__(self, name: str):
        self.name = name

class Definition(ASTNode):
    def __init__(self, name: str, value: ASTNode):
        self.name = name
        self.value = value

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
    
    def current_token(self) -> Optional[Token]:
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None
    
    def eat(self, token_type: str) -> Token:
        token = self.current_token()
        if not token:
            raise SyntaxError(f"Ожидается {token_type}, получен конец файла")
        if token.type != token_type:
            raise SyntaxError(f"Ожидается {token_type}, получено {token.type} на позиции {token.line}:{token.col}")
        self.pos += 1
        return token
    
    def parse_number(self) -> Number:
        token = self.eat('NUMBER')
        # Преобразуем восьмеричное число в десятичное
        octal_str = token.value[2:]  # Убираем '0o' или '0O'
        return Number(int(octal_str, 8))
    
    def parse_array(self) -> Array:
        self.eat('LPAREN')
        elements = []
        
        # Парсим элементы до тех пор, пока не встретим ')'
        while self.current_token() and self.current_token().type != 'RPAREN':
            elements.append(self.parse_value())
            
            # После элемента может быть запятая или конец массива
            if self.current_token() and self.current_token().type == 'COMMA':
                self.eat('COMMA')
        
        self.eat('RPAREN')
        return Array(elements)
    
    def parse_constant(self) -> Constant:
        self.eat('BANG')
        self.eat('LBRACKET')
        name = self.eat('IDENT').value
        self.eat('RBRACKET')
        return Constant(name)
    
    def parse_value(self) -> ASTNode:
        token = self.current_token()
        if not token:
            raise SyntaxError("Неожиданный конец файла при разборе значения")
        
        if token.type == 'NUMBER':
            return self.parse_number()
        elif token.type == 'LPAREN':
            return self.parse_array()
        elif token.type == 'BANG':
            return self.parse_constant()
        else:
            raise SyntaxError(f"Неожиданный токен {token.type} на позиции {token.line}:{token.col}")
    
    def parse_definition(self) -> Definition:
        self.eat('DEF')
        name = self.eat('IDENT').value
        self.eat('ASSIGN')
        value = self.parse_value()
        return Definition(name, value)
    
    def parse(self) -> List[Definition]:
        definitions = []
        while self.current_token():
            definitions.append(self.parse_definition())
        return definitions

class Evaluator:
    def __init__(self, definitions: List[Definition]):
        self.definitions = {defn.name: defn for defn in definitions}
        self.cache = {}
    
    def evaluate(self, node: ASTNode):
        if isinstance(node, Number):
            return node.value
        elif isinstance(node, Array):
            return [self.evaluate(elem) for elem in node.elements]
        elif isinstance(node, Constant):
            if node.name not in self.cache:
                if node.name not in self.definitions:
                    raise NameError(f"Неопределенная константа '{node.name}'")
                self.cache[node.name] = self.evaluate(self.definitions[node.name].value)
            return self.cache[node.name]
        elif isinstance(node, Definition):
            return self.evaluate(node.value)
    
    def to_toml(self) -> str:
        result = []
        for name, defn in self.definitions.items():
            value = self.evaluate(defn.value)
            if isinstance(value, list):
                toml_value = f"[{', '.join(str(v) for v in value)}]"
            else:
                toml_value = str(value)
            result.append(f"{name} = {toml_value}")
        return '\n'.join(result)