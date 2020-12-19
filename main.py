# bot.py
import os
import discord
from datetime import date, time, datetime
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('DISCORD_TOKEN') # Get the bot's Discord token from our .env file

intents = discord.Intents.all() # Enable all intents (members list, presence info etc.)
client = discord.Client(intents=intents) # Initialize client with all intents

today = date.today()

@client.event
async def on_ready(): # This is called when a connection to Discord is achieved
    msg = f'{client.user} has connected to Discord! ' + 'at ' + datetime.now().strftime("%d-%m-%Y-%X") + '\n'
    logfile = open("logs-" + (today.strftime("%d-%m-%Y")) + ".txt", "a+")
    print(msg)
    logfile.write(msg)
    msg = f'{client.user} is connected to the following servers (guilds):\n'
    print(msg)
    logfile.write(msg)
    for guild in client.guilds: # For every server (guild) the bot is connected to, list the members in it
        msg = f'{guild.name} (ID: {guild.id})\n'
        print(msg)
        logfile.write(msg)
        members = '\n - '.join([member.name for member in guild.members])
        msg = f'Members of the server:\n - {members}\n'
        print(msg)
        logfile.write(msg)
    logfile.close()

@client.event
async def on_member_join(member): # This is called when a new member joins
    msg = f'New member joined {member.guild}: {member.name} ' + 'at ' + datetime.now().strftime("%d-%m-%Y-%X") + '\n'
    logfile = open("logs-" + (today.strftime("%d-%m-%Y")) + ".txt", "a+")
    print(msg)
    logfile.write(msg)
    logfile.close()
    channel = discord.utils.get(member.guild.channels, name="greetings") # Get info for the channel called "greetings" TODO: Be able to change channel
    channel_id = channel.id
    await channel.send(f'{member.name} just joined the server! Welcome!') # Send message

@client.event
async def on_member_remove(member): # This is called when a member leaves for any reason (self leave, ban, etc.)
    msg = f'Member left {member.guild}: {member.name}\n ' + 'at ' + datetime.now().strftime("%d-%m-%Y-%X") + '\n'
    logfile = open("logs-" + (today.strftime("%d-%m-%Y")) + ".txt", "a+")
    print(msg)
    logfile.write(msg)
    logfile.close()
    channel = discord.utils.get(member.guild.channels, name="greetings")
    channel_id = channel.id
    await channel.send(f'{member.name} just left the server. Hope to see you back soon!')

@client.event
async def on_message(message):
    message.content = message.content.lower()
    if message.author == client.user:
        return
    if message.content.startswith('happy birthday'):
        await message.channel.send('Happy Birthday!')


client.run(token)
