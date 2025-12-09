import asyncio
import discord
from discord.ext import commands
from datetime import datetime

from services.database import Database

class Reminders(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Database()

    @commands.command(name="add_task", help="Adds a task to the users to-do list.")
    async def add_task(self, ctx, *, text: str):
        
        if not text.strip():
            return await ctx.send("Please add a task :)")

        
        timestamp = datetime.utcnow().isoformat()
        user_id = ctx.author.id
        await self.db.add_task(user_id, text, timestamp)
        await ctx.send(f"Task added! for user {ctx.author.mention}.")


    @commands.command(name="get_tasks", help="Gets the tasks for the user.")
    async def get_tasks(self, ctx):
        user_id = ctx.author.id
        tasks = await self.db.get_tasks(user_id)

        if not tasks:
            return await ctx.send(f"You {ctx.author.mention} have no tasks.")

        #Breakdown of rows
        # task_id = tasks[0]
        # task_user_id = tasks[1]
        # task = tasks[2]
        # task_time = tasks[3]
        # completed = tasks[4]
            
        task_list = "\n".join(
            f"Completed\n#{task['task_id']}: {task['text']}\n" 
            if task['completed'] == 1 
            else f"Not Completed\n#{task['task_id']}: {task['text']}\n"
            for task in tasks 
        ) # Creates the task list string
        
        await ctx.send(f"{ctx.author.mention}'s tasks:\n{(task_list)}")


    @commands.command(name="complete_task", help="Marks a task as completed.")
    async def complete_task(self, ctx, task_id: int):
        user_id = ctx.author.id
        tasks = await self.db.get_tasks(user_id)
        
        task_ids = {task['task_id'] for task in tasks} # Set of task IDs for quick lookup
        
        if task_id not in task_ids:
            return await ctx.send(f"Task ID {task_id} not found for {ctx.author.mention}.")

        await self.db.mark_task_completed(user_id, task_id)
        await ctx.send(f"Task #{task_id} marked as completed for {ctx.author.mention}.")



    @commands.command(name="delete_task", help="Deletes a task from the user's to-do list.")
    async def delete_task(self, ctx, task_id: int):
        user_id = ctx.author.id
        tasks = await self.db.get_tasks(user_id)
        task_ids = {task['task_id'] for task in tasks}
        if task_id not in task_ids:
            return await ctx.send(f"Task ID {task_id} not found for {ctx.author.mention}.")
        await self.db.delete_task(user_id, task_id)
        await ctx.send(f"Task #{task_id} deleted for {ctx.author.mention}.")




    @commands.command(name="set_reminder", help="Sets a reminder for the user.")
    async def set_reminder(self, ctx, due_time: str, *, text: str,):
        user_id = ctx.author.id

        # Parse time like "10m", "2h", "1d"
        seconds = self.parse_time(due_time)
        if seconds is None:
            return await ctx.send("Invalid time format! Use examples: `10m`, `2h`, `1d`, `7y`.")

        due_timestamp = (datetime.utcnow().timestamp() + seconds)

        await self.db.set_reminder(user_id, text, due_timestamp)

        await ctx.send(
            f"⏰ Reminder set for **{due_time}**: '{text}' for {ctx.author.mention}"
        )

    def parse_time(self, t: str):
        t = t.lower()
        if t.endswith("s"):
            return int(t[:-1])
        if t.endswith("m"):
            return int(t[:-1]) * 60
        if t.endswith("h"):
            return int(t[:-1]) * 3600
        if t.endswith("d"):
            return int(t[:-1]) * 86400
        if t.endswith("y"):
            return int(t[:-1]) * 31536000
        return None
    


    @commands.command(name="get_reminders", help="Gets the reminders for the user.")
    async def get_reminders(self, ctx):
        user_id = ctx.author.id
        reminders = await self.db.get_reminders(user_id)
        if not reminders:
            return await ctx.send(f"You {ctx.author.mention} have no reminders.")
        # reminder_list = "\n".join(
        #     f"#{reminder['reminder_id']}: {reminder['text']} "
        #     f"(due at {datetime.fromtimestamp(reminder['due_time']).strftime('%Y-%m-%d %H:%M:%S UTC')})"
        #     for reminder in reminders
        # )
        # await ctx.send(f"{ctx.author.mention}'s reminders:\n{reminder_list}")
        embed = discord.Embed(
            title=f"{ctx.author.display_name}'s Reminders",
            color=0x00ff00
        )

        # Add each reminder as a field
        for reminder in reminders:
            due_time = datetime.fromtimestamp(reminder['due_time']).strftime('%Y-%m-%d %H:%M:%S UTC')
            embed.add_field(
                name=f"#{reminder['reminder_id']}",
                value=f"{reminder['text']} (due {due_time})",
                inline=False
            )

        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_ready(self):
        # Start the loop when the bot is ready
        self.bot.loop.create_task(self.reminder_loop())


    async def reminder_loop(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            due = await self.db.get_due_reminders()

            for reminder_id, user_id, text in due:
                user = self.bot.get_user(int(user_id))
                if user:
                    try:
                        await user.send(f"⏰ **Reminder:** {text}")
                    except:
                        pass

                await self.db.delete_reminder(reminder_id)

            await asyncio.sleep(10)  # check every 10 seconds


    # async def reminder_countdown(self, ctx, seconds, text):
    #     await asyncio.sleep(seconds)
    #     await ctx.send(f"🔔 Reminder: {ctx.author.mention} — {text}")


async def setup(bot):
    cog = Reminders(bot)
    await cog.db.connect()
    await bot.add_cog(cog)