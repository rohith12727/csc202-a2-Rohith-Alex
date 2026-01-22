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

#Converts a string to a float, but returns none if the string is blank
def str_to_float(s: str) -> float | None:
    if s == "":
        return None
    return float(s)

#converts arrays of strings to Row objects
def array_to_row(data: list[str]) -> Rows:
    return Rows(data[0], int(data[1]), 
        str_to_float(data[2]),str_to_float(data[3]), str_to_float(data[4]), str_to_float(data[5]), str_to_float(data[6]), str_to_float(data[7]))
    
file: TypeAlias = Literal["sample-file.csv", "some_ghg_emissions.csv"]
#parses csv file and returns all data in a row collectively in a LinkedList
def read_csv_lines(filename: file)-> list[list[str]]:
    rows: list[list[str]] = []

    with open(filename, newline="") as csvfile:
        reader = csv.reader(csvfile)

        _ = next(reader)  # skip header

        for fields in reader:
            rows.append(fields)

    return rows


#returns the length of a LinkedList of row objects
def listlen(ll: LinkedList) ->int:
    if ll is None:
        return 0
    else:
        rest_of_list: LinkedList = ll.rest
        return 1+ listlen(rest_of_list)
    
#FIX LATER
def filter(ll:LinkedList,):
    pass

sample_ll: LinkedList = RLNode(Rows("1", 2000, None, None, None, None, None, None), 
                        RLNode(Rows("1", 2000, None, None, None, None, None, None), 
                        RLNode(Rows("1", 2000, None, None, None, None, None, None), None)))
sample_ll_2:LinkedList = RLNode(Rows("1", 2000, None, None, None, None, None, None), None)
sample_ll_3:LinkedList = None

class Tests(unittest.TestCase):
    
    'def test_array_to_row(self): , def test_read_csv-lines(self):,'
    def test_str_to_float(self):
        self.assertEqual(str_to_float("3434"), 3434.0)
        self.assertEqual(str_to_float("23.32"), 23.32)
        self.assertEqual(str_to_float("0.3214"), 0.3214)
        self.assertEqual(str_to_float(".00001"), .00001)

    def test_list_len(self):
        self.assertEqual(listlen(sample_ll), 3)
        self.assertEqual(listlen(sample_ll_2), 1)
        self.assertEqual(listlen(sample_ll_3), 0)




if (__name__ == '__main__'):
    unittest.main()
