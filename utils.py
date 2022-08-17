from __future__ import annotations

from enum import Enum
from functools import total_ordering
from typing import Dict

"""
Common bridge concepts such as Cardinal Direction, Suit, and Card Rank represented as Enums
"""


@total_ordering
class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    __from_str_map__ = {"N": NORTH, "E": EAST, "S": SOUTH, "W": WEST}
    __to_str__ = {NORTH : "North",SOUTH : "South",EAST : "East",WEST : "West"}

    @classmethod
    def from_str(cls, direction_str: str) -> Direction:
        return Direction(cls.__from_str_map__[direction_str.upper()])

    def __lt__(self, other: Direction) -> bool:
        return self.value < other.value

    def __repr__(self) -> str:
        return self.name

    def next(self) -> Direction:
        return self.offset(1)

    def partner(self) -> Direction:
        return self.offset(2)

    def previous(self) -> Direction:
        return self.offset(3)

    def offset(self, offset: int) -> Direction:
        return Direction((self.value + offset) % 4)

    def abbreviation(self) -> str:
        return self.name[0]

    def to_str(self) -> str :
        return self.__to_str__[self.value]

@total_ordering
class Declaration(Enum):
    PASS = 0, "Pass", "p","P"
    DOUBLE = 1, 'X', "d","X"
    REDOUBLE = 2, "XX", "r","XX"

    __from_str_map__ = {"PASS": PASS, "P": PASS, "X": DOUBLE, "XX": REDOUBLE}
    __color__ = {PASS : 'green', DOUBLE : 'red', REDOUBLE :"blue"}

    @classmethod
    def from_str(cls, declaration_str: str) -> Declaration:
        return Declaration(cls.__from_str_map__[declaration_str.upper()])

    @classmethod
    def from_int(cls, declaration_int: int) -> Declaration:
         if declaration_int==1 : return Declaration.DOUBLE
         if declaration_int==2 : return Declaration.REDOUBLE
         return Declaration.PASS

    def __lt__(self, other: Direction) -> bool:
        return self.value < other.value

    def print_as_lin(self) -> str:
        return self.value[2]

    def print_as_pbn(self) -> str:
        return self.value[1]

    def print_as_txt(self) -> str:
        return self.value[3]

    def barbu_multiplactor(self) -> int :
        return self.value[0]

    def color(self) -> str :
        return self.__color__[self.value]

    def next(self) -> Declaration:
        if self == Declaration.PASS :
            return Declaration.DOUBLE
        elif self == Declaration.DOUBLE :
            return Declaration.REDOUBLE
        return Declaration.PASS
        


    @classmethod
    def is_str_declaration(cls, bidding_suit_str) -> bool:
        if bidding_suit_str.upper() in cls.__from_str_map__:
            return True
        return False

    def __str__(self) -> str:
        return self.value[1]

def declaration_dic_transformation(init_dic : Dict[Direction,Dict[Direction,Declaration]]) :
    new_dic = {
        Direction.NORTH : {
            Direction.SOUTH : Declaration.PASS,
            Direction.EAST : Declaration.DOUBLE,
            Direction.WEST : Declaration.PASS
        },
        Direction.SOUTH : {
            Direction.EAST : Declaration.PASS,
            Direction.WEST : Declaration.PASS
        },
        Direction.EAST : {
            Direction.WEST : Declaration.PASS
        },

        
    }
    for direction1,dic in new_dic.items() :
        for direction2,decla in dic.items() :
            new_dic[direction1][direction2] = max(init_dic[direction1][direction2],init_dic[direction2][direction1])
            
    return new_dic
