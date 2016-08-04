#!/usr/bin/env python

from flask import Flask, request, jsonify

import json
import sys
import csv
import time
import yaml
import MySQLdb

app = Flask(__name__)


def to_csv(parsed_input):
    """Get a dict of event data and save it to CSV file
    """
    keys = parsed_input.keys()
    try:
        csv_file_name = str(parsed_input['user_id']) + "_" + time.strftime("%d_%m_%Y") + "_data.csv"
    except KeyError:
        csv_file_name = str(parsed_input['account_id']) + "_" + time.strftime("%d_%m_%Y") + "_data.csv"


    with open(csv_file_name, 'w') as csvfile:
        #dict_writer = csv.DictWriter(csvfile, fieldnames=['user_id', 'height', 'weight', ])
        dict_writer = csv.DictWriter(csvfile, fieldnames=keys)
        dict_writer.writeheader() # writing header in the csv file
        dict_writer.writerow(parsed_input)

    return csv_file_name + "\n"


def send_event(json_event):
    with open("config.yaml", 'r') as stream:
        router_settings = yaml.load(stream)

    if json_event['event'] in router_settings['routing']:
        for service in router_settings['routing'][json_event['event']]:
            print "Sending {event} event to {services} service.".format(event = json_event['event'], services = service) 

    # Open database connection
    db = MySQLdb.connect("localhost","root","","shoppimon_hub")

    # Prepare a cursor object using cursor() method
    cursor = db.cursor()

    # Prepare SQL query to INSERT a record into the database.
    sql = ("INSERT INTO user_data(event_id, time, user_id, account_id, event, source, attributes) "
           "VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s' )") % (
            json_event['event_id'], 
            json_event['time'], 
            json_event['user_id'], 
            json_event['account_id'], 
            json_event['event'], 
            json_event['source'], 
            json.dumps(json_event['attributes']))
    
    try:
        # Execute the SQL command
        cursor.execute(sql)
        # Commit your changes in the database
        db.commit()
    except:
        # Rollback in case there is any error
        db.rollback()
        print "Error"

    # disconnect from server
    db.close()


@app.route('/user_events', methods=['POST'])
def save_user_event():
    data = request.json
    if ('user_id' not in data.keys()) and ('account_id' not in data.keys()):
        return 'Error! user_id or account_id field is missing\n'
    elif 'event' not in data.keys():
        return 'Error! event field is missing\n'
    elif 'source' not in data.keys():
        return 'Error! source field is missing\n'
    else:   
        filename = to_csv(data)
        send_event(data)
        return filename


if __name__ == '__main__':
    app.run(debug=True)