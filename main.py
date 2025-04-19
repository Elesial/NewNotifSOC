import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import asyncio
from datetime import datetime
import json

# Load environment variables
load_dotenv()

# Bot configuration
class BotConfig:
    def __init__(self):
        self.prefix = '!'
        self.owner_ids = []  # Add your Discord user ID here
        self.default_color = discord.Color.blue()
        self.version = "1.0.0"

# Initialize bot with configuration
config = BotConfig()
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=config.prefix, intents=intents, owner_ids=config.owner_ids)

# Load cogs
async def load_extensions():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    print(f'Bot is in {len(bot.guilds)} guilds')
    await bot.change_presence(activity=discord.Game(name=f"{config.prefix}help"))

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found. Use !help to see available commands.")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to use this command.")
    else:
        await ctx.send(f"An error occurred: {str(error)}")

# Basic commands
@bot.command(name='ping')
async def ping(ctx):
    latency = round(bot.latency * 1000)
    await ctx.send(f'Pong! Latency: {latency}ms')

@bot.command(name='info')
async def info(ctx):
    embed = discord.Embed(
        title="Bot Information",
        color=config.default_color,
        timestamp=datetime.utcnow()
    )
    embed.add_field(name="Version", value=config.version)
    embed.add_field(name="Guilds", value=len(bot.guilds))
    embed.add_field(name="Users", value=len(bot.users))
    embed.add_field(name="Commands", value=len(bot.commands))
    await ctx.send(embed=embed)

async def main():
    async with bot:
        await load_extensions()
        await bot.start(os.getenv('DISCORD_TOKEN'))

if __name__ == "__main__":
    asyncio.run(main()) 