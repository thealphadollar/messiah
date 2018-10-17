#!/usr/bin/python
#-*- coding: utf-8 -*-

from flask import Flask, request, jsonify
from db_handler import DBHandler

app = Flask(__name__)

@app.route('/history', methods=['GET'])
def get_history():
    country = request.args.get('country')

    db_handle = DBHandler()
    query = db_handle.query("Country", country)

    return jsonify(query)

if __name__ == '__main__':
    app.run(debug=True)