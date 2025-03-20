#File: tournament.py
#Author: Taylor King
#Description This file contains the Tournament class for managing a bracketstyle car competition. It reads the configuration from a JSON file, loads any relevant attributes, and  manages sponsors, teams, car purchases, and the competition process.

import json

#Tournament class
class Tournament:
    """
    Represents a bracket-style competition focused on fuel-efficient cars and teams sponsored by car makers.
    """
    def __init__(self, config_path='./data/config.json'):
        """
        Initialises the Tournament by reading a json config file.

        :param config_path: Path to the config file.
        :type config_path: str
        """
        with open(config_path, 'r') as f:
            config = json.load(f)

        #Required attributes from config.json as follows:
        self.name = config['tournament_name']
        self.car_data_path = config['car_data_path']
        self.nteams = config.get('nteams', 16)
        self.default_low = config['default_low']
        self.default_high = config['default_high']
        self.default_incr = config['default_incr']
