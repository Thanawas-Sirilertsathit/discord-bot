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
GUILD_ID = int(config("GUILD_ID_TEST"))
CHANNEL_ID = int(config("CHANNEL_ID_TEST"))
SHOPOWNER_ID = int(config("SHOPOWNER_ID"))

# Operating hours
OFFICIAL_START_HOUR = 9
OFFICIAL_END_HOUR = 23

def load_reservations():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_reservations(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def parse_datetime(dt_str: str) -> datetime:
    return datetime.strptime(dt_str, "%Y-%m-%d %H:%M")

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
    gamemode="Game mode for this session (e.g., 'Chesed Insane, Joint Firing Drill, Chokmah')"
)
@app_commands.guilds(discord.Object(id=GUILD_ID))
async def reserve(interaction: discord.Interaction, year: int, month: int, day: int, hour: int, minute: int, gamemode: str):
    try:
        start_time = datetime(year, month, day, hour, minute)
        end_time = start_time + timedelta(hours=1)

        if start_time < datetime.now():
            await interaction.response.send_message(
                "⛔ Cannot reserve a past time slot.", ephemeral=True
            )
            return
        if not (OFFICIAL_START_HOUR <= hour <= OFFICIAL_END_HOUR):
            await interaction.response.send_message(
                f"⛔ Reservations are only allowed from {OFFICIAL_START_HOUR}:00 to {OFFICIAL_END_HOUR}:00.", 
                ephemeral=True
            )
            return
        if start_time.hour == OFFICIAL_END_HOUR and start_time.minute != 0:
            await interaction.response.send_message(
                "⛔ Last reservation must start at 23:00 and end at 00:00.", ephemeral=True
            )
            return
        reservations = load_reservations()
        for r in reservations:
            if r["start"] == start_time.strftime("%Y-%m-%d %H:%M"):
                await interaction.response.send_message(
                    "❌ This time slot is already reserved.", ephemeral=True
                )
                return

        reservations.append({
            "user": interaction.user.id,
            "start": start_time.strftime("%Y-%m-%d %H:%M"),
            "end": end_time.strftime("%Y-%m-%d %H:%M"),
            "gamemode": gamemode
        })
        save_reservations(reservations)

        embed = discord.Embed(
            title="✅ Reservation Confirmed",
            color=discord.Color.green(),
            timestamp=start_time
        )
        embed.add_field(name="Time", value=f"{start_time.strftime('%Y-%m-%d %H:%M')} - {end_time.strftime('%H:%M')}", inline=False)
        embed.add_field(name="Reserved by", value=interaction.user.display_name, inline=False)
        embed.add_field(name="Gamemode", value=gamemode, inline=False)
        embed.set_footer(text="Blue Archive Raid Session")

        await interaction.response.send_message(embed=embed)

    except ValueError:
        await interaction.response.send_message(
            "❌ Invalid date/time input.", ephemeral=True
        )


@bot.tree.command(
    name="schedule",
    description="Show all upcoming Blue Archive session reservations"
)
@app_commands.guilds(discord.Object(id=GUILD_ID))
async def schedule(interaction: discord.Interaction):
    now = datetime.now()
    reservations = load_reservations()
    upcoming = []

    for r in reservations:
        start_time = parse_datetime(r["start"])
        if start_time >= now:
            upcoming.append(r)

    if not upcoming:
        await interaction.response.send_message("📭 There are no upcoming reservations.", ephemeral=True)
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
        user_id = r["user"]
        gamemode = r.get("gamemode", "N/A")
        member = guild.get_member(user_id)
        username = member.display_name if member else "Unknown"
        embed.add_field(
            name=f"⏰ {start_time.strftime('%Y-%m-%d %H:%M')} - {end_time.strftime('%H:%M')}",
            value=f"📘 Reserved by: {username}\n🎮 Gamemode: {gamemode}\n───────────────────",
            inline=False
        )

    await interaction.response.send_message(embed=embed, ephemeral=False)


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

            await channel.send(
                content=f"<@{SHOPOWNER_ID}> Meeting time!",
                embed=embed
            )
        else:
            updated.append(r)
    save_reservations(updated)


# @bot.event
# async def on_ready():
#     bot.tree.clear_commands(guild=discord.Object(id=GUILD_ID))
#     bot.tree.sync(guild=discord.Object(id=GUILD_ID))
#     await bot.change_presence(activity=discord.Game(name="Typewriter 🔤"))
#     print(f"✅ Logged in as {bot.user}")

@bot.event
async def on_ready():
    activity = discord.Game(name="Typewriter 🔤")
    await bot.change_presence(activity=activity)
    print(f'✅ Logged in as {bot.user} and status set to Typewriter.')

    try:
        synced = await bot.tree.sync(guild=discord.Object(id=GUILD_ID))
        print(f"🔄 Synced {len(synced)} command(s) globally.")
        reservation_alerts.start()
    except Exception as e:
        print(f"⚠ Failed to sync commands: {e}")

if __name__ == "__main__":
    bot.run(BOT_TOKEN)
