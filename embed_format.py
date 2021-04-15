""" 
The function of this Cog is simple, just take a list of strings and add one by one to an embed message, with a random color.
"""

from discord.ext import commands
from discord import Embed as Em

import random # To select random colors.

class Embed(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
   
    def convertMessage(self, args = []):
        print(args)
        bot = self.bot

        if not args:
            print("Error! Can't use empty arguments.")
            return
        
        embedVar = Em(title=f"{args[0]}", color=self.getRandomColor()) # Select first value from list as Embed Title. Then set a random color using the function below.
        embedVar.set_footer(text=f"{bot.user}", icon_url=bot.user.avatar_url)

        for arg in args:
            if arg == args[0]: # We've already use first value as Title, so we ignore it.
                pass
            else:
                if isinstance(arg, str):
                    embedVar.add_field(name="\n\u200b", value=f"{arg}", inline=False)
        return embedVar

    def getRandomColor(self):
        colors = {
            "DEFAULT" : 0,
            "AQUA": 1752220,
            "GREEN": 3066993,
            "BLUE": 3447003,
            "PURPLE": 10181046,
            "GOLD": 15844367,
            "ORANGE": 15105570,
            "RED": 15158332,
            "GREY": 9807270,
            "DARKER_GREY": 8359053,
            "NAVY": 3426654,
            "DARK_AQUA": 1146986,
            "DARK_GREEN": 2067276,
            "DARK_BLUE": 2123412,
            "DARK_PURPLE": 7419530,
            "DARK_GOLD": 12745742,
            "DARK_ORANGE": 11027200,
            "DARK_RED": 10038562,
            "DARK_GREY": 9936031,
            "LIGHT_GREY": 12370112,
            "DARK_NAVY": 2899536,
            "LUMINOUS_VIVID_PINK": 16580705,
            "DARK_VIVID_PINK": 12320855
        }
        name, selected_color = random.choice(list(colors.items()))
        return selected_color