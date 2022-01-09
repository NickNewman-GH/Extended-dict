import pytest
from extendedDict import ExtendedDict, ExtendedDictException

@pytest.fixture
def plocDict():
    map = ExtendedDict()
    map["value1"] = 1; map["value2"] = 2; map["value3"] = 3
    map["1"] = 10; map["2"] = 20; map["3"] = 30
    map["(1, 5)"] = 100; map["5, 5"] = 200; map["(10, 5)"] = 300
    map["(1, 5, 3)"] = 400; map["5, 5, 4"] = 500; map["(10, 5, 5)"] = 600
    return map

class TestExtendedDict:
    
    def test_creation(self):
        map = ExtendedDict()
        map['value1'] = 'text'
        assert map.ploc.dict == {'value1': 'text'}
        assert map.iloc.dict == {'value1': 'text'}

class TestIloc:
    
    def test_getitem(self):
        map = ExtendedDict()
        map["value1"] = 1
        map["value2"] = 2
        map["value3"] = 3
        assert map.iloc[0] == 1
        assert map.iloc[2] == 3
        assert map.iloc[-2] == 2
        with pytest.raises(ExtendedDictException):
            map.iloc['f']
        with pytest.raises(ExtendedDictException):
            map.iloc[4]
        with pytest.raises(ExtendedDictException):
            map.iloc[-4]

class TestPloc:
    
    def test_getitem(self, plocDict):
        map = plocDict
        assert map.ploc[">=1"] == {1: 10, 2: 20, 3: 30}
        assert map.ploc[">0 @    >0"] == {(1, 5): 100, (5, 5): 200, (10, 5): 300}
        assert map.ploc["<5 | >=5       |   >=3"] == {(1, 5, 3): 400}
        assert map.ploc[">2.5 ; >-5.6"] == {(5, 5): 200, (10, 5): 300}
        with pytest.raises(ExtendedDictException):
            map.ploc["<5 $ >=5* >=3"]
        with pytest.raises(ExtendedDictException):
            map.ploc["<=<5 $ >=5 $ >=3"]
        with pytest.raises(ExtendedDictException):
            map.ploc["5<> $ >=5 $ >=3"]
        with pytest.raises(ExtendedDictException):
            map.ploc["<<"]
        with pytest.raises(ExtendedDictException):
            map.ploc[""]