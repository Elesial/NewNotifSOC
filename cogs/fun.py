import discord
from discord.ext import commands
import random
import aiohttp
import json

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='8ball')
    async def eight_ball(self, ctx, *, question):
        """Ask the magic 8-ball a question"""
        responses = [
            "It is certain.", "It is decidedly so.", "Without a doubt.",
            "Yes - definitely.", "You may rely on it.", "As I see it, yes.",
            "Most likely.", "Outlook good.", "Yes.", "Signs point to yes.",
            "Reply hazy, try again.", "Ask again later.", "Better not tell you now.",
            "Cannot predict now.", "Concentrate and ask again.", "Don't count on it.",
            "My reply is no.", "My sources say no.", "Outlook not so good.",
            "Very doubtful."
        ]
        embed = discord.Embed(
            title="🎱 Magic 8-Ball",
            description=f"Question: {question}\nAnswer: {random.choice(responses)}",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)

    @commands.command(name='meme')
    async def meme(self, ctx):
        """Get a random meme from Reddit"""
        async with aiohttp.ClientSession() as session:
            async with session.get('https://meme-api.com/gimme') as response:
                if response.status == 200:
                    data = await response.json()
                    embed = discord.Embed(
                        title=data['title'],
                        color=discord.Color.blue()
                    )
                    embed.set_image(url=data['url'])
                    await ctx.send(embed=embed)
                else:
                    await ctx.send("Couldn't fetch a meme. Try again later!")

    @commands.command(name='roll')
    async def roll(self, ctx, dice: str):
        """Roll dice in NdN format"""
        try:
            rolls, limit = map(int, dice.split('d'))
        except Exception:
            await ctx.send('Format has to be in NdN!')
            return

        if rolls > 25:
            await ctx.send('Too many dice! Maximum is 25.')
            return

        if limit > 100:
            await ctx.send('Dice sides too high! Maximum is 100.')
            return

        results = [random.randint(1, limit) for r in range(rolls)]
        total = sum(results)
        
        embed = discord.Embed(
            title="🎲 Dice Roll",
            description=f"Rolling {dice}...",
            color=discord.Color.blue()
        )
        embed.add_field(name="Results", value=', '.join(map(str, results)))
        embed.add_field(name="Total", value=str(total))
        await ctx.send(embed=embed)

    @commands.command(name='choose')
    async def choose(self, ctx, *choices: str):
        """Choose between multiple options"""
        if len(choices) < 2:
            await ctx.send("Please provide at least 2 choices!")
            return
        
        choice = random.choice(choices)
        embed = discord.Embed(
            title="🤔 Choice Maker",
            description=f"I choose: **{choice}**",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Fun(bot)) 