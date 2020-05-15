__author__ = "Mihir Shrestha"

ADD, SUBTRACT, MULTIPLY, DIVIDE, INTEGER, EOF = 'ADD', 'SUBTRACT', 'MULTIPLY', 'DIVIDE', 'INTEGER', 'EOF'


class Token:
    def __init__(self, value, tokenType):
        self.value = value
        self.tokenType = tokenType

    def __str__(self):
        return f"Token({self.value}, {self.tokenType})"

    def __repr__(self):
        return self.__str__()


class Interpreter:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.currentToken = None

    def eat(self, tokenType):
        if self.currentToken.type == tokenType:
            self.advance()
        else:
            self.error()

    def error(self):
        raise Exception("Invalid Syntax")

    def advance(self):
        if self.text[self.pos] == len(self.text):
            return Token(None, EOF)
        else:
            self.pos += 1
            self.currentToken = self.text[self.pos]

    def clear_white_space(self):
        while self.currentToken.isspace():
            self.advance()

    def get_full_integer(self):
        currentInteger = ''
        while self.currentToken.value.isdigit():
            currentInteger += self.currentToken
            self.advance()
        self.currentToken = Token(int(currentInteger), INTEGER)

    def parse(self):
        self.currentToken = self.advance()

        self.clear_white_space()

        leftValue = self.currentToken.value
        self.eat(INTEGER)

        self.clear_white_space()

        if self.currentToken == '-':

        self.eat()

        rightValue = self.currentToken.value
