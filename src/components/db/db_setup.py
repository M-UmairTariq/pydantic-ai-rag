from __future__ import annotations as _annotations
from contextlib import asynccontextmanager
import os
import asyncpg
import dotenv

dotenv.load_dotenv()


# Connection string for PostgreSQL database
DB_DSN = os.environ.get("DB_DSN")

DB_SCHEMA = """
    CREATE EXTENSION IF NOT EXISTS vector;

    CREATE TABLE IF NOT EXISTS text_chunks (
        id serial PRIMARY KEY,
        chunk text NOT NULL,
        embedding vector(1536) NOT NULL
    );
    CREATE INDEX IF NOT EXISTS idx_text_chunks_embedding ON text_chunks USING hnsw (embedding vector_l2_ops);
    """
    
    
@asynccontextmanager
async def database_connect(create_db: bool = False):
    """Manage database connection pool."""
    pool = await asyncpg.create_pool(dsn=DB_DSN)
    try:
        if create_db:
            async with pool.acquire() as conn:
                await conn.execute(DB_SCHEMA)
        yield pool
    finally:
        await pool.close()

