from fastapi import APIRouter, UploadFile, File, HTTPException
import logging

from src.components.doc_handler.doc_handler import add_text_to_db, extract_text_from_pdf
from src.components.rag_agent.rag import run_agent
from src.schemas.QuestionRequestSchema import QuestionRequest

# Initialize logging
logging.basicConfig(level=logging.INFO)

router = APIRouter(prefix="/rag" , tags=["RAG"])


@router.get("/")
async def rag():
    return {"message": "RAG"}


## Upload File to Database
@router.post("/upload-document/")
async def upload_file(file: UploadFile = File(...)):
    """Upload a file and process its contents for embedding."""
    try:
        content = await file.read()
        file_type = file.content_type

        if file_type == "text/plain" or file_type == "text/markdown":
            text = content.decode("utf-8")
            await add_text_to_db(text)
            return {"message": "Text file processed successfully."}

        elif file_type == "application/pdf":
            text = extract_text_from_pdf(content)
            await add_text_to_db(text)
            return {"message": "PDF file processed successfully."}

        else:
            raise HTTPException(status_code=400, detail="Unsupported file type.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")




@router.post("/ask")
async def ask_question(request: QuestionRequest):
    """Route to ask a question and get an RAG-based answer."""
    try:
        answer = await run_agent(request.question)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))