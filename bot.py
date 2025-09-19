import os
import discord
from discord.ext import commands
from discord.ui import View, Button
from flask import Flask
from threading import Thread

# ------------------------
# Keep-Alive Setup
# ------------------------
app = Flask('')

@app.route('/')
def home():
    return "Bot läuft!", 200

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

keep_alive()

# ------------------------
# Discord Bot Setup
# ------------------------
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

# ------------------------
# IDs
# ------------------------
WHITELIST_CHANNEL_ID = 1418451615337152602
ROLE_ADD_ID = 1401757969137406004   # Whitelist Rolle
ROLE_REMOVE_ID = 1401763417357815848 # Entfernte Rolle

# ------------------------
# Button View
# ------------------------
class WhitelistButton(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="🌐 Open Whitelist",
        style=discord.ButtonStyle.primary,
        custom_id="whitelist_btn"
    )
    async def whitelist(self, interaction: discord.Interaction, button: Button):
        guild = interaction.guild
        member = interaction.user
        role_add = guild.get_role(ROLE_ADD_ID)
        role_remove = guild.get_role(ROLE_REMOVE_ID)

        if role_add:
            await member.add_roles(role_add)
        if role_remove:
            await member.remove_roles(role_remove)

        await interaction.response.send_message(
            f"✅ {member.mention}, you are now whitelisted!",
            ephemeral=True
        )

# ------------------------
# Events
# ------------------------
@bot.event
async def on_ready():
    print(f"✅ Eingeloggt als {bot.user}")

    # Streaming Status
    activity = discord.Streaming(
        name="discord.gg/supernova",
        url="https://www.twitch.tv/qirixn"
    )
    await bot.change_presence(status=discord.Status.online, activity=activity)
    print("🎬 Streaming Status gesetzt!")

    # Embed nur einmal senden
    channel = bot.get_channel(WHITELIST_CHANNEL_ID)
    if channel:
        async for message in channel.history(limit=50):
            if message.author == bot.user:
                break
        else:
            embed = discord.Embed(
                title="**Here you find our Whitelist**",
                description="Just click on the button below to get one of us.",
                color=0x8f1eae
            )
            embed.set_author(
                name="Supernova x Whitelist",
                icon_url="https://images-ext-1.discordapp.net/external/ORAM7L-2USvIhk9TKRteJkF9JyLXFa0RNBvrfual4E0/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/1401488134457524244/067dd861b8a4de1438d12c7bc283d935.webp?width=848&height=848"
            )
            embed.set_footer(
                text="© 2022–2024 Superbova. All Rights Reserved.",
                icon_url="https://images-ext-1.discordapp.net/external/ORAM7L-2USvIhk9TKRteJkF9JyLXFa0RNBvrfual4E0/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/1401488134457524244/067dd861b8a4de1438d12c7bc283d935.webp?width=848&height=848"
            )
            await channel.send(embed=embed, view=WhitelistButton())

# ------------------------
# Start Bot
# ------------------------
bot.run(os.getenv("DISCORD_TOKEN"))
