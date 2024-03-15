import asyncpg


class Database:
    def __init__(self):
        self.pool = None

    async def _ensure_pool(self):
        if not self.pool:
            self.pool = await asyncpg.create_pool("postgres://postgres:postgres@localhost:5432/postgres")

    async def gimme(self):
        """returns a database connection"""
        await self._ensure_pool()
        return await self.pool.acquire()
