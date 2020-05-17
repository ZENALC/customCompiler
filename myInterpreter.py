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
            self.currentToken = self.get_next_token()
        else:
            self.error()

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
        result = self.currentToken.value
        self.eat(INTEGER)

        while self.currentToken.tokenType != EOF:
            operator = self.currentToken
            self.advance()
            self.eat(self.currentToken.tokenType)

            nextToken = self.currentToken
            self.eat(INTEGER)

            if operator.tokenType == ADD:
                result += nextToken.value
            elif operator.tokenType == SUBTRACT:
                result -= nextToken.value
            elif operator.tokenType == MULTIPLY:
                result *= nextToken.value
            elif operator.tokenType == DIVIDE:
                result /= nextToken.value

        return result


if __name__ == "__main__":
    while True:
        text = input(">>")
        if text is "":
            continue
        interpreter = Interpreter(text)
        print(interpreter.parse())
