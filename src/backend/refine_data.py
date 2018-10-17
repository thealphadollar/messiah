"""
To refine the data downloaded from the internet
"""
import json
import os


EARTHQUAKE_DATA_FILE = "data/eq.json"


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


if __name__=='__main__':
    refine_earthquake_data()
