import aiosqlite

db_path = "agregator.db"

async def create_table():
    async with aiosqlite.connect(db_path) as db:
        await db.execute("""CREATE TABLE IF NOT EXISTS channels (
            creator_id INT,
            channel_id INT
            )
            """)
        await db.commit()

class Database:
    @staticmethod
    async def add_channel(creator_id, channel_id):
        async with aiosqlite.connect(db_path) as db:
            await db.execute("INSERT INTO channels (creator_id, channel_id) VALUES (?, ?)", (creator_id, channel_id))
            await db.commit()

    @staticmethod
    async def get_channels():
        async with aiosqlite.connect(db_path) as db:
            async with db.execute("SELECT channel_id FROM channels") as cur:
                ids = await cur.fetchall()
                channel_ids = []
                for id in ids:
                    channel_ids.append(id[0])
                return channel_ids
            
    @staticmethod
    async def if_channel_added(channel_id):
        async with aiosqlite.connect(db_path) as db:
            cursor = await db.execute("SELECT channel_id FROM channels WHERE channel_id = ?", (channel_id,))
            result = await cursor.fetchone()
            return result is not None

    @staticmethod
    async def get_my_channels(creator_id):
        async with aiosqlite.connect(db_path) as db:
            cur = await db.execute("SELECT channel_id FROM channels WHERE creator_id = ?", (creator_id,))
            ids = await cur.fetchall()
            channel_ids = []
            for id in ids:
                channel_ids.append(id[0])
            return channel_ids
    
    @staticmethod
    async def delete_channel(channel_id: int):
        async with aiosqlite.connect(db_path) as db:
            await db.execute("DELETE FROM channels WHERE channel_id = ?",
                        (channel_id,))
            await db.commit()