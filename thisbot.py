import discord
from discord.ext import commands
import random
import json
from decouple import config
from collections import Counter

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.dm_messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="*", intents=intents)
BOT_TOKEN = config('BOT_TOKEN')

# JSON file to store user data
DATA_FILE = "econ_data.json"

def create_deck():
    """Create a card deck."""
    suits = ['♥️', '♦️', '♣️', '♠️']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    return [f"{rank} of {suit}" for suit in suits for rank in ranks]

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
        print("Success saved")

def get_or_create_chips(player_id, default=1000):
    """Initialize chips 1000."""
    data = load_player_data()
    if str(player_id) not in data:
        data[str(player_id)] = default
        save_player_data(data)
    return data[str(player_id)]

def update_player_chips(player_id, chips):
    """Update chips value for a player."""
    data = load_player_data()
    data[str(player_id)] = chips
    save_player_data(data)
    print("Success updated")


class PokerGame:
    """Pokergame class."""
    def __init__(self, players):
        """Initialize game."""
        self.players = {player: {'hand': [], 'chips': get_or_create_chips(player.id), 'bet': 0, 'folded': False} for player in players}
        self.pot = 0
        self.table_cards = []
        self.current_bet = 0
        self.active_players = players[:]

    def deal_hands(self, deck):
        """Give cards to each player."""
        for i, player in enumerate(self.players):
            self.players[player]['hand'] = [deck.pop() for _ in range(2)]

    def deal_table(self, deck):
        """Display cards on the table."""
        self.table_cards = [deck.pop() for _ in range(5)]

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
        winners = [player for player, (score, _) in scores.items() if score == max_score]
        winner_cards = {winner: self.players[winner]['hand'] + self.table_cards for winner in winners}
        return winners, max_score, scores, winner_cards


def evaluate_hand(hand, table_cards):
    """Calculate rank and score"""
    combined = hand + table_cards
    ranks = '2 3 4 5 6 7 8 9 10 J Q K A'.split()
    suits = ['♥️', '♦️', '♣️', '♠️']
    rank_values = {rank: i for i, rank in enumerate(ranks, start=2)}
    cards_by_rank = Counter(card.split(' ')[0] for card in combined)
    cards_by_suit = Counter(card.split(' ')[-1] for card in combined)
    rank_count = sorted(cards_by_rank.values(), reverse=True)
    sorted_ranks = sorted(cards_by_rank, key=lambda r: (rank_values[r], cards_by_rank[r]), reverse=True)
    def is_straight(ranks_list):
        indexes = sorted(rank_values[rank] for rank in ranks_list)
        return all(b == a + 1 for a, b in zip(indexes, indexes[1:]))
    def is_flush():
        return any(count >= 5 for count in cards_by_suit.values())
    is_flush_hand = is_flush()
    straight = is_straight(sorted_ranks)
    if is_flush_hand and straight:  # Straight flush
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


@bot.command()
async def poker(ctx, *players: discord.Member):
    """Poker game for fun (to invoke command please use *poker @player1 @...)"""
    if not players:
        await ctx.send("Please mention at least one player!")
        return

    if len(players) > 9:
        await ctx.send("You can only have up to 10 players!")
        return

    players = list(set(players))
    if ctx.author not in players:
        players.append(ctx.author)

    deck = create_deck()
    random.shuffle(deck)

    game = PokerGame(players)
    game.deal_hands(deck)
    game.deal_table(deck)

    # Send private DMs with hands
    for player in players:
        try:
            hand = ', '.join(game.players[player]['hand'])
            await player.send(f"Your hand: {hand}")
        except discord.Forbidden:
            await ctx.send(f"Could not send a DM to {player.mention}. They need to enable DMs from server members.")

    # Send table cards in the channel
    await ctx.send(f"Table cards: {', '.join(game.table_cards)}")

    # Betting phase
    for player in players:
        if game.players[player]['folded']:
            continue

        await ctx.send(f"{player.mention}, it's your turn! Current bet: {game.current_bet}. Your chips: {game.players[player]['chips']}. Type \\*bet <amount> or \\*fold.")

        def check(m):
            return m.author == player and (m.content.startswith("*bet") or m.content == "*fold")

        try:
            msg = await bot.wait_for('message', check=check, timeout=60.0)
            if msg.content.startswith("*bet"):
                amount = int(msg.content.split()[1])
                if game.place_bet(player, amount):
                    await ctx.send(f"{player.mention} bets {amount} chips.")
                else:
                    await ctx.send(f"{player.mention}, you don't have enough chips!")
            elif msg.content == "*fold":
                game.fold(player)
                await ctx.send(f"{player.mention} folds.")
        except:
            await ctx.send(f"{player.mention} took too long and has been folded.")
            game.fold(player)

    # Determine winner
    winners, max_score, scores, winner_cards = game.determine_winner()
    game.distribute_pot(winners)

    hand_rankings = [
        "High Card", "One Pair", "Two Pairs", "Three of a Kind",
        "Straight", "Flush", "Full House", "Four of a Kind", "Straight Flush"
    ]

    if len(winners) == 1:
        winner = winners[0]
        winner_hand = ', '.join(winner_cards[winner])
        await ctx.send(f"The winner is {winner.mention} with a {hand_rankings[max_score - 1]}!\nTheir cards: {winner_hand}")
    else:
        await ctx.send(f"It's a tie between: {', '.join(winner.mention for winner in winners)} with a {hand_rankings[max_score - 1]}!")

    # Display everyone's chip counts
    results = "\n".join([f"{player.mention}: {game.players[player]['chips']} chips" for player in players])
    await ctx.send(f"Final chip counts:\n{results}")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

bot.run(BOT_TOKEN)
