from fastapi import APIRouter
from app.models.questions import Question, QuestionsResponse
from app.models.answers import Answer, AnswerCreate, AnswerResponse
from typing import List

router = APIRouter(
    prefix="/questions",
    tags=["questions"],
    responses={404: {"description": "Not found"}},
)

# Sample survey questions data
SAMPLE_QUESTIONS = [
    Question(
        id=1,
        text="What is your favorite color?",
        type="multiple_choice",
        options=["Red", "Blue", "Green", "Yellow"]
    ),
    Question(
        id=2,
        text="How often do you use our product?",
        type="single_choice",
        options=["Daily", "Weekly", "Monthly", "Rarely"]
    ),
    Question(
        id=3,
        text="What features would you like to see in our product?",
        type="text",
        options=None
    ),
    Question(
        id=4,
        text="How satisfied are you with our service?",
        type="single_choice",
        options=["Very Satisfied", "Satisfied", "Neutral", "Dissatisfied", "Very Dissatisfied"]
    ),
    Question(
        id=5,
        text="Would you recommend our product to others?",
        type="single_choice",
        options=["Definitely Yes", "Probably Yes", "Not Sure", "Probably Not", "Definitely Not"]
    )
]

@router.get("/", response_model=QuestionsResponse, summary="Get survey questions",
         description="Retrieve a list of survey questions")
async def get_questions():
    """Get survey questions"""
    response = QuestionsResponse(
        message="Successfully retrieved questions",
        data=SAMPLE_QUESTIONS
    )
    return response