
import discord
from discord.ext import commands
from embed_format import Embed
import asyncio


class Poll(commands.Cog):


    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, aliases=['encuesta'], help="Make a poll")
    async def poll(self, ctx, *args):
        
        messages = []

        poll_order_dict = {
        ":one:":'1️⃣',
        ":two:":'2️⃣', 
        ":three:":'3️⃣', 
        ":four:":'4️⃣', 
        ":five:":'5️⃣'}

        options = {}
        
        messages.append("You have 60 seconds to react before the poll is finished.")

        for arg in range(len(args)):
            options[list(poll_order_dict)[arg]] = args[arg]
            messages.append(f"{list(poll_order_dict)[arg]} : {args[arg]}")
        
        print(options)

        try:
            embed = Embed(self.bot)
            
            embedVar = embed.convertMessage(messages)
            bot_msg = await ctx.channel.send(embed = embedVar)
        except Exception as e:
            print(e.args)
            for message in messages:
                bot_msg = await ctx.channel.send(message)
        
        emojis = list(poll_order_dict.values())
        
        for arg in range(len(args)):
            await bot_msg.add_reaction(emoji=emojis[arg])
        
        await asyncio.sleep(60)

        # Tomando mensaje en caché luego de esperar a las reacciones || Takes cached message before waiting the reactions.
        cache_msg = discord.utils.get(self.bot.cached_messages, id=bot_msg.id)

        # Para cada reacción en el mensaje guardado, buscar el que tiene mayor cantidad de reacciones. || For each reaction on the saved message, search the most reacted one.
        counts = {react.emoji: react.count for react in cache_msg.reactions}
        emojis = [react.emoji for react in cache_msg.reactions]
        winner = max(emojis, key=counts.get)
        
        # Usando un for para buscar una clave a través de su valor || Using a for sentence, search a key through it's value.
        for key, value in poll_order_dict.items():
            if winner == value:
                winner_to_text = key
            else:
                pass

        messages.clear()
        messages.append("Poll result:")
        messages.append(f"**Option {options[winner_to_text]}** won")
        
        try:
            embed = Embed(self.bot)
            
            embedVar = embed.convertMessage(messages)
            bot_msg = await ctx.channel.send(embed = embedVar)
        except Exception as e:
            print(e.args)
            for message in messages:
                bot_msg = await ctx.channel.send(message)
        


