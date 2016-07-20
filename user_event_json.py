#!/usr/bin/env python

from flask import Flask, request, jsonify

import json
import sys
import csv
import time


def to_csv(parsed_input):
    # Create csv file and write data to it
    keys = parsed_input.keys()
    csv_file_name = str(parsed_input['user_id']) + "_" + time.strftime("%d_%m_%Y") + "_data.csv"

    with open(csv_file_name, 'w') as csvfile:
        #dict_writer = csv.DictWriter(csvfile, fieldnames=['height', 'weight', 'name'])
        dict_writer = csv.DictWriter(csvfile, fieldnames=keys)
        dict_writer.writeheader() # writing header in the csv file
        dict_writer.writerow(parsed_input)

    return csv_file_name


app = Flask(__name__)

@app.route('/user_events', methods=['POST'])
def save_user_event():
    data = request.json
    if 'user_id' not in data.keys():
        return 'Error! user_id field is missing\n'
    else:   
        filename = to_csv(data)
        return filename


if __name__ == '__main__':
    app.run(debug=True)

