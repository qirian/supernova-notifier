import os
import discord
from discord.ext import commands
from discord.ui import Button, View
from flask import Flask
from threading import Thread

# ------------------------
# Keep-Alive Setup
# ------------------------
app = Flask('')

@app.route('/')
def home():
    return "Whitelist Bot läuft!", 200

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    Thread(target=run).start()

keep_alive()

# ------------------------
# Discord Bot Setup
# ------------------------
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

# ------------------------
# IDs & Config
# ------------------------
GUILD_ID = 1401492898293481505
WHITELIST_CHANNEL_ID = 1418451615337152602
ROLE_ADD_ID = 1401757969137406004   # Member-Role
ROLE_REMOVE_ID = 1401763417357815848  # Pre-Whitelist Role
AUTHOR_ICON = "https://images-ext-1.discordapp.net/external/ORAM7L-2USvIhk9TKRteJkF9JyLXFa0RNBvrfual4E0/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/1401488134457524244/067dd861b8a4de1438d12c7bc283d935.webp?width=848&height=848"

# ------------------------
# Create Whitelist Embed
# ------------------------
def create_whitelist_embed():
    embed = discord.Embed(
        title="**Here you find our Whitelist**",
        description="Just click on the button below to get one of us.",
        color=0x8f1eae
    )
    embed.set_author(name="Supernova x Whitelist", icon_url=AUTHOR_ICON)
    embed.set_footer(text="© 2022–2024 Superbova. All Rights Reserved.", icon_url=AUTHOR_ICON)
    return embed

# ------------------------
# Whitelist Button
# ------------------------
class WhitelistButton(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="✅ Whitelist Me", style=discord.ButtonStyle.success, custom_id="whitelist_btn")
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
            f"🎉 {member.mention}, you are now whitelisted!",
            ephemeral=True
        )

# ------------------------
# Events
# ------------------------
@bot.event
async def on_ready():
    print(f"✅ Whitelist Bot eingeloggt als {bot.user}")
    activity = discord.Streaming(name="Whitelist Bot Online", url="https://www.twitch.tv/qirixn")
    await bot.change_presence(status=discord.Status.online, activity=activity)

    # Send Whitelist Embed once on bot start
    guild = bot.get_guild(GUILD_ID)
    if guild:
        channel = bot.get_channel(WHITELIST_CHANNEL_ID)
        if channel:
            embed = create_whitelist_embed()
            view = WhitelistButton()
            await channel.send(embed=embed, view=view)

# ------------------------
# Run Bot
# ------------------------
bot.run(os.getenv("DISCORD_TOKEN"))
