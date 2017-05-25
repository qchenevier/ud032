# -*- coding: utf-8 -*-
# Find the time and value of max load for each of the regions
# COAST, EAST, FAR_WEST, NORTH, NORTH_C, SOUTHERN, SOUTH_C, WEST
# and write the result out in a csv file, using pipe character | as the delimiter.
# An example output can be seen in the "example.csv" file.
import xlrd
import os
import csv
from zipfile import ZipFile
datafile = "2013_ERCOT_Hourly_Load_Data.xls"
outfile = "2013_Max_Loads.csv"


def open_zip(datafile):
    with ZipFile(datafile.replace('.xls', '.zip'), 'r') as myzip:
        myzip.extractall()


def parse_file(datafile):
    workbook = xlrd.open_workbook(datafile)
    sheet = workbook.sheet_by_index(0)
    data = None
    # YOUR CODE HERE
    # Remember that you can use xlrd.xldate_as_tuple(sometime, 0) to convert
    # Excel date to Python tuple of (year, month, day, hour, minute, second)
    labels = sheet.row(0)
    dates = [xlrd.xldate_as_tuple(cell.value, 0) for cell in sheet.col_slice(0, 1)]
    data = [['Station', 'Year', 'Month', 'Day', 'Hour', 'Max Load']]
    col_num = 1
    while col_num < sheet.ncols - 1:
        label = labels[col_num].value
        col_data = [cell.value for cell in sheet.col_slice(col_num, 1)]
        max_value = max(col_data)
        col_data.index(max_value)
        max_date = dates[col_data.index(max_value)]
        col_num += 1
        data.append([label] + list(max_date)[0:4] + [max_value])

    return data

def save_file(data, filename):
    with open(filename, 'w', newline='') as f:
    # with open(filename, 'wb') as f:
        csv_writer = csv.writer(f, delimiter='|')
        csv_writer.writerows(data)


def test():
    open_zip(datafile)
    data = parse_file(datafile)
    save_file(data, outfile)

    ans = {'FAR_WEST': {'Max Load': "2281.2722140000024", 'Year': "2013", "Month": "6", "Day": "26", "Hour": "17"}}

    fields = ["Year", "Month", "Day", "Hour", "Max Load"]
    with open(outfile) as of:
        csvfile = csv.DictReader(of, delimiter="|")
        for line in csvfile:
            s = line["Station"]
            if s == 'FAR_WEST':
                for field in fields:
                    assert ans[s][field] == line[field]


test()
