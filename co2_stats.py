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
    electricity_and_heat_per_capita: Union[float, None]
    energy: Union[float, None]
    energy_per_capita: Union[float, None]
    total_emissions: Union[float, None]
    total_emissions_per_capita: Union[float, None]



LinkedList: TypeAlias = Union["RLNode",None]
@dataclass(frozen=True)
class RLNode:
    first: Rows
    rest: LinkedList

#converts arrays of strings to Row objects
def array_to_row(data: list[str]) -> Rows:
    return Rows(data[0], int(data[1]), float(data[2]),float(data[3]), float(data[4]), float(data[5]), float(data[6]), float(data[7]))
    
file: TypeAlias = Literal["sample-file.csv", "some_ghg_emissions.csv"]
#parses csv file and returns all data in a row collectively in a LinkedList
def read_csv_lines(file_name: file)-> LinkedList:
    'expected_labels : List[str] = ['item','price','number in stock']'
    with open(file_name, newline="") as csvfile:
        iter = csv.reader(csvfile)
        topline : List[str] = next(iter)
        if not (topline == expected_labels):
            raise ValueError(f"unexpected first line: got: {topline}")
    Dataset = []
    for line in iter:
        Dataset.append(line)
    return Dataset


#returns the length of a LinkedList of row objects
def listlen(ll: LinkedList) ->int:
    if ll is None:
        return 0
    else:
        rest_of_list: LinkedList = ll.rest
        return 1+ listlen(rest_of_list)
    
#FIX LATER
def filter(ll:LinkedList, )

class Tests(unittest.TestCase):
    pass
    'def test_array_to_row(self): , def test_read_csv-lines(self):, def test_listlen(self):'
      

if (__name__ == '__main__'):
    unittest.main()
