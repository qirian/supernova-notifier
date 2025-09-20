import os
import discord
from discord.ext import commands, tasks
from keep_alive import keep_alive

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# ---- Profile Picture ----
PROFILE_PIC_URL = "https://cdn.discordapp.com/attachments/1401822345953546284/1418750912758943754/emvpuh1.gif"

# ---- On Ready ----
@bot.event
async def on_ready():
    print(f"Bot logged in as {bot.user}")

    # Streaming Status
    await bot.change_presence(activity=discord.Streaming(
        name="discord.gg/supernova",
        url="https://www.twitch.tv/qirixn"
    ))

    # Optional: Update profile picture
    try:
        async with bot.session if hasattr(bot, 'session') else None:
            await bot.user.edit(avatar=await (await discord.http.Route('GET', PROFILE_PIC_URL)).read())
    except Exception as e:
        print(f"Could not update profile picture: {e}")

# ---- Keep Alive ----
keep_alive()  # keeps the bot online with Render + UptimeRobot

# ---- Start Bot ----
bot.run(os.getenv("DISCORD_TOKEN"))
