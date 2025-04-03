import io
import os

import pdfplumber
from src.components.chunking.chunking import insert_chunks, split_text_into_chunks
from src.components.db.db_setup import database_connect
from openai import AsyncOpenAI

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

## Check if the database table exists
async def check_table_exists() -> bool:
    """Check if the database table exists."""
    async with database_connect() as pool:
        return await pool.fetchval("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables
                WHERE table_name = 'text_chunks'
            )
        """)
        
## Add PDF Document to Vector Database
def extract_text_from_pdf(pdf_content: bytes) -> str:
    """Extract text from PDF content using pdfplumber."""
    with pdfplumber.open(io.BytesIO(pdf_content)) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text

## Add Text Document to Vector Database
async def add_text_to_db(text: str):
    """Add plain text to the embeddings database."""
    openai_client = AsyncOpenAI(api_key=OPENAI_API_KEY)
    table_exists = await check_table_exists()
    async with database_connect(create_db=not table_exists) as pool:
        chunks = await split_text_into_chunks(text)
        await insert_chunks(pool, chunks, openai_client)
        
## Update Vector Database with Text Document
async def update_db_with_text(text: str):
    """Update the embeddings database with new text."""
    openai_client = AsyncOpenAI(api_key=OPENAI_API_KEY)
    async with database_connect() as pool:
        chunks = await split_text_into_chunks(text)
        await insert_chunks(pool, chunks, openai_client)