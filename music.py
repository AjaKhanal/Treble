import discord
from discord.ext import commands
import youtube_dl
from datetime import datetime

ERROR = "There is no music playing"
NO_CHANNEL = ["You are not in a voice channel. Please join one and try again. :sunglasses:", "join - not in channel"]


class music(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def join(self, ctx):
        try:
            voice_channel = ctx.author.voice.channel

            if ctx.voice_client is None:
                await voice_channel.connect()
            else:
                await ctx.voice_client.move_to(voice_channel)
            msg = f'Joined {voice_channel}'
            await ctx.send(msg)
            log_command(ctx, msg)

        except:
            await ctx.send(NO_CHANNEL[0])
            log_command(ctx, NO_CHANNEL[1])

    @commands.command(aliases=['dc', 'leave'])
    async def disconnect(self, ctx):
        await ctx.voice_client.disconnect()
        log_command(ctx, "disconnect")

    @commands.command()
    async def play(self, ctx, url):
        try:
            if ctx.voice_client is None:
                voice_channel = ctx.author.voice.channel
                await voice_channel.connect()
                log_command(ctx, f'Joined {voice_channel}')

            ctx.voice_client.stop()
            FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                              'options': '-vn'}
            YDL_OPTIONS = {'format': 'bestaudio'}
            vc = ctx.voice_client

            log_command(ctx, "playing " + url)
            await ctx.send("Playing music")

            with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(url, download=False)
                url2 = info['formats'][0]['url']
                source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
                vc.play(source)

        except:
            await ctx.send(NO_CHANNEL[0])
            log_command(ctx, NO_CHANNEL[1])

    @commands.command()
    async def pause(self, ctx):
        if ctx.voice_client is None:
            await ctx.send(ERROR)
            log_command(ctx, "pause - " + ERROR)
        else:
            await ctx.send("Paused")
            ctx.voice_client.pause()
            log_command(ctx, "pause")

    @commands.command()
    async def resume(self, ctx):
        if ctx.voice_client is None:
            await ctx.send(ERROR)
            log_command(ctx, "resume - " + ERROR)
        else:
            await ctx.send("Resuming")
            ctx.voice_client.resume()
            log_command(ctx, "resume")

    @commands.command()
    async def stop(self, ctx):
        if ctx.voice_client is None:
            await ctx.send(ERROR)
            log_command(ctx, "stop - " + ERROR)
        else:
            await ctx.send("Stopped")
            ctx.voice_client.stop()
            log_command(ctx, "stop")


def setup(client):
    client.add_cog(music(client))


def log_command(ctx, command):
    print(f'[{datetime.now()}]: Command: {command}, User: {ctx.author.name}')

