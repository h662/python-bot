import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from scheduler import setup_scheduler

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")


intents = discord.Intents.default()
intents.message_content = True 
intents.members = True 

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")
    # 실제 채널 ID로 교체
    CHANNEL_ID = 1231937037532270657
    setup_scheduler(bot, CHANNEL_ID)

@bot.command(name="ping")
async def ping(ctx):
    await ctx.send("Pong!")

bot.run(TOKEN)