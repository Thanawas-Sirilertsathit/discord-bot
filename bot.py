import asyncio
import discord
from discord.ext import commands
import random
from decouple import config
from datetime import timedelta, datetime
from helper_functions import *
from poker import PokerGame
from bombgame import BombCardGame
from discord.ext.commands import BucketType
from crop import *
from fountain import *
from crafting import *
from towerdodge import *
from gomoku import *
from pve import *
from duel.character_list import CharacterList

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.dm_messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="*", intents=intents)
BOT_TOKEN = config('BOT_TOKEN')

# JSON file to store user data
DATA_FILE = "econ_data.json"

@bot.group(invoke_without_command=True)
async def game(ctx):
    """Prefix for game commands."""
    await ctx.send("Available games : Bomb game, 11-9 game, Poker and Slot.")

@bot.group(invoke_without_command=True)
async def econ(ctx):
    """Prefix for economic related commands."""
    await ctx.send("Available commands : daily, farm, harvest, view_farm and balance.")

@game.command()
@commands.cooldown(1, 120, BucketType.user)
async def poker(ctx, *players: discord.Member):
    """Poker game for fun (*poker @player1 @player2 @...)."""
    if not players:
        await ctx.send("Please mention at least one player!")
        return

    if len(players) > 9:
        await ctx.send("You can only have up to 10 players!")
        return

    players = list(set(players))
    players = [player for player in players if not player.bot]
    if ctx.author not in players:
        players.append(ctx.author)

    if len(players) < 2:
        await ctx.send("You need at least two players!")
        return

    await ctx.send(f"{', '.join(player.mention for player in players)} are you ready to start the poker game? Reply with 'yes' to accept or 'no' to cancel.")
    
    responses = {player: None for player in players}

    def check(msg):
        return msg.author in players and msg.content.lower() in ["yes", "no"]

    try:
        # Wait until all players respond (or timeout after 60 seconds)
        while None in responses.values():
            msg = await bot.wait_for("message", check=check, timeout=60.0)
            responses[msg.author] = msg.content.lower()
            await ctx.send(f"{msg.author.mention} has responded with '{msg.content.lower()}'.")

    except:
        await ctx.send("Game start timed out. Not all players confirmed in time.")
        return

    # If any player responds with 'no', cancel the game
    if any(response == "no" for response in responses.values()):
        await ctx.send("Game has been canceled because some players did not confirm.")
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
        if len(game.active_players) <= 1:
            break
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

@poker.error
async def poker_error(ctx, error):
    """Handle poker cooldown error"""
    if isinstance(error, commands.CommandOnCooldown):
        retry_after = error.retry_after
        minutes, seconds = divmod(retry_after, 60)
        cooldown_message = (
            f"⏳ {ctx.author.mention}, the poker table is being cleaned up! "
            f"Please wait {int(minutes)} minutes and {int(seconds)} seconds before trying again."
        )
        await ctx.send(cooldown_message)
        return

@econ.command()
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


@econ.command()
async def balance(ctx, user: discord.Member = None):
    """Check your current chip balance or create account."""
    if user is None:
        user = ctx.author

    data = load_player_data()
    player_data = get_or_create_chips(user.id)
    current_chips = player_data['chips']
    await ctx.send(f"{user.mention}, your current balance is {current_chips} 🪙.")


@game.command()
@commands.cooldown(1, 120, BucketType.user)
async def bombgame(ctx, *players: discord.Member):
    """Start a bomb card game (*bombgame @player1 @player2 ...)."""
    if not players:
        await ctx.send("Please mention at least one player!")
        return

    players = list(set(players))
    players = [player for player in players if not player.bot]
    if ctx.author not in players:
        players.append(ctx.author)

    if len(players) < 2:
        await ctx.send("You need at least two players!")
        return
    await ctx.send(f"{', '.join(player.mention for player in players)} are you ready to start the bomb game? Reply with 'yes' to accept or 'no' to cancel.")
    
    responses = {player: None for player in players}

    def check(msg):
        return msg.author in players and msg.content.lower() in ["yes", "no"]

    try:
        # Wait until all players respond (or timeout after 60 seconds)
        while None in responses.values():
            msg = await bot.wait_for("message", check=check, timeout=60.0)
            responses[msg.author] = msg.content.lower()
            await ctx.send(f"{msg.author.mention} has responded with '{msg.content.lower()}'.")

    except:
        await ctx.send("Game start timed out. Not all players confirmed in time.")
        return

    # If any player responds with 'no', cancel the game
    if any(response == "no" for response in responses.values()):
        await ctx.send("Game has been canceled because some players did not confirm.")
        return

    game = BombCardGame(players)
    await ctx.send(
        f"Starting the Bomb Card Game with {len(players)} players! Each player will take turns picking numbered cards."
    )

    turn = 0
    while not game.check_game_end():
        current_player = game.active_players[turn % len(game.active_players)]

        def check(m):
            return m.author == current_player

        valid_choice = False
        while not valid_choice:
            try:
                await ctx.send(
                    f"{current_player.mention}, it's your turn! Available cards: {game.display_cards()}.\n"
                    "Type the number of the card you want to pick."
                )
                msg = await bot.wait_for("message", check=check, timeout=60.0)

                if not msg.content.isdigit():
                    await ctx.send(f"{current_player.mention}, please enter a valid number!")
                    continue

                chosen_card = int(msg.content)

                if chosen_card not in game.card_map:
                    await ctx.send(
                        f"{current_player.mention}, that card is either invalid or has already been picked! Please choose again."
                    )
                    continue

                valid_choice = True

            except Exception:
                await ctx.send(
                    f"{current_player.mention} took too long to pick a card and is eliminated!"
                )
                game.active_players.remove(current_player)
                game.losers.append(current_player)
                break

        if not valid_choice:
            continue  # Skip to next player if they failed to choose

        # Process the chosen card
        card = game.pick_card(current_player, chosen_card)
        if card == 'BOMB':
            await ctx.send(
                f"{current_player.mention} picked card {chosen_card} and got a 💣 BOMB! {current_player.mention} is eliminated!"
            )
        else:
            await ctx.send(
                f"{current_player.mention} picked card {chosen_card} and got a ✅ SAFE card!"
            )

        if game.check_game_end():
            break

        turn += 1

    winner = game.winner
    if winner:
        current_chips = get_or_create_chips(winner.id)['chips']
        update_player_chips(winner.id, current_chips + 100)
        await ctx.send(
            f"🎉 {winner.mention} is the winner and earns 100 chips! Congratulations!"
        )
    else:
        await ctx.send("No winner this time!")

    # Display everyone's final chip counts
    results = "\n".join(
        [f"{player.mention}: {get_or_create_chips(player.id)['chips']} 🪙" for player in players]
    )
    await ctx.send(f"Final chip counts:\n{results}")

@bombgame.error
async def bombgame_error(ctx, error):
    """Handle bombgame cooldown error"""
    if isinstance(error, commands.CommandOnCooldown):
        retry_after = error.retry_after
        minutes, seconds = divmod(retry_after, 60)
        cooldown_message = (
            f"⏳ {ctx.author.mention}, the bombgame is being prepared! "
            f"Please wait {int(minutes)} minutes and {int(seconds)} seconds before trying again."
        )
        await ctx.send(cooldown_message)
        return

@game.command()
@commands.cooldown(1, 10, BucketType.user)
async def slot(ctx):
    """Play a slot machine game for 10 chips."""
    player_id = ctx.author.id
    data = load_player_data()

    # Ensure the player has enough chips
    if str(player_id) not in data or data[str(player_id)]['chips'] < 10:
        await ctx.send(f"{ctx.author.mention}, you need at least 10 🪙 to play the slot machine!")
        return

    # Deduct the entry fee
    update_player_chips(player_id, data[str(player_id)]['chips'] - 10)

    # Weighted slot symbols with probabilities
    symbols = ["🍒", "🍋", "🍉", "⭐", "🔔", "🎹", "7️⃣"]
    weights = [30, 25, 20, 15, 5, 4, 1]

    # Function to select a symbol based on weights
    def weighted_choice(symbols, weights):
        return random.choices(symbols, weights, k=1)[0]

    # Generate the slot machine grid ensuring no vertical matches
    grid = []
    for _ in range(3):  # 3 rows
        row = []
        for col in range(3):  # 3 columns
            symbol = weighted_choice(symbols, weights)
            # Ensure that no vertical match occurs
            while any(symbol == grid[r][col] for r in range(len(grid))):
                symbol = weighted_choice(symbols, weights)
            row.append(symbol)
        grid.append(row)

    # Format the grid for display
    grid_display = "\n".join([" | ".join(row) for row in grid])

    # Define rewards for each symbol
    symbol_rewards = {
        "🍒": 50,
        "🍋": 100,
        "🍉": 200,
        "⭐": 500,
        "🔔": 1000,
        "🎹": 3000,
        "7️⃣": 7777
    }

    # Check for winning combinations
    prize = 0

    # Horizontal lines
    for row in grid:
        if row[0] == row[1] == row[2]:
            prize += symbol_rewards[row[0]]

    # Diagonal lines
    if grid[0][0] == grid[1][1] == grid[2][2]:
        prize += symbol_rewards[grid[0][0]]
    if grid[0][2] == grid[1][1] == grid[2][0]:
        prize += symbol_rewards[grid[0][2]]

    # Respond with the slot result
    await ctx.send(f"{ctx.author.mention} rolled the slot machine using 10 🪙!\n```{grid_display}```")

    if prize > 0:
        current_chips = data[str(player_id)]['chips']
        update_player_chips(player_id, current_chips + prize)
        await ctx.send(f"🎉 {ctx.author.mention}, you won {prize} 🪙! Your new balance is {current_chips + prize} 🪙.")
    else:
        await ctx.send(f"{ctx.author.mention}, better luck next time! You didn't win any chips this time.")

@slot.error
async def slot_error(ctx, error):
    """Handle slot cooldown error"""
    if isinstance(error, commands.CommandOnCooldown):
        retry_after = error.retry_after
        minutes, seconds = divmod(retry_after, 60)
        cooldown_message = (
            f"⏳ {ctx.author.mention}, the slot machine is cooling down! "
            f"Please wait {int(seconds)} seconds before trying again."
        )
        await ctx.send(cooldown_message)
        return

@econ.command()
async def farm(ctx, crop: str, amount: str = "1"):
    """Plant a crop in one of your fields (*farm <crop> [amount])."""
    player_id = ctx.author.id
    data = load_player_data()

    # Check if user exists in data
    if str(player_id) not in data:
        data[str(player_id)] = {
            'chips': 1000,
            'fields': [None] * 5
        }
    else:
        user_data = data[str(player_id)]
        if 'fields' not in user_data:
            user_data['fields'] = [None] * 5

    user_data = data[str(player_id)]
    empty_fields = [i for i, field in enumerate(user_data['fields']) if field is None]
    # Validate amount (either "all" or an integer)
    if amount.lower() == "all":
        seed_cost = 10
        amount = len(empty_fields)
    else:
        try:
            amount = int(amount)
            if amount <= 0:
                await ctx.send(f"{ctx.author.mention}, please provide a valid amount (or 'all').")
                return
        except ValueError:
            await ctx.send(f"{ctx.author.mention}, please provide a valid amount (or 'all').")
            return

    # Check if the user has enough chips to buy the seeds
    seed_cost = 10
    total_cost = seed_cost * amount
    if user_data['chips'] < total_cost:
        await ctx.send(f"{ctx.author.mention}, you need at least {total_cost} 🪙 to plant {amount} {crop}(s)!")
        return

    # Validate crop
    if crop.lower() not in CROP_GROWTH:
        available_crops = ', '.join([f"{CROP_EMOJI[key]} ({key})" for key in CROP_GROWTH.keys()])
        await ctx.send(f"{ctx.author.mention}, invalid crop! Available crops: {available_crops}.")
        return

    if len(empty_fields) < amount or amount <= 0:
        await ctx.send(f"{ctx.author.mention}, you don't have enough empty fields. You have {len(empty_fields)} empty fields.")
        return

    # Deduct chips and plant crops
    user_data['chips'] -= total_cost
    crop_name = crop.lower()

    for i in range(amount):
        empty_field_index = empty_fields[i]
        user_data['fields'][empty_field_index] = {
            'crop': crop_name,
            'plant_time': datetime.now().isoformat(),
            'growth_time': CROP_GROWTH[crop_name]
        }

    save_player_data(data)
    growth_time_minutes = CROP_GROWTH[crop_name] // 60
    await ctx.send(f"{ctx.author.mention}, you planted {CROP_EMOJI[crop_name]} {amount} time(s) in fields {', '.join(str(i + 1) for i in empty_fields[:amount])}! Each will be ready to harvest in {growth_time_minutes} minutes.")

@econ.command()
async def harvest(ctx):
    """Harvest your crops and earn chips (*harvest)."""
    player_id = ctx.author.id
    data = load_player_data()

    if str(player_id) not in data:
        await ctx.send(f"{ctx.author.mention}, you don't have any crops to harvest!")
        return

    user_data = data[str(player_id)]
    fields = user_data['fields']
    now = datetime.now()

    total_earnings = 0
    harvested_crops = []

    for i, field in enumerate(fields):
        if field is not None:
            plant_time = datetime.fromisoformat(field['plant_time'])
            growth_time = timedelta(seconds=field['growth_time'])

            if now >= plant_time + growth_time:
                crop = field['crop']
                min_yield, max_yield = CROP_YIELD[crop]
                earnings = random.randint(min_yield, max_yield)
                total_earnings += earnings
                harvested_crops.append((i + 1, CROP_EMOJI[crop], earnings))
                fields[i] = None  # Clear the field after harvesting

    if total_earnings > 0:
        user_data['chips'] += total_earnings
        save_player_data(data)

        crop_details = "\n".join([f"Field {field}: {emoji} (+{earnings} 🪙)" for field, emoji, earnings in harvested_crops])
        await ctx.send(
            f"{ctx.author.mention}, you harvested the following crops:\n{crop_details}\n"
            f"You earned a total of {total_earnings} 🪙! Your new balance is {user_data['chips']} 🪙."
        )
    else:
        await ctx.send(f"{ctx.author.mention}, none of your crops are ready to harvest yet! Check back later.")

@econ.command()
async def view_farm(ctx):
    """View the status of your farm (*view_farm)."""
    player_id = ctx.author.id
    data = load_player_data()

    if str(player_id) not in data:
        await ctx.send(f"{ctx.author.mention}, you don't have any fields yet! Plant some crops to get started.")
        return

    user_data = data[str(player_id)]
    fields = user_data.get('fields', [None] * 5)
    now = datetime.now()

    field_status = []
    for i, field in enumerate(fields):
        if field is None:
            field_status.append(f"Field {i + 1}: Empty 🌱")
        else:
            crop = field['crop']
            plant_time = datetime.fromisoformat(field['plant_time'])
            growth_time = timedelta(seconds=field['growth_time'])
            harvestable = now >= plant_time + growth_time

            status = "Ready to harvest ✅" if harvestable else "Still growing ⏳"
            time_left = max((plant_time + growth_time - now).seconds // 60, 0)
            field_status.append(
                f"Field {i + 1}: {CROP_EMOJI[crop]} ({crop}) - {status} "
                f"({time_left} minutes left)" if not harvestable else f"Field {i + 1}: {CROP_EMOJI[crop]} ({crop}) - {status}"
            )

    farm_status = "\n".join(field_status)
    await ctx.send(f"{ctx.author.mention}, here is the status of your farm:\n{farm_status}")

@bot.command()
async def leaderboard(ctx):
    """View the leaderboard for the top 10 users with the most chips in the server."""
    data = load_player_data()
    guild_members = ctx.guild.members

    leaderboard_data = []
    for player_id, player_data in data.items():
        try:
            member = await ctx.guild.fetch_member(int(player_id))
        except (discord.NotFound, discord.HTTPException):
            member = None
        if member and not member.bot:
            leaderboard_data.append((member, player_data['chips']))

    leaderboard_data.sort(key=lambda x: x[1], reverse=True)
    top_users = leaderboard_data[:10]

    if not top_users:
        await ctx.send("No players with chips found in this server!")
        return

    # Format the leaderboard
    leaderboard_message = "**🏆 Server Leaderboard 🏆**\n"
    for rank, (member, chips) in enumerate(top_users, start=1):
        leaderboard_message += f"**{rank}.** {member.display_name} - {chips} 🪙\n"

    await ctx.send(leaderboard_message)

@bot.command()
@commands.cooldown(1, 10, BucketType.user)
async def fountain(ctx):
    """Throw 1 chip into Kanade's Wish Fountain and pray for good fortune!"""
    player_id = ctx.author.id
    data = load_player_data()
    fountain_data = load_fountain_data()
    fountain_coins = fountain_data["fountain_coins"]
    user_data = get_or_create_chips(player_id)

    # Check if the user has at least 1 chip to throw into the fountain
    if user_data['chips'] < 1:
        await ctx.send(f"{ctx.author.mention}, you need at least 1 🪙 to throw into the Wish Fountain!")
        return

    user_data['chips'] -= 1
    fountain_coins += 1
    fountain_data["fountain_coins"] = fountain_coins
    result = random.choice(OUTCOMES)
    if "LUCKY" in result:  # Lucky outcome
        user_data['chips'] += fountain_coins
        await ctx.send(f"{ctx.author.mention}, you threw 1 🪙 into the Wish Fountain! 🎉 "
                       f"Kanade's Wish Fountain splashed {fountain_coins} 🪙 in front of you! 🎉")
        fountain_data["fountain_coins"] = 0
    else:
        await ctx.send(f"{ctx.author.mention}, you threw 1 🪙 into the Wish Fountain! {result}")

    save_player_data(data)
    save_fountain_data(fountain_data)

@fountain.error
async def fountain_error(ctx, error):
    """Handle fountain cooldown error"""
    if isinstance(error, commands.CommandOnCooldown):
        retry_after = error.retry_after
        minutes, seconds = divmod(retry_after, 60)
        cooldown_message = (
            f"⏳ {ctx.author.mention}, the fountain is being cleaned! "
            f"Please wait {int(seconds)} seconds before trying again."
        )
        await ctx.send(cooldown_message)
        return

@game.command()
@commands.cooldown(1, 120, BucketType.user)
async def plane(ctx):
    """Start a 11-9 game."""
    player = ctx.author
    game = TowerDodge()
    await ctx.send(f"Starting 11-9 operation! Survive 10 rounds to win. You have 2 lives as twin towers.")

    while game.round < 10 and game.lives > 0:
        game.next_round()
        plane_count = 1
        if game.round > 5:
            plane_count = 2
        await ctx.send(f"Round {game.round}: There are {plane_count} ✈️ approaching! Choose: left, right, up, or down.")

        def check_move(m):
            return m.author == player

        valid_move = False
        while not valid_move:
            try:
                msg = await bot.wait_for("message", check=check_move, timeout=30.0)
                move = msg.content.lower()
                if move not in game.directions:
                    await ctx.send(f"{player.mention}, invalid move! Choose left, right, up, or down.")
                    continue
                valid_move = True
            except:
                await ctx.send(f"{player.mention} did not move in time and loses a life!")
                if game.hit():
                    await ctx.send(f"{player.mention} is eliminated!")
                    return
                break

        plane_directions = random.sample(game.directions, plane_count)
        await ctx.send(f"The ✈️ move {', '.join(plane_directions)}!")

        if move in plane_directions:
            await ctx.send(f"✈️ {player.mention}'s tower moved {move} and got hit 💔!")
            if game.hit():
                await ctx.send(f"✈️ {player.mention}! Your tower has been destroyed ❌!")
                break
        else:
            await ctx.send(f"{player.mention}'s tower dodged the planes safely ✅!")

    if game.round == 10 and game.lives > 0:
        current_chips = get_or_create_chips(player.id)['chips']
        update_player_chips(player.id, current_chips + 1000)
        await ctx.send(f"🎉 {player.mention} survived all 10 rounds and earns 1000 chips! Congratulations!")
    else:
        await ctx.send(f"Game over, {player.mention}. Better luck next time!")

    results = f"{player.mention}: {get_or_create_chips(player.id)['chips']} 🪙"
    await ctx.send(f"Final chip count:\n{results}")

@plane.error
async def plane_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        retry_after = error.retry_after
        minutes, seconds = divmod(retry_after, 60)
        cooldown_message = (
            f"⏳ {ctx.author.mention}, the tower is being prepared! "
            f"Please wait {int(minutes)} minutes and {int(seconds)} seconds before trying again."
        )
        await ctx.send(cooldown_message)

pve_game = PVEGame()

@bot.command()
async def start(ctx):
    """Start the tower climbing PVE game."""
    response = pve_game.start_game()
    await ctx.send(response)


@bot.command()
async def battle(ctx):
    """Battle against the enemy (1 enemy at a time)."""
    response = pve_game.battle_turn()
    await ctx.send(response)

@bot.command()
async def shop(ctx):
    """Display current shop items."""
    shop_list = "\n".join([f"{char.name} (HP: {char.HP}, ATK: {char.ATK}, DEF: {char.DEF}, Cost: {char.Cost}, Element: {char.element}, Trait: {char.trait})" for char in pve_game.shop])
    await ctx.send(f"**Available characters in shop:**\n{shop_list}")

@bot.command()
async def reroll(ctx):
    """Reroll the shop using 1 coin."""
    response = pve_game.reroll_shop()  # Only returns a string
    shop_list = "\n".join([
        f"{char.name} (HP: {char.HP}, ATK: {char.ATK}, DEF: {char.DEF}, Cost: {char.Cost}, Element: {char.element}, Trait: {char.trait})"
        for char in pve_game.shop])
    await ctx.send(f"**{response}**\n{shop_list}")


@bot.command()
async def buy(ctx, *character_name: str):
    """Buy characters into your inventory."""
    character_name = " ".join(character_name).capitalize()
    response = pve_game.buy_character(character_name)
    await ctx.send(response)

@bot.command()
async def enemies(ctx):
    """See enemy line up in the current floor."""
    enemy_list = "\n".join([enemy.name for enemy in pve_game.enemies])
    await ctx.send(f"Upcoming enemies:\n{enemy_list}")

@bot.command()
async def choose(ctx, *character_name: str):
    """Choosing character to fight in the battle."""
    character_name = " ".join(character_name).capitalize()
    response = pve_game.choose_character(character_name)
    await ctx.send(response)

@bot.command()
async def inventory(ctx):
    """Show the player character inventory."""
    if not pve_game.inventory:
        await ctx.send("Your inventory is empty.")
        return
    inventory_list = "\n".join([
        f"{char.name} (HP: {char.HP}, ATK: {char.ATK}, DEF: {char.DEF}, Element: {char.element}, Trait: {char.trait})"
        for char in pve_game.inventory
    ])
    await ctx.send(f"Your inventory:\n{inventory_list}")

char_list = CharacterList()

@bot.command()
async def info(ctx, *character_name: str):
    """Command to view character ability information in Tower climbing game."""
    character_name = " ".join(character_name).capitalize()
    char_list.generate_list()
    character_classes = char_list.chars_list
    selected_char = next((c for c in character_classes if c.name == character_name), None)
    if selected_char:
        character_instance = selected_char
        character_info = character_instance.view_info()
        await ctx.send(f"**{character_instance.name} Information:**\n{character_info}")
    else:
        await ctx.send("Character not found. Please check the name and try again.")
    char_list.reset()
    

@bot.event
async def on_ready():
    activity = discord.Game(name="Piano 🎹")
    await bot.change_presence(activity=activity)
    print(f'Logged in as {bot.user} and status set to Playing Piano 🎹.')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        pass
    elif isinstance(error, commands.CommandOnCooldown):
        pass
    else:
        raise error

if __name__ == '__main__':
    bot.run(BOT_TOKEN)
