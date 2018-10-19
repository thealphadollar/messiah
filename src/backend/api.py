#!/usr/bin/python
#-*- coding: utf-8 -*-

from flask import Flask, request, jsonify
from db_handler import DBHandler
import json
import os
import random

CASUALTY_DATA_FILE = "data/random_facts.json"

app = Flask(__name__)

@app.route('/history', methods=['GET'])
def get_history():
    country = request.args.get('country')

    db_handle = DBHandler()
    query = db_handle.query("Country", country)

    return jsonify(query)


@app.route('/random_facts', methods=['GET'])
def get_random_facts():
    with open(os.path.join(os.path.dirname(__file__), CASUALTY_DATA_FILE)) as f:
        data = json.loads(f.read())

    n = len(data)
    i = random.randint(0, n)
    
    deaths = data[i]['Deaths']
    year = data[i]['Year']
    disaster = data[i]['Type']

    return ("Do you know {deaths} number of people died in {year} from {disaster}").format(deaths=deaths, year=year, disaster=disaster)

if __name__ == '__main__':
    app.run(debug=True)