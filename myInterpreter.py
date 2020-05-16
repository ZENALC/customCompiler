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
        self.currentCharacter = self.text[self.pos]
        self.currentToken = None

    def eat(self, tokenType):
        if self.currentToken.tokenType == tokenType:
            self.advance()
            self.currentToken = self.get_next_token()
        else:
            self.error()

    def error(self):
        raise Exception("Invalid Syntax")

    def advance(self):
        if self.pos != len(self.text) - 1:
            self.pos += 1
            self.currentCharacter = self.text[self.pos]
        else:
            self.currentCharacter = None

    def clear_white_space(self):
        while self.currentCharacter is not None and self.currentCharacter.isspace():
            self.advance()

    def get_full_integer(self):
        currentInteger = ''
        while self.currentCharacter is not None and self.currentCharacter.isdigit():
            currentInteger += self.currentCharacter
            self.advance()
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

        else:
            self.error()

    def parse(self):
        self.currentToken = self.get_next_token()
        leftToken = self.currentToken
        self.eat(INTEGER)

        operand = self.currentToken
        if operand.tokenType == ADD:
            self.eat(ADD)
        elif operand.tokenType == SUBTRACT:
            self.eat(SUBTRACT)
        elif operand.tokenType == MULTIPLY:
            self.eat(MULTIPLY)
        elif operand.tokenType == DIVIDE:
            self.eat(DIVIDE)
        else:
            self.error()

        rightToken = self.currentToken
        self.eat(INTEGER)

        if operand.tokenType == ADD:
            return leftToken.value + rightToken.value
        elif operand.tokenType == SUBTRACT:
            return leftToken.value - rightToken.value
        elif operand.tokenType == MULTIPLY:
            return leftToken.value * rightToken.value
        elif operand.tokenType == DIVIDE:
            return leftToken.value / rightToken.value


if __name__ == "__main__":
    while True:
        interpreter = Interpreter(input(">>"))
        print(interpreter.parse())
