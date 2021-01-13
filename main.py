"""
PythonDiscordBot - A general-purpose Discord bot made with Python/Discord.py
Copyright (C) 2020 Kosmas Raptis

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""

# bot.py
import os
import discord
from datetime import date, time, datetime
from dotenv import load_dotenv
from discord.ext import commands
import pyttsx3

load_dotenv()
token = os.getenv('DISCORD_TOKEN') # Get the bot's Discord token from our .env file

intents = discord.Intents.all() # Enable all intents (members list, presence info etc.)
bot = commands.Bot(command_prefix='kel', intents=intents) # Initialize bot with all intents (permissions)

#configure text-to-speech
engine = pyttsx3.init()

def speak(text):
    engine.setProperty("rate", 150)
    engine.say(text)
    engine.runAndWait()
    filePath = './sound.mp3'
    engine.save_to_file(text, filePath)
    engine.runAndWait()
    return os.path.abspath(filePath)

@bot.event
async def on_ready(): # This is called when a connection to Discord is achieved
    today = date.today() # Get what day it currently is. Needed because bot is meant to run for multiple days in 1 run.
    logmsg= f'{bot.user} has connected to Discord! ' + 'at ' + datetime.now().strftime("%d-%m-%Y-%X") + '\n' # Use a string that we log and print to the terminal
    logfile = open("logs-" + (today.strftime("%d-%m-%Y")) + ".txt", "a+") # Open today's logfile in append mode, create if it doesn't exist
    print(logmsg) # Print our log message
    logfile.write(logmsg) # Write the log message to the logfile
    logmsg= f'{bot.user} is connected to the following servers (guilds):\n'
    print(logmsg)
    logfile.write(logmsg)
    for guild in bot.guilds: # For every server (guild) the bot is connected to, print and log the members in it
        logmsg= f'{guild.name} (ID: {guild.id})\n'
        print(logmsg)
        logfile.write(logmsg)
        members = '\n - '.join([member.name for member in guild.members]) # loop over all of a server's members
        logmsg= f'Members of the server:\n - {members}\n'
        print(logmsg)
        logfile.write(logmsg)
    logfile.close()

@bot.event
async def on_member_join(member): # This is called when a new member joins
    today = date.today()
    logmsg= f'New member joined {member.guild}: {member.name} ' + 'at ' + datetime.now().strftime("%d-%m-%Y-%X") + '\n'
    logfile = open("logs-" + member.guild.name + (today.strftime("%d-%m-%Y")) + ".txt", "a+")
    print(logmsg)
    logfile.write(logmsg)
    logfile.close()
    channel = discord.utils.get(member.guild.channels, name="greetings") # Get info for the channel called "greetings" TODO: Be able to change channel
    await channel.send(f'{member.name} just joined the server! Welcome!') # Send message

@bot.event
async def on_member_remove(member): # This is called when a member leaves for any reason (self leave, ban, etc.)
    today = date.today()
    logmsg= f'Member left {member.guild}: {member.name}\n ' + 'at ' + datetime.now().strftime("%d-%m-%Y-%X") + '\n'
    logfile = open("logs-" + member.guild.name + (today.strftime("%d-%m-%Y")) + ".txt", "a+")
    print(logmsg)
    logfile.write(logmsg)
    logfile.close()
    channel = discord.utils.get(member.guild.channels, name="greetings")
    channel_id = channel.id
    await channel.send(f'{member.name} just left the server. Hope to see you back soon!')

@bot.event
async def on_message(message): # This is called when a message is sent
    message.content = message.content.lower()
    if message.author == bot.user:
        return
    if message.content.startswith('happy birthday'):
        await message.channel.send('Happy Birthday!')
    await bot.process_commands(message) # Wait for the bot to process all commands before exiting, required to handle commands with this event

@bot.command(name='hey')
async def hey(ctx): # Called when the hey command is used
    today = date.today()
    guild = ctx.guild # ctx = Context, holds info about the message that called the command, like server, message sender etc.
    logmsg= f'command hey was called ' + 'at ' + datetime.now().strftime("%d-%m-%Y-%X") + '\n'
    logfile = open("logs-" + guild.name + (today.strftime("%d-%m-%Y")) + ".txt", "a+")
    print(logmsg)
    logfile.write(logmsg)
    logfile.close()
    await ctx.send(f'Hello, {ctx.author.mention}! Nice to see you here!') # Wait for the message to be sent to the guild the Context is in

@bot.command(name='goodnight')
async def goodnight(ctx): # Called when the goodnight command is used
    today = date.today()
    guild = ctx.guild
    logmsg= f'command goodnight was called ' + 'at ' + datetime.now().strftime("%d-%m-%Y-%X") + '\n'
    logfile = open("logs-" + guild.name + (today.strftime("%d-%m-%Y")) + ".txt", "a+")
    print(logmsg)
    logfile.write(logmsg)
    logfile.close()
    await ctx.send(f'Goodnight, {ctx.author.mention}')

@bot.command()
async def tts(text, name = "tts"): # Called when the tts command is used
    today = date.today()
    guild = ctx.guild # ctx = Context, holds info about the message that called the command, like server, message sender etc.
    logmsg= f'command tts was called ' + 'at ' + datetime.now().strftime("%d-%m-%Y-%X") + '\n'
    logfile = open("logs-" + guild.name + (today.strftime("%d-%m-%Y")) + ".txt", "a+")
    print(logmsg)
    logfile.write(logmsg)
    logfile.close()

    channel = ctx.author.voice.channel
    await channel.connect()
    
    if not text:
        # We have nothing to speak
        await ctx.send(f"Hey {ctx.author.mention}, I need to know what to say please.")
        return

    vc = ctx.voice_client # We use it more then once, so make it an easy variable
    if not vc:
        # We are not currently in a voice channel
        await ctx.send("I need to be in a voice channel to do this, please use the connect command.")
        return

    try:
        vc.play(discord.FFmpegPCMAudio(speak(text)))

        # set the volume to 1
        vc.source = discord.PCMVolumeTransformer(vc.source)
        vc.source.volume = 1

    # Handle the exceptions that can occur
    except ClientException as e:
        await ctx.send(f"A client exception occured:\n`{e}`")
    except TypeError as e:
        await ctx.send(f"TypeError exception:\n`{e}`")
    except OpusNotLoaded as e:
        await ctx.send(f"OpusNotLoaded exception: \n`{e}`")

@bot.event
async def on_command_error(event, *args, **kwargs): # Called when there's an error in the last command that was used (like command not found)
    today = date.today()
    with open("logs-" + (event.guild.name) + (today.strftime("%d-%m-%Y")) + ".txt", "a+") as f:
        logmsg= f'Unhandled command: {args[0]} ' + 'at ' + datetime.now().strftime("%d-%m-%Y-%X") + '\n'
        print(logmsg)
        f.write(logmsg)
        await event.send(f'There was an error processing this command') # The event can be used like a Context

@bot.event
async def on_guild_join(guild): # Called when the bot joins a server
    today = date.today()
    logmsg = f'Joined guild {guild.name} ' + 'at ' + datetime.now().strftime("%d-%m-%Y-%X") + '\n'
    logfile = open("logs-" + (today.strftime("%d-%m-%Y")) + ".txt", "a+")
    print(logmsg)
    logfile.write(logmsg)
    logfile.close()
    channel = discord.utils.get(guild.channels, name="greetings")
    channel_id = channel.id
    await channel.send(f'''Hey, it\'s *me*, ***Goku!***- er, I mean, hello!
I'm kel! I am a general-purpose Discord bot, here to try and make your server better.
To see the list of my commands, type kelhelp''')


@bot.command(name='bam')
async def bam(ctx, user: discord.User, *, reason='God knows what'):
    today = date.today()
    guild = ctx.guild
    logmsg = f'command bam was called ' + 'at ' + datetime.now().strftime("%d-%m-%Y-%X") + '\n'
    logfile = open("logs-" + guild.name + (today.strftime("%d-%m-%Y")) + ".txt", "a+")
    logfile.write(logmsg)
    logfile.close()
    print(logmsg)
    await ctx.channel.send(f'{user.mention} just got bammed for {reason}!')

@bot.command(name='fr')
async def fr(ctx, *, arg):
    today = date.today()
    guild = ctx.guild
    logmsg= f'New feature request in ' + guild.name + ' at ' + datetime.now().strftime("%d-%m-%Y-%X") + ': \n' + arg + '\n'
    logfile = open("features-" + guild.name + (today.strftime("%d-%m-%Y")) + ".txt", "a+")
    logfile.write(logmsg)
    logfile.close()
    print(logmsg)
    await ctx.channel.send(f'{ctx.author.mention}, your request has been logged succesfully.')

bot.run(token)
