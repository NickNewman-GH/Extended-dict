from enum import auto, Enum

class TokenType(Enum):
    NUMBER = auto()
    MORE = auto()
    MORE_EQUAL = auto()
    LESS = auto()
    LESS_EQUAL = auto()
    EQUAL = auto()
    NOT_EQUAL = auto()
    EOS = auto()

class Token():
    def __init__(self, type_: TokenType, value: str):
        self.type_ = type_
        self.value = value

    def __str__(self):
        return f"Token({self.type_}, {self.value})"

    def __repr__(self):
        return str(self)