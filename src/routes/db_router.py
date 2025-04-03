from fastapi import APIRouter, HTTPException
import logging

from src.components.db.db_setup import database_connect

# Initialize logging
logging.basicConfig(level=logging.INFO)

router = APIRouter(prefix="/db" , tags=["Database"])


# Database health check
@router.get("/health")
async def db_health():
    try:
        async with database_connect() as pool:
            await pool.execute("SELECT 1;")
        return {"status": "ok", "message": "Database is healthy."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")