#File: tournament.py
#Author: Taylor King
#Description This file contains the Tournament class for managing a bracketstyle car competition. It reads the configuration from a JSON file, loads any relevant attributes, and  manages sponsors, teams, car purchases, and the competition process.

import json
import random
import csv

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
        :raises TypeError: If 'nteams' is not an integer.
        :raises AssertionError: If 'nteams' is not positive and non-zero.
        :raises AssertionError: If 'nteams' is not a power of two.
        """
        with open(config_path, 'r') as f:
            config = json.load(f)

        #Required attributes from config.json as follows:
        self.name = config['tournament_name']
        self.car_data_path = config['car_data_path']
        self.nteams = config.get('nteams', 16)

        #Validate that nteams is an integer.
        if not isinstance(self.nteams, int):
            raise TypeError("The number of teams must be an integer.")

        #Validate that nteams is positive and non-zero integer.
        assert self.nteams > 0, "Number of teams must be positive and non-zero."

        # Validate that nteams is a power of two
        assert (self.nteams & (self.nteams - 1) == 0), "Number of teams must be a power of two."

        self.default_low = config['default_low']
        self.default_high = config['default_high']
        self.default_incr = config['default_incr']

        self.sponsors = []
        self.budgets = []
        self.teams = []


    def __repr__(self):
        """
        Returns an unambiguous str of the Tournament obj.
        """
        return f"Tournament(name='{self.name}', nteams={self.nteams})"

    def __str__(self):
        """
        Returns a readable str of the Tournament obj.
        """
        return f"{self.name} ({self.nteams} teams)"

    def generate_sponsors(self, sponsor_list=None, low=None, high=None, incr=None, fixed_budget=None):
        """
        Generates a unique sponsor and budget for each team.
        
        :param sponsor_list: Optional list of sponsors to explicitly include.
        :param low: Lower bound for random budgets (default from config).
        :param high: Upper bound for random budgets (default from config).
        :param incr: Increment for budgets (default from config).
        :param fixed_budget: Optional fixed budget for all teams.
        :raises AssertionError: If fixed_budget is provided but outside allowed range.
        """
        #Use default values if not specified.
        low = low if low is not None else self.default_low
        high = high if high is not None else self.default_high
        incr = incr if incr is not None else self.default_incr
    
        available_makers = ['Ford', 'Toyota', 'BMW', 'Honda', 'Tesla', 'Hyundai', 'Chevrolet', 'Volkswagen',
                            'Audi', 'Nissan', 'Mazda', 'Kia', 'Subaru', 'Mercedes', 'Volvo', 'Jaguar']
    
        #Validate fixed_budget.
        if fixed_budget is not None:
            assert low <= fixed_budget <= high, "fixed_budget must be within low and high bounds."
    
        self.sponsors = []
        self.budgets = []
    
        #Use provided sponsors first.
        if sponsor_list:
            assert len(sponsor_list) <= self.nteams, "Sponsor list longer than number of teams."
            self.sponsors.extend(sponsor_list)
    
        #Select remaining sponsors randomly with no duplicates.
        remaining_makers = list(set(available_makers) - set(self.sponsors))
        random.shuffle(remaining_makers)
        while len(self.sponsors) < self.nteams:
            self.sponsors.append(remaining_makers.pop())
    
        #Assign budgets.
        for _ in range(self.nteams):
            if fixed_budget is not None:
                budget = fixed_budget
            else:
                budget = random.randrange(low, high + incr, incr)
            self.budgets.append(budget)

    def generate_teams(self):
        """
        Generates Team objects for each sponsor and budget pair. Populates the Tournament's teams attribute.
        """
        self.teams = []
        for sponsor, budget in zip(self.sponsors, self.budgets):
            team = self.Team(sponsor, budget)
            self.teams.append(team)

    def buy_cars(self):
        """
        Allows each team to purchase their initial inventory.
        """
        for team in self.teams:
            self._purchase_inventory(team)

    def _purchase_inventory(self, team):
        """
        Purchases optimal cars for team based on sponsor, maximising MPG-H within budget using greedy algorithm.
        Greedy algorithm justification:
        At each step, select the car with the highest MPG-H per cost ratio, providing a good local optimum.
        Greedy method is efficient (O(n log n)) and practical for this budget-constrained selection.
    
        :param team: The Team object for which inventory is purchased.
        """
        #Load car data clearly from csv file.
        available_cars = []
        with open(self.car_data_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['Make'] == team.sponsor:
                    available_cars.append({
                        'Model': row['Model'],
                        'Cost': int(row['Cost']),
                        'MPG-H': int(row['MPG-H']),
                        'Ratio': int(row['MPG-H']) / int(row['Cost']) #Efficiency clearly calculated.
                    })
    
        #Sort cars clearly by MPG-H per cost ratio (descending) greedy criterion.
        available_cars.sort(key=lambda x: x['Ratio'], reverse=True)
    
        #Clear loop to buy cars greedily.
        for car in available_cars:
            if car['Cost'] <= team.budget:
                team.inventory.append(car['Model'])
                team.budget -= car['Cost'] #Clearly update budget.
    
    class Team:
        """
        Represents a single competing team with sponsor, budget, inventory, active status, and performance record.
        """
        def __init__(self, sponsor, budget):
            """
            Initialises a Team object.
    
            :param sponsor: The car maker sponsoring this team.
            :param budget: Initial budget allocated to the team.
            """
            self.sponsor = sponsor            #Immutable
            self.budget = budget              #Mutable (budget changes after car purchases)
            self.inventory = []               #Mutable (cars are added throughout tournament)
            self.active = True                #Mutable (changes if eliminated)
            self.performance = {              #Mutable (updated after matches)
                'wins': 0,
                'losses': 0,
                'scores': [],
                'cars_used': 0
            }
    
        def __str__(self):
            """
            Returns a clear, readable representation of the team.
            """
            return f"Team {self.sponsor} | Budget: ${self.budget} | Active: {self.active} | Inventory: {self.inventory}"
    
