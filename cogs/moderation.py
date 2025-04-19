import discord
from discord.ext import commands
from datetime import datetime, timedelta

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(kick_members=True)
    @commands.command(name='kick')
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        """Kick a member from the server"""
        if member.top_role >= ctx.author.top_role:
            await ctx.send("You can't kick someone with a higher or equal role!")
            return
        
        await member.kick(reason=reason)
        embed = discord.Embed(
            title="Member Kicked",
            description=f"{member.mention} has been kicked by {ctx.author.mention}",
            color=discord.Color.red(),
            timestamp=datetime.utcnow()
        )
        if reason:
            embed.add_field(name="Reason", value=reason)
        await ctx.send(embed=embed)

    @commands.has_permissions(ban_members=True)
    @commands.command(name='ban')
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        """Ban a member from the server"""
        if member.top_role >= ctx.author.top_role:
            await ctx.send("You can't ban someone with a higher or equal role!")
            return
        
        await member.ban(reason=reason)
        embed = discord.Embed(
            title="Member Banned",
            description=f"{member.mention} has been banned by {ctx.author.mention}",
            color=discord.Color.red(),
            timestamp=datetime.utcnow()
        )
        if reason:
            embed.add_field(name="Reason", value=reason)
        await ctx.send(embed=embed)

    @commands.has_permissions(manage_messages=True)
    @commands.command(name='clear')
    async def clear(self, ctx, amount: int):
        """Clear a specified number of messages"""
        if amount <= 0:
            await ctx.send("Please specify a positive number of messages to clear.")
            return
        
        await ctx.channel.purge(limit=amount + 1)
        msg = await ctx.send(f"Cleared {amount} messages!")
        await asyncio.sleep(3)
        await msg.delete()

    @commands.has_permissions(manage_roles=True)
    @commands.command(name='mute')
    async def mute(self, ctx, member: discord.Member, duration: int, *, reason=None):
        """Mute a member for a specified duration in minutes"""
        if member.top_role >= ctx.author.top_role:
            await ctx.send("You can't mute someone with a higher or equal role!")
            return
        
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not muted_role:
            muted_role = await ctx.guild.create_role(name="Muted")
            for channel in ctx.guild.channels:
                await channel.set_permissions(muted_role, speak=False, send_messages=False)
        
        await member.add_roles(muted_role)
        embed = discord.Embed(
            title="Member Muted",
            description=f"{member.mention} has been muted by {ctx.author.mention}",
            color=discord.Color.orange(),
            timestamp=datetime.utcnow()
        )
        embed.add_field(name="Duration", value=f"{duration} minutes")
        if reason:
            embed.add_field(name="Reason", value=reason)
        await ctx.send(embed=embed)
        
        await asyncio.sleep(duration * 60)
        await member.remove_roles(muted_role)

async def setup(bot):
    await bot.add_cog(Moderation(bot)) 