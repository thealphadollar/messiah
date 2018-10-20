#!/usr/bin/python
#-*- coding: utf-8 -*-

from flask import Flask, request, jsonify, render_template, abort
from db_handler import DBHandler
import json
import os
import random

CASUALTY_DATA_FILE = "data/random_facts.json"

app = Flask(__name__)

@app.route('/history', methods=['GET'])
def get_history():
    """
    Returns the history of disasters for a country/city
    """

    args = ['Country', 'City']
    query = None

    arg = request.args.to_dict().keys()[0]

    if arg in args:
        val = request.args.get(arg)
        db_handle = DBHandler()
        query = db_handle.query(arg, val)

    return jsonify(query)


"""
@app.route('/random_facts', methods=['GET'])
def get_random_facts():
    #Return a random fact from past years data

    with open(os.path.join(os.path.dirname(__file__), CASUALTY_DATA_FILE)) as f:
        data = json.loads(f.read())

    n = len(data)
    i = random.randint(0, n)
    
    deaths = data[i]['Deaths']
    year = data[i]['Year']
    disaster = data[i]['Type']

    return ("Do you know {deaths} number of people died in {year} from {disaster}").format(deaths=deaths, year=year, disaster=disaster)
"""

@app.route('/random_facts', methods=['GET'])
def get_random_facts():
    """
    Return a random fact from past years data
    """

    with open(os.path.join(os.path.dirname(__file__), CASUALTY_DATA_FILE)) as f:
        data = json.loads(f.read())

    facts = []

    for item in data:
        deaths = item['Deaths']
        year = item['Year']
        disaster = item['Type']

        facts.append('{deaths} {year} {disaster}'.format(deaths=deaths, year=year, disaster=disaster))

    return render_template('random_facts.html', facts=facts)

if __name__ == '__main__':
    app.run(debug=True)