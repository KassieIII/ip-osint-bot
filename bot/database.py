import aiosqlite
from datetime import datetime


class Database:
    """Async SQLite wrapper for storing lookup history."""

    def __init__(self, db_path: str):
        self.db_path = db_path
        self._conn: aiosqlite.Connection | None = None

    async def __aenter__(self):
        self._conn = await aiosqlite.connect(self.db_path)
        self._conn.row_factory = aiosqlite.Row
        await self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS lookups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                lookup_type TEXT NOT NULL,
                target TEXT NOT NULL,
                result_summary TEXT,
                created_at TEXT NOT NULL
            )
            """
        )
        await self._conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_user_id ON lookups(user_id)"
        )
        await self._conn.commit()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._conn:
            await self._conn.close()

    async def save_lookup(
        self, user_id: int, lookup_type: str, target: str, summary: str
    ) -> None:
        await self._conn.execute(
            "INSERT INTO lookups (user_id, lookup_type, target, result_summary, created_at) VALUES (?, ?, ?, ?, ?)",
            (user_id, lookup_type, target, summary, datetime.utcnow().isoformat()),
        )
        await self._conn.commit()

    async def get_history(self, user_id: int, limit: int = 10) -> list[dict]:
        cursor = await self._conn.execute(
            "SELECT lookup_type, target, created_at FROM lookups WHERE user_id = ? ORDER BY id DESC LIMIT ?",
            (user_id, limit),
        )
        rows = await cursor.fetchall()
        return [
            {
                "lookup_type": row["lookup_type"],
                "target": row["target"],
                "created_at": row["created_at"][:16].replace("T", " "),
            }
            for row in rows
        ]
