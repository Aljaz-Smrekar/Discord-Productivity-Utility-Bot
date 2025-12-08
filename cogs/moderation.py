import re
import discord
from discord.ext import commands

from services.database import Database

bad_word_pattern = r"\bn[\W_]*[i1!|][\W_]*[gq9]+[\W_]*[ae4@3r]?"

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Database()


    @commands.Cog.listener()
    async def on_ready(self):
        print("Ready to go!")
        print(f'Logged in as {self.bot.user.name} ID: ({self.bot.user.id})')


    @commands.Cog.listener()
    async def on_member_join(self, member):
        await member.send(f'Welcome to the server, {member.name}!')


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        
        if message.author == self.bot.user:
            return
    
        msg = message.content.lower()

        if re.search(bad_word_pattern, msg):
            try:
                await message.delete() #WILL TRY TO ALTER ISNTEAD OF DELETIGN THE FULL THING
                await message.channel.send(f"{message.author.mention}, you said a naughty word... \nMaybe don't use that word...")
            except discord.Forbidden:
                print("Missing permissions to delete messages.")

        if "hello" in msg or 'hi' in msg:
            await message.channel.send(f'Hello, {message.author.mention}!')

        # await self.bot.process_commands(message)


    @commands.command()
    async def ping(self, ctx):
        await ctx.send("Pong!")


async def setup(bot):
    cog = Moderation(bot)
    await cog.db.connect()
    await bot.add_cog(cog)