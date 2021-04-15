#Import discord libraries

import discord
from discord.ext import commands
from discord.utils import get
from economy import Economy

#Import cogs

from sql import SQLite
from shop import Shop
from embed_format import Embed
from poll import Poll

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
    print("I'm connected to: ")
    for x in bot.guilds:
        print (x.name) # Return each name of servers where the bot is connected
        print('')
    await bot.change_presence(activity = discord.Activity(type=discord.ActivityType.watching, name="100% lucha")) # Uncomment to get a "Watching..." status with name value as description

@bot.event
async def on_message(ctx):
    await bot.wait_until_ready()
    
    if ctx.author == bot.user:
        return
    else:
        print(ctx.author, ': ', ctx.content, ' | ', ctx.author.guild, ' | ', ctx.created_at) # Just to have control of incoming messages on console

    await bot.process_commands(ctx)

#Defining cogs and running the bot
bot.add_cog(Shop(bot))
bot.add_cog(SQLite(bot))
bot.add_cog(Economy(bot))
bot.add_cog(Embed(bot))
bot.add_cog(Poll(bot))

#Running the bot
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


