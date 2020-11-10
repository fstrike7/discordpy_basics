import sqlite3
import time
import os

from discord.ext import commands 

"""
Introduction:
Using the model "sql.py" we create a new Database to manage a user "wallet".
Note that I've eliminated the Server_ID and Server_Name to make the currency independent from each server, 
but you can easily add a Server identification to the SQL database and use it on each SQL.execute functions, 
to make the economy depent from the server who's calling the function.
"""

class Economy(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.author == self.bot.user:
            return
        
        DIR = os.path.dirname(__file__) # Defines a path for the database file
        db = sqlite3.connect(os.path.join(DIR, "Economy.db")) #Connect to the database
        SQL = db.cursor() # Cursor for the DB

        SQL.execute('create table if not exists Economy('
                    '"Num" integer not null primary key autoincrement, '
                    '"User_ID" integer, '
                    '"Server_ID" integer, '
                    ' "Currency" integer, '
                    ' "LastDaily" integer '
                    ')') # Here we create the table with each statement for the DB, a list with every data type can found in: https://www.sqlite.org/datatype3.html
    

        user_id = int(ctx.author.id)
        server_id = int(ctx.guild.id)
        
        SQL.execute(f'select User_ID from Economy where User_ID="{user_id}"')
        check = SQL.fetchone()

        if not check: # This "if" statement, check if the user exist in the database.
            SQL.execute('insert into Economy(User_ID, Server_ID, Currency) values(?,?,?)', (user_id, server_id, 10))
            db.commit()
            print ("Adding a new user to DB and giving $10 to start using the bot commands")


    @commands.command(pass_context=True, aliases=["currency", "money"]) # A simple command which check your actual currency
    async def wallet(self, ctx):
        
        DIR = os.path.dirname(__file__)
        db = sqlite3.connect(os.path.join(DIR, "Economy.db"))
        SQL = db.cursor()

        user_id = int(ctx.author.id)
        server_id = int(ctx.guild.id)

        SQL.execute(f'select Currency from Economy where User_ID="{user_id}" and Server_ID="{server_id}"')
        currency = SQL.fetchone()

        if not currency[0]:
            await ctx.channel.send("You don't have money, check the daily reward using $daily")
        else:
            await ctx.channel.send(f"Your actual currency is ${currency[0]}")

    def checkWallet(self, ctx, amount): # A function to check if "amount" value is higher than actual currency. Used in shop.py
        DIR = os.path.dirname(__file__)
        db = sqlite3.connect(os.path.join(DIR, "Economy.db"))
        SQL = db.cursor()

        user_id = int(ctx.author.id)
        server_id = int(ctx.guild.id)

        SQL.execute(f'select Currency from Economy where User_ID="{user_id}" and Server_ID="{server_id}"')
        currency = SQL.fetchone()

        if amount <= currency[0]: # If statement is True, then rest amount value from "Currency" and returns True,
            SQL.execute(f'update Economy set Currency = ? where User_ID="{user_id}" and Server_ID={server_id}', (currency[0] - amount,)) 
            db.commit()
            return True
        else:                      # otherwise just return False.
            return False


    @commands.command(pass_context=True, aliases=["reward"]) # Using the time module, we create a reward system which gift $10 each 24hs.
    async def daily(self, ctx):
        
        DIR = os.path.dirname(__file__)
        db = sqlite3.connect(os.path.join(DIR, "Economy.db"))
        SQL = db.cursor()

        timeNow = int(time.time()) # Returns seconds since epoch, more info at: https://docs.python.org/3/library/time.html

        a_day_in_seconds = 86400 # 24hs in seconds

        user_id = int(ctx.author.id)
        server_id = int(ctx.guild.id)
        

        SQL.execute(f'select LastDaily from Economy where User_ID="{user_id}" and Server_ID={server_id}')
        lastDaily = SQL.fetchone()
        print(f'Actual last daily from {ctx.author.name} is {lastDaily[0]}')

        if not lastDaily[0]: #Check if user have a "LastDaily" value in the database. If not:

            SQL.execute(f'select Currency from Economy where User_ID="{user_id}" and Server_ID={server_id}')
            db.commit()
            actualCurrency = SQL.fetchone() # Checking actual currency

            reward = (actualCurrency[0]+10) # Take the actual currency from wallet and add $10.

            SQL.execute(f'update Economy set LastDaily = ? where User_ID="{user_id}" and Server_ID="{server_id}"', (timeNow,)) # Assign a LastDaily value.
            db.commit()

            if not actualCurrency[0] or actualCurrency[0] == 0: # Check if user has money in wallet. If not:
                SQL.execute(f'insert into Economy(Currency) values(?) where User_ID="{user_id}" and Server_ID="{server_id}"', (10)) # Set currency to 10.
                db.commit()
            else:
                SQL.execute(f'update Economy set Currency = {reward} where User_ID ="{user_id}" and Server_ID="{server_id}"') # Otherwise, give actualCurrency + $10 (reward variable)
                db.commit()

            await ctx.channel.send(f'Gifted $10 to {ctx.author.name}, use it wisely.')
            return

        else:
            if ((timeNow-lastDaily[0]) >= a_day_in_seconds) : # If user has a lastDaily value, bot checks if more than 24 hours (in seconds) have passed since its last use.

                SQL.execute(f'select Currency from Economy where User_ID="{user_id}" and Server_ID="{server_id}"')
                db.commit()

                actualCurrency = SQL.fetchone() # Checking actual currency

                reward = (actualCurrency[0]+10)

                SQL.execute(f'update Economy set Currency = ? where User_ID="{user_id}" and Server_ID="{server_id}"', (reward,)) # Give user's reward
                db.commit()

                SQL.execute(f'update Economy set LastDaily = ? where User_ID="{user_id}" and Server_ID="{server_id}"', (timeNow,)) # Change user's lastDaily value
                db.commit()

                await ctx.channel.send(f'Gifted $10 to {ctx.author.name}, use it wisely.')
                return
            else:
                nextDaily = int( ((lastDaily[0] + a_day_in_seconds)-lastDaily[0]) / 60)
                await ctx.channel.send(f"You have to wait 24hours to get the daily reward, next daily reward in: {nextDaily} minutes.")
    
    @commands.command(pass_context=True, aliases=["give"])
    @commands.has_role('admin')
    async def addmoney(self, ctx, arg, arg2): # A command to give money to users, only-usable by admins, in this command we use an "arg" parameter, you can find more info about this in: https://discordpy.readthedocs.io/en/latest/ext/commands/commands.html 
        
        DIR = os.path.dirname(__file__)
        db = sqlite3.connect(os.path.join(DIR, "Economy.db"))
        SQL = db.cursor()
        
        server_id = int(ctx.guild.id)

        if isinstance(arg, int): # An if statement to check if users give us a @mention at first argument, if not, money goes to the author of the message.
            arg2 = arg
            arg = ctx.author.mention
        else:
            pass

        try: # A try statement to check if arg is a valid @mention type, to do this we...
            user_id = int(''.join(filter(str.isdigit, arg))) # take the "arg" parameter and, using a filter function, we only concatenate integers, so if we have something like "<!184824808310177732>" this function returns "184824808310177732".

        except ValueError:
            await ctx.channel.send('Invalid user mention')
            return

        SQL.execute(f'select Currency from Economy where User_ID="{user_id}" and Server_ID={server_id}')
        db.commit()
        actualCurrency = SQL.fetchone() # Returns a tuple where first position indicates actual money from user.

        arg2 = int(arg2) # Convert string to int

        try:                                        # A try statement to see if User had money, this actually works to avoid new users who doesn't has a Database entry
            addMoney = (actualCurrency[0]+arg2)
        except TypeError:
            SQL.execute(f'insert into Economy(Currency) values(?) where User_ID="{user_id}" and Server_ID={server_id}', (10)) # Gives the initial $10
            db.commit()
            addMoney = (actualCurrency[0]+arg2)


        
        SQL.execute(f'update Economy set Currency = ? where User_ID="{user_id}" and Server_ID={server_id}', (addMoney,))
        db.commit()

        await ctx.channel.send('Updated wallet from %s' % (arg))

"""
Disclaimer:

To make some endnotes I would like to clarify something, this Cog is actually independent from others Cogs,
no need to relate with shop.py or sql.py, so you can just add to your main bot and use it as you wish.
Also remark that you can make the database independent from each server and have an unique Economy system, just deleting the Server ID parameter from all SQL.execute() function
Hope you can understand and replicate the code for your own server/bot, anyway if you have any question or suggestion let me know.

"""