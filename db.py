import aiosqlite

DB_PATH = "jail.db"

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS sanctions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                issuer_id INTEGER NOT NULL,
                ore_count INTEGER NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            );
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT NOT NULL,
                agent_id INTEGER,
                subject_id INTEGER,
                description TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            );
        """)
        await db.commit()

async def add_sanction(user_id: int, issuer_id: int, ore: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO sanctions(user_id, issuer_id, ore_count) VALUES(?,?,?)",
            (user_id, issuer_id, ore)
        )
        await db.commit()

async def fetch_history(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute(
            "SELECT id, issuer_id, ore_count, timestamp "
            "FROM sanctions WHERE user_id = ? ORDER BY timestamp DESC",
            (user_id,)
        )
        return await cur.fetchall()

async def add_log(event_type: str, agent_id: int, subject_id: int, desc: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO logs(event_type, agent_id, subject_id, description) VALUES(?,?,?,?)",
            (event_type, agent_id, subject_id, desc)
        )
        await db.commit()
