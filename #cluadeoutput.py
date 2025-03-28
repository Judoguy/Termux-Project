#cluadeoutput

import numpy as np
from tabulate import tabulate
from itertools import permutations

def format_currency(amount):
    """Format amount as currency with a + sign for positive values"""
    if amount > 0:
        return f"+${amount:.2f}"
    else:
        return f"${amount:.2f}"

def display_results(title, scenarios):
    """Display the results in a nicely formatted table"""
    print(f"\n{title}")
    print("=" * 90)
    headers = ["Scenario", "Original Bet", "Hedge Bet", "Net Profit", "ROI %"]
    table_data = []
    
    for scenario in scenarios:
        original_bet = scenario.get("original_bet", 0)
        hedge_bet = scenario.get("hedge_bet", 0)
        profit = scenario.get("profit", 0)
        total_investment = original_bet + hedge_bet
        roi = (profit / total_investment) * 100 if total_investment > 0 else 0
        
        table_data.append([
            scenario["name"],
            f"${original_bet:.2f}",
            f"${hedge_bet:.2f}",
            format_currency(profit),
            f"{roi:.1f}%"
        ])
    
    print(tabulate(table_data, headers=headers, tablefmt="grid"))
    print("\n")

def hedge_exacta():
    """
    Example 1: Hedging an Exacta bet
    - Original bet: $20 exacta on horses 3-5 (horse 3 to win, horse 5 to place)
    - Hedge: $5 exacta box on horses 3, 5, 7 (covers all permutations)
    """
    print("\n1. HEDGING AN EXACTA BET")
    print("Strategy: Using an exacta box to hedge a straight exacta bet")
    
    # Setup
    straight_exacta_horses = (3, 5)  # Horse 3 to win, horse 5 to place
    straight_exacta_bet = 20
    straight_exacta_odds = 25  # 25-1 payout
    
    box_horses = [3, 5, 7]  # Boxing these three horses
    box_permutations = list(permutations(box_horses, 2))
    box_cost_per_combo = 5
    box_total_cost = box_cost_per_combo * len(box_permutations)
    box_odds = 18  # Lower odds because it's a more likely outcome
    
    # Calculate outcomes
    scenarios = []
    
    # Scenario 1: Original exacta (3-5) hits
    # You win the straight exacta and one permutation of the box
    original_win = straight_exacta_bet * straight_exacta_odds
    box_win = box_cost_per_combo * box_odds  # Win on the 3-5 box permutation
    total_cost = straight_exacta_bet + box_total_cost
    profit = original_win + box_win - total_cost
    scenarios.append({
        "name": f"Horses finish {straight_exacta_horses[0]}-{straight_exacta_horses[1]} (original exacta hits)",
        "original_bet": straight_exacta_bet,
        "hedge_bet": box_total_cost,
        "profit": profit
    })
    
    # Scenario 2: A different permutation in the box hits (e.g., 5-3, 3-7, 7-3, 5-7, or 7-5)
    # Assume 5-3 hits as an example
    box_only_win = box_cost_per_combo * box_odds
    profit = box_only_win - (straight_exacta_bet + box_total_cost)
    scenarios.append({
        "name": "Horses finish in a different order covered by the box (e.g., 5-3)",
        "original_bet": straight_exacta_bet,
        "hedge_bet": box_total_cost,
        "profit": profit
    })
    
    # Scenario 3: Neither the straight exacta nor any box permutation hits
    profit = -(straight_exacta_bet + box_total_cost)
    scenarios.append({
        "name": "No covered combination hits",
        "original_bet": straight_exacta_bet,
        "hedge_bet": box_total_cost,
        "profit": profit
    })
    
    display_results("Exacta Hedging Results", scenarios)

def hedge_trifecta():
    """
    Example 2: Hedging a Trifecta bet
    - Original bet: $10 trifecta 2-5-8 (exact order)
    - Hedge: $1 trifecta part-wheel with 2, 5, 8 with additional horses
    """
    print("\n2. HEDGING A TRIFECTA BET")
    print("Strategy: Using a part-wheel to hedge a straight trifecta bet")
    
    # Setup
    straight_trifecta = [2, 5, 8]  # Horses 2-5-8 in exact order
    straight_trifecta_bet = 10
    straight_trifecta_odds = 180  # 180-1 payout
    
    # Part wheel: 2 with 5,8,9 with 5,8,9,10 (covering more combinations)
    # This means horse 2 must win, one of 5,8,9 must place, and one of 5,8,9,10 must show
    wheel_key_horse = 2
    wheel_place_horses = [5, 8, 9]
    wheel_show_horses = [5, 8, 9, 10]
    
    # Count valid combinations (we must exclude duplicates like 2-5-5)
    valid_combos = 0
    for place in wheel_place_horses:
        for show in wheel_show_horses:
            if place != show:
                valid_combos += 1
    
    wheel_cost_per_combo = 1
    wheel_total_cost = wheel_cost_per_combo * valid_combos
    wheel_base_odds = 60  # Lower odds for the wheel combinations
    
    # Calculate outcomes
    scenarios = []
    
    # Scenario 1: Original trifecta (2-5-8) hits
    # You win the straight trifecta and one part of the wheel
    original_win = straight_trifecta_bet * straight_trifecta_odds
    wheel_win = wheel_cost_per_combo * wheel_base_odds
    total_cost = straight_trifecta_bet + wheel_total_cost
    profit = original_win + wheel_win - total_cost
    scenarios.append({
        "name": "Horses finish 2-5-8 (original trifecta hits)",
        "original_bet": straight_trifecta_bet,
        "hedge_bet": wheel_total_cost,
        "profit": profit
    })
    
    # Scenario 2: A different part of the wheel hits (e.g., 2-5-9, 2-9-8, etc.)
    wheel_only_win = wheel_cost_per_combo * wheel_base_odds
    profit = wheel_only_win - (straight_trifecta_bet + wheel_total_cost)
    scenarios.append({
        "name": "Different wheel combination hits (e.g., 2-5-9)",
        "original_bet": straight_trifecta_bet,
        "hedge_bet": wheel_total_cost,
        "profit": profit
    })
    
    # Scenario 3: Neither the straight trifecta nor any part of the wheel hits
    profit = -(straight_trifecta_bet + wheel_total_cost)
    scenarios.append({
        "name": "No covered combination hits",
        "original_bet": straight_trifecta_bet,
        "hedge_bet": wheel_total_cost,
        "profit": profit
    })
    
    display_results("Trifecta Hedging Results", scenarios)

def hedge_pick_six():
    """
    Example 3: Hedging a Pick 6 bet
    - Original bet: $48 Pick 6 ticket with multiple selections in some races
    - Hedge: Additional bets on the last leg to secure a profit
    """
    print("\n3. HEDGING A PICK 6 BET")
    print("Strategy: Hedging the final leg of a Pick 6 when first 5 legs have hit")
    
    # Setup
    pick6_investment = 48  # Total cost of original Pick 6 ticket
    potential_payout = 10000  # Estimated payout if Pick 6 hits
    
    # Assume we're alive to the final leg with horse #3
    final_leg_horse = 3
    win_bet_options = [
        {"horse": 1, "bet": 300, "odds": 4},  # $300 on horse #1 at 4-1
        {"horse": 5, "bet": 200, "odds": 7},  # $200 on horse #5 at 7-1
        {"horse": 8, "bet": 100, "odds": 15}  # $100 on horse #8 at 15-1
    ]
    total_hedge_bet = sum(option["bet"] for option in win_bet_options)
    
    # Calculate outcomes
    scenarios = []
    
    # Scenario 1: Original Pick 6 horse (#3) wins
    pick6_profit = potential_payout - pick6_investment - total_hedge_bet
    scenarios.append({
        "name": f"Horse #{final_leg_horse} wins (original Pick 6 hits)",
        "original_bet": pick6_investment,
        "hedge_bet": total_hedge_bet,
        "profit": pick6_profit
    })
    
    # Scenarios for each hedged horse winning
    for option in win_bet_options:
        horse = option["horse"]
        bet = option["bet"]
        win_amount = bet * option["odds"]
        profit = win_amount - pick6_investment - total_hedge_bet
        scenarios.append({
            "name": f"Horse #{horse} wins at {option['odds']}-1 odds",
            "original_bet": pick6_investment,
            "hedge_bet": total_hedge_bet,
            "profit": profit
        })
    
    # Scenario: A different horse wins (not covered by any bet)
    profit = -(pick6_investment + total_hedge_bet)
    scenarios.append({
        "name": "A different horse wins (not covered by any bet)",
        "original_bet": pick6_investment,
        "hedge_bet": total_hedge_bet,
        "profit": profit
    })
    
    display_results("Pick 6 Hedging Results", scenarios)

def hedge_superfecta():
    """
    Example 4: Hedging a Superfecta bet with a box strategy
    """
    print("\n4. HEDGING A SUPERFECTA BET")
    print("Strategy: Hedging a straight superfecta with a smaller superfecta box")
    
    # Setup
    straight_superfecta = [4, 7, 2, 9]  # Horses in exact order: 4-7-2-9
    straight_bet = 5
    straight_odds = 1200  # 1200-1 payout
    
    # Box the top 3 finishers with 2 additional horses for 4th position
    box_horses = [4, 7, 2, 9, 11]  # Adding horse #11 as an additional possibility
    
    # A partial box: 4-7-2 with 9,11 for 4th position (2 combinations)
    # Simplifying for demonstration purposes
    box_combinations = 2
    box_cost_per_combo = 2
    box_total_cost = box_combinations * box_cost_per_combo
    box_odds = 600  # Lower odds for the box combinations
    
    # Calculate outcomes
    scenarios = []
    
    # Scenario 1: Original superfecta (4-7-2-9) hits
    original_win = straight_bet * straight_odds
    box_win = box_cost_per_combo * box_odds  # Also win on the box
    total_cost = straight_bet + box_total_cost
    profit = original_win + box_win - total_cost
    scenarios.append({
        "name": "Horses finish 4-7-2-9 (original superfecta hits)",
        "original_bet": straight_bet,
        "hedge_bet": box_total_cost,
        "profit": profit
    })
    
    # Scenario 2: A different box combination hits (e.g., 4-7-2-11)
    box_only_win = box_cost_per_combo * box_odds
    profit = box_only_win - (straight_bet + box_total_cost)
    scenarios.append({
        "name": "Different box combination hits (e.g., 4-7-2-11)",
        "original_bet": straight_bet,
        "hedge_bet": box_total_cost,
        "profit": profit
    })
    
    # Scenario 3: Neither the straight superfecta nor any box combination hits
    profit = -(straight_bet + box_total_cost)
    scenarios.append({
        "name": "No covered combination hits",
        "original_bet": straight_bet,
        "hedge_bet": box_total_cost,
        "profit": profit
    })
    
    display_results("Superfecta Hedging Results", scenarios)

def dutch_betting():
    """
    Example 5: Dutch Betting (a form of arbitrage across multiple horses)
    """
    print("\n5. DUTCH BETTING")
    print("Strategy: Betting on multiple horses in proportions that guarantee the same return")
    
    # Setup
    horses = [
        {"number": 1, "odds": 3, "probability": 0.25},  # 3-1 odds
        {"number": 4, "odds": 5, "probability": 0.15},  # 5-1 odds
        {"number": 6, "odds": 9, "probability": 0.10},  # 9-1 odds
    ]
    
    # Target return (we want to win $100 profit regardless of which horse wins)
    target_profit = 100
    
    # Calculate optimal stakes for each horse to achieve equal profit
    total_probability = sum(horse["probability"] for horse in horses)
    total_stake = 0
    
    for horse in horses:
        # Calculate stake needed for this horse
        stake = target_profit / horse["odds"]
        horse["stake"] = stake
        total_stake += stake
    
    # Calculate outcomes
    scenarios = []
    
    # Scenario for each horse winning
    for horse in horses:
        winnings = horse["stake"] * horse["odds"]
        profit = winnings - total_stake
        scenarios.append({
            "name": f"Horse #{horse['number']} wins at {horse['odds']}-1 odds",
            "original_bet": 0,  # No original bet, this is a different strategy
            "hedge_bet": total_stake,
            "profit": profit
        })
    
    # Scenario: A different horse wins (not covered by any bet)
    profit = -total_stake
    scenarios.append({
        "name": "A different horse wins (not covered)",
        "original_bet": 0,
        "hedge_bet": total_stake,
        "profit": profit
    })
    
    display_results("Dutch Betting Results", scenarios)

# Run all examples
if __name__ == "__main__":
    print("\nEXOTIC HORSE RACING BET HEDGING STRATEGIES")
    print("=========================================")
    
    hedge_exacta()
    hedge_trifecta()
    hedge_pick_six()
    hedge_superfecta()
    dutch_betting()
    
    print("\nSummary of Exotic Bet Hedging:")
    print("1. Exacta hedging: Use box bets to cover multiple finish orders")
    print("2. Trifecta hedging: Use part-wheels to protect key horses")
    print("3. Pick 6 hedging: Secure profit when alive to final leg")
    print("4. Superfecta hedging: Cover additional combinations for 4th position")
    print("5. Dutch betting: Distribute stakes to achieve equal return regardless of outcome")
    print("\nExotic bet hedging requires careful stake calculation and understanding of bet structures")
    print("The optimal strategy balances coverage against cost while managing potential returns")