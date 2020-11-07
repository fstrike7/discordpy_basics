
import sqlite3 # Import SQLite3 library
import os # Import OS library

from discord.ext import commands 

class SQL(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self): # When Cog is connected

        DIR = os.path.dirname(__file__)
        db = sqlite3.connect(os.path.join(DIR, "Guilds.db"))
        SQL = db.cursor()

        SQL.execute('create table if not exists Guilds('
                    '"Num" integer not null primary key autoincrement, '
                    '"Server_ID" integer, '
                    '"Server_Name" text '
                    ')') # First of all, create a table "Guilds" which contains info from servers, such as name and ID.

        for x in self.bot.guilds: # Iterate with list "bot.guilds", which contains an object Guild for each guild where the bot is connected
            server_name = str(x.name)
            server_id = x.id
            SQL.execute('insert into Guilds(Server_ID, Server_Name) values(?,?)', (server_id, server_name)) 
            db.commit()

        
    @commands.Cog.listener() # Like bot.event, this Cog will run each time the event "on_message" is executed
    async def on_message(self, ctx):
        if ctx.author == self.bot.user:
            return
        
        DIR = os.path.dirname(__file__) # Defines a path for the database file
        db = sqlite3.connect(os.path.join(DIR, "Users.db")) #Connect to the database, assigning a name
        SQL = db.cursor() # Cursor for the DB

        SQL.execute('create table if not exists Users('
                    '"Num" integer not null primary key autoincrement, '
                    '"Server_ID" integer, '
                    '"Server_Name" text, '
                    '"User_ID" integer, '
                    '"User_Name" text'
                    ')') # Here we create the table with each statement for the DB, a list with every data type can found in: https://www.sqlite.org/datatype3.html
    

        server_name = str(ctx.guild.name)
        server_id = ctx.guild.id
        user_id = int(ctx.author.id)
        user_name = str(ctx.author)
        
        SQL.execute(f'select User_ID from Users where Server_ID="{server_id}" and Server_Name="{server_name}" and User_ID="{user_id}"')
        check = SQL.fetchone()
        if not check: # This "if" statement, check if the user exist in the database, if it's return False, create a row for that user.
            SQL.execute('insert into Users(Server_ID, Server_Name, User_ID, User_Name) values(?,?,?,?)', (server_id, server_name, user_id, user_name))
            db.commit()

        
        await self.bot.process_commands(ctx)
    
    @commands.command(pass_context=True)
    #@commands.has_role("admin")          #  Uncomment to make the command only usable for admins, you can also change "admin" for the role(name) you want.
    async def members(self, ctx): # A simple command which returns a list with each member registered on the database file, only from the server where the message arrives.

        DIR = os.path.dirname(__file__)
        db = sqlite3.connect(os.path.join(DIR, "Users.db"))
        SQL = db.cursor()

        server_id = ctx.guild.id

        SQL.execute(f"SELECT User_Name FROM Users where Server_ID='{server_id}'")
        for row in SQL:
            await ctx.channel.send(row)
        