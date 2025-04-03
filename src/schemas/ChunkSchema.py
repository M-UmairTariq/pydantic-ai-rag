from pydantic import BaseModel

class Chunk(BaseModel):
    chunk: str