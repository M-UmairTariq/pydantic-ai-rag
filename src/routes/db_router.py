from fastapi import APIRouter, HTTPException
import logging

from src import db

# Initialize logging
logging.basicConfig(level=logging.INFO)

router = APIRouter(prefix="/db" , tags=["Database"])


# Database health check
@router.get("/health")
async def db_health():
    try:
        pool = await db.connect(create_tables=False)
        await pool.execute("SELECT 1;")
        
        return {"status": "ok", "message": "Database is healthy."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")