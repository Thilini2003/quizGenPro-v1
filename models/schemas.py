from pydantic import BaseModel, Field
from typing import List, Optional

class MCQQuestion(BaseModel):
    question: str
    options: List[str] = Field(..., min_items=4, max_items=4)
    correct_answer: str
    explanation: Optional[str] = None

class MCQRequest(BaseModel):
    topic: str = Field(..., min_length=3, max_length=200)
    num_questions: int = Field(default=5, ge=1, le=50)
    difficulty: str = Field(default="medium", pattern="^(easy|medium|hard)$")
    subtopics: Optional[List[str]] = None

class MCQResponse(BaseModel):
    questions: List[MCQQuestion]
    download_url: str
    total_questions: int