import discord
from discord.ext import commands
import random
import time

class Secret(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name="secret", help="A secret command.")
    @commands.has_role("W boyS")
    async def secret(self, ctx):
        await ctx.send("This is a secret command!\nOnly super secret users can do this command")


    @commands.command(name="russian_roulette", help="Play a game of Russian Roulette and risk gettign timedout of the server.")
    async def russian_roulette(self, ctx):
        await ctx.send("You are playing Russian Roulette with your Operating System...\nSpinning the cylinder...")
        start_time = time.time()
        delay_seconds = 3
        while (time.time() - start_time) < delay_seconds:
            await ctx.send("AND...")

        chance = random.randint(1, 6)
        if chance == 1:
            await ctx.send("Bang! Your Operating System has crashed!")
            await ctx.author.timeout(duration=60, reason="Lost at Russian Roulette.")
        else:
            await ctx.send("Click! You survived this round of Russian Roulette.\n"
            "Your Operating System is safe... for now.....")


    @commands.command(name="choose", help="Make a random choice from a list of options.")
    async def choose(ctx, *choices: str):
        """Chooses between multiple choices."""
        await ctx.send(random.choice(choices))


    


async def setup(bot):
    await bot.add_cog(Secret(bot))