#Import discord libraries

import discord
from discord.ext import commands
from discord.utils import get

#Import cogs

from sql import SQL

# Setting a bot prefix


BOT_PREFIX = '$'
bot = commands.Bot(command_prefix=BOT_PREFIX)


#Open and read token, just for my own security, you can define TOKEN as a string and also works

token = open('token.txt', 'r')
TOKEN = token.readline()

# Bot events, you can also check a complete list of available events in the documentation: https://discordpy.readthedocs.io/en/latest/api.html#discord-api-events

@bot.event
async def on_ready():
    print('Bot ready')
    print('Logged on as {0}!'.format(bot.user))
    for x in bot.guilds:
        print (x.name) # Return each name of servers where the bot is connected
    await bot.change_presence(activity = discord.Game('Github test'))

@bot.event
async def on_message(ctx):
    await bot.wait_until_ready()
    
    if ctx.author == bot.user:
        return
    else:
        print(ctx.author, ': ', ctx.content, ' | ', ctx.author.guild) # Just to have control of incoming messages on console

#Defining cogs and running the bot
bot.add_cog(SQL(bot))
bot.run(TOKEN)

"""
 Disclaimer:
 You can set your commands only-usable for admins or other rols using:
    @bot.command()                  <- For Bot commands
    @commands.has_role('RoleName') 
 or:
    @commands.command()             <- For Cog commands
    @commands.has_role('RoleName')

"""


