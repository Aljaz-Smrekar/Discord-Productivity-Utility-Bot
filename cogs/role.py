import discord
from discord.ext import commands


class Role(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.saved_role = None


    @commands.command(name="set_role", help="Sets the role to be assigned to users.")
    async def set_role(self, ctx):
        role_parts = ctx.message.content.split(maxsplit=1)
        if len(role_parts) < 2:
            return await ctx.send("Please provide a role name after the command.")
        self.saved_role = role_parts[1]

        try:
            if self.saved_role:
                await ctx.send(f"Role has been set to '{self.saved_role}'.")
                await ctx.send(f"!assign will result in assigning the role '{self.saved_role}' to the user.")
            else:
                return await ctx.send("Please provide a valid role name.")
            
        except IndexError:
            return await ctx.send("Please provide a role name after the command.")


    @commands.command(name="get_role", help="Gets the currently set role.")
    async def get_role(self, ctx):
        if self.saved_role:
            await ctx.send(f"The currently set role is '{self.saved_role}'.")
        else:
            await ctx.send("No role has been set yet. Use !set_role to set a role.")


    @commands.command(name="assign", help="Adds a role to a user.")
    async def assign(self, ctx):
        if not self.saved_role:
            return await ctx.send("No role set yet. Use `!set_role <role>` first.")
        
        role = discord.utils.get(ctx.guild.roles, name=self.saved_role)

        if not role:
            await ctx.send("Make sure that !set_role has been used to set a valid and existing role.")
            return await ctx.send(
                f"Role '{self.saved_role}' does not exist on this server."
            )
        
        await ctx.author.add_roles(role)
        await ctx.send(f"Role '{role.name}' assigned to {ctx.author.mention}!")


    @commands.command(name="remove_role", help="Removes a role from a user.")
    async def remove_role(self, ctx):
        if not self.saved_role:
            return await ctx.send("No role set yet. Use `!set_role <role>` first.")
        role = discord.utils.get(ctx.guild.roles, name=self.saved_role)
        if not role:
            await ctx.send("Make sure that !set_role has been used to set a valid and existing role.")
            return await ctx.send(
                f"Role '{self.saved_role}' does not exist on this server."
            )
        await ctx.author.remove_roles(role)
        await ctx.send(f"Role '{role.name}' removed from {ctx.author.mention}!")
        

async def setup(bot):
    await bot.add_cog(Role(bot))