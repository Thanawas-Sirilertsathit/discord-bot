import discord
from discord.ext import commands
import random
from decouple import config
from datetime import timedelta, datetime
from helper_functions import *
from poker import PokerGame

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.dm_messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="*", intents=intents)
BOT_TOKEN = config('BOT_TOKEN')

# JSON file to store user data
DATA_FILE = "econ_data.json"


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

    if len(players) < 2:
        await ctx.send("You need at least two players!")
        return

    deck = create_deck()
    random.shuffle(deck)

    game = PokerGame(players)
    game.collect_initial_chips(10)
    await ctx.send(f"Each player has contributed 10 🪙 to the pot. The pot now contains {game.pot} 🪙.")

    removed_players = [player for player in players if game.players[player]['folded']]
    if removed_players:
        await ctx.send(
            f"The following players were removed from the game due to insufficient chips: "
            f"{', '.join(player.mention for player in removed_players)}"
        )
    game.deal_hands(deck)
    game.deal_table(deck)

    # Send private DMs with hands
    for player in players:
        try:
            hand = ' '.join(game.players[player]['hand'])
            await player.send(f"Your hand: {hand}")
        except discord.Forbidden:
            await ctx.send(f"Could not send a DM to {player.mention}. They need to enable DMs from server members.")

    # Betting and turn phases
    turn = 1
    for _ in range(4):
        if turn == 1:
            # No cards revealed in the first turn
            await ctx.send(f"Turn {turn}: No table cards revealed yet.")
        elif turn == 2:
            # Reveal 3 cards
            game.table_cards = [deck.pop() for _ in range(3)]
            await ctx.send(f"Turn {turn}: Table cards revealed: {' '.join(game.table_cards)}")
        elif turn == 3:
            # Reveal 1 card
            game.table_cards.append(deck.pop())
            await ctx.send(f"Turn {turn}: One more card revealed: {game.table_cards[-1]}")
            await ctx.send(f"Current table cards: {' '.join(game.table_cards)}")
        elif turn == 4:
            # Reveal the last card
            game.table_cards.append(deck.pop())
            await ctx.send(f"Turn {turn}: The final table card revealed: {game.table_cards[-1]}")
            await ctx.send(f"Current table cards: {' '.join(game.table_cards)}")

        # Betting phase
        for player in players:
            if game.players[player]['folded']:
                continue

            await ctx.send(f"{player.mention}, it's your turn! Current bet: {game.current_bet} 🪙. Your chips: {game.players[player]['chips']} 🪙. Type \\*bet <amount>, \\*fold, or \\*check.")

            def check(m):
                return m.author == player and (m.content.startswith("*bet") or m.content == "*fold" or m.content == "*check")

            while True:
                try:
                    msg = await bot.wait_for('message', check=check, timeout=60.0)

                    if msg.content.startswith("*bet"):
                        try:
                            amount = int(msg.content.split()[1])
                            if amount <= 0:
                                await ctx.send(f"{player.mention}, you must bet a positive amount!")
                            elif amount > game.players[player]['chips']:
                                await ctx.send(f"{player.mention}, you don't have enough chips to bet {amount}!")
                            else:
                                game.place_bet(player, amount)
                                await ctx.send(f"{player.mention} bets {amount} 🪙.")
                                break
                        except ValueError:
                            await ctx.send(f"{player.mention}, please enter a valid number for the bet amount!")
                    elif msg.content == "*fold":
                        game.fold(player)
                        await ctx.send(f"{player.mention} folds.")
                        break
                    elif msg.content == "*check":
                        await ctx.send(f"{player.mention} checks. No bet made.")
                        break
                except Exception:
                    await ctx.send(f"{player.mention} took too long and has been folded.")
                    game.fold(player)
                    break

        turn += 1

    # Determine winner
    winners, max_score, scores, winner_cards = game.determine_winner()
    game.distribute_pot(winners)

    hand_rankings = [
        "High Card", "One Pair", "Two Pairs", "Three of a Kind",
        "Straight", "Flush", "Full House", "Four of a Kind", "Straight Flush"
    ]

    if len(winners) == 1:
        winner = winners[0]
        winner_hand = ' '.join(winner_cards[winner])
        await ctx.send(f"The winner is {winner.mention} with {hand_rankings[max_score - 1]}!\nTheir cards: {winner_hand}")
    else:
        await ctx.send(f"It's a tie between: {', '.join(winner.mention for winner in winners)} with a {hand_rankings[max_score - 1]}!")

    # Display everyone's chip counts
    results = "\n".join([f"{player.mention}: {game.players[player]['chips']} 🪙" for player in players])
    await ctx.send(f"Final chip counts:\n{results}")


@bot.command()
async def daily(ctx):
    """Claim daily 1000 chips."""
    player_id = ctx.author.id
    data = load_player_data()
    
    if can_claim_daily_reward(player_id):
        current_chips = data[str(player_id)]['chips']
        new_chips = current_chips + 1000
        update_player_chips(player_id, new_chips)
        update_last_claim(player_id)
        await ctx.send(f"{ctx.author.mention}, you've claimed your daily reward of 1000 🪙! You now have {new_chips} 🪙.")
    else:
        next_claim_time = datetime.fromisoformat(data[str(player_id)]['last_claim']) + timedelta(days=1)
        await ctx.send(f"{ctx.author.mention}, you can claim your next daily reward at {next_claim_time.strftime('%Y-%m-%d %H:%M:%S')}.")


@bot.command()
async def balance(ctx, user: discord.Member = None):
    """Check your current chip balance."""
    if user is None:
        user = ctx.author

    data = load_player_data()
    if str(user.id) in data:
        current_chips = data[str(user.id)]['chips']
        await ctx.send(f"{user.mention}, your current balance is {current_chips} 🪙.")
    else:
        await ctx.send(f"{user.mention}, you don't have any 🪙 yet.")


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        pass
    else:
        raise error

if __name__ == '__main__':
    bot.run(BOT_TOKEN)
