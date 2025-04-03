import io

import pdfplumber
        
## Add PDF Document to Vector Database
async def extract_text_from_pdf(pdf_content: bytes) -> str:
    """Extract text from PDF content using pdfplumber."""
    with pdfplumber.open(io.BytesIO(pdf_content)) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text

# ## Update Vector Database with Text Document
# async def update_db_with_text(text: str):
#     """Update the embeddings database with new text."""
#     openai_client = AsyncOpenAI(api_key=OPENAI_API_KEY)
#     async with database_connect() as pool:
#         chunks = await split_text_into_chunks(text)
#         await insert_chunks(pool, chunks, openai_client)