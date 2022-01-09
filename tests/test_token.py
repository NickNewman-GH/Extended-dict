import pytest
from extendedDict import Token, TokenType

class TestToken:
    
    def test_creation(self):
        token = Token(TokenType.NUMBER, '-5.2')
        assert token.type_ == TokenType.NUMBER and token.value == '-5.2'
        with pytest.raises(AttributeError):
            token = Token(TokenType.LEFT, '<-')
    
    def test_str(self):
        token = Token(TokenType.NUMBER, 'sometext')
        assert str(token) == 'Token(TokenType.NUMBER, sometext)'
    
    def test_repr(self):
        token = Token(TokenType.EQUAL, 'anothertext')
        assert repr(token) == 'Token(TokenType.EQUAL, anothertext)'
