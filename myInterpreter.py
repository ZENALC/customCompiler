__author__ = "Mihir Shrestha"

ADD, SUBTRACT, MULTIPLY, DIVIDE, INTEGER, POWER, EOF, LPAREN, RPAREN = 'ADD', 'SUBTRACT', 'MULTIPLY', 'DIVIDE', \
                                                                       'INTEGER', 'POWER', 'EOF', 'LPAREN', 'RPAREN'


class Token:
    def __init__(self, value, tokenType):
        self.value = value
        self.tokenType = tokenType

    def __str__(self):
        return f"Token('{self.value}', {self.tokenType})"

    def __repr__(self):
        return self.__str__()


class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.currentCharacter = self.text[self.pos]
        self.currentToken = None

    def error(self):
        raise Exception("Invalid Syntax")

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.currentCharacter = None
        else:
            self.currentCharacter = self.text[self.pos]

    def clear_white_space(self):
        while self.currentCharacter is not None and self.currentCharacter.isspace():
            self.advance()

    def get_full_integer(self):
        currentInteger = ''
        while self.currentCharacter is not None and self.currentCharacter.isdigit():
            currentInteger += self.currentCharacter
            self.advance()
        self.pos -= 1
        self.currentCharacter = self.text[self.pos]
        return int(currentInteger)

    def get_next_token(self):
        self.clear_white_space()

        if self.currentCharacter is None:
            return Token(None, EOF)
        if self.currentCharacter.isdigit():
            return Token(self.get_full_integer(), INTEGER)
        elif self.currentCharacter == '+':
            return Token('+', ADD)
        elif self.currentCharacter == '-':
            return Token('-', SUBTRACT)
        elif self.currentCharacter == '*':
            return Token('*', MULTIPLY)
        elif self.currentCharacter == '/':
            return Token('/', DIVIDE)
        elif self.currentCharacter == '^':
            return Token('^', POWER)
        elif self.currentCharacter == '(':
            return Token('(', LPAREN)
        elif self.currentCharacter == ')':
            return Token(')', RPAREN)
        else:
            self.error()


class Interpreter:
    def __init__(self, lexer):
        self.lexer = lexer
        self.currentToken = self.lexer.get_next_token()

    def eat(self, tokenType):
        if self.currentToken.tokenType == tokenType:
            self.lexer.advance()
            self.currentToken = self.lexer.get_next_token()
        else:
            self.lexer.error()

    def factor(self):
        token = self.currentToken
        if token.tokenType == INTEGER:
            self.eat(INTEGER)
            if self.currentToken.tokenType == POWER:
                self.eat(POWER)
                otherToken = self.currentToken
                self.eat(INTEGER)
                return token.value ** otherToken.value
            return token.value
        elif token.tokenType == LPAREN:
            self.eat(LPAREN)
            result = self.parse()
            self.eat(RPAREN)
            return result

    def term(self):
        result = self.factor()

        while self.currentToken.tokenType in (MULTIPLY, DIVIDE):
            operator = self.currentToken
            self.eat(self.currentToken.tokenType)

            if operator.tokenType == MULTIPLY:
                result *= self.factor()
            elif operator.tokenType == DIVIDE:
                result /= self.factor()

        return result

    def parse(self):
        result = self.term()

        while self.currentToken.tokenType in (ADD, SUBTRACT, INTEGER):
            operator = self.currentToken
            self.eat(self.currentToken.tokenType)

            if operator.tokenType == ADD:
                result += self.term()
            elif operator.tokenType == SUBTRACT:
                result -= self.term()
            elif operator.tokenType == INTEGER:
                self.lexer.error()

        return result


if __name__ == "__main__":
    while True:
        text = input(">>")
        if text is "":
            continue
        lexer = Lexer(text)
        interpreter = Interpreter(lexer)
        print(interpreter.parse())
