#File: test_tournament.py
#Author: Taylor King
#Description: This file contains unit tests for the Tournament class, applying a TDD approach, ensuring the Tournament class initialisation and attribute loading from config.json functions correctly.

import json
from tournament import Tournament

#Test initialisation
def test_init():
    """
    Test initialisation of a Tournament instance to ensure required attributes match config.json.
    """
    print("Running Tournament initialization tests...")

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

if __name__ == '__main__':
    test_init()
