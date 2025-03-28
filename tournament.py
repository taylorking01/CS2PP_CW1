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

        #Validate that nteams is a power of two.
        assert (self.nteams & (self.nteams - 1) == 0), "Number of teams must be a power of two."

        self.default_low = config['default_low']
        self.default_high = config['default_high']
        self.default_incr = config['default_incr']

        self.sponsors = []
        self.budgets = []
        self.teams = []

    def __ge__(self, other):
        """
        Compare two Tournament instances based on their champion's performance.
        
        :param other: Another Tournament instance.
        :return: True if self's champion has a higher total MPG-H, False otherwise.
        """
        if not isinstance(other, Tournament):
            raise TypeError("Comparison must be between Tournament instances.")

        #Ensure champions exist before comparison.
        if self.champion is None or other.champion is None:
            raise ValueError("Cannot compare tournaments without a champion.")
    
        #Calculate total MPG-H for each champion.
        self_score = self._team_total_mpg(self.champion)
        other_score = self._team_total_mpg(other.champion)

        print(f"Comparing {self.name} (Score: {self_score}) vs {other.name} (Score: {other_score})")

    
        return self_score >= other_score

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

    def hold_event(self):
        """
        Runs the tournament event through pairwise matches until one champion remains.
        Each winner receives a £50,000 prize after match victory and immediately buys one additional car.
        """
        active_teams = self.teams.copy()
    
        #Loop until one champion remains.
        while len(active_teams) > 1:
            next_round_teams = []
    
            #Pairwise matchups.
            for i in range(0, len(active_teams), 2):
                team_a = active_teams[i]
                team_b = active_teams[i+1]
    
                #Calculate total MPG-H clearly.
                mpg_a = self._team_total_mpg(team_a)
                mpg_b = self._team_total_mpg(team_b)
    
                #Decide match winner clearly.
                winner, loser = (team_a, team_b) if mpg_a >= mpg_b else (team_b, team_a)
    
                #Update performance clearly.
                winner.performance['wins'] += 1
                loser.performance['losses'] += 1
                winner.performance['scores'].append(max(mpg_a, mpg_b))
                loser.active = False #Eliminated clearly.
    
                #Award prize money clearly.
                winner.budget += 50000
    
                #Winner buys exactly one additional car (clearly enforced).
                self._purchase_single_car(winner)
    
                #Advance winner clearly.
                next_round_teams.append(winner)
    
            active_teams = next_round_teams
    
        #Clearly record the final champion.
        self.champion = active_teams[0]
    
    def _team_total_mpg(self, team):
        """
        Calculates total MPG-H for all cars in team's inventory.
        """
        if team is None or not team.inventory:
            return 0  #Avoids errors when champion has no cars.

        
        total_mpg = 0
        with open(self.car_data_path, 'r') as f:
            reader = csv.DictReader(f)
            car_mpg = {row['Model']: int(row['MPG-H']) for row in reader}
    
        for car in team.inventory:
            total_mpg += car_mpg.get(car, 0)
    
        return total_mpg
    
    def _purchase_single_car(self, team):
        """
        Purchases exactly one car after winning, clearly following the greedy method.
        """
        available_cars = []
        with open(self.car_data_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['Make'] == team.sponsor:
                    available_cars.append({
                        'Model': row['Model'],
                        'Cost': int(row['Cost']),
                        'MPG-H': int(row['MPG-H']),
                        'Ratio': int(row['MPG-H']) / int(row['Cost'])
                    })
    
        #Sort clearly by best efficiency.
        available_cars.sort(key=lambda x: x['Ratio'], reverse=True)
    
        #Attempt to buy exactly one car (clearly enforced).
        for car in available_cars:
            if car['Cost'] <= team.budget:
                print(f"Champion {team.sponsor} is buying {car['Model']} for {car['Cost']} (Remaining budget: {team.budget})")
                team.inventory.append(car['Model'])
                team.budget -= car['Cost']
                return  #**Fix: Ensure only ONE purchase is made.**

    def show_win_record(self):
        """
        Prints the win-loss record for each team in the tournament.
        """
        print("\nTournament Win-Loss Record:\n")
        
        #Record win/loss for each team.
        record = {team.sponsor: [] for team in self.teams}
        rounds = len(bin(self.nteams)) - 3  # Number of rounds (log2(nteams))
    
        for r in range(rounds):
            for team in self.teams:
                if team.performance['wins'] > r:
                    record[team.sponsor].append('W     ')
                elif team.performance['losses'] > r:
                    record[team.sponsor].append('L     ')
    
        #Print results with proper alignment.
        max_len = max(len(team.sponsor) for team in self.teams)
        for sponsor, results in record.items():
            print(f"{sponsor.rjust(max_len)}: {results}")

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

class Tournament_optimised(Tournament):
    """
    A subclass of Tournament that implements a dynamic programming (unbounded knapsack)
    approach to select the best combination of cars for a given budget.
    """

    def _purchase_inventory(self, team):
        """
        Uses dynamic programming (Unbounded Knapsack) to select the optimal set of cars 
        within the budget, maximizing total MPG-H.

        :param team: The Team object for which inventory is purchased.
        """
        available_cars = []
        with open(self.car_data_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['Make'] == team.sponsor:
                    available_cars.append({
                        'Model': row['Model'],
                        'Cost': int(row['Cost']),
                        'MPG-H': int(row['MPG-H'])
                    })

        n = len(available_cars)
        budget = team.budget

        # dp[i][b] = maximum MPG-H using the first i cars with budget b
        dp = [[0]*(budget+1) for _ in range(n+1)]
        # car_selection[i][b] = the actual list of cars that produce dp[i][b]
        car_selection = [[[] for _ in range(budget+1)] for _ in range(n+1)]

        for i in range(1, n+1):
            car = available_cars[i-1]
            cost = car['Cost']
            mpg = car['MPG-H']

            for b in range(budget+1):
                # 1) Skip this car
                skip_val = dp[i-1][b]
                skip_sel = car_selection[i-1][b]

                # 2) Use this car if cost <= b (unbounded => dp[i][b-cost], not dp[i-1][b-cost])
                if cost <= b:
                    take_val = dp[i][b-cost] + mpg
                    take_sel = car_selection[i][b-cost] + [car]
                else:
                    take_val = -1  # invalid

                # Compare skip vs take
                if skip_val >= take_val:
                    dp[i][b] = skip_val
                    car_selection[i][b] = skip_sel
                else:
                    dp[i][b] = take_val
                    car_selection[i][b] = take_sel

        # Reconstruct best selection from dp[n][budget]
        best_inventory = car_selection[n][budget]
        team.inventory = [c['Model'] for c in best_inventory]

        # Deduct total cost of all chosen cars
        total_cost = sum(c['Cost'] for c in best_inventory)
        team.budget = budget - total_cost

        print(f"DP selected: {team.inventory}, Remaining budget: {team.budget}")
