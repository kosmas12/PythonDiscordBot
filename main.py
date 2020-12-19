# bot.py
import os

import discord
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    print(f'{client.user} is connected to the following servers (guilds):')
    for guild in client.guilds:
        print(f'{guild.name} (ID: {guild.id})')
        members = '\n - '.join([member.name for member in guild.members])
        print(f'Members of the server:\n - {members}')

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f'Hello {member.name}! Welcome to the server!')

client.run(token)
