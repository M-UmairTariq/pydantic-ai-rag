from typing import List

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