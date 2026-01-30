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

# Converts a string to a float, but returns none if the string is blank
def str_to_float(s: str) -> float | None:
    if s == "":
        return None
    return float(s)

# converts arrays of strings to Row objects
def array_to_row(data: list[str]) -> Rows:
    return Rows(
                data[0], 
                int(data[1]), 
                str_to_float(data[2]),
                str_to_float(data[3]), 
                str_to_float(data[4]), 
                str_to_float(data[5]), 
                str_to_float(data[6]), 
                str_to_float(data[7])
            )
    
file: TypeAlias = Literal["sample-file.csv", "some_ghg_emissions.csv"]
# parses csv file and returns all data in a row collectively in a LinkedList
def read_csv_lines(filename: file) -> LinkedList:
    rows: list[list[str]] = []

    with open(filename, newline="") as csvfile:
        reader = csv.reader(csvfile)

        _ = next(reader)  # skip header

        for fields in reader:
            rows.append(fields)

    linked = None

    for item in reversed(rows):
        linked = RLNode(array_to_row(item), linked)

    return linked

# returns the length of a LinkedList of row objects
def listlen(ll: LinkedList) ->int:
    if ll is None:
        return 0
    else:
        rest_of_list: LinkedList = ll.rest
        return 1 + listlen(rest_of_list)
    
Fields : TypeAlias = Literal[
                                "country", 
                                "year", 
                                "electricity_and_heat_co2_emissions", 
                                "electricity_and_heat_co2_emissions_per_capita", 
                                "energy_co2_emissions",
                                "energy_co2_emissions_per_capita",
                                "total_co2_emissions_excluding_lucf",
                                "total_co2_emissions_excluding_lucf_per_capita"
                            ]

field_list = [
            "country", 
            "year", 
            "electricity_and_heat_co2_emissions", 
            "electricity_and_heat_co2_emissions_per_capita", 
            "energy_co2_emissions",
            "energy_co2_emissions_per_capita",
            "total_co2_emissions_excluding_lucf",
            "total_co2_emissions_excluding_lucf_per_capita"
        ]

Types : TypeAlias = Literal["less_than", "equal", "greater_than"]

# return desired field value in a row
def traverse(row : Rows, field : Fields) -> Union[float, str, int, None]:
    if field == "country":
        return row.country_name
    elif field == "year":
        return row.country_year
    elif field == "electricity_and_heat_co2_emissions":
        return row.electricity_and_heat
    elif field == "electricity_and_heat_co2_emissions_per_capita":
        return row.electricity_and_heat_per_capita
    elif field == "energy_co2_emissions":
        return row.energy
    elif field == "energy_co2_emissions_per_capita":
        return row.energy_per_capita
    elif field == "total_co2_emissions_excluding_lucf":
        return row.total_emissions
    elif field == "total_co2_emissions_excluding_lucf_per_capita":
        return row.total_emissions_per_capita

# not all fields are comparable with all of the comparison types
# for example one country cannot ge greater or less than another,
# but you can check if they are equal (the same)
def filter(ll : LinkedList, field : Fields, type : Types, val : Union[int, str, float]) -> Optional[RLNode]:
    # first traverse through all data points and ignore ones with no field

    match ll:
        case None:
            return None
        case RLNode(f, r):
            if traverse(f, field) == None:
                return filter(r, field, type, val)
            else:
                if type == "less_than":
                    if float(traverse(f, field)) < float(val):
                        return RLNode(f, filter(r, field, type, val))
                    else:
                        return filter(r, field, type, val)

                elif type == "equal":
                    if str(traverse(f, field)) == str(val):
                        return RLNode(f, filter(r, field, type, val))
                    else:
                        return filter(r, field, type, val)

                elif type == "greater_than":
                    if float(traverse(f, field)) > float(val):
                        return RLNode(f, filter(r, field, type, val))
                    else:
                        return filter(r, field, type, val)

# amount of countries in the dataset
def answer_1(ll: LinkedList) -> int:
    if ll is None:
        return 0
    some_year = ll.first.country_year
    filtered = filter(ll, "year", "equal", some_year)
    return listlen(filtered)

# years represented for mexico
def answer_2(ll: LinkedList) -> LinkedList:
    mexico_rows = filter(ll, "country", "equal", "Mexico")
    _ = listlen(mexico_rows)
    return mexico_rows

# countries with higher per-capita total greenhouse emissions than 1990 US
def answer_3(ll: LinkedList) -> LinkedList:
    rows_1990 = filter(ll, "year", "equal", 1990)

    us_1990_ll = filter(rows_1990, "country", "equal", "United States")
    if us_1990_ll is None:
        return None
    us_1990_pc = us_1990_ll.first.total_emissions_per_capita
    if us_1990_pc is None:
        return None
    higher_than_us = filter(
        rows_1990,
        "total_co2_emissions_excluding_lucf_per_capita",
        "greater_than",
        us_1990_pc
    )
    _ = listlen(higher_than_us)
    return higher_than_us

# countries with higher per-capita total greenhouse emissions than 2020 US
def answer_4(ll: LinkedList) -> LinkedList:
    rows_2020 = filter(ll, "year", "equal", 2020)

    us_2020_ll = filter(rows_2020, "country", "equal", "United States")
    if us_2020_ll is None:
        return None

    us_2020_pc = us_2020_ll.first.total_emissions_per_capita
    if us_2020_pc is None:
        return None

    higher_than_us = filter(
        rows_2020,
        "total_co2_emissions_excluding_lucf_per_capita",
        "greater_than",
        us_2020_pc
    )
    _ = listlen(higher_than_us)
    return higher_than_us

# population of Luxembourg
def answer_5(ll : LinkedList) -> int:
    lux = filter(ll, "country", "equal", "Luxembourg")
    lux_2014 = filter(lux, "year", "equal", 2014)
    lux_2014_emissions = lux_2014.first.total_emissions
    per_capita = lux_2014.first.total_emissions_per_capita
    return (lux_2014_emissions / per_capita) * 1_000_000

# increase in total electricity and heat emissions in China
def answer_6(ll : LinkedList) -> float:
    china = filter(ll, "country", 'equal', 'China')
    china_1990 = filter(china, "year", 'equal', 1990)
    china_2020 = filter(china, 'year', 'equal', 2020)
    china_2020_eh = china_2020.first.electricity_and_heat
    china_1990_eh = china_1990.first.electricity_and_heat
    pc = (china_2020_eh - china_1990_eh) / china_1990_eh
    return 1 + pc

# China's 2070 electricity and heat emissions
def answer_7(ll : LinkedList) -> float:
    growth_rate = answer_6(ll)
    china = filter(ll, "country", 'equal', 'China')
    china_2020 = filter(china, 'year', 'equal', 2020)
    final_eh = china_2020.first.electricity_and_heat * (growth_rate) ** (50/30)


sample_ll: LinkedList = RLNode(Rows("1", 2000, None, None, None, None, None, None), 
                        RLNode(Rows("1", 2000, None, None, None, None, None, None), 
                        RLNode(Rows("1", 2000, None, None, None, None, None, None), None)))
sample_ll_2:LinkedList = RLNode(Rows("1", 2000, None, None, None, None, None, None), None)
sample_ll_3:LinkedList = None

class Tests(unittest.TestCase):
    
    def test_array_to_row(self):
        self.assertEqual(
                        array_to_row(
                            [
                                'Lithuania','1996','7.11','1.9102515',
                                '13.92','3.7399015','14.24','3.8258765'
                            ]
                            ),
                                Rows('Lithuania',1996,7.11,1.9102515,
                                        13.92,3.7399015,14.24,3.8258765
                                    )
                        )
    
    def test_str_to_float(self):
        self.assertEqual(str_to_float("3434"), 3434.0)
        self.assertEqual(str_to_float("23.32"), 23.32)
        self.assertEqual(str_to_float("0.3214"), 0.3214)
        self.assertEqual(str_to_float(".00001"), .00001)

    def test_listlen(self):
        self.assertEqual(listlen(sample_ll), 3)
        self.assertEqual(listlen(sample_ll_2), 1)
        self.assertEqual(listlen(sample_ll_3), 0)


    def test_filter(self):
        self.assertEqual(filter(
            read_csv_lines('sample-file.csv'), 
            "electricity_and_heat_co2_emissions", 
            "less_than", 
            5.5
        ), 
            RLNode(Rows('Lithuania',2000,5.07,1.4084746,10.22,2.8391736,10.52,2.9225154), 
                RLNode(Rows('Lithuania',2002,5.33,1.5160139,10.93,3.108824,11.22,3.1913087), 
                    RLNode(Rows('Lithuania',2003,5.24,1.5102245,10.94,3.1530259,11.23,3.2366068), None))))
        
        self.assertEqual(filter(
            read_csv_lines('sample-file.csv'),
            "country",
            "equal",
            "Japan"
        ),
            None
        )

    def test_read_csv_lines(self):
        expected_rows: list[Rows] = [
            Rows('Lithuania', 1994, 7.27, 1.9281462, 14.44, 3.8297703, 14.82, 3.930554),
            Rows('Lithuania', 1995, 6.41, 1.710579, 13.44, 3.586612, 13.75, 3.669339),
            Rows('Lithuania', 1996, 7.11, 1.9102515, 13.92, 3.7399015, 14.24, 3.8258765),
            Rows('Lithuania', 1997, 6.65, 1.7997795, 13.56, 3.6699264, 13.92, 3.767358),
            Rows('Lithuania', 1998, 7.49, 2.0433695, 14.29, 3.8984983, 14.71, 4.0130796),
            Rows('Lithuania', 1999, 6.05, 1.6648555, 11.9, 3.2746744, 12.25, 3.3709884),
            Rows('Lithuania', 2000, 5.07, 1.4084746, 10.22, 2.8391736, 10.52, 2.9225154),
            Rows('Lithuania', 2001, 5.53, 1.5533075, 10.87, 3.0532465, 11.16, 3.1347039),
            Rows('Lithuania', 2002, 5.33, 1.5160139, 10.93, 3.108824, 11.22, 3.1913087),
            Rows('Lithuania', 2003, 5.24, 1.5102245, 10.94, 3.1530259, 11.23, 3.2366068)
        ]

        actual_rows: list[Rows] = []

        result: LinkedList = read_csv_lines("sample-file.csv")

        while result:
            actual_rows.append(result.first)
            result = result.rest

        self.assertEqual(actual_rows, expected_rows)

if (__name__ == '__main__'):
    unittest.main()
