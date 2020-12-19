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
    print(f'New member joined {member.guild}: {member.name}\n')
    channel = channel = discord.utils.get(member.guild.channels, name="greetings")
    channel_id = channel.id
    await channel.send(f'{member.name} just joined the server! Welcome!')

@client.event
async def on_member_remove(member):
    print(f'Member left {member.guild}: {member.name}\n')
    channel = channel = discord.utils.get(member.guild.channels, name="greetings")
    channel_id = channel.id
    await channel.send(f'{member.name} just left the server. Hope to see you back soon!')

client.run(token)
