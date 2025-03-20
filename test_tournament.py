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

#Test the nteams is a positive and nonzero integer
def test_nteams_positive_nonzero():
    """
    Test Tournament initialisation with zero or negative nteams to ensure AssertionError is raised appropriately.
    """
    print("Running Tournament nteams positive, non-zero assertion test...")

    invalid_configs = [
        {"nteams": 0, "description": "zero teams"},
        {"nteams": -8, "description": "negative number of teams"}
    ]

    for config_case in invalid_configs:
        #Prepare invalid config data.
        invalid_config = {
            "car_data_path": "./data/cars_modified.csv",
            "tournament_name": f"Invalid {config_case['description']} Tournament",
            "nteams": config_case["nteams"],
            "default_low": 10000,
            "default_high": 50000,
            "default_incr": 5000
        }

        #Write temp invalid config file.
        invalid_config_path = f"./data/invalid_{config_case['description']}_config.json"
        with open(invalid_config_path, 'w') as f:
            json.dump(invalid_config, f)

        try:
            #Attempt to create Tournament with invalid nteams.
            Tournament(invalid_config_path)
            assert False, f"AssertionError was expected but not raised for {config_case['description']}."
        except AssertionError as e:
            assert str(e) == "Number of teams must be positive and non-zero.", "Incorrect assertion message."
            print(f"Correctly caught assertion for {config_case['description']}.")

    print("nteams positive, non-zero assertion tests passed.")

def test_nteams_power_of_two():
    """
    Test Tournament initialisation with nteams not being a power of two to ensure AssertionError is raised appropriately.
    """
    print("Running Tournament nteams power-of-two assertion test...")

    invalid_configs = [
        {"nteams": 3, "description": "not a power of 2 (3)"},
        {"nteams": 12, "description": "not a power of 2 (12)"},
        {"nteams": 7, "description": "not a power of 2 (7)"}
    ]

    for config_case in invalid_configs:
        #Prepare invalid config data.
        invalid_config = {
            "car_data_path": "./data/cars_modified.csv",
            "tournament_name": f"Invalid {config_case['description']} Tournament",
            "nteams": config_case["nteams"],
            "default_low": 10000,
            "default_high": 50000,
            "default_incr": 5000
        }

        #Write temporary invalid config file.
        invalid_config_path = f"./data/invalid_{config_case['description']}_config.json"
        with open(invalid_config_path, 'w') as f:
            json.dump(invalid_config, f)

        try:
            #Attempt to create Tournament with invalid nteams.
            Tournament(invalid_config_path)
            assert False, f"AssertionError was expected but not raised for {config_case['description']}."
        except AssertionError as e:
            assert str(e) == "Number of teams must be a power of two.", "Incorrect assertion message."
            print(f"Correctly caught assertion for {config_case['description']}.")

    print("nteams power-of-two assertion tests passed.")

def test_tournament_repr_str():
    """
    Test the __repr__ and __str__ methods for sensible object representation.
    """
    print("Running Tournament object representation tests...")

    tournament = Tournament('./data/config.json')

    #Test __repr__
    expected_repr = f"Tournament(name='{tournament.name}', nteams={tournament.nteams})"
    actual_repr = repr(tournament)
    assert actual_repr == expected_repr, f"__repr__ output incorrect. Got: {actual_repr}"

    #Test __str__
    expected_str = f"{tournament.name} ({tournament.nteams} teams)"
    actual_str = str(tournament)
    assert actual_str == expected_str, f"__str__ output incorrect. Got: {actual_str}"

    print("__repr__ and __str__ methods tests passed.")

def test_generate_sponsors():
    """
    Test generate_sponsors method for sponsor selection, budget allocation, handling optional sponsor_list, and fixed_budget.
    """
    print("Running generate_sponsors tests...")

    #Setup Tournament obj.
    tournament = Tournament('./data/config.json')

    #Makes are:
    available_makers = ['Ford', 'Toyota', 'BMW', 'Honda', 'Tesla', 'Hyundai', 'Chevrolet', 'Volkswagen',
                        'Audi', 'Nissan', 'Mazda', 'Kia', 'Subaru', 'Mercedes', 'Volvo', 'Jaguar']

    #Test default behaviour.
    tournament.generate_sponsors()
    assert len(tournament.sponsors) == tournament.nteams, "Incorrect number of sponsors assigned."
    assert len(set(tournament.sponsors)) == tournament.nteams, "Duplicate sponsors assigned."

    #Test sponsor_list argument.
    specific_sponsors = ['Ford', 'Toyota', 'Tesla']
    tournament.generate_sponsors(sponsor_list=specific_sponsors)
    assert set(specific_sponsors).issubset(set(tournament.sponsors)), "Specific sponsors not correctly assigned."

    #Test fixed_budget argument within bounds.
    tournament.generate_sponsors(fixed_budget=30000)
    assert all(budget == 30000 for budget in tournament.budgets), "Fixed budget incorrectly assigned."

    #Test fixed_budget outside bounds raises AssertionError.
    try:
        tournament.generate_sponsors(fixed_budget=99999999)
        assert False, "AssertionError expected due to invalid fixed_budget but not raised."
    except AssertionError as e:
        print("Correctly caught invalid fixed_budget assertion.")

    print("generate_sponsors tests passed.")

def test_generate_teams():
    """
    Test generate_teams method to ensure correct team generation and initialisation based on sponsors and budgets.
    """
    print("Running generate_teams tests...")

    #Setup Tournament and generate sponsors first.
    tournament = Tournament('./data/config.json')
    tournament.generate_sponsors()

    #Generate teams.
    tournament.generate_teams()

    #Assert correct number of teams generated.
    assert len(tournament.teams) == tournament.nteams, "Incorrect number of teams generated."

    #Assert teams have correct sponsors and budgets.
    for idx, team in enumerate(tournament.teams):
        assert team.sponsor == tournament.sponsors[idx], "Team sponsor mismatch."
        assert team.budget == tournament.budgets[idx], "Team budget mismatch."
        assert team.inventory == [], "Team inventory should initially be empty."
        assert team.active is True, "Team active status should initially be True."
        assert team.performance == {'wins': 0, 'losses': 0, 'scores': [], 'cars_used': 0}, "Team performance record mismatch."

    print("generate_teams tests passed.")

def test_team_object():
    """
    Test the internal Team class within Tournament for correct attribute assignment, mutability, and string representation.
    """
    print("Running internal Team class tests...")

    #Setup a single team object directly.
    tournament = Tournament('./data/config.json')
    sponsor = "Tesla"
    budget = 45000
    team = tournament.Team(sponsor, budget)

    #Check attributes.
    assert team.sponsor == sponsor, "Incorrect team sponsor."
    assert team.budget == budget, "Incorrect team budget."
    assert team.inventory == [], "Inventory should initially be empty."
    assert team.active is True, "Active status should initially be True."
    assert team.performance == {'wins': 0, 'losses': 0, 'scores': [], 'cars_used': 0}, "Incorrect initial performance record."

    #Test mutability.
    team.inventory.append("Model 3")
    team.active = False
    team.performance['wins'] += 1
    team.performance['scores'].append(120)
    assert team.inventory == ["Model 3"], "Inventory mutability issue."
    assert team.active is False, "Active status mutability issue."
    assert team.performance['wins'] == 1, "Performance record mutability issue."
    assert team.performance['scores'] == [120], "Performance score mutability issue."

    #Test __str__ representation.
    expected_str = "Team Tesla | Budget: $45000 | Active: False | Inventory: ['Model 3']"
    actual_str = str(team)
    assert actual_str == expected_str, f"__str__ method incorrect. Got: {actual_str}"

    print("Internal Team class tests passed.")


if __name__ == '__main__':
    test_init()
    test_nteams_integer()
    test_nteams_positive_nonzero()
    test_nteams_power_of_two()
    test_tournament_repr_str()
    test_generate_sponsors()
    test_generate_teams()
    test_team_object()

