import csv
from typing import *
from dataclasses import dataclass
import unittest
import math
import sys
sys.setrecursionlimit(10**6)

@dataclass(frozen = True)
class Rows:
    country_name: str
    country_year: int
    electricity_and_heat: Union[float, None]
    energy: Union[float, None]
    total_emissions: Union[float, None]


LinkedList: TypeAlias = Union["RLNode",None]
@dataclass(frozen=True)
class RLNode:
    first: Rows
    rest: LinkedList

#converts arrays of strings to Row objects
def array_to_row(data: list[str]) -> Rows:
    return Rows(data[0], int(data[1]), float(data[2]),float(data[3]), float(data[4]))


file: TypeAlias = Literal["sample-file.csv", "some_ghg_emissions.csv"]
#parses csv file and returns all data in a row collectively in a LinkedList
def read_csv_lines(file_name: file)-> LinkedList:
    pass


class Tests(unittest.TestCase):
    pass
    'def test_array_to_row(self): , def test_read_csv-lines(self):'
      

if (__name__ == '__main__'):
    unittest.main()
