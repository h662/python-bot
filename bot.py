import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from scheduler import setup_scheduler
from quiz import QuizCog

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
    CHANNEL_ID = 1369635004597928000
    setup_scheduler(bot, CHANNEL_ID)

@bot.command(name="ping")
async def ping(ctx):
    await ctx.send("Pong!")

async def setup_hook():
    await bot.add_cog(QuizCog(bot))
    print("✅ QuizCog successfully loaded")

bot.setup_hook = setup_hook

bot.run(TOKEN)