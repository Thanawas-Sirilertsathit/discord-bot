@bot.command()
@commands.cooldown(1, 120, BucketType.user)
async def gomoku(ctx, player2: discord.Member):
    """Play a Gomoku game together."""
    player1 = ctx.author
    if player1 == player2:
        await ctx.send("You can't play against yourself!")
        return
    
    players = [player1, player2]
    await ctx.send(f"{', '.join(player.mention for player in players)} are you ready to start the gomoku game? Reply with 'yes' to accept or 'no' to cancel.")
    
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

    if any(response == "no" for response in responses.values()):
        await ctx.send("Game has been canceled because some players did not confirm.")
        return

    game = Gomoku(player1, player2)
    await ctx.send(f"{player1.mention} vs {player2.mention}! Game start!\n{game.display_board()}")

    while not game.winner:
        await ctx.send(f"{game.current_player.mention}, it's your turn! Use `*place x y` to place your piece (0-14).")

        def check(msg):
            return msg.author == game.current_player and msg.content.startswith("*place")

        try:
            msg = await bot.wait_for("message", check=check, timeout=60.0)
            _, x, y = msg.content.split()
            x, y = int(x), int(y)
            if 0 <= x < 15 and 0 <= y < 15 and game.place_piece(x, y):
                await ctx.send(f"Move placed at {x}, {y}\n{game.display_board()}")
            else:
                await ctx.send("Invalid move! Try again.")
                continue
        except Exception:
            await ctx.send(f"{game.current_player.mention} took too long! Game forfeited.")
            return
    
    winner = game.winner
    await ctx.send(f"{winner.mention} wins! 🎉 100 coins awarded!")

@gomoku.error
async def gomoku_error(ctx, error):
    """Handle gomoku cooldown error."""
    if isinstance(error, commands.CommandOnCooldown):
        retry_after = error.retry_after
        minutes, seconds = divmod(retry_after, 60)
        cooldown_message = (
            f"⏳ {ctx.author.mention}, the gomoku board is being prepared! "
            f"Please wait {int(minutes)} minutes and {int(seconds)} seconds before trying again."
        )
        await ctx.send(cooldown_message)