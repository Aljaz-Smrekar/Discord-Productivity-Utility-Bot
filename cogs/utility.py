import discord
from discord.ext import commands

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name="poll", help="Creates a simple yes/no poll.")
    async def poll(self, ctx):
        poll_parts = ctx.message.content.split(maxsplit=1)
        if len(poll_parts) < 2:
            return await ctx.send("Please provide a question for the poll after the command.")
        question = poll_parts[1]
        embed = discord.Embed(title="New Poll", description=question, color=0x00ff00)
        poll_message = await ctx.send(embed=embed)
        await poll_message.add_reaction("👍")
        await poll_message.add_reaction("👎")



async def setup(bot):
    await bot.add_cog(Utility(bot))