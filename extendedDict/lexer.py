from .token import TokenType, Token

class LexerException(Exception):
    pass

class Lexer():
    
    def __init__(self, text: str):
        self._pos : int = -1
        self._current_char: str = None
        if not isinstance(text, str):
            raise LexerException(f'Text must be a {str}, not {type(text)}')
        self._text = text
        self._forward()

    def next(self) -> Token:
        while self._current_char != None:
            if self._current_char == " ":
                self._skip()
                continue
            if self._current_char.isdigit() or self._current_char == "+" or self._current_char == "-":
                return Token(TokenType.NUMBER, self._number())
            if self._current_char == ">":
                char = self._current_char
                self._forward()
                if self._current_char == "=":
                    char += self._current_char
                    self._forward()
                    return Token(TokenType.MORE_EQUAL, char)
                else:
                    return Token(TokenType.MORE, char)
            if self._current_char == "<":
                char = self._current_char
                self._forward()
                if self._current_char == "=":
                    char += self._current_char
                    self._forward()
                    return Token(TokenType.LESS_EQUAL, char)
                elif self._current_char == ">":
                    char += self._current_char
                    self._forward()
                    return Token(TokenType.NOT_EQUAL, char)
                else:
                    return Token(TokenType.LESS, char)
            if self._current_char == "=":
                char = self._current_char
                self._forward()
                return Token(TokenType.EQUAL, char)
            raise LexerException(f"Bad token '{self._current_char}'")
        return Token(TokenType.EOS, None)

    def _forward(self):
        self._pos += 1
        if self._pos >= len(self._text):
            self._current_char = None
        else:
            self._current_char = self._text[self._pos]
    
    def _skip(self):
        while self._current_char == ' ':
            self._forward()

    def _number(self):
        result: list = []
        left = None
        wasPoint = False
        while self._current_char and (
        self._current_char.isdigit() or 
        self._current_char == '.' or 
        self._current_char == '+' or 
        self._current_char == '-'):
            if left:
                if not self._current_char.isdigit() and (left == '.' or left == '-' or left == '+'):
                    raise LexerException(f"Wrong number in condition '{self._text}'")
                elif left.isdigit() and (self._current_char == '-' or self._current_char == '+'):
                    raise LexerException(f"Wrong number in condition '{self._text}'")
            if self._current_char == '.':
                if wasPoint:
                    raise LexerException(f"Wrong number in condition '{self._text}'")
                else:
                    wasPoint = True
            result.append(self._current_char)
            left = self._current_char
            self._forward()
        if left == '.' or left == '-' or left == '+':
            raise LexerException(f"Wrong number in condition '{self._text}'")
        return  "".join(result)