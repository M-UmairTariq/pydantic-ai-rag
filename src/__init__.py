from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from main import logger

from src.routes.db_router import router as db_router
from src.routes.rag_router import router as rag_router
from src.db.db import db

import os

from dotenv import load_dotenv

load_dotenv()


# Connection string for PostgreSQL database
DB_DSN = os.environ.get("DB_DSN")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage database connection pool."""
    await db.connect(create_tables=True)
    logger.info("Database connected")
    yield
    
    await db.close()



app = FastAPI(lifespan=lifespan)

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
