#cluade output ver0.01
import numpy as np
from tabulate import tabulate

def format_currency(amount):
    """Format amount as currency with a + sign for positive values"""
    if amount > 0:
        return f"+${amount:.2f}"
    else:
        return f"${amount:.2f}"

def display_results(title, scenarios):
    """Display the results in a nicely formatted table"""
    print(f"\n{title}")
    print("=" * 80)
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

# Example 1: Hedging Across Multiple Horses
def hedge_multiple_horses():
    print("\n1. HEDGING ACROSS MULTIPLE HORSES")
    print("Strategy: Betting on multiple horses in the same race")
    
    # Setup
    horse3_odds = 4  # 4-1 odds
    horse7_odds = 8  # 8-1 odds
    bet_on_horse3 = 100
    bet_on_horse7 = 50
    total_investment = bet_on_horse3 + bet_on_horse7
    
    # Calculate outcomes
    scenarios = []
    
    # Scenario 1: Horse 3 wins
    horse3_winnings = bet_on_horse3 * horse3_odds
    horse3_profit = horse3_winnings - total_investment
    scenarios.append({
        "name": "Horse #3 wins (4-1 odds)",
        "original_bet": bet_on_horse3,
        "hedge_bet": bet_on_horse7,
        "profit": horse3_profit
    })
    
    # Scenario 2: Horse 7 wins
    horse7_winnings = bet_on_horse7 * horse7_odds
    horse7_profit = horse7_winnings - total_investment
    scenarios.append({
        "name": "Horse #7 wins (8-1 odds)",
        "original_bet": bet_on_horse3,
        "hedge_bet": bet_on_horse7,
        "profit": horse7_profit
    })
    
    # Scenario 3: Neither horse wins
    neither_profit = -total_investment
    scenarios.append({
        "name": "Neither horse wins",
        "original_bet": bet_on_horse3,
        "hedge_bet": bet_on_horse7,
        "profit": neither_profit
    })
    
    display_results("Multiple Horses Hedge Results", scenarios)

# Example 2: Lay Betting
def hedge_lay_betting():
    print("\n2. LAY BETTING")
    print("Strategy: Betting against your original selection on a betting exchange")
    
    # Setup
    original_odds = 5  # 5-1 morning odds
    new_odds = 2       # 2-1 current odds
    original_bet = 100
    lay_bet = 200      # Amount you stand to lose if the horse wins
    
    # Calculate outcomes
    scenarios = []
    
    # Scenario 1: Horse wins
    win_profit = (original_bet * original_odds) - original_bet - lay_bet
    scenarios.append({
        "name": "Horse wins",
        "original_bet": original_bet,
        "hedge_bet": lay_bet / new_odds,  # Actual amount staked on the exchange
        "profit": win_profit
    })
    
    # Scenario 2: Horse loses
    lose_profit = -original_bet + lay_bet
    scenarios.append({
        "name": "Horse loses",
        "original_bet": original_bet,
        "hedge_bet": lay_bet / new_odds,  # Actual amount staked on the exchange
        "profit": lose_profit
    })
    
    display_results("Lay Betting Hedge Results", scenarios)

# Example 3: Each-Way Betting
def hedge_each_way():
    print("\n3. EACH-WAY BETTING")
    print("Strategy: Placing one bet to win and another for the horse to place")
    
    # Setup - UK style with pounds
    odds = 10  # 10-1 odds
    stake = 10  # £10 each-way = £20 total (£10 win, £10 place)
    place_fraction = 1/4  # Quarter odds for place
    
    # Calculate outcomes
    scenarios = []
    
    # Scenario 1: Horse wins
    win_return = stake * odds + stake  # Win bet returns
    place_return = stake * (odds * place_fraction) + stake  # Place bet returns
    win_profit = win_return + place_return - (stake * 2)
    scenarios.append({
        "name": "Horse wins (1st place)",
        "original_bet": stake * 2,  # Total each-way stake
        "hedge_bet": 0,
        "profit": win_profit
    })
    
    # Scenario 2: Horse places
    place_profit = place_return - (stake * 2)
    scenarios.append({
        "name": "Horse places (2nd or 3rd)",
        "original_bet": stake * 2,  # Total each-way stake
        "hedge_bet": 0,
        "profit": place_profit
    })
    
    # Scenario 3: Horse doesn't place
    no_place_profit = -(stake * 2)
    scenarios.append({
        "name": "Horse doesn't place",
        "original_bet": stake * 2,  # Total each-way stake
        "hedge_bet": 0,
        "profit": no_place_profit
    })
    
    # Convert pounds to dollars for consistency (approximate conversion)
    for scenario in scenarios:
        scenario["original_bet"] *= 1.25
        scenario["profit"] *= 1.25
    
    display_results("Each-Way Betting Results", scenarios)

# Example 4: In-Running/Live Betting
def hedge_in_running():
    print("\n4. IN-RUNNING/LIVE BETTING")
    print("Strategy: Placing additional bets during the race")
    
    # Setup
    original_odds = 1  # Even money (1-1)
    new_leader_odds = 1  # Even money (1-1)
    original_bet = 100
    hedge_bet = 30
    
    # Calculate outcomes
    scenarios = []
    
    # Scenario 1: Original horse recovers and wins
    original_win_profit = (original_bet * original_odds) - original_bet - hedge_bet
    scenarios.append({
        "name": "Original horse recovers and wins",
        "original_bet": original_bet,
        "hedge_bet": hedge_bet,
        "profit": original_win_profit
    })
    
    # Scenario 2: New leader wins
    new_leader_profit = (hedge_bet * new_leader_odds) - hedge_bet - original_bet
    scenarios.append({
        "name": "New leader wins",
        "original_bet": original_bet,
        "hedge_bet": hedge_bet,
        "profit": new_leader_profit
    })
    
    display_results("In-Running Betting Hedge Results", scenarios)

# Example 5: Hedging Across Multiple Bets (Parlay/Accumulator)
def hedge_parlay():
    print("\n5. HEDGING ACROSS MULTIPLE BETS (PARLAY/ACCUMULATOR)")
    print("Strategy: Hedging the final leg of a multi-race bet")
    
    # Setup
    parlay_bet = 10
    potential_parlay_payout = 1000
    hedge_amount = 200  # Spread across other horses in the final race
    
    # Calculate outcomes
    scenarios = []
    
    # Scenario 1: Parlay horse wins final leg
    parlay_win_profit = potential_parlay_payout - parlay_bet - hedge_amount
    scenarios.append({
        "name": "Parlay horse wins final leg",
        "original_bet": parlay_bet,
        "hedge_bet": hedge_amount,
        "profit": parlay_win_profit
    })
    
    # Scenario 2: Parlay horse loses, but hedge bet wins
    # Assuming the hedge is spread across other horses to return approximately $300
    hedge_win_amount = 300
    hedge_win_profit = hedge_win_amount - hedge_amount - parlay_bet
    scenarios.append({
        "name": "Parlay horse loses, hedge wins",
        "original_bet": parlay_bet,
        "hedge_bet": hedge_amount,
        "profit": hedge_win_profit
    })
    
    display_results("Parlay/Accumulator Hedge Results", scenarios)

# Run all the examples
if __name__ == "__main__":
    print("\nHORSE RACING HEDGING STRATEGIES SIMULATOR")
    print("==========================================")
    
    hedge_multiple_horses()
    hedge_lay_betting()
    hedge_each_way()
    hedge_in_running()
    hedge_parlay()
    
    print("\nSummary:")
    print("Hedging is a risk management strategy that can protect against losses or secure profits")
    print("The optimal hedging strategy depends on your risk tolerance and specific betting situation")
    print("While hedging reduces potential maximum returns, it increases your chances of a positive outcome")