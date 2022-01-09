import pytest
from extendedDict import Lexer, LexerException
from extendedDict import TokenType

@pytest.fixture
def textsAndResNext():
    return {
        '     ':(TokenType.EOS, None), 
        ' 56.26':(TokenType.NUMBER, '56.26'), 
        ' > ':(TokenType.MORE, '>'), 
        '>= ':(TokenType.MORE_EQUAL, '>='), 
        '<':(TokenType.LESS, '<'), 
        '<=':(TokenType.LESS_EQUAL, '<='), 
        '=':(TokenType.EQUAL, '='), 
        '<>':(TokenType.NOT_EQUAL, '<>'), 
        '< >':(TokenType.LESS, '<')}

@pytest.fixture
def wrongNumbers():
    return ('-56-3', '9.9.26', '1.',
    '-.', '.+', '+-', '--5.6')

class TestLexer:

    def test_creation(self):
        lexer = Lexer('sometext')
        assert (lexer._pos == 0 and 
        lexer._current_char == 's' and 
        lexer._text == 'sometext')

        with pytest.raises(LexerException):
            Lexer(True)

        with pytest.raises(LexerException):
            Lexer(89198)

    def test_next(self, textsAndResNext):
        for text in textsAndResNext:
            token = Lexer(text).next()
            assert token.type_ == textsAndResNext[text][0] and token.value == textsAndResNext[text][1]

        with pytest.raises(LexerException):
	        Lexer(' #').next()

    def test_number(self, wrongNumbers):
        for wrongNum in wrongNumbers:
            with pytest.raises(LexerException):
	            Lexer(wrongNum).next()