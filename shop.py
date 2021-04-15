"""
Disclaimer:
A simple Cog which allows admins to add/delete Items to a "shop list", assigning a price and and allowing to buy them,
this list is simply a SQL DB conformed by an Item name and value, independent of each server.
You can make the list "global" by deleting "Server_Name" and "Server_ID" from every SQL.execute parameter.
In this case, the Cog is directly connected with the Economy.py Cog, but not viceversa.
"""

from discord.ext import commands
import sqlite3
import os
# Import an external Cog
from economy import Economy

class Shop(commands.Cog):    
    def __init__(self, bot):
        self.bot = bot
    @commands.Cog.listener()
    async def on_ready(self): # We define a new DB with items for each server, to do this we replicate the SQL.execute from sql.py and add an "Item_Name" and "Item_Name" values.
        DIR = os.path.dirname(__file__)
        db = sqlite3.connect(os.path.join(DIR, "Items.db")) # Setting up a DB called "Items.db" on main folder.
        SQL = db.cursor()

        SQL.execute('create table if not exists Items('
                    '"Num" integer not null primary key autoincrement, '
                    '"Server_ID" integer, '
                    '"Server_Name" text, '
                    '"Item_Name" text, '
                    '"Item_Value" integer '
                    ')')


    @commands.command(pass_context=True)
    @commands.has_role('admin')
    async def addItem(self, ctx, arg=None, arg2=None): # Function only-usable by admins, which allows to add Items to the SQL database, using Server_ID as parameter

        DIR = os.path.dirname(__file__)
        db = sqlite3.connect(os.path.join(DIR, "Items.db"))
        SQL = db.cursor()

        server_name = str(ctx.guild.name)
        server_id = ctx.guild.id

        if arg is not None: # If a name was given
            
            SQL.execute(f'SELECT Item_Name FROM Items WHERE Server_ID="{server_id}"') # Select the item from the Db to check if already exists
            db.commit()
            check = SQL.fetchall() # fetchall() returns a list of tuples with each Item_Name on database, but can return None if is empty

            if check is not None: # If Item_Name row exists in the DB, checks if the new item is duplicated
                for x in check:
                    if arg in x[0]:
                        await ctx.channel.send('This item already exists in the shop list, try another name.')
                        return
                    else:
                        pass
            else: # If Item_Name row doesn't exists

                if arg2 is not None: # Check if a "value" parameter was given

                    price = int(arg2) # Convert the price to integer

                    if isinstance(arg, str) and isinstance(price, int):
                        SQL.execute('insert into Items(Item_Name, Item_Value, Server_ID, Server_Name) values(?,?,?,?)', (arg, price, server_id, server_name))
                        db.commit()
                        await ctx.channel.send(f"Added {arg} with value ${price} to the shop list.")
                    else:
                        await ctx.channel.send("Incorrect values for Item name and Item value") # If Item name is not string, or Item value is not integer, returns an error message.
                
                else:
                    await ctx.channel.send("Give me a price for %s" % (arg)) # If no price was given, ask for one...
                    arg2 = await self.bot.wait_for("message") # Note that "arg2" variable returns a Message type, not string,
                    price = int(arg2.content) #                 so we need to call "arg2.content" to recieve a string

                    if isinstance(arg, str) and isinstance(price, int):
                        SQL.execute('insert into Items(Item_Name, Item_Value, Server_ID, Server_Name) values(?,?,?,?)', (arg, price, server_id, server_name))
                        db.commit()
                        await ctx.channel.send(f"Added {arg} with value ${price} to the shop list.")
                    else:
                        await ctx.channel.send("Incorrect values for Item name and Item value")
                

        else:                       # If no name was given
            await ctx.channel.send("Give me the name of Item you want to add to the shop list: ") # Ask for one

            arg = await self.bot.wait_for("message")
            name = arg.content # Make a string with the message content

            SQL.execute(f'SELECT Item_Name FROM Items WHERE Server_ID="{server_id}"') # Select the item from the Db to check if already exists
            db.commit()
            check = SQL.fetchall()

            if check is not None:
                for x in check:
                    if name in x[0]:
                        await ctx.channel.send('This item already exists in the shop list, try another name.')
                        return
                    else:
                        pass

            else:
                await ctx.channel.send("Give me a price for %s" % (arg.content))
                arg2 = await self.bot.wait_for("message")
                price = int(arg2.content)

                if isinstance(name, str) and isinstance(price, int):
                    SQL.execute('insert into Items(Item_Name, Item_Value, Server_ID, Server_Name) values(?,?,?,?)', (name, price, server_id, server_name))
                    db.commit()
                    await ctx.channel.send(f"Added {name} with value ${price} to the shop list.")
                else:
                    await ctx.channel.send("Incorrect values for Item name and Item value")

            
    @commands.command(pass_context=True)
    @commands.has_role('admin')
    async def delItem(self, ctx, arg=None): # Function only-usable by admins, to delete Items from the SQL database

        DIR = os.path.dirname(__file__)
        db = sqlite3.connect(os.path.join(DIR, "Items.db"))
        SQL = db.cursor()

        server_id = ctx.guild.id

        if arg is not None:

            SQL.execute(f'SELECT Item_Name FROM Items WHERE Server_ID="{server_id}"') # Select the item from the Db to check if exists
            db.commit()
            check = SQL.fetchall()
            
            for x in check: # As we see, check is a list with all Items from Server_ID, so we iterate in each tuple to see if argument given is there.
                if not arg in x[0]:
                    pass
                else:
                    SQL.execute(f'DELETE from Items where Item_Name="{arg}" and Server_ID="{server_id}"') # Eliminates every row called "Item_Name" from "Server_ID"
                    db.commit()
                    await ctx.channel.send('Item %s removed from shop list' % (arg))
                    return
                await ctx.channel.send('Item %s not found in the shop list' % (arg))
        else:
            await ctx.channel.send("Give me the name of Item you want to delete from shop list: ") # If no Item_Name was given, ask for one.
            arg = await self.bot.wait_for("message")
            name = arg.content # Make string from Message object

            SQL.execute(f'SELECT Item_Name FROM Items WHERE Server_ID="{server_id}"') # Select the item from the Db to check if exists
            db.commit()
            check = SQL.fetchall() # Returns a list

            for x in check:
                if not name in x[0]:
                    pass
                else:
                    SQL.execute(f'DELETE from Items where Item_Name="{name}" and Server_ID="{server_id}"')
                    db.commit()
                    await ctx.channel.send('Item %s removed from shop list' % (name))
                    return
                await ctx.channel.send('Item %s not found in the shop list' % (name))

            


    @commands.command(pass_context=True)
    async def buy(self, ctx, arg='list'): # A command to buy an specific item, if argument is not passed, it's returns a list with available items.

        economy = Economy(self.bot)
        
        listed_items = self.getItems(ctx)

        if arg == 'list' :
            if not listed_items:
                await ctx.channel.send('Not available articles in server')
                return
            else:
                await ctx.channel.send('Available items: ')
                for item in listed_items:
                    await ctx.channel.send(f"{item}: ${listed_items[item]}")
        else:
            if arg in listed_items:
                boolean = economy.checkWallet(ctx, listed_items[arg])
                if boolean is True:
                    await ctx.channel.send('Purchased %s' % (arg))
                else:
                    await ctx.channel.send("You don't have enough money to buy this article")
                pass
            else:
                ctx.channel.send('Error 404: Item not found')
            
    def getItems(self, ctx):

        DIR = os.path.dirname(__file__)
        db = sqlite3.connect(os.path.join(DIR, "Items.db"))
        SQL = db.cursor()

        server_id = ctx.guild.id

        listed_items = {}

        SQL.execute(f'SELECT Item_Name, Item_Value FROM Items WHERE Server_ID="{server_id}"')
        db.commit()
        item_list = SQL.fetchall()

        for (x, y) in item_list:
            listed_items[x] = y
        return listed_items
    

