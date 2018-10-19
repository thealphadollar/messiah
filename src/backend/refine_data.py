"""
To refine the data downloaded from the internet
"""
import json
import os


EARTHQUAKE_DATA_FILE = "data/eq.json"
FLOOD_DATA_FILE = "data/floods.json"


def refine_earthquake_data():
    """
    removes unnecessary columns from earthquake data

    :return: None
    """
    path_to_eq_data = os.path.join(os.path.dirname(__file__), EARTHQUAKE_DATA_FILE)
    with open(path_to_eq_data, "r") as eq_file:
        eq_dict = json.load(eq_file)

    new_eq_data = []

    for data in eq_dict:
        # print(data)
        # break
        new_eq_data.append(
            {
                'Date': data['Date'],
                'Latitude': data['Latitude'],
                'Longitude': data['Longitude'],
                'Magnitude': str(data['Magnitude']) + " " + data['Magnitude Type'],
                'Source': data['Source']
            }
        )
    with open(path_to_eq_data, "w") as eq_file:
        json.dump(new_eq_data, eq_file)


def refine_flood_data():
    """
    removes unnecessary columns from flood data

    :return: None
    """
    path_to_fld_data = os.path.join(os.path.dirname(__file__), FLOOD_DATA_FILE)
    with open(path_to_fld_data, "r") as fld_file:
        fld_dict = json.load(fld_file)

    new_fld_data = []

    for data in fld_dict:
        # print(data)
        # break
        new_fld_data.append(
            {
                'Date': data['Began'],
                'Latitude': data['lat'],
                'Longitude': data['long'],
                'Magnitude': str("Severity " + str(data['Severity'])),
                'Source': data['Validation']
            }
        )
    with open(path_to_fld_data, "w") as fld_file:
        json.dump(new_fld_data, fld_file)


if __name__=='__main__':
    # refine_earthquake_data()
    # refine_flood_data()
