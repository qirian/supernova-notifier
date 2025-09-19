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
    return "Verification Bot läuft!", 200

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
WELCOME_CHANNEL_ID = 1418440616131428482
ROLE_ADD_ID = 1401757969137406004
ROLE_REMOVE_ID = 1401763417357815848
AUTHOR_ICON = "https://images-ext-1.discordapp.net/external/ORAM7L-2USvIhk9TKRteJkF9JyLXFa0RNBvrfual4E0/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/1401488134457524244/067dd861b8a4de1438d12c7bc283d935.webp?width=848&height=848"

# ------------------------
# Create Verification Embed
# ------------------------
def create_verification_embed():
    embed = discord.Embed(
        title="**Here you find our Verification**",
        description="Just click on the Button below and get a Member.",
        color=0x8f1eae
    )
    embed.set_author(name="Supernova x Verification", icon_url=AUTHOR_ICON)
    embed.set_footer(text="© 2022–2024 Superbova. All Rights Reserved.", icon_url=AUTHOR_ICON)
    return embed

# ------------------------
# Verification Button
# ------------------------
class VerificationButton(View):
    def __init__(self):
        super().__init__(timeout=None)
        button = Button(label="Verify Here", url="https://your-verification-link.com")
        self.add_item(button)

# ------------------------
# Events
# ------------------------
@bot.event
async def on_ready():
    print(f"✅ Verification Bot eingeloggt als {bot.user}")
    activity = discord.Streaming(name="Verification Bot Online", url="https://www.twitch.tv/qirixn")
    await bot.change_presence(status=discord.Status.online, activity=activity)

    # Send Verification Embed once on bot start
    guild = bot.get_guild(GUILD_ID)
    if guild:
        channel = bot.get_channel(WELCOME_CHANNEL_ID)
        if channel:
            embed = create_verification_embed()
            view = VerificationButton()
            await channel.send(embed=embed, view=view)

# ------------------------
# Role Management Command (Optional)
# ------------------------
# Hier kann der Bot die Rolle automatisch geben, wenn der User die Verification abgeschlossen hat
# Zum Beispiel über ein Command:
@bot.command()
async def verify(ctx, member: discord.Member):
    guild = ctx.guild
    role_add = guild.get_role(ROLE_ADD_ID)
    role_remove = guild.get_role(ROLE_REMOVE_ID)
    if role_add and role_remove:
        await member.add_roles(role_add)
        await member.remove_roles(role_remove)
        await ctx.send(f"{member.mention} has been verified!")

# ------------------------
# Run Bot
# ------------------------
bot.run(os.getenv("DISCORD_TOKEN"))
