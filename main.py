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
import requests
from youtube_dl import YoutubeDL as YouTubeDL

load_dotenv()
token = os.getenv('DISCORD_TOKEN') # Get the bot's Discord token from our .env file

intents = discord.Intents.all() # Enable all intents (members list, presence info etc.)
bot = commands.Bot(command_prefix='kel', intents=intents) # Initialize bot with all intents (permissions)

#configure text-to-speech
engine = pyttsx3.init()

class Misc(commands.Cog):

    def speak(self, text):
        engine.setProperty("rate", 150)
        engine.say(text)
        engine.runAndWait()
        filePath = './sound.mp3'
        engine.save_to_file(text, filePath)
        engine.runAndWait()
        return os.path.abspath(filePath)

    @commands.command(name='hey')
    async def hey(self, ctx):  # Called when the hey command is used
        today = date.today()
        self.guild = ctx.guild  # ctx = Context, holds info about the message that called the command, like server, message sender etc.
        logmsg = f'command hey was called ' + 'at ' + datetime.now().strftime("%d-%m-%Y-%X") + '\n'
        logfile = open("logs-" + guild.name + (today.strftime("%d-%m-%Y")) + ".txt", "a+")
        print(logmsg)
        logfile.write(logmsg)
        logfile.close()
        await ctx.send(
            f'Hello, {ctx.author.mention}! Nice to see you here!')  # Wait for the message to be sent to the guild the Context is in

    @commands.command(name='goodnight')
    async def goodnight(self, ctx):  # Called when the goodnight command is used
        today = date.today()
        self.guild = ctx.guild
        logmsg = f'command goodnight was called ' + 'at ' + datetime.now().strftime("%d-%m-%Y-%X") + '\n'
        logfile = open("logs-" + guild.name + (today.strftime("%d-%m-%Y")) + ".txt", "a+")
        print(logmsg)
        logfile.write(logmsg)
        logfile.close()
        await ctx.send(f'Goodnight, {ctx.author.mention}')

    def is_connected(self, ctx):
        voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
        return voice_client and voice_client.is_connected()

    @commands.command(name='tts')
    async def tts(self, ctx, *, arg):  # Called when the tts command is used
        today = date.today()
        self.guild = ctx.guild  # ctx = Context, holds info about the message that called the command, like server, message sender etc.
        logmsg = f'command tts was called ' + 'at ' + datetime.now().strftime("%d-%m-%Y-%X") + '\n'
        logfile = open("logs-" + ctx.guild.name + (today.strftime("%d-%m-%Y")) + ".txt", "a+")
        print(logmsg)
        logfile.write(logmsg)
        logfile.close()

        if not self.is_connected(ctx):
            channel = ctx.author.voice.channel
            await channel.connect()

        if not arg:
            # We have nothing to speak
            await ctx.send(f"Hey {ctx.author.mention}, I need to know what to say please.")
            return

        vc = ctx.voice_client  # We use it more then once, so make it an easy variable
        if not vc:
            # We are not currently in a voice channel
            await ctx.send("I need to be in a voice channel to do this, please use the connect command.")
            return

        try:
            vc.play(discord.FFmpegPCMAudio(self.speak(arg)))

            # set the volume to 1
            vc.source = discord.PCMVolumeTransformer(vc.source)
            vc.source.volume = 1

        # Handle the exceptions that can occur
        except discord.ClientException as e:
            await ctx.send(f"A client exception occured:\n`{e}`")
        except TypeError as e:
            await ctx.send(f"TypeError exception:\n`{e}`")
        except discord.opus.OpusNotLoaded as e:
            await ctx.send(f"OpusNotLoaded exception: \n`{e}`")

    @commands.command(name='bam')
    async def bam(self, ctx, user: discord.User, *, reason='God knows what'):
        today = date.today()
        self.guild = ctx.guild
        logmsg = f'command bam was called ' + 'at ' + datetime.now().strftime("%d-%m-%Y-%X") + '\n'
        logfile = open("logs-" + self.guild.name + (today.strftime("%d-%m-%Y")) + ".txt", "a+")
        logfile.write(logmsg)
        logfile.close()
        print(logmsg)
        await ctx.channel.send(f'{user.mention} just got bammed for {reason}!')

    @commands.command(name='bonk')
    async def bonk(self, ctx, user: discord.User, *, reason='no horni'):
        today = date.today()
        self.guild = ctx.guild
        logmsg = f'command bonk was called ' + 'at ' + datetime.now().strftime("%d-%m-%Y-%X") + '\n'
        logfile = open("logs-" + self.guild.name + (today.strftime("%d-%m-%Y")) + ".txt", "a+")
        logfile.write(logmsg)
        logfile.close()
        print(logmsg)
        await ctx.channel.send(f'{user.mention} just got bonked by {ctx.author.mention} for {reason}!')

    @commands.command(name='fr')
    async def fr(self, ctx, *, arg):
        today = date.today()
        self.guild = ctx.guild
        logmsg = f'New feature request in ' + self.guild.name + ' at ' + datetime.now().strftime(
            "%d-%m-%Y-%X") + ': \n' + arg + '\n'
        logfile = open("features-" + self.guild.name + (today.strftime("%d-%m-%Y")) + ".txt", "a+")
        logfile.write(logmsg)
        logfile.close()
        print(logmsg)
        await ctx.channel.send(f'{ctx.author.mention}, your request has been logged succesfully.')


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

class YouTube(commands.Cog):
    def search(self, arg):
        with YouTubeDL({'format': 'bestaudio', 'noplaylist': 'True'}) as ydl:
            try:
                requests.get(arg)
            except:
                info = ydl.extract_info(f"ytsearch:{arg}", download=False)['entries'][0]
            else:
                info = ydl.extract_info(arg, download=False)
        return (info, info['formats'][0]['url'])

    @commands.command(name='yt')
    async def yt(self, ctx, query):
        FFMPEG_OPTS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        video, source = self.search(query)
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)

        channel = ctx.author.voice.channel

        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()

        await ctx.send(f'Now playing {source["title"]}.')

        voice.play(discord.FFmpegPCMAudio(source, **FFMPEG_OPTS), after=lambda e: print('done', e))
        voice.is_playing()


bot.add_cog(Misc(bot))
bot.add_cog(YouTube(bot))
bot.run(token)
