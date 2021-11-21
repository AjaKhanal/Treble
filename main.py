import discord
from discord.ext import commands
from datetime import datetime
from constants import TOKEN
import music

client = commands.Bot(command_prefix='-', intents=discord.Intents.all())
cogs = [music]

for i in range(len(cogs)):
    cogs[i].setup(client)


@client.event
async def on_ready():
    print('We have logged in as {0.user} '.format(client))


@client.command()
async def ping(message):
    await message.send(f'{round(client.latency * 1000)} ms')
    music.log_command(message, 'ping')


client.run(TOKEN)
