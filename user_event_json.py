#!/usr/bin/env python

from flask import Flask, request, jsonify

import json
import sys
import csv
import time
import MySQLdb
import yaml
import boto3

__config = None

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




def notify_user(json_event, router_settings):
    if json_event['event'] in router_settings['routing']:
        for service in router_settings['routing'][json_event['event']]:
            print "Sending {event} event to {services} service.".format(event = json_event['event'], services = service)


def db_connect():
    # Open database connection
    db = MySQLdb.connect("localhost","root","","shoppimon_hub")
    return db


def send_event(json_event, db):
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

    router_settings = get_config("s3://shoppimon-artifacts/event_hub_config.yml")
    notify_user(data, router_settings)
    db = db_connect()
    send_event(data, db)


def get_config(path):
    global __config

    if path.startswith("s3"):
        # Use Amazon S3
        s3 = boto3.client('s3')

        bucket_name = path.split("/")[2]
        key_name = path.split(bucket_name)[-1]

        # Download object at bucket-name with key-name to tmp.txt
        s3.download_file(bucket_name, key_name, "tmp.yaml")

        if __config is None:
            with open("tmp.yaml", 'r') as stream:
                __config = yaml.load(stream)
        
    else:
        if __config is None:
            with open(path, 'r') as stream:
                __config = yaml.load(stream)

    return __config


if __name__ == '__main__':
    app.run(debug=True)