import os
import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import View, Button, Modal, TextInput
from keep_alive import keep_alive

# --------------------------
# Setup
# --------------------------
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# Channel IDs
VOUCH_CHANNEL_ID = 1418781950994550815

# Embed Style (same as Welcomer)
EMBED_COLOR = 0x7b28a1
THUMBNAIL_URL = "https://cdn.discordapp.com/attachments/1401822345953546284/1418750912758943754/emvpuh1.gif"
IMAGE_URL = "https://cdn.discordapp.com/banners/1402963593527431280/a_00aa2372c379edf2e6dbbccc1ad36c50.gif?size=1024&animated=true"
AUTHOR_ICON = "https://cdn.discordapp.com/attachments/1401822345953546284/1418750912758943754/emvpuh1.gif"
FOOTER_ICON = "https://cdn.discordapp.com/attachments/1401822345953546284/1418750912758943754/emvpuh1.gif"
FOOTER_TEXT = "© 2022–2024 Supernova | Hosted by Levin. All Rights Reserved."

# --------------------------
# Vouch Modal
# --------------------------
class VouchModal(Modal, title="⭐ Vouch Form"):
    stars = TextInput(label="Stars (1-5)", placeholder="Enter a number between 1 and 5", required=True, max_length=1)
    feedback = TextInput(label="Feedback", style=discord.TextStyle.paragraph, placeholder="Enter your feedback here...", required=True, max_length=500)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            stars_value = int(self.stars.value)
            if stars_value < 1 or stars_value > 5:
                await interaction.response.send_message("Invalid star rating! Please enter a number between 1 and 5.", ephemeral=True)
                return
        except ValueError:
            await interaction.response.send_message("Invalid input! Stars must be a number between 1 and 5.", ephemeral=True)
            return

        # Build Vouch Embed
        embed = discord.Embed(
            title="Vouch x Supernova | Hosted by Levin.",
            description=f"**Stars:** {'⭐' * stars_value}\n**Feedback:** {self.feedback.value}",
            color=EMBED_COLOR
        )
        embed.set_thumbnail(url=THUMBNAIL_URL)
        embed.set_image(url=IMAGE_URL)
        embed.set_author(name="Supernova x Welcomer", icon_url=AUTHOR_ICON)
        embed.set_footer(text=FOOTER_TEXT, icon_url=FOOTER_ICON)

        vouch_channel = bot.get_channel(VOUCH_CHANNEL_ID)
        if vouch_channel:
            await vouch_channel.send(content=f"Vouch from {interaction.user.mention}", embed=embed)
            await interaction.response.send_message("Thank you for your vouch!", ephemeral=True)
        else:
            await interaction.response.send_message("Error: Vouch channel not found.", ephemeral=True)

# --------------------------
# Vouch Button
# --------------------------
class VouchView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Button(label="⭐ Vouch", style=discord.ButtonStyle.primary, custom_id="vouch_button"))

    @discord.ui.button(label="⭐ Vouch", style=discord.ButtonStyle.primary, custom_id="vouch_button")
    async def vouch_button_callback(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_modal(VouchModal())

# --------------------------
# Command to send the Vouch Panel
# --------------------------
@bot.tree.command(name="sendvouch", description="Send the Vouch Panel")
async def sendvouch(interaction: discord.Interaction):
    embed = discord.Embed(
        title="Vouch x Supernova | Hosted by Levin.",
        description="After your Purchase you could give us your Feedback and let us know if it worked.",
        color=EMBED_COLOR
    )
    embed.set_thumbnail(url=THUMBNAIL_URL)
    embed.set_image(url=IMAGE_URL)
    embed.set_author(name="Supernova x Welcomer", icon_url=AUTHOR_ICON)
    embed.set_footer(text=FOOTER_TEXT, icon_url=FOOTER_ICON)

    await interaction.response.send_message(embed=embed, view=VouchView())

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
