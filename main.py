# bot.py
import os
import discord
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('DISCORD_TOKEN') # Get the bot's Discord token from our .env file

intents = discord.Intents.all() # Enable all intents (members list, presence info etc.)
client = discord.Client(intents=intents) # Initialize client with all intents

@client.event
async def on_ready(): # This is called when a connection to Discord is achieved
    print(f'{client.user} has connected to Discord!')
    print(f'{client.user} is connected to the following servers (guilds):')
    for guild in client.guilds: # For every server (guild) the bot is connected to, list the members in it
        print(f'{guild.name} (ID: {guild.id})')
        members = '\n - '.join([member.name for member in guild.members])
        print(f'Members of the server:\n - {members}')

@client.event
async def on_member_join(member): # This is called when a new member joins
    print(f'New member joined {member.guild}: {member.name}\n')
    channel = discord.utils.get(member.guild.channels, name="greetings") # Get info for the channel called "greetings" TODO: Be able to change channel
    channel_id = channel.id
    await channel.send(f'{member.name} just joined the server! Welcome!') # Send message

@client.event
async def on_member_remove(member): # This is called when a member leaves for any reason (self leave, ban, etc.)
    print(f'Member left {member.guild}: {member.name}\n')
    channel = channel = discord.utils.get(member.guild.channels, name="greetings")
    channel_id = channel.id
    await channel.send(f'{member.name} just left the server. Hope to see you back soon!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('happy birthday'):
        await message.channel.send('Happy Birthday!')


client.run(token)
