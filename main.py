# bot.py
import os
import discord
from datetime import date, time, datetime
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
token = os.getenv('DISCORD_TOKEN') # Get the bot's Discord token from our .env file

intents = discord.Intents.all() # Enable all intents (members list, presence info etc.)
bot = commands.Bot(command_prefix='kel', intents=intents) # Initialize bot with all intents

@bot.event
async def on_ready(): # This is called when a connection to Discord is achieved
    today = date.today()
    msg = f'{bot.user} has connected to Discord! ' + 'at ' + datetime.now().strftime("%d-%m-%Y-%X") + '\n'
    logfile = open("logs-" + (today.strftime("%d-%m-%Y")) + ".txt", "a+")
    print(msg)
    logfile.write(msg)
    msg = f'{bot.user} is connected to the following servers (guilds):\n'
    print(msg)
    logfile.write(msg)
    for guild in bot.guilds: # For every server (guild) the bot is connected to, list the members in it
        msg = f'{guild.name} (ID: {guild.id})\n'
        print(msg)
        logfile.write(msg)
        members = '\n - '.join([member.name for member in guild.members])
        msg = f'Members of the server:\n - {members}\n'
        print(msg)
        logfile.write(msg)
    logfile.close()

@bot.event
async def on_member_join(member): # This is called when a new member joins
    today = date.today()
    msg = f'New member joined {member.guild}: {member.name} ' + 'at ' + datetime.now().strftime("%d-%m-%Y-%X") + '\n'
    logfile = open("logs-" + member.guild.name + (today.strftime("%d-%m-%Y")) + ".txt", "a+")
    print(msg)
    logfile.write(msg)
    logfile.close()
    channel = discord.utils.get(member.guild.channels, name="greetings") # Get info for the channel called "greetings" TODO: Be able to change channel
    channel_id = channel.id
    await channel.send(f'{member.name} just joined the server! Welcome!') # Send message

@bot.event
async def on_member_remove(member): # This is called when a member leaves for any reason (self leave, ban, etc.)
    today = date.today()
    msg = f'Member left {member.guild}: {member.name}\n ' + 'at ' + datetime.now().strftime("%d-%m-%Y-%X") + '\n'
    logfile = open("logs-" + member.guild.name + (today.strftime("%d-%m-%Y")) + ".txt", "a+")
    print(msg)
    logfile.write(msg)
    logfile.close()
    channel = discord.utils.get(member.guild.channels, name="greetings")
    channel_id = channel.id
    await channel.send(f'{member.name} just left the server. Hope to see you back soon!')

@bot.event
async def on_message(message):
    message.content = message.content.lower()
    if message.author == bot.user:
        return
    if message.content.startswith('happy birthday'):
        await message.channel.send('Happy Birthday!')
    await bot.process_commands(message)

@bot.command(name='hey')
async def hey(ctx):
    today = date.today()
    guild = ctx.guild
    msg = f'command hey was called ' + 'at ' + datetime.now().strftime("%d-%m-%Y-%X") + '\n'
    logfile = open("logs-" + guild.name + (today.strftime("%d-%m-%Y")) + ".txt", "a+")
    print(msg)
    logfile.write(msg)
    logfile.close()
    await ctx.send(f'Hey, it\'s *me*, ***Goku!***')

@bot.command(name='goodnight')
async def goodnight(ctx):
    today = date.today()
    guild = ctx.guild
    msg = f'command goodnight was called ' + 'at ' + datetime.now().strftime("%d-%m-%Y-%X") + '\n'
    logfile = open("logs-" + guild.name + (today.strftime("%d-%m-%Y")) + ".txt", "a+")
    print(msg)
    logfile.write(msg)
    logfile.close()
    await ctx.send(f'Goodnight, {ctx.author.mention}')

@bot.event
async def on_command_error(event, *args, **kwargs):
    today = date.today()
    with open("logs-" + (today.strftime("%d-%m-%Y")) + ".txt", "a+") as f:
        msg = f'Unhandled command: {args[0]}\n'
        print(msg)
        f.write(msg)
        await event.send(f'This command isn\'t implemented yet')



bot.run(token)
