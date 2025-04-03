import asyncpg
import os

DB_SCHEMA = """
    CREATE EXTENSION IF NOT EXISTS vector;

    CREATE TABLE IF NOT EXISTS text_chunks (
        id serial PRIMARY KEY,
        chunk text NOT NULL,
        embedding vector(1536) NOT NULL
    );
    CREATE INDEX IF NOT EXISTS idx_text_chunks_embedding ON text_chunks USING hnsw (embedding vector_l2_ops);
"""

class Database:
    def __init__(self):
        self.pool = None

    async def connect(self, create_tables: bool = False):
        self.pool = await asyncpg.create_pool(dsn=os.getenv("DB_DSN"))

        if create_tables:
            async with self.pool.acquire() as conn:
                await conn.execute(DB_SCHEMA)
        
        return self.pool
    
    async def close(self):
        await self.pool.close()


db = Database()