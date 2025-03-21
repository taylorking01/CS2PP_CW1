#File: test_tournament_comparison.py
#Author: Taylor King
#Description: Tests the comparison of two Tournament instances based on their champions' performance.

from tournament import Tournament

def test_tournament_comparison():
    """
    Test the comparison of two Tournament instances by running them and using the >= operator.
    """
    print("Running Tournament comparison test...")

    #Execute first tournament (t1).
    t1 = Tournament('./data/config.json')
    t1.generate_sponsors()
    t1.generate_teams()
    t1.buy_cars()
    t1.hold_event()

    #Execute second tournament (t2) with a different config.
    t2 = Tournament('./data/config2.json')
    t2.generate_sponsors()
    t2.generate_teams()
    t2.buy_cars()
    t2.hold_event()

    #Compare champions using >= operator.
    higher = t1 if t1 >= t2 else t2

    #Assert the comparison works.
    assert higher is not None, "Comparison should return a valid Tournament instance."
    assert isinstance(higher, Tournament), "Comparison should return a Tournament instance."
    
    #Print result.
    print(f"The champion of the {higher.name} Tournament scored higher.")

    print("Tournament comparison test passed.")

if __name__ == '__main__':
    test_tournament_comparison()
