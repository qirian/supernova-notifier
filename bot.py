import os
import discord
from discord.ext import commands, tasks
from keep_alive import keep_alive

intents = discord.Intents.default()
intents.members = True  # Needed to detect boosts (member updates)
bot = commands.Bot(command_prefix="!", intents=intents)

# ---- Profile Picture ----
PROFILE_PIC_URL = "https://cdn.discordapp.com/attachments/1401822345953546284/1418750912758943754/emvpuh1.gif"

# ---- Image Links for Embed ----
IMG_THUMB = PROFILE_PIC_URL
IMG_AUTHOR = PROFILE_PIC_URL
IMG_FOOTER = PROFILE_PIC_URL

# ---- Channel ID for Boosts ----
BOOST_CHANNEL_ID = 1418440616131428482  # Set your boost channel ID

# ---- On Ready ----
@bot.event
async def on_ready():
    print(f"Bot logged in as {bot.user}")

    # Streaming Status
    await bot.change_presence(activity=discord.Streaming(
        name="discord.gg/supermova",
        url="https://www.twitch.tv/qirixn"
    ))

# ---- Detect Boosts ----
@bot.event
async def on_member_update(before, after):
    # Nitro boost detection
    if before.premium_since != after.premium_since and after.premium_since:
        channel = bot.get_channel(BOOST_CHANNEL_ID)
        if not channel:
            print("Boost channel not found")
            return

        # Count current boosters
        booster_count = sum(1 for m in after.guild.members if m.premium_since)

        embed = discord.Embed(
            title="A new Boost has appeared.",
            description=f"Thank you {after.mention} for your Boost! We have than to you **{booster_count} Boosts**.",
            color=discord.Color(int("7b28a1", 16))
        )
        embed.set_author(name="Supernova x Welcomer", icon_url=IMG_AUTHOR)
        embed.set_thumbnail(url=IMG_THUMB)
        embed.set_footer(text="© 2022–2024 Supernova | Hosted by Levin. All Rights Reserved.", icon_url=IMG_FOOTER)

        try:
            await channel.send(embed=embed)
            print(f"Boost embed sent for {after}")
        except Exception as e:
            print(f"Could not send boost embed for {after}: {e}")

# ---- Keep Alive ----
keep_alive()  # keeps the bot online with Render + UptimeRobot

# ---- Start Bot ----
bot.run(os.getenv("DISCORD_TOKEN"))
