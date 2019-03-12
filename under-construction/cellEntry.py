from enum import Enum

class EntryValue(Enum):
    MINE = -1
    ZERO = 0
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NULL = None

    def isNum(self):
        return type(self.value) is int and self.value >= 0
    
    def is_num_and_g_t_zero(self):
        return type(self.value) is int and self.value > 0

    def isZero(self):
        return self.value == 0
    
    def isMine(self):
        return self.value == -1


class Entry:

    def __init__(self, value: EntryValue):
        if type(value) != EntryValue:
            raise TypeError
        self._value = value
    
    @property
    def value(self):
        return self._value

    def isMine(self) -> bool:
        return self.value == EntryValue.MINE

    def __str__(self):
        return str(self.value)

