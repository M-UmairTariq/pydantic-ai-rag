from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routes.db_router import router as db_router
from src.routes.rag_router import router as rag_router

app = FastAPI()

app.include_router(rag_router)
app.include_router(db_router)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type", "Authorization"],
)

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Hello World"}

# Health check endpoint
@app.get("/health")
async def health():
    return {"status": "ok"}
