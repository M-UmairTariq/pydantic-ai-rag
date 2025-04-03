# Initialize logging
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src:app", host="0.0.0.0", port=80, reload=True)
