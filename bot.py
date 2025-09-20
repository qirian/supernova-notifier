import os
import discord
from discord.ext import commands
from keep_alive import keep_alive

# --------------------------
# Intents und Bot Setup
# --------------------------
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# --------------------------
# On Ready Event
# --------------------------
@bot.event
async def on_ready():
    print(f"Notifier Bot logged in as {bot.user}")

    # Streaming Status
    await bot.change_presence(activity=discord.Streaming(
        name="discord.gg/supernova",
        url="https://www.twitch.tv/qirixn"
    ))

# --------------------------
# Keep Alive für Render + UptimeRobot
# --------------------------
keep_alive()  # startet den Webserver, damit Bot online bleibt

# --------------------------
# Start Bot
# --------------------------
bot.run(os.getenv("DISCORD_TOKEN"))
