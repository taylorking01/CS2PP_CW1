#File: test_tournament_optimised.py
#Author: Taylor King
#Description: Tests the performance of greedy vs dp.

from tournament import *
import random

def test_optimised_vs_greedy():
    """
    Compare the performance of Tournament (greedy) and Tournament_optimised (DP) using the same fixed settings.
    """
    print("Running Tournament Optimisation Tests...")

    #Create fixed config (ensuring no randomness).
    config_path = './data/config.json'

    #Run standard tournament (greedy approach).
    t1 = Tournament(config_path)
    random.seed(123)
    t1.generate_sponsors()
    t1.generate_teams()
    t1.buy_cars()
    t1.hold_event()

    #Run optimised tournament (DP approach).
    t2 = Tournament_optimised(config_path)
    random.seed(123)
    t2.generate_sponsors()
    t2.generate_teams()
    t2.buy_cars()
    t2.hold_event()

    #Fetch results.
    mpg_greedy = t1._team_total_mpg(t1.champion)
    mpg_dp = t2._team_total_mpg(t2.champion)

    print(f"Champion of Greedy Tournament: {t1.champion} (MPG-H: {mpg_greedy})")
    print(f"Champion of DP Tournament: {t2.champion} (MPG-H: {mpg_dp})")

    #Check that DP approach is at least as good as greedy.
    assert mpg_dp >= mpg_greedy, "Dynamic programming should never perform worse than greedy."

    #Ensure both tournaments followed normal rules (e.g., champions must exist.
    assert t1.champion is not None and t2.champion is not None, "Both tournaments must have a champion."
    assert isinstance(t1.champion, t1.Team) and isinstance(t2.champion, t2.Team), "Champion must be a Team instance."

    print("Tournament Optimisation Tests Passed.")

#Run the test.
if __name__ == '__main__':
    test_optimised_vs_greedy()
