import os
import discord
from discord.ext import commands
from discord import app_commands
from keep_alive import keep_alive

# --------------------------
# Setup
# --------------------------
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# Channel ID for Vouches
VOUCH_CHANNEL_ID = 1418781950994550815

# Embed Style (same as Welcomer)
EMBED_COLOR = 0x7b28a1
THUMBNAIL_URL = "https://cdn.discordapp.com/attachments/1401822345953546284/1418750912758943754/emvpuh1.gif"
IMAGE_URL = "https://cdn.discordapp.com/banners/1402963593527431280/a_00aa2372c379edf2e6dbbccc1ad36c50.gif?size=1024&animated=true"
AUTHOR_ICON = "https://cdn.discordapp.com/attachments/1401822345953546284/1418750912758943754/emvpuh1.gif"
FOOTER_ICON = "https://cdn.discordapp.com/attachments/1401822345953546284/1418750912758943754/emvpuh1.gif"
FOOTER_TEXT = "© 2022–2024 Supernova | Hosted by Levin. All Rights Reserved."

# --------------------------
# Slash Command /vouch
# --------------------------
@bot.tree.command(name="vouch", description="Leave a vouch with stars and feedback.")
@app_commands.describe(
    stars="Enter a number between 1 and 5",
    feedback="Write your feedback about your purchase"
)
async def vouch(interaction: discord.Interaction, stars: int, feedback: str):
    if stars < 1 or stars > 5:
        await interaction.response.send_message("Invalid star rating! Please enter a number between 1 and 5.", ephemeral=True)
        return

    embed = discord.Embed(
        title="Vouch x Supernova | Hosted by Levin.",
        description=f"**Stars:** {'⭐' * stars}\n**Feedback:** {feedback}",
        color=EMBED_COLOR
    )
    embed.set_thumbnail(url=THUMBNAIL_URL)
    embed.set_image(url=IMAGE_URL)
    embed.set_author(name="Supernova x Welcomer", icon_url=AUTHOR_ICON)
    embed.set_footer(text=FOOTER_TEXT, icon_url=FOOTER_ICON)

    vouch_channel = bot.get_channel(VOUCH_CHANNEL_ID)
    if vouch_channel:
        await vouch_channel.send(content=f"Vouch from {interaction.user.mention}", embed=embed)
        await interaction.response.send_message("Your vouch has been submitted. Thank you!", ephemeral=True)
    else:
        await interaction.response.send_message("Error: Vouch channel not found.", ephemeral=True)

# --------------------------
# On Ready
# --------------------------
@bot.event
async def on_ready():
    print(f"Notifier Bot logged in as {bot.user}")
    await bot.change_presence(activity=discord.Streaming(
        name="discord.gg/supernova",
        url="https://www.twitch.tv/qirixn"
    ))

    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(f"Error syncing commands: {e}")

# --------------------------
# Keep Alive
# --------------------------
keep_alive()

# --------------------------
# Run Bot
# --------------------------
bot.run(os.getenv("DISCORD_TOKEN"))
