#!/usr/bin/python
#-*- coding: utf-8 -*-

from flask import Flask, request, jsonify, render_template, abort
from flask_cors import CORS, cross_origin
from .db_handler import DBHandler
from .predict import *
import json
import os
import random
import datetime
import pandas as pd

CASUALTY_DATA_FILE = "data/random_facts.json"

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/history', methods=['GET'])
@cross_origin()
def get_history():
    """
    Returns the history of disasters for a country/city
    """

    args = ['Country', 'City']
    query = None

    arg = list(request.args.to_dict().keys())[0]

    if arg in args:
        val = request.args.get(arg)
        db_handle = DBHandler()
        query = db_handle.query(arg, val)

    # reducing the length of the response
    if len(query) < 5:
        query = random.sample(query, len(query))
    else:
        query = random.sample(query, 5)

    return jsonify(query)


@app.route('/history_full', methods=['GET'])
@cross_origin()
def get_full_history():
    """
    Returns the history of disasters for a country/city
    """

    args = ['Country', 'City']
    query = None

    arg = list(request.args.to_dict().keys())[0]

    if arg in args:
        val = request.args.get(arg)
        db_handle = DBHandler()
        query = db_handle.query(arg, val)
        
    data=pd.DataFrame(jsonify(query))
    data.columns=['Deaths', 'Date', 'City', 'Country', 'Severity', 'Source', 'Disaster']
    data=data.drop(['City', 'Source'], 1)
    dic = data.to_dict()
    return (dic)


@app.route('/show_random_facts', methods=['GET'])
def show_random_facts():
    #Return a random fact from past years data

    with open(os.path.join(os.path.dirname(__file__), CASUALTY_DATA_FILE)) as f:
        data = json.loads(f.read())

    n = len(data)
    i = random.randint(0, n)
    
    deaths = data[i]['Deaths']
    year = data[i]['Year']
    disaster = data[i]['Type']

    return ("Do you know {deaths} number of people died in {year} from {disaster}?").format(deaths=deaths, year=year, disaster=disaster)


@app.route('/random_facts', methods=['GET'])
@cross_origin()
def get_random_facts():
    """
    Return a random fact from past years data
    """

    with open(os.path.join(os.path.dirname(__file__), CASUALTY_DATA_FILE)) as f:
        data = json.loads(f.read())

    facts = []

    for item in data:
        facts.append([item['Deaths'], item['Year'], item['Type']])

    return jsonify(facts)


@app.route('/predict_eq_mag', methods=['GET'])
def get_eq_mag():
    """
    Predict Earthquake from lattitude, longitude, depth, date
    """

    args = request.args.to_dict()
    lat = args['lat']
    long = args['long']
    depth = args['depth']

    try:
        date = args['date']
    
    except KeyError:
        now = datetime.datetime.now()
        date = '%s/%s/%s' % (now.month, now.day, now.year)



    return str(predict_eq(lat, long, depth, str(date)))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
