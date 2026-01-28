from fastapi import APIRouter
from app.models.answers import Answer, AnswerCreate, AnswerResponse
from typing import List

router = APIRouter(
    prefix="/answers",
    tags=["answers"],
    responses={404: {"description": "Not found"}},
)

# In-memory storage for answers (this should be moved to a proper database in production)
answers_storage: List[Answer] = []

@router.post("/", response_model=AnswerResponse, summary="Submit answers",
          description="Submit answers to survey questions")
async def submit_answers(answer_create: AnswerCreate):
    """Submit answers to survey questions"""
    global answers_storage
    answers_storage.extend(answer_create.answers)

    return AnswerResponse(
        message="Answers submitted successfully",
        data=answer_create.answers
    )