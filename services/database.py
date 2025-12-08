import aiosqlite
import os
import datetime

DB_PATH = "data/main.db"

# Add a summary for the whole thing

class Database:
    def __init__(self):
        """Initialize the database (doesn't connect yet)"""
        self.db = None

    async def connect(self):
        # Step 1: Make sure the 'data' folder exists
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

        # Step 2: Connect to the database file (creates it if it doesn't exist)
        self.db = await aiosqlite.connect(DB_PATH)

         # Step 3: Create the tasks table if it doesn't exist

        # await self.db.execute("""
        # CREATE TABLE IF NOT EXISTS bad (
        #     user_id TEXT NOT NULL PRIMARY,
        #     times_said_bad INTEGER,
        #     timeout_number INTEGER,
        # )
        # """)

        await self.db.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            task_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            text TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            completed INTEGER DEFAULT 0
        )
        """)

        await self.db.execute("""
        CREATE TABLE IF NOT EXISTS reminders (
            reminder_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            text TEXT NOT NULL,
            due_time TEXT NOT NULL
        )
        """)

        await self.db.commit()

        print("Database connected and tables created!")
        



    async def add_task(self, user_id: int, text: str, timestamp):
        

        await self.db.execute(
            """
            INSERT INTO tasks (user_id, text, timestamp)
            VALUES (?, ?, ?)
            """,
            (user_id, text, timestamp)
        )

        await self.db.commit()

    
    async def get_tasks(self, user_id: int):
        cursor = await self.db.execute(
            """
            SELECT *
            FROM tasks
            WHERE user_id = ?
            """,
            (user_id,) 
            )
        rows = await cursor.fetchall()
        tasks = []
        for row in rows:
            tasks.append({
                'task_id': row[0],
                'user_id': row[1],
                'text': row[2],
                'timestamp': row[3],
                'completed': row[4]
            })
        
        return tasks


    async def mark_task_completed(self, user_id: int, task_id: int):
        await self.db.execute(
            """
            UPDATE tasks
            SET completed = 1
            WHERE user_id = ? AND task_id = ?
            """,
            (user_id, task_id)
        )
        await self.db.commit()


    async def delete_task(self, user_id: int, task_id: int):
        await self.db.execute(
            """
            DELETE FROM tasks
            WHERE user_id = ? AND task_id = ?
            """,
            (user_id, task_id)
        )
        await self.db.commit()


    async def set_reminder(self, user_id: int, text: str, due_time: float):
        await self.db.execute(
            """
            INSERT INTO reminders (user_id, text, due_time)
            VALUES (?, ?, ?)
            """,
            (user_id, text, due_time)
        )
        await self.db.commit()

    async def get_reminders(self, user_id: int):
        cursor = await self.db.execute(
            """
            SELECT *
            FROM reminders
            WHERE user_id = ?
            """,
            (user_id,)
        )
        rows = await cursor.fetchall()
        reminders = []
        for row in rows:
            reminders.append({
                'reminder_id': row[0],
                'user_id': row[1],
                'text': row[2],
                'due_time': float(row[3])
            })
        return reminders
    


    async def get_due_reminders(self):
        cursor = await self.db.execute(
            """
            SELECT reminder_id, user_id, text
            FROM reminders
            WHERE due_time <= ?
            """,
            (datetime.datetime.utcnow().timestamp(),)
        )
        return await cursor.fetchall()
    

    async def delete_reminder(self, reminder_id: int):
        await self.db.execute(
            "DELETE FROM reminders WHERE reminder_id = ?",
            (reminder_id,)
        )
        await self.db.commit()


    # TODO: Create add_task() x
    # TODO: Create get_tasks() x
    # TODO: Create mark_task_completed() x
    # TODO: Create add_reminder() x
    # TODO: Create get_reminders() x
