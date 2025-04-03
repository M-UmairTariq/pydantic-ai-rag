# Define a request model for the question
from pydantic import BaseModel


class QuestionRequest(BaseModel):
    question: str