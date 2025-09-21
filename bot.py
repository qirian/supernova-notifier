import os
import discord
from discord.ext import commands
from discord import app_commands
from keep_alive import keep_alive

# -------------------------
# Konfiguration
# -------------------------
GUILD_ID = 1401492898293481505          # Test-Guild für sofortige Slash-Command Registrierung
VOUCH_CHANNEL_ID = 1418781950994550815  # Channel, in den Vouches gepostet werden sollen

# Embed Style (wie Welcomer)
EMBED_COLOR = 0x7b28a1
THUMBNAIL_URL = "https://cdn.discordapp.com/attachments/1401822345953546284/1418750912758943754/emvpuh1.gif"
IMAGE_URL     = "https://cdn.discordapp.com/banners/1402963593527431280/a_00aa2372c379edf2e6dbbccc1ad36c50.gif?size=1024&animated=true"
AUTHOR_ICON   = THUMBNAIL_URL
FOOTER_TEXT   = "© 2022–2024 Supernova | Hosted by Levin. All Rights Reserved."
FOOTER_ICON   = THUMBNAIL_URL

# -------------------------
# Bot Setup
# -------------------------
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# -------------------------
# Fehler-Handler für App-Commands
# -------------------------
@bot.event
async def on_app_command_error(interaction: discord.Interaction, error: Exception):
    print("App command error:", type(error).__name__, error)
    try:
        await interaction.response.send_message("An error occurred. The staff has been notified.", ephemeral=True)
    except Exception:
        pass

# -------------------------
# Slash Command /vouch
# -------------------------
@bot.tree.command(name="vouch", description="Leave a vouch with stars (1-5) and feedback.")
@app_commands.describe(
    stars="Number between 1 and 5",
    feedback="Your feedback about your purchase"
)
async def vouch(interaction: discord.Interaction, stars: int, feedback: str):
    # Validate stars
    if stars < 1 or stars > 5:
        await interaction.response.send_message("Invalid star rating! Please enter a number between 1 and 5.", ephemeral=True)
        return

    # Build embed (Feedback oben, Sterne unten, User mention im Embed)
    embed = discord.Embed(
        title="Vouch x Supernova | Hosted by Levin.",
        description=f"{interaction.user.mention}\n\n**Feedback:** {feedback}\n**Stars:** {'⭐' * stars}",
        color=EMBED_COLOR
    )
    embed.set_thumbnail(url=THUMBNAIL_URL)
    embed.set_image(url=IMAGE_URL)
    embed.set_author(name="Supernova x Notifier", icon_url=AUTHOR_ICON)
    embed.set_footer(text=FOOTER_TEXT, icon_url=FOOTER_ICON)

    # Send embed to Vouch Channel (nur einmal!)
    try:
        vouch_channel = bot.get_channel(VOUCH_CHANNEL_ID)
        if vouch_channel is None:
            vouch_channel = await bot.fetch_channel(VOUCH_CHANNEL_ID)

        await vouch_channel.send(embed=embed)  # Embed wird nur einmal gesendet
        await interaction.response.send_message("Your vouch has been submitted. Thank you!", ephemeral=True)
    except discord.Forbidden:
        await interaction.response.send_message("I don't have permission to post in the vouch channel.", ephemeral=True)
    except Exception as e:
        print("Failed to send vouch:", e)
        await interaction.response.send_message("Failed to submit vouch (see logs).", ephemeral=True)

# -------------------------
# On Ready & Sync
# -------------------------
@bot.event
async def on_ready():
    print(f"Notifier Bot logged in as {bot.user} (id={bot.user.id})")

    # Präsenz
    try:
        await bot.change_presence(activity=discord.Streaming(
            name="discord.gg/supernova",
            url="https://www.twitch.tv/qirixn"
        ))
    except Exception as e:
        print("Could not set presence:", e)

    # Guild-Sync für sofortige Slash-Commands
    try:
        guild_obj = discord.Object(id=GUILD_ID)
        synced = await bot.tree.sync(guild=guild_obj)
        print(f"Synced {len(synced)} command(s) to guild {GUILD_ID}.")
    except Exception as e:
        print("Guild sync failed, trying global sync:", e)
        try:
            synced = await bot.tree.sync()
            print(f"Globally synced {len(synced)} command(s).")
        except Exception as e2:
            print("Global sync failed:", e2)

# -------------------------
# Keep Alive + Run
# -------------------------
keep_alive()
bot.run(os.getenv("DISCORD_TOKEN"))
