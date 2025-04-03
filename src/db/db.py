import asyncpg
import os
import json
from typing import List

from src.components.chunking.chunking import Chunk, split_text_into_chunks
from src import openai


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

    async def insert_chunks(self, chunks: List[Chunk]):
        """Insert text chunks into the database with embeddings."""
        
        if not self.pool:
            raise ValueError("Database not connected")

        for chunk in chunks:
            embedding_response = await openai.embeddings.create(
                input=chunk.chunk,
                model="text-embedding-3-small"
            )
        
            # Extract embedding data and convert to JSON format
            assert len(embedding_response.data) == 1, f"Expected 1 embedding, got {len(embedding_response.data)}"
            embedding_data = json.dumps(embedding_response.data[0].embedding)

            # Insert into the database
            await self.pool.execute(
                'INSERT INTO text_chunks (chunk, embedding) VALUES ($1, $2)',
                chunk.chunk,
                embedding_data 
            )

    async def check_table_exists(self) -> bool:
        """Check if the database table exists."""

        if not self.pool:
            raise ValueError("Database not connected")

        return await self.pool.fetchval("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables
                WHERE table_name = 'text_chunks'
            )
        """)
    
    async def add_text_to_db(self, text: str):
        """Add plain text to the embeddings database."""

        if not self.pool:
            raise ValueError("Database not connected")

        chunks = await split_text_into_chunks(text)
        await self.insert_chunks(chunks)




db = Database()