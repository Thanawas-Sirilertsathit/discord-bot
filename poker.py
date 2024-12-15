from helper_functions import *
class PokerGame:
    """Pokergame class."""
    def __init__(self, players):
        """Initialize game."""
        self.players = {player: {'hand': [], 'chips': get_or_create_chips(player.id)["chips"], 'bet': 0, 'folded': False} for player in players}
        self.pot = 0
        self.table_cards = []
        self.current_bet = 0
        self.active_players = players[:]
        self.revealed_cards = 0

    def deal_hands(self, deck):
        """Give cards to each player."""
        for i, player in enumerate(self.players):
            self.players[player]['hand'] = [deck.pop() for _ in range(2)]

    def deal_table(self, deck):
        """Deal table cards in phases."""
        if self.revealed_cards < 3:  # First phase: Deal no cards
            self.table_cards = []
        elif self.revealed_cards < 4:  # Second phase: Reveal 3 cards
            self.table_cards = [deck.pop() for _ in range(3)]
        elif self.revealed_cards < 5:  # Third phase: Reveal 1 more card
            self.table_cards = self.table_cards + [deck.pop()]
        else:  # Final phase: Reveal all 5 cards
            self.table_cards = self.table_cards + [deck.pop()]

    def place_bet(self, player, amount):
        """Bet chips."""
        if amount > self.players[player]['chips']:
            return False
        self.players[player]['chips'] -= amount
        self.players[player]['bet'] += amount
        self.pot += amount
        self.current_bet = max(self.current_bet, self.players[player]['bet'])
        update_player_chips(player.id, self.players[player]['chips'])
        return True

    def fold(self, player):
        """Surrender."""
        self.players[player]['folded'] = True
        self.active_players.remove(player)

    def distribute_pot(self, winners):
        """Distribute prize."""
        if len(winners) > 0:
            winnings = self.pot // len(winners)
            for winner in winners:
                self.players[winner]['chips'] += winnings
                update_player_chips(winner.id, self.players[winner]['chips'])

    def determine_winner(self):
        """Select winners."""
        scores = {}
        for player, data in self.players.items():
            if not data['folded']:
                score, best_hand = evaluate_hand(data['hand'], self.table_cards)
                scores[player] = (score, best_hand)

        max_score = max(scores.values(), key=lambda x: x[0])[0]
        potential_winners = {player: high_cards for player, (score, high_cards) in scores.items() if score == max_score}

        # Tie-breaking by high cards
        ranks = '2 3 4 5 6 7 8 9 10 J Q K A'.split()
        suits = ['♥️', '♦️', '♣️', '♠️']
        rank_values = {rank: i for i, rank in enumerate(ranks, start=2)}
        if len(potential_winners) > 1:
            sorted_winners = sorted(
                potential_winners.items(),
                key=lambda item: [rank_values[rank] for rank in item[1]],
                reverse=True
            )
            max_high_cards = sorted_winners[0][1]
            winners = [player for player, high_cards in sorted_winners if high_cards == max_high_cards]
        else:
            winners = list(potential_winners.keys())

        winner_cards = {winner: self.players[winner]['hand'] + self.table_cards for winner in winners}
        return winners, max_score, scores, winner_cards

    def collect_initial_chips(self, amount=10):
        """Collect initial chips from all players to the pot."""
        for player in self.players:
            if self.players[player]['chips'] >= amount:
                self.players[player]['chips'] -= amount
                self.players[player]['bet'] += amount
                self.pot += amount
                update_player_chips(player.id, self.players[player]['chips'])
                self.current_bet =  amount
            else:
                # Automatically Fold
                self.players[player]['folded'] = True
                self.active_players.remove(player)