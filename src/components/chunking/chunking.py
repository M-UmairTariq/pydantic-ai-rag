import json
from typing import List
import asyncpg
from openai import AsyncOpenAI

from src.schemas.ChunkSchema import Chunk


async def split_text_into_chunks(text: str, max_words: int = 400, overlap: float = 0.2) -> List[Chunk]:
    """Split long text into smaller chunks based on word count with overlap."""
    words = text.split()
    chunks = []
    step_size = int(max_words * (1 - overlap))

    for start in range(0, len(words), step_size):
        end = start + max_words
        chunk_words = words[start:end]
        if chunk_words:
            chunks.append(Chunk(chunk=" ".join(chunk_words)))

    return chunks

async def insert_chunks(pool: asyncpg.Pool, chunks: List[Chunk], openai_client: AsyncOpenAI):
    """Insert text chunks into the database with embeddings."""
    for chunk in chunks:
        embedding_response = await openai_client.embeddings.create(
            input=chunk.chunk,
            model="text-embedding-3-small"
        )
        
        # Extract embedding data and convert to JSON format
        assert len(embedding_response.data) == 1, f"Expected 1 embedding, got {len(embedding_response.data)}"
        embedding_data = json.dumps(embedding_response.data[0].embedding)

        # Insert into the database
        await pool.execute(
            'INSERT INTO text_chunks (chunk, embedding) VALUES ($1, $2)',
            chunk.chunk,
            embedding_data 
        )