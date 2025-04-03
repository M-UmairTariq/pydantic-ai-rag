from fastapi import APIRouter, HTTPException

from src.db.db import db
from main import logger


router = APIRouter(prefix="/db" , tags=["Database"])


# Database health check
@router.get("/health")
async def db_health():
    try:
        pool = await db.connect(create_tables=False)
        await pool.execute("SELECT 1;")
        logger.info("Database is healthy.")
        return {"status": "ok", "message": "Database is healthy."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")