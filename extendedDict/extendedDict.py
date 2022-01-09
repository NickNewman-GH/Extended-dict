import re, operator
from .lexer import Lexer
from .token import TokenType

class ExtendedDictException(Exception):
    pass

class ExtendedDict(dict):

    def __init__(self):
        self.iloc = self.iloc(self)
        self.ploc = self.ploc(self)

    class iloc:
        def __init__(self, dict):
            self.dict = dict

        def __getitem__(self, index):
            if not isinstance(index, int):
                raise ExtendedDictException("ExtendedDict index must be an integer")
            if index > len(self.dict) - 1 or index < -len(self.dict):
                raise ExtendedDictException("ExtendedDict index out of range")
            keys = sorted(self.dict.keys())
            return self.dict[keys[index]]
    
    class ploc:
        def __init__(self, dict):
            self.dict = dict

        def __getitem__(self, сonditions):
            foreignChars = list(set(re.findall(r'[^><=\d.\-+ ]', сonditions)))
            if len(foreignChars) > 1:
                raise ExtendedDictException(f"Bad сonditions. Too many foreign characters: {', '.join(foreignChars)}")
            elif len(foreignChars) == 1:
                separator = foreignChars[0]
                сonditions = сonditions.split(separator)
            else:
                сonditions = [сonditions]

            for index, condition in enumerate(сonditions):
                lexer = Lexer(condition)
                сonditions[index] = self._toTokens(lexer)

            return self._getDictByConditions(сonditions)


        def _isNumbers(self, reworkedKey):
            for number in reworkedKey:
                try:
                    int(number)
                except ValueError:
                    try:
                        float(number)
                    except ValueError:
                        return False
            return True

        def _toNumber(self, string):
            try:
                return int(string)
            except ValueError:
                return float(string)

        def _getDictByConditions(self, сonditions):
            resultDict = {}
            compOperations = {
            TokenType.MORE: operator.gt, TokenType.MORE_EQUAL: operator.ge, 
            TokenType.LESS: operator.lt, TokenType.LESS_EQUAL: operator.le,
            TokenType.EQUAL: operator.eq, TokenType.NOT_EQUAL: operator.ne}
            
            for key in self.dict:
                numberList = key.strip()
                numberList = numberList[1:-1] if numberList[0] == '(' and numberList[-1] == ')' else numberList
                numberList = numberList.split(',')
                if len(numberList) == len(сonditions) and self._isNumbers(numberList):
                    numberList = tuple(map(self._toNumber, numberList))
                    isAllTrue = True
                    for index, condition in enumerate(сonditions):
                        if not compOperations[condition[0].type_](numberList[index], self._toNumber(condition[1].value)):
                            isAllTrue = False
                            break
                    if isAllTrue:
                        if len(numberList) == 1:
                            resultDict[numberList[0]] = self.dict[key]
                        else:
                            resultDict[numberList] = self.dict[key]
            return resultDict
            
        def _checkTokenSequence(self, tokens):
            signTypes = [TokenType.MORE, TokenType.MORE_EQUAL, 
            TokenType.LESS, TokenType.LESS_EQUAL,
            TokenType.EQUAL, TokenType.NOT_EQUAL]
            if len(tokens) != 2:
                raise ExtendedDictException(f"Wrong condition '{' '.join([token.value for token in tokens])}'")
            elif tokens[0].type_ not in signTypes or tokens[1].type_ != TokenType.NUMBER:
                raise ExtendedDictException(f"Wrong condition '{' '.join([token.value for token in tokens])}'")

        def _toTokens(self, lexer):
            tokens = []
            token = lexer.next()
            while token.type_ != TokenType.EOS:
                tokens.append(token)
                token = lexer.next()
            self._checkTokenSequence(tokens)
            return tuple(tokens)