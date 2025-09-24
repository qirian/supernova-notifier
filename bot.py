import discord
from discord.ext import commands
from discord import app_commands
import os
from keep_alive import keep_alive

# Intents
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# Channel IDs
VOUCH_CHANNEL_ID = 1418781950994550815

# Embed Style (wie beim Welcomer Bot)
EMBED_COLOR = 0x7b28a1
THUMBNAIL_URL = "https://cdn.discordapp.com/attachments/1401822345953546284/1418750912758943754/emvpuh1.gif"
IMAGE_URL     = "https://cdn.discordapp.com/banners/1402963593527431280/a_00aa2372c379edf2e6dbbccc1ad36c50.gif?size=1024&animated=true"
AUTHOR_ICON   = THUMBNAIL_URL
FOOTER_TEXT   = "© 2022–2024 Supernova | Hosted by Levin. All Rights Reserved."
FOOTER_ICON   = THUMBNAIL_URL

# -------------------------
# Events
# -------------------------
@bot.event
async def on_ready():
    print(f"Notifier Bot logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} slash command(s).")
    except Exception as e:
        print(f"Error syncing commands: {e}")

    # Streaming Presence
    await bot.change_presence(activity=discord.Streaming(
        name="discord.gg/supernovaeu",
        url="https://www.twitch.tv/qirixn"
    ))

# -------------------------
# Vouch Command
# -------------------------
@bot.tree.command(name="vouch", description="Leave a vouch with stars (1–5) and feedback")
@app_commands.describe(stars="Number of stars (1–5)", feedback="Your feedback about your purchase")
async def vouch(interaction: discord.Interaction, stars: int, feedback: str):
    if stars < 1 or stars > 5:
        await interaction.response.send_message("Please provide a star rating between 1 and 5.", ephemeral=True)
        return

    # Custom Star Emoji
    star_emoji = "<:Star:1419087858286727268>"
    stars_display = star_emoji * stars

    # Build Embed
    embed = discord.Embed(
        title="Vouch x Supernova | Hosted by Levin.",
        description=f"**Feedback:** {feedback}\n**Stars:** {stars_display}\n\nVouched by {interaction.user.mention}",
        color=EMBED_COLOR
    )
    embed.set_thumbnail(url=THUMBNAIL_URL)
    embed.set_image(url=IMAGE_URL)
    embed.set_author(name="Supernova x Notifier", icon_url=AUTHOR_ICON)
    embed.set_footer(text=FOOTER_TEXT, icon_url=FOOTER_ICON)

    # Send to Vouch Channel
    channel = interaction.guild.get_channel(VOUCH_CHANNEL_ID)
    if channel:
        await channel.send(embed=embed)
        await interaction.response.send_message("Your vouch has been submitted!", ephemeral=True)
    else:
        await interaction.response.send_message("Vouch channel not found.", ephemeral=True)

# -------------------------
# Keep Alive + Run
# -------------------------
keep_alive()
bot.run(os.getenv("DISCORD_TOKEN"))
