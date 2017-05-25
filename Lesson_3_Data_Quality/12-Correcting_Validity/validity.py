"""
Your task is to check the "productionStartYear" of the DBPedia autos datafile for valid values.
The following things should be done:
- check if the field "productionStartYear" contains a year
- check if the year is in range 1886-2014
- convert the value of the field to be just a year (not full datetime)
- the rest of the fields and values should stay the same
- if the value of the field is a valid year in range, as described above,
  write that line to the output_good file
- if the value of the field is not a valid year,
  write that line to the output_bad file
- discard rows (neither write to good nor bad) if the URI is not from dbpedia.org
- you should use the provided way of reading and writing data (DictReader and DictWriter)
  They will take care of dealing with the header.

You can write helper functions for checking the data and writing the files, but we will call only the
'process_file' with 3 arguments (inputfile, output_good, output_bad).
"""
import csv
import pprint

INPUT_FILE = 'autos.csv'
OUTPUT_GOOD = 'autos-valid.csv'
OUTPUT_BAD = 'FIXME-autos.csv'

def process_file(input_file, output_good, output_bad):
    import re

    with open(input_file, "r") as f, open(output_good, 'w') as good_f, open(output_bad, 'w') as bad_f:
        reader = csv.DictReader(f)
        header = reader.fieldnames

        good_writer = csv.DictWriter(good_f, fieldnames=header, delimiter=',')
        good_writer.writeheader()
        bad_writer = csv.DictWriter(bad_f, fieldnames=header, delimiter=',')
        bad_writer.writeheader()

        #COMPLETE THIS FUNCTION
        for line in reader:
            if line['URI'].startswith('http://dbpedia.org'):
                year_extract = re.compile(r'\d{4}').findall(line['productionStartYear'])
                if year_extract:
                    year = int(year_extract[0])
                    print(year)
                    if (year >= 1886) & (year <= 2014):
                        print('its ok')
                        line['productionStartYear'] = year
                        good_writer.writerow(line)
                    else:
                        print('baaad')
                        bad_writer.writerow(line)
                else:
                    print('very baaad')
                    bad_writer.writerow(line)


def test():

    process_file(INPUT_FILE, OUTPUT_GOOD, OUTPUT_BAD)


if __name__ == "__main__":
    test()

test()
