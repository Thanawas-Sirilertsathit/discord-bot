import random
class BombCardGame:
    def __init__(self, players):
        """Initialize the game."""
        self.players = players
        self.active_players = players[:]
        self.cards = []
        self.card_map = {}
        self.losers = []
        self.winner = None
        self.initialize_cards()

    def initialize_cards(self):
        """Prepare the deck with bombs and safe cards."""
        total_cards = len(self.players) * 3
        bomb_count = len(self.players) - 1
        safe_count = total_cards - bomb_count

        self.cards = ['BOMB'] * bomb_count + ['SAFE'] * safe_count
        random.shuffle(self.cards)
        self.card_map = {i + 1: self.cards[i] for i in range(len(self.cards))}

    def pick_card(self, player, card_number):
        """Allow a player to pick a specific card."""
        if card_number not in self.card_map:
            return None

        card = self.card_map.pop(card_number)
        if card == 'BOMB':
            self.active_players.remove(player)
            self.losers.append(player)
        return card

    def check_game_end(self):
        """Check if only one player is left."""
        if len(self.active_players) == 1:
            self.winner = self.active_players[0]
            return True
        return False

    def display_cards(self):
        """Show available card numbers."""
        return " ".join(str(num) for num in sorted(self.card_map.keys()))