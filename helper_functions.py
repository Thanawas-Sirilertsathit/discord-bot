import json
from datetime import datetime, timedelta
from collections import Counter
from itertools import combinations
DATA_FILE = "econ_data.json"

def create_deck():
    """Create a card deck."""
    suits = ['♥️', '♦️', '♣️', '♠️']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    return [f"[ {rank} {suit} ]" for suit in suits for rank in ranks]

def load_player_data():
    """Read player data."""
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_player_data(data):
    """Write json file."""
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

def get_or_create_chips(player_id, default=1000):
    """Initialize chips 1000."""
    data = load_player_data()
    if str(player_id) not in data:
        data[str(player_id)] = {'chips': default, 'last_claim': None}
        save_player_data(data)
    return data[str(player_id)]

def update_last_claim(player_id):
    """Update the last claim time to the current time."""
    data = load_player_data()
    data[str(player_id)]['last_claim'] = datetime.now().isoformat()
    save_player_data(data)

def update_player_chips(player_id, chips):
    """Update chips value for a player."""
    data = load_player_data()
    data[str(player_id)]["chips"] = chips
    save_player_data(data)

def can_claim_daily_reward(player_id):
    """Check if the player can claim the daily reward."""
    data = load_player_data()
    last_claim = data.get(str(player_id), {}).get('last_claim')
    
    if not last_claim:
        return True
    
    last_claim_time = datetime.fromisoformat(last_claim)
    now = datetime.now()
    if now - last_claim_time >= timedelta(days=1):
        return True
    return False

def evaluate_hand(hand, table_cards):
    """Calculate rank and score"""
    combined = hand + table_cards
    ranks = '2 3 4 5 6 7 8 9 10 J Q K A'.split()
    suits = ['♥️', '♦️', '♣️', '♠️']
    rank_values = {rank: i for i, rank in enumerate(ranks, start=2)}
    cards_by_rank = Counter(card.split()[1] for card in combined)
    cards_by_suit = Counter(card.split()[2].strip() for card in combined)
    rank_count = sorted(cards_by_rank.values(), reverse=True)
    sorted_ranks = sorted(cards_by_rank, key=lambda r: (rank_values[r], cards_by_rank[r]), reverse=True)
    def is_straight(ranks_list):
        indexes = sorted(set(rank_values[rank] for rank in ranks_list))
        for i in range(len(indexes) - 4):
            if indexes[i + 4] - indexes[i] == 4:
                return True
        # Check for low-Ace straight (5 4 3 2 A)
        if {2, 3, 4, 5, 14}.issubset(set(rank_values[rank] for rank in ranks_list)):
            return True
        return False

    def is_flush():
        return any(count >= 5 for count in cards_by_suit.values())
    
    def is_straight_flush(hand):
        """Check if the hand is a straight flush (straight + all same suit)"""
        possible_hands = combinations(range(len(hand)), 5)
        rank_values_dict = {rank: i for i, rank in enumerate(rank_values, start=2)}
        # Check each combination for a straight flush
        for indices in possible_hands:
            # Extract the selected cards and their ranks and suits
            selected_cards = [hand[i] for i in indices]
            selected_ranks = [selected_cards[i].split()[1] for i in range(5)]
            selected_suits = [selected_cards[i].split()[2].strip() for i in range(5)]

            selected_rank_values = [rank_values_dict[rank] for rank in selected_ranks]
            selected_rank_values.sort()

            if len(set(selected_rank_values)) == 5:
                if all(selected_rank_values[i + 1] - selected_rank_values[i] == 1 for i in range(4)):
                    if len(set(selected_suits)) == 1:
                        return True
                if {2, 3, 4, 5, 14}.issubset(set(selected_rank_values)):
                    if len(set(selected_suits)) == 1:
                        return True

        return False

    is_flush_hand = is_flush()
    straight = is_straight(sorted_ranks)
    is_straight_flush_hand = is_straight_flush(combined)
    if is_straight_flush_hand:  # Straight flush
        return 9, sorted_ranks[:5]
    if rank_count[0] == 4:  # Four of a kind
        return 8, [sorted_ranks[0], sorted_ranks[1]]
    if rank_count[0] == 3 and rank_count[1] >= 2:  # Full house
        return 7, [sorted_ranks[0], sorted_ranks[1]]
    if is_flush_hand:  # Flush
        return 6, sorted_ranks[:5]
    if straight:  # Straight
        return 5, sorted_ranks[:5]
    if rank_count[0] == 3:  # Three of a kind
        return 4, [sorted_ranks[0], sorted_ranks[1], sorted_ranks[2]]
    if rank_count[0] == 2 and rank_count[1] == 2:  # Two pairs
        return 3, [sorted_ranks[0], sorted_ranks[1], sorted_ranks[2]]
    if rank_count[0] == 2:  # One pair
        return 2, [sorted_ranks[0], sorted_ranks[1], sorted_ranks[2], sorted_ranks[3]]
    # High card
    return 1, sorted_ranks[:5]