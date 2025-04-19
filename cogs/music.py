import discord
from discord.ext import commands
import asyncio
import youtube_dl
from youtube_dl import YoutubeDL

# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilename': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        
        if 'entries' in data:
            data = data['entries'][0]
            
        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = []
        self.current = None

    @commands.command(name='join')
    async def join(self, ctx):
        """Joins a voice channel"""
        if ctx.author.voice is None:
            await ctx.send("You are not connected to a voice channel!")
            return

        channel = ctx.author.voice.channel
        if ctx.voice_client is not None:
            await ctx.voice_client.move_to(channel)
        else:
            await channel.connect()

    @commands.command(name='play')
    async def play(self, ctx, *, url):
        """Plays from a url (almost anything youtube_dl supports)"""
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel!")
                return

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            self.queue.append(player)
            
            if not ctx.voice_client.is_playing():
                await self.play_next(ctx)
            else:
                await ctx.send(f'Added to queue: {player.title}')

    async def play_next(self, ctx):
        if self.queue:
            self.current = self.queue.pop(0)
            ctx.voice_client.play(self.current, after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(ctx), self.bot.loop))
            await ctx.send(f'Now playing: {self.current.title}')

    @commands.command(name='stop')
    async def stop(self, ctx):
        """Stops and disconnects the bot from voice"""
        if ctx.voice_client is None:
            await ctx.send("I'm not playing anything!")
            return

        self.queue.clear()
        ctx.voice_client.stop()
        await ctx.voice_client.disconnect()

    @commands.command(name='skip')
    async def skip(self, ctx):
        """Skip the current song"""
        if ctx.voice_client is None or not ctx.voice_client.is_playing():
            await ctx.send("I'm not playing anything!")
            return

        ctx.voice_client.stop()
        await ctx.send("Skipped the current song!")

    @commands.command(name='queue')
    async def show_queue(self, ctx):
        """Show the current queue"""
        if not self.queue:
            await ctx.send("The queue is empty!")
            return

        embed = discord.Embed(title="Music Queue", color=discord.Color.blue())
        for i, song in enumerate(self.queue, 1):
            embed.add_field(name=f"{i}.", value=song.title, inline=False)
        
        await ctx.send(embed=embed)

    @commands.command(name='pause')
    async def pause(self, ctx):
        """Pause the current song"""
        if ctx.voice_client is None or not ctx.voice_client.is_playing():
            await ctx.send("I'm not playing anything!")
            return

        ctx.voice_client.pause()
        await ctx.send("Paused!")

    @commands.command(name='resume')
    async def resume(self, ctx):
        """Resume the current song"""
        if ctx.voice_client is None or not ctx.voice_client.is_paused():
            await ctx.send("I'm not paused!")
            return

        ctx.voice_client.resume()
        await ctx.send("Resumed!")

async def setup(bot):
    await bot.add_cog(Music(bot)) 