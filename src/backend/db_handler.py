"""
class to handle all database operations
"""

import os
import json
import sqlite3
from contextlib import contextmanager
from sqlite3 import Error

import reverse_geocode


DB_PATH = os.path.join(os.path.dirname(__file__), "data/data.db")

# indexes for various disaster values in database
DIS_ID = 0
DIS_DATE = 1
DIS_CITY = 2
DIS_COUN = 3
DIS_MAGN = 4
DIS_SOUR = 5
DIS_TYPE = 6


class DBHandler:
    """
    Class providing endpoints to interact with the database of disasters
    """
    def __init__(self):
        pass

    def query(self, query_type, keyword):
        """
        allows gathering data matching the given keyword for the given query

        :param query_type: column to match e.g "City" NOTE: CASE SENSITIVE
                Accepted values (as it is in string format) are:
                    -Date
                    -City
                    -Country
                    -Magnitude
                    -Source
                    -DisType
        :param keyword: keyword to match, e.g. "India" NOTE: FIRST LETTER CAPITAL
        :return: list containing column values for all disasters indexed as marked at top
        """
        keyword = keyword.title()
        query_cmd = """SELECT * FROM disasters
                        WHERE {q_type}='{keyword}'
                        """.format(
            q_type=query_type,
            keyword=keyword
        )
        with self._connect() as db_cur:
            db_cur.execute(query_cmd)
            data = db_cur.fetchall()
        # print(type(data))
        # print(data)

        if len(data) != 0:
            return data
        else:
            print("No matching data for {query} in {col} column".format(
                query=keyword,
                col=query_type
            ))

    def _instantiate(self):
        """
        Instantiate a db file with the required table(s)
        TO BE CALLED MANUALLY FROM WITHIN SCRIPT

        :return: None
        """
        print("creating database with table(s) at " + DB_PATH)

        with self._connect() as db_cur:

            # create disasters table
            db_cur.execute("""CREATE TABLE IF NOT EXISTS disasters (
                            dis_id integer PRIMARY KEY,
                            Date text,
                            City text,
                            Country text NOT NULL,
                            Magnitude text,
                            Source text,
                            DisType text NOT NULL 
                            );
            """)

            # indexing columns for faster access
            db_cur.execute("""CREATE INDEX IF NOT EXISTS indexed_type ON disasters(
                                DisType
                                );
            """)

    def _add_data(self, dis_type, json_path, require_rev_geocoding):
        """
        Adds data to the database.

        :param dis_type: type of disaster data, e.g. "earthquake"
        :param json_path: path to the json file relative to script path
        :param require_rev_geocoding: True if json contains lat and long, False otherwise.
        :return: None
        """
        path_to_data = os.path.join(os.path.dirname(__file__), json_path)
        with open(path_to_data, "r") as data_file:
            data_list = json.load(data_file)

        with self._connect() as db_cur:
            for data in data_list:
                if require_rev_geocoding:
                    data['City'], data['Country'] = self._rev_geocode(data['Latitude'], data['Longitude'])
                    del data['Latitude']
                    del data['Longitude']
                data['DisType'] = dis_type

                cols = ', '.join('"{}"'.format(col) for col in data.keys())
                vals = ', '.join('"{}"'.format(col) for col in data.values())

                try:
                    command = """INSERT INTO "disasters"
                                ({keys})
                                VALUES ({values})""".format(
                        keys=cols,
                        values=vals
                    )
                    # print(command)
                    db_cur.execute(command)
                except Error as err:
                    print("Failed to insert data")
                    print(err)
                # break

    @staticmethod
    def _rev_geocode(lat, long):
        """
        reverse codes a pair of latitude and longitude into city and country
        :param lat: latitude of the place
        :param long: longitude of the place
        :return: city, country
        """
        coordinate = (lat, long)
        loc_data = reverse_geocode.get(coordinate)
        return loc_data['city'], loc_data['country']

    @staticmethod
    @contextmanager
    def _connect():
        """
        provides connection to the database

        :yields: Cursor to database
        :return: None
        """
        try:
            conn = sqlite3.connect(DB_PATH, timeout=30)
            yield conn.cursor()
            conn.commit()
            conn.close()
        except Error as err:
            print("Failed to connect to the database")
            print(err)
            raise Exception


if __name__ == '__main__':
    manual_db_handle = DBHandler()
    # manual_db_handle._instantiate()
    # manual_db_handle._add_data("earthquake", "data/eq.json", True)
    manual_db_handle.query("Country", "india")
