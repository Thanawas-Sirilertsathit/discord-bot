@bot.command()
@commands.cooldown(1, 300, commands.BucketType.user)
async def mine(ctx):
    """Mine for random resources for crafting objects."""
    data = load_player_data()
    user_id = str(ctx.author.id)
    if user_id not in data:
        data[user_id] = {"chips": 0, "fields": [], "inventory": {}, "crafting_slots": []}

    inventory = data[user_id].setdefault("inventory", {})
    mine_amount = random.randint(3,6)
    mine_array = []
    for i in range(mine_amount):
        mined_item = random.choice(RESOURCE)
        mine_array.append(mined_item)
        if mined_item not in inventory:
            inventory[mined_item] = 0
        inventory[mined_item] += 1
        save_player_data(data)
    mined_items_display = ', '.join(mine_array)
    await ctx.send(f"{ctx.author.mention} mined {mined_items_display}! It's added to your inventory.")

@mine.error
async def mine_error(ctx, error):
    """Handle mine cooldown error."""
    if isinstance(error, commands.CommandOnCooldown):
        retry_after = error.retry_after
        minutes, seconds = divmod(retry_after, 60)
        cooldown_message = (
            f"⛏️ {ctx.author.mention}, you need to wait {int(minutes)} minutes and {int(seconds)} seconds to mine again."
        )
        await ctx.send(cooldown_message)

@bot.command()
async def inventory(ctx):
    """Check your inventory."""
    user_id = str(ctx.author.id)
    data = load_player_data()
    if user_id not in data or not data[user_id].get("inventory"):
        await ctx.send(f"{ctx.author.mention}, your inventory is empty. Start mining to gather resources!")
        return

    inventory = data[user_id]["inventory"]
    inv = '\n'.join([f"{item}: {count}" for item, count in inventory.items()])
    await ctx.send(f"{ctx.author.mention}'s Inventory:\n{inv}")

@bot.command()
async def craft(ctx, item: str):
    """Craft an item using resources."""
    data = load_player_data()
    user_id = str(ctx.author.id)
    if user_id not in data:
        data[user_id] = {"chips": 0, "fields": [], "inventory": {}, "crafting_slots": []}
    inventory = data[user_id].setdefault("inventory", {})
    crafting_slots = data[user_id].setdefault("crafting_slots", [])
    if len(crafting_slots) >= 3:
        await ctx.send(f"{ctx.author.mention}, you already have 3 crafting slots in use. Wait for a slot to free up.")
        return
    selected_item = None
    for emoji, recipe in CRAFTING_RECIPE.items():
        if item.lower() == recipe['name'].lower() or item == emoji:
            selected_item = emoji
            break
    if not selected_item:
        available_items = ', '.join([f"{emoji} ({recipe['name']})" for emoji, recipe in CRAFTING_RECIPE.items()])
        await ctx.send(f"{ctx.author.mention}, unknown item. Available items to craft: {available_items}")
        return
    recipe = CRAFTING_RECIPE[selected_item]
    missing_items = [
        f"{resource} ({amount - inventory.get(resource, 0)} more needed)"
        for resource, amount in recipe.items()
        if resource not in ['time', 'value', 'name'] and inventory.get(resource, 0) < amount
    ]
    if missing_items:
        await ctx.send(
            f"{ctx.author.mention}, you don't have enough resources to craft {selected_item} ({recipe['name']}). Missing: {', '.join(missing_items)}"
        )
        return
    for resource, amount in recipe.items():
        if resource not in ['time', 'value', 'name']:
            inventory[resource] -= amount
            if inventory[resource] == 0:
                del inventory[resource]

    total_seconds = recipe['time']
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    time_str = f"{hours} hour(s) {minutes} minute(s)" if hours > 0 else f"{minutes} minute(s)"

    finish_time = (datetime.now() + timedelta(seconds=recipe['time'])).isoformat()
    crafting_slots.append({"item": selected_item, "name": recipe['name'], "finish_time": finish_time})
    
    save_player_data(data)
    
    await ctx.send(f"{ctx.author.mention} has started crafting {selected_item} ({recipe['name']}). It will take {time_str}.")

@bot.command()
async def collect(ctx):
    """Collect completed crafting items and sell them for money."""
    data = load_player_data()
    user_id = str(ctx.author.id)
    if user_id not in data:
        data[user_id] = {"chips": 0, "fields": [], "inventory": {}, "crafting_slots": []}

    crafting_slots = data[user_id].setdefault("crafting_slots", [])
    inventory = data[user_id].setdefault("inventory", {})

    # Check for completed crafting jobs
    current_time = datetime.now()
    completed_items = []

    for slot in crafting_slots[:]:
        finish_time = datetime.fromisoformat(slot['finish_time'])
        if current_time >= finish_time:
            completed_items.append(slot)
            crafting_slots.remove(slot)

    if not completed_items:
        await ctx.send(f"{ctx.author.mention}, you have no completed crafting jobs to collect.")
        return

    total_coins = 0
    for item in completed_items:
        crafted_item = item['item']
        inventory[crafted_item] = inventory.get(crafted_item, 0) + 1
        recipe = CRAFTING_RECIPE[crafted_item]
        total_coins += recipe['value']

    data[user_id]['chips'] += total_coins
    save_player_data(data)

    collected_summary = ', '.join([f"{item['item']} ({CRAFTING_RECIPE[item['item']]['name']})" for item in completed_items])
    await ctx.send(
        f"{ctx.author.mention}, you collected the following items: {collected_summary}. "
        f"You earned a total of {total_coins} coins!"
    )

@bot.command()
async def view_craft(ctx):
    """View current crafting slots and their remaining time."""
    data = load_player_data()
    user_id = str(ctx.author.id)
    
    if user_id not in data:
        data[user_id] = {"chips": 0, "fields": [], "inventory": {}, "crafting_slots": []}
    
    crafting_slots = data[user_id].setdefault("crafting_slots", [])

    if not crafting_slots:
        await ctx.send(f"{ctx.author.mention}, you have no active crafting jobs.")
        return

    current_time = datetime.now()
    craft_status = []

    for i, slot in enumerate(crafting_slots, start=1):
        finish_time = datetime.fromisoformat(slot['finish_time'])
        remaining_time = (finish_time - current_time).total_seconds()

        if remaining_time > 0:
            hours, remainder = divmod(int(remaining_time), 3600)
            minutes, seconds = divmod(remainder, 60)
            time_left = f"{hours}h {minutes}m {seconds}s" if hours > 0 else f"{minutes}m {seconds}s"
        else:
            time_left = "Ready to collect ✅"

        craft_status.append(f"{i}. {slot['item']} ({slot['name']}) - {time_left}")

    status_message = "\n".join(craft_status)
    await ctx.send(f"{ctx.author.mention}, your current crafting jobs:\n{status_message}")

@bot.command()
async def recipe(ctx):
    """List of all crafting recipes."""
    available_recipes = []
    for emoji, recipe in CRAFTING_RECIPE.items():
        total_seconds = recipe['time']
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        time_str = f"{hours} hour(s) {minutes} minute(s)" if hours > 0 else f"{minutes} minute(s)"
        resources_needed = '\n'.join([f"{resource}: {amount}" for resource, amount in recipe.items() if resource not in ['time', 'value', 'name']])
        available_recipes.append(f"{emoji} - {recipe['name']} (Time: {time_str})\nResources:\n{resources_needed}")

    if available_recipes:
        embed = discord.Embed(
            title="Available Crafting Recipes",
            description=f"Here are the available crafting recipes, {ctx.author.mention}:",
            color=discord.Color.orange()
        )

        for recipe_info in available_recipes:
            embed.add_field(name="Recipe", value=recipe_info, inline=False)
        
        await ctx.send(embed=embed)
    else:
        await ctx.send(f"{ctx.author.mention}, there are no available recipes.")
