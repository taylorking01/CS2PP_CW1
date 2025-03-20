#File: test_tournament.py
#Author: Taylor King
#Description: This file contains unit tests for the Tournament class, applying a TDD approach, ensuring the Tournament class initialisation and attribute loading from config.json functions correctly.

import json
from tournament import Tournament

#Test initialisation.
def test_init():
    """
    Test initialisation of a Tournament instance to ensure required attributes match config.json.
    """
    print("Running Tournament initialisation tests...")

    #Initialise the Tournament.
    tournament = Tournament('./data/config.json')

    #Load the config file separately for comparison.
    with open('./data/config.json') as f:
        config = json.load(f)

    #Assertions are as follows:
    assert tournament.name == config['tournament_name'], "Tournament name mismatch."
    assert tournament.car_data_path == config['car_data_path'], "Car data path mismatch."
    assert tournament.nteams == config.get('nteams', 16), "nteams value mismatch."
    assert tournament.default_low == config['default_low'], "Default_low mismatch."
    assert tournament.default_high == config['default_high'], "Default_high mismatch."
    assert tournament.default_incr == config['default_incr'], "Default_incr mismatch."

    print("All init tests passed.")

#Test nteams is integer
def test_nteams_integer():
    """
    Test Tournament initialisation with non-integer nteams to ensure TypeError is raised appropriately.
    """
    print("Running Tournament nteams integer validation test...")

    #Prepare invalid config data.
    invalid_config = {
        "car_data_path": "./data/cars_modified.csv",
        "tournament_name": "Invalid Teams Tournament",
        "nteams": "sixteen",  #Invalid.
        "default_low": 10000,
        "default_high": 50000,
        "default_incr": 5000
    }

    #Write temp invalid config file.
    invalid_config_path = './data/invalid_config.json'
    with open(invalid_config_path, 'w') as f:
        json.dump(invalid_config, f)

    try:
        #Try to create Tournament with invalid nteams.
        Tournament(invalid_config_path)
        assert False, "TypeError was expected but not raised."
    except TypeError as e:
        assert str(e) == "The number of teams must be an integer.", "Incorrect exception message."
        print("Correctly caught non-integer nteams initialisation.")

    print("nteams integer validation test passed.")

if __name__ == '__main__':
    test_init()
    test_nteams_integer()
