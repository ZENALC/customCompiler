__author__ = "Mihir Shrestha"

ADD, SUBTRACT, MULTIPLY, DIVIDE, INTEGER, POWER, EOF, LPAREN, RPAREN = 'ADD', 'SUBTRACT', 'MULTIPLY', 'DIVIDE', \
                                                                       'INTEGER', 'POWER', 'EOF', 'LPAREN', 'RPAREN'


# Token class that will contain value and token type.
class Token:
    def __init__(self, value, tokenType):
        self.value = value
        self.tokenType = tokenType

    #  Return token representation in string format.
    def __str__(self):
        return f"Token('{self.value}', {self.tokenType})"

    #  Return token representation in string format.
    def __repr__(self):
        return self.__str__()


# Lexer class that will go through text given.
class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.currentCharacter = self.text[self.pos]
        self.currentToken = None

    def error(self):
        raise Exception("Invalid Syntax")

    # Advance position by 1 if not at end of line.
    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.currentCharacter = None
        else:
            self.currentCharacter = self.text[self.pos]

    # Keep iterating through text while current character is a space character.
    def clear_white_space(self):
        while self.currentCharacter is not None and self.currentCharacter.isspace():
            self.advance()

    # Keep iterating through text while current character is a digit.
    def get_full_integer(self):
        currentInteger = ''
        while self.currentCharacter is not None and self.currentCharacter.isdigit():
            currentInteger += self.currentCharacter
            self.advance()
        self.pos -= 1  # Currently, advance() is called after eat(), so we decrease the position, for that to work.
        self.currentCharacter = self.text[self.pos]  # Same as above, resetting currentCharacter to what it was before.
        return int(currentInteger)

    # Return a token that corresponds to current character
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


# Interpreter class that will go through text given.
class Interpreter:
    def __init__(self, lexer):
        self.lexer = lexer
        self.currentToken = self.lexer.get_next_token()

    # Eat a token if its type matches the one given.
    def eat(self, tokenType):
        if self.currentToken.tokenType == tokenType:
            self.lexer.advance()
            self.currentToken = self.lexer.get_next_token()
        else:
            self.lexer.error()

    # If token given is an integer, check if the next one if is an exponent, if it is, return the result of token to the
    # power of new token. Else if token is a left parenthesis, call the parse function and recursively repeat.
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

    # Handle multiplication and division.
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

    # Handle addition and subtraction.
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
        arg = input(">>")
        if arg is "":
            continue
        myLexer = Lexer(arg)
        interpreter = Interpreter(myLexer)
        print(interpreter.parse())
