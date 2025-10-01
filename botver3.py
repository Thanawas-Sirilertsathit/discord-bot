import discord
import asyncio
from discord.ext import commands, tasks
from discord import app_commands
import json
from datetime import datetime, timedelta
from decouple import config

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="*", intents=intents)
BOT_TOKEN = config("BOT_TOKEN")

DATA_FILE = "reservation.json"
STAT_FILE = "stat.json"
GUILD_ID = int(config("GUILD_ID"))
CHANNEL_ID = int(config("CHANNEL_ID"))
SHOPOWNER_ID = int(config("SHOPOWNER_ID"))

# Operating hours
OFFICIAL_START_HOUR = 9
OFFICIAL_END_HOUR = 23

# ----------------- Helper functions -----------------
def load_reservations():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_reservations(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def load_stats():
    try:
        with open(STAT_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_stats(data):
    with open(STAT_FILE, "w") as f:
        json.dump(data, f, indent=2)

def parse_datetime(dt_str: str) -> datetime:
    return datetime.strptime(dt_str, "%Y-%m-%d %H:%M")

def add_exp(user_id: int, exp: int, confirmed=False):
    stats = load_stats()
    uid = str(user_id)
    if uid not in stats:
        stats[uid] = {"exp": 0, "level": 0, "reservations": 0, "confirmations": 0}
    stats[uid]["exp"] += exp
    if confirmed:
        stats[uid]["confirmations"] += 1
    stats[uid]["level"] = stats[uid]["exp"] // 10
    save_stats(stats)
    return stats[uid]

def add_reservation_stat(user_id: int):
    stats = load_stats()
    uid = str(user_id)
    if uid not in stats:
        stats[uid] = {"exp": 0, "level": 0, "reservations": 0, "confirmations": 0}
    stats[uid]["reservations"] += 1
    save_stats(stats)
    return stats[uid]

def count_user_reservations(user_id: int):
    reservations = load_reservations()
    now = datetime.now()
    return sum(1 for r in reservations if r["user"] == user_id and parse_datetime(r["start"]) >= now)

# ----------------- Commands -----------------
@bot.tree.command(
    name="reserve",
    description="Reserve a 1-hour time slot for BA business",
)
@app_commands.describe(
    year="Year (e.g., 2025)",
    month="Month (1-12)",
    day="Day (1-31)",
    hour="Hour (0-23, 24h format)",
    minute="Minute (0-59)",
    gamemode="Game mode for this session"
)
@app_commands.guilds(discord.Object(id=GUILD_ID))
async def reserve(interaction: discord.Interaction, year: int, month: int, day: int, hour: int, minute: int, gamemode: str):
    try:
        start_time = datetime(year, month, day, hour, minute)
        end_time = start_time + timedelta(hours=1)

        if start_time < datetime.now():
            await interaction.response.send_message("⛔ Cannot reserve a past time slot.", ephemeral=True)
            return
        if not (OFFICIAL_START_HOUR <= hour <= OFFICIAL_END_HOUR):
            await interaction.response.send_message(f"⛔ Reservations allowed {OFFICIAL_START_HOUR}:00-{OFFICIAL_END_HOUR}:00.", ephemeral=True)
            return
        if start_time.hour == OFFICIAL_END_HOUR and start_time.minute != 0:
            await interaction.response.send_message("⛔ Last reservation must start exactly at 23:00.", ephemeral=True)
            return

        # limit concurrent reservations
        if count_user_reservations(interaction.user.id) >= 3:
            await interaction.response.send_message("❌ You can only have 3 active reservations at a time.", ephemeral=True)
            return

        reservations = load_reservations()
        for r in reservations:
            if r["start"] == start_time.strftime("%Y-%m-%d %H:%M"):
                await interaction.response.send_message("❌ This time slot is already reserved.", ephemeral=True)
                return

        reservations.append({
            "user": interaction.user.id,
            "start": start_time.strftime("%Y-%m-%d %H:%M"),
            "end": end_time.strftime("%Y-%m-%d %H:%M"),
            "gamemode": gamemode,
            "confirmed": False
        })
        save_reservations(reservations)

        # Add EXP + stats
        stats = add_exp(interaction.user.id, 1)
        add_reservation_stat(interaction.user.id)

        embed = discord.Embed(
            title="✅ Reservation Confirmed",
            color=discord.Color.green(),
            timestamp=start_time
        )
        embed.add_field(name="Time", value=f"{start_time.strftime('%Y-%m-%d %H:%M')} - {end_time.strftime('%H:%M')}", inline=False)
        embed.add_field(name="Reserved by", value=interaction.user.display_name, inline=False)
        embed.add_field(name="Gamemode", value=gamemode, inline=False)
        embed.add_field(name="EXP", value=f"{stats['exp']} (Level {stats['level']})", inline=False)
        embed.set_footer(text="Blue Archive Raid Session")

        await interaction.response.send_message(embed=embed)

    except ValueError:
        await interaction.response.send_message("❌ Invalid date/time input.", ephemeral=True)


@bot.tree.command(
    name="confirm",
    description="Confirm a user's reservation (Shopowner only)."
)
@app_commands.describe(user="The user to confirm reservation for")
@app_commands.guilds(discord.Object(id=GUILD_ID))
async def confirm(interaction: discord.Interaction, user: discord.User):
    if interaction.user.id != SHOPOWNER_ID:
        await interaction.response.send_message("⛔ Only the shopowner can confirm reservations.", ephemeral=True)
        return

    reservations = load_reservations()
    found = False
    for r in reservations:
        if r["user"] == user.id and not r.get("confirmed", False):
            r["confirmed"] = True
            found = True
            stats = add_exp(user.id, 3, confirmed=True)  # add 3 exp + confirmation
            save_reservations(reservations)

            embed = discord.Embed(
                title="🔒 Reservation Confirmed by Head Sensei",
                color=discord.Color.gold()
            )
            embed.add_field(name="User", value=user.mention, inline=False)
            embed.add_field(name="Gamemode", value=r.get("gamemode", "N/A"), inline=False)
            embed.add_field(name="EXP", value=f"{stats['exp']} (Level {stats['level']})", inline=False)
            embed.set_footer(text="Blue Archive Raid Session")
            await interaction.response.send_message(embed=embed)
            break

    if not found:
        await interaction.response.send_message("❌ No unconfirmed reservations found for that user.", ephemeral=True)


@bot.tree.command(
    name="schedule",
    description="Show all upcoming Blue Archive session reservations"
)
@app_commands.guilds(discord.Object(id=GUILD_ID))
async def schedule(interaction: discord.Interaction):
    now = datetime.now()
    reservations = load_reservations()
    upcoming = [r for r in reservations if parse_datetime(r["start"]) >= now]

    if not upcoming:
        await interaction.response.send_message("📭 No upcoming reservations.", ephemeral=True)
        return

    upcoming.sort(key=lambda x: x["start"])

    embed = discord.Embed(
        title="📅 Upcoming Blue Archive Raid Session Reservations",
        color=discord.Color.blue()
    )
    guild = bot.get_guild(GUILD_ID)
    for r in upcoming:
        start_time = parse_datetime(r["start"])
        end_time = parse_datetime(r["end"])
        member = guild.get_member(r["user"])
        username = member.display_name if member else "Unknown"
        gamemode = r.get("gamemode", "N/A")
        confirmed = "✅ Confirmed" if r.get("confirmed", False) else "⌛ Pending"
        embed.add_field(
            name=f"⏰ {start_time.strftime('%Y-%m-%d %H:%M')} - {end_time.strftime('%H:%M')}",
            value=f"📘 Reserved by: {username}\n🎮 Gamemode: {gamemode}\n{confirmed}\n───────────────────",
            inline=False
        )

    await interaction.response.send_message(embed=embed, ephemeral=False)


@bot.tree.command(
    name="profile",
    description="Show user profile stats"
)
@app_commands.describe(user="User to show profile for (optional)")
@app_commands.guilds(discord.Object(id=GUILD_ID))
async def profile(interaction: discord.Interaction, user: discord.User = None):
    user = user or interaction.user
    stats = load_stats().get(str(user.id), {"exp": 0, "level": 0, "reservations": 0, "confirmations": 0})

    exp = stats["exp"]
    level = stats["level"]
    reservations = stats.get("reservations", 0)
    confirmations = stats.get("confirmations", 0)

    # Progress bar
    exp_in_level = exp % 10
    bar_length = 10
    filled = "🟩" * exp_in_level
    empty = "⬜" * (bar_length - exp_in_level)
    progress_bar = f"{filled}{empty} ({exp_in_level}/10)"

    # Ongoing reservation
    reservations_data = load_reservations()
    now = datetime.now()
    upcoming = [r for r in reservations_data if r["user"] == user.id and parse_datetime(r["start"]) >= now]
    upcoming.sort(key=lambda x: x["start"])
    ongoing_text = f"⏰ {parse_datetime(upcoming[0]['start']).strftime('%Y-%m-%d %H:%M')} ({upcoming[0].get('gamemode','N/A')})" if upcoming else "None"

    embed = discord.Embed(
        title=f"👤 {user.display_name}'s Profile",
        color=discord.Color.purple()
    )
    embed.set_thumbnail(url=user.display_avatar.url)
    embed.add_field(name="User", value=user.mention, inline=False)
    embed.add_field(name="Level", value=str(level), inline=True)
    embed.add_field(name="EXP", value=progress_bar, inline=False)
    embed.add_field(name="Ongoing Reservation", value=ongoing_text, inline=False)
    embed.add_field(name="Total Reservations", value=str(reservations), inline=True)
    embed.add_field(name="Confirmations", value=str(confirmations), inline=True)

    await interaction.response.send_message(embed=embed)


# ----------------- Alerts -----------------
@tasks.loop(seconds=30)
async def reservation_alerts():
    now = datetime.now().replace(second=0, microsecond=0)
    reservations = load_reservations()
    channel = bot.get_channel(CHANNEL_ID)

    if channel is None:
        print("⚠ Channel not found. Check CHANNEL_ID.")
        return

    updated = []
    for r in reservations:
        start_time = parse_datetime(r["start"])
        if start_time == now:
            try:
                user = await bot.fetch_user(r["user"])
            except discord.NotFound:
                user = None

            gamemode = r.get("gamemode", "N/A")

            embed = discord.Embed(
                title="🔔 Customer Reservation Alert",
                color=discord.Color.green(),
                timestamp=start_time
            )
            embed.add_field(name="Time", value=start_time.strftime("%Y-%m-%d %H:%M"), inline=False)
            embed.add_field(name="Reserved by", value=user.mention if user else "Unknown", inline=False)
            embed.add_field(name="Gamemode", value=gamemode, inline=False)
            embed.set_footer(text="Please prepare for Blue Archive session with customer!")

            await channel.send(content=f"<@{SHOPOWNER_ID}> Meeting time!", embed=embed)
        else:
            updated.append(r)
    save_reservations(updated)


@bot.event
async def on_ready():
    activity = discord.Game(name="Typewriter 🔤")
    await bot.change_presence(activity=activity)
    print(f'✅ Logged in as {bot.user} and status set to Typewriter.')

    try:
        synced = await bot.tree.sync(guild=discord.Object(id=GUILD_ID))
        print(f"🔄 Synced {len(synced)} command(s).")
        reservation_alerts.start()
    except Exception as e:
        print(f"⚠ Failed to sync commands: {e}")


if __name__ == "__main__":
    bot.run(BOT_TOKEN)
