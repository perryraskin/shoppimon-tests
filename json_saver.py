#!/usr/bin/env python

import json
import sys
import csv
import time

def json_in(fh):
    contents = json.load(fh)
    return contents

def to_csv(parsed_input):
    # Create csv file and write data to it
    keys = parsed_input.keys()
    csv_file_name = time.strftime("%d_%m_%Y") + "_data.csv"

    with open(csv_file_name, 'w') as csvfile:
        #dict_writer = csv.DictWriter(csvfile, fieldnames=['height', 'weight', 'name'])
        dict_writer = csv.DictWriter(csvfile, fieldnames=keys)
        dict_writer.writeheader() # writing header in the csv file
        dict_writer.writerow(parsed_input)

def main():
    user_input = json_in(sys.stdin)
    to_csv(user_input)

if __name__ == '__main__':
    main()
