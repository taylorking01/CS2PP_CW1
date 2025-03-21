#File: test_execute_tournament.py
#Author: Taylor King
#Description: Tests the full execution of the Tournament class and its methods.

from tournament import Tournament

def test_full_tournament_execution():
    """
    Test the complete execution of the Tournament from initialisation to showing results.
    """
    print("Running full Tournament execution test...")

    #Setup Tournament.
    tournament = Tournament('./data/config.json')

    #Execute tournament steps.
    tournament.generate_sponsors()
    tournament.generate_teams()
    tournament.buy_cars()
    tournament.hold_event()

    #Assert a champion is produced.
    assert tournament.champion is not None, "Tournament should have a champion after execution."

    #Assert champion has valid attributes.
    champion = tournament.champion
    assert isinstance(champion.sponsor, str), "Champion sponsor should be a string."
    assert champion.budget >= 0, "Champion budget should be non-negative."
    assert len(champion.inventory) > 0, "Champion should have cars in inventory."

    #Print champion details clearly.
    print(f"The champion of '{tournament.name}' Tournament is the {champion}.")

    #Call and test the show_win_record method (visual/manual inspection needed).
    print("\nTournament Win Record:")
    tournament.show_win_record()

    print("Full Tournament execution test passed.")

if __name__ == '__main__':
    test_full_tournament_execution()
