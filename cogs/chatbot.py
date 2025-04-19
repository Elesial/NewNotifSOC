import discord
from discord.ext import commands
import random
import json
import os

class ChatBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.prompt_file = 'data/chatbot_prompts.json'
        # Initialize default name before loading prompts
        self.name = "Discord Bot"  # Default name
        self.load_prompts()

    def load_prompts(self):
        """Load prompts from file or create default prompts"""
        os.makedirs('data', exist_ok=True)
        try:
            with open(self.prompt_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.responses = data.get('responses', self.get_default_responses())
                self.help_responses = data.get('help_responses', self.get_default_help_responses())
                self.personality = data.get('personality', "Saya adalah bot Discord yang ramah dan membantu.")
                # Only update name if it exists in the file
                if 'name' in data:
                    self.name = data['name']
        except FileNotFoundError:
            self.responses = self.get_default_responses()
            self.help_responses = self.get_default_help_responses()
            self.personality = "Saya adalah bot Discord yang ramah dan membantu."
            self.save_prompts()

    def save_prompts(self):
        """Save current prompts to file"""
        data = {
            'responses': self.responses,
            'help_responses': self.help_responses,
            'personality': self.personality,
            'name': self.name
        }
        with open(self.prompt_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def get_default_responses(self):
        return [
            "Halo! Ada yang bisa saya bantu?",
            "Hai! Saya siap membantu Anda!",
            "Halo! Saya adalah bot yang siap membantu!",
            "Hai! Ada yang bisa saya bantu hari ini?",
            "Halo! Saya di sini untuk membantu Anda!",
            "Hai! Saya adalah asisten Discord Anda!",
            "Halo! Ada yang bisa saya lakukan untuk Anda?",
            "Hai! Saya siap melayani Anda!",
            "Halo! Saya adalah bot yang ramah!",
            "Hai! Ada yang bisa saya bantu sekarang?"
        ]

    def get_default_help_responses(self):
        return [
            "Saya bisa membantu dengan berbagai hal! Coba ketik !help untuk melihat semua perintah yang tersedia.",
            "Saya memiliki banyak fitur! Gunakan !help untuk melihat daftar perintah.",
            "Saya bisa memainkan musik, memoderasi server, dan banyak lagi! Ketik !help untuk info lebih lanjut.",
            "Saya memiliki fitur musik, moderasi, dan hiburan! Coba !help untuk melihat semuanya.",
            "Saya siap membantu dengan musik, moderasi, dan hiburan! Gunakan !help untuk melihat semua perintah."
        ]

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if self.bot.user.mentioned_in(message):
            if any(word in message.content.lower() for word in ['help', 'bantuan', 'fitur', 'command', 'perintah']):
                response = random.choice(self.help_responses)
            else:
                response = random.choice(self.responses)
            
            embed = discord.Embed(
                description=response,
                color=discord.Color.blue()
            )
            embed.set_author(
                name=self.name,
                icon_url=self.bot.user.avatar.url if self.bot.user.avatar else None
            )
            await message.channel.send(embed=embed)

    @commands.command(name='setpersonality')
    @commands.is_owner()
    async def set_personality(self, ctx, *, personality):
        """Set the bot's personality (Owner only)"""
        self.personality = personality
        self.save_prompts()
        await ctx.send(f"Personality updated successfully!")

    @commands.command(name='setname')
    @commands.is_owner()
    async def set_name(self, ctx, *, name):
        """Set the bot's display name (Owner only)"""
        self.name = name
        self.save_prompts()
        await ctx.send(f"Display name updated successfully!")

    @commands.command(name='setresponse')
    @commands.is_owner()
    async def set_response(self, ctx, *, response):
        """Add a custom response (Owner only)"""
        self.responses.append(response)
        self.save_prompts()
        await ctx.send(f"Response added successfully! Total responses: {len(self.responses)}")

    @commands.command(name='sethelp')
    @commands.is_owner()
    async def set_help(self, ctx, *, response):
        """Add a custom help response (Owner only)"""
        self.help_responses.append(response)
        self.save_prompts()
        await ctx.send(f"Help response added successfully! Total help responses: {len(self.help_responses)}")

    @commands.command(name='removeresponse')
    @commands.is_owner()
    async def remove_response(self, ctx, index: int):
        """Remove a response by index (Owner only)"""
        if 0 <= index < len(self.responses):
            removed = self.responses.pop(index)
            self.save_prompts()
            await ctx.send(f"Response removed: {removed}")
        else:
            await ctx.send("Invalid index!")

    @commands.command(name='removehelp')
    @commands.is_owner()
    async def remove_help(self, ctx, index: int):
        """Remove a help response by index (Owner only)"""
        if 0 <= index < len(self.help_responses):
            removed = self.help_responses.pop(index)
            self.save_prompts()
            await ctx.send(f"Help response removed: {removed}")
        else:
            await ctx.send("Invalid index!")

    @commands.command(name='listresponses')
    @commands.is_owner()
    async def list_responses(self, ctx):
        """List all responses and settings (Owner only)"""
        embed = discord.Embed(
            title="Chatbot Settings",
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name="Personality",
            value=self.personality,
            inline=False
        )
        
        embed.add_field(
            name="Display Name",
            value=self.name,
            inline=False
        )
        
        embed.add_field(
            name="General Responses",
            value="\n".join(f"{i+1}. {response}" for i, response in enumerate(self.responses)),
            inline=False
        )
        
        embed.add_field(
            name="Help Responses",
            value="\n".join(f"{i+1}. {response}" for i, response in enumerate(self.help_responses)),
            inline=False
        )
        
        await ctx.send(embed=embed)

    @commands.command(name='resetprompts')
    @commands.is_owner()
    async def reset_prompts(self, ctx):
        """Reset all prompts to default (Owner only)"""
        self.responses = self.get_default_responses()
        self.help_responses = self.get_default_help_responses()
        self.personality = "Saya adalah bot Discord yang ramah dan membantu."
        self.name = "Discord Bot"
        self.save_prompts()
        await ctx.send("All prompts have been reset to default!")

async def setup(bot):
    await bot.add_cog(ChatBot(bot)) 