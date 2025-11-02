import disnake
import aiosqlite


class AtlasVersion:
    def __init__(self):
        self.path_version_database = "databases/version.db"

    ### CREATE TABLE IF NOT EXISTS FOR VERSION BOT
    async def create_table_version(self):
        async with aiosqlite.connect(self.path_version_database) as db:
            cursor = await db.cursor()
            query = '''CREATE TABLE IF NOT EXISTS version (
                bot INTEGER PRIMARY KEY,
                major INTEGER,
                minor INTEGER,
                maintenance INTEGER,
                date STR,
                time STR,
                relative_time STR
            )'''
            await cursor.execute(query)
            await db.commit()

    ### ADD BOT TO TABLE VERSION
    async def add_bot_to_table_version(self, user: disnake.Member):
        async with aiosqlite.connect(self.path_version_database) as db:
            cursor = await db.cursor()
            query = "SELECT * FROM version WHERE bot = ?"
            await cursor.execute(query, (user.id, ))
            data = await cursor.fetchone()
            if data is None:
                query = "INSERT OR IGNORE INTO version (bot, major, minor, maintenance, date, time, relative_time) VALUES (?, ?, ?, ?, ?, ?, ?)"
                await cursor.execute(query, (user.id, 0, 0, 0, "None", "None", "None"))
                await db.commit()
                return query

    ### UPDATE VERSION BOT
    async def update_bot_version(self, user: disnake.Member, major: int, minor: int, maintenance: int, date: str, time: str, relative_time: str):
        async with aiosqlite.connect(self.path_version_database) as db:
            cursor = await db.cursor()
            query = "UPDATE version SET major = ?, minor = ?, maintenance = ?, date = ?, time = ?, relative_time = ? WHERE bot = ?"
            await cursor.execute(query, (major, minor, maintenance, date, time, relative_time, user.id))
            await db.commit()

    ### GET VERSION BOT
    async def get_bot_version(self, user: disnake.Member):
        async with aiosqlite.connect(self.path_version_database) as db:
            cursor = await db.cursor()
            query = "SELECT major, minor, maintenance FROM version WHERE bot = ?"
            await cursor.execute(query, (user.id,))
            data = await cursor.fetchone()
            if data:
                major, minor, maintenance = data
                return f"{major}.{minor}.{maintenance}"
            else:
                return "Version not found"
            
    ### GET LAST UPDATE TIME BOT
    async def get_bot_last_update_time(self, user: disnake.Member):
        async with aiosqlite.connect(self.path_version_database) as db:
            cursor = await db.cursor()
            query = "SELECT date, time, relative_time FROM version WHERE bot = ?"
            await cursor.execute(query, (user.id,))
            data = await cursor.fetchone()
            if data:
                date, time, relative_time = data
                return f"{date}"
            else:
                return "Last update time not found"
            


