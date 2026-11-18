import sqlite3
import asyncio

class SessionDatabase:
    def __init__(self, db_path: str = "sessions.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.create_table()

    def create_table(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS session_state (
                    session_id TEXT PRIMARY KEY,
                    history TEXT
                )
            """)

    async def save_session_async(self, session_id: str, history: list):
        """Asynchronously writes state back to the SQLite persistent database."""
        await asyncio.sleep(0.01) # Simulate async I/O
        import json
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT OR REPLACE INTO session_state (session_id, history) VALUES (?, ?)",
                (session_id, json.dumps(history))
            )

    async def load_session_async(self, session_id: str) -> list:
        """Asynchronously loads state from the SQLite persistent database."""
        await asyncio.sleep(0.01) # Simulate async I/O
        import json
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT history FROM session_state WHERE session_id = ?", (session_id,))
            row = cursor.fetchone()
            return json.loads(row[0]) if row else []
