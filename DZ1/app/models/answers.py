from pydantic import BaseModel
from typing import List, Optional, Union
from app.models.questions import Question

class Answer(BaseModel):
    question_id: int
    answer: Union[str, List[str]]

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "question_id": 1,
                    "answer": "Blue"
                },
                {
                    "question_id": 3,
                    "answer": "More customization options"
                }
            ]
        }
    }

class AnswerCreate(BaseModel):
    answers: List[Answer]

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "answers": [
                        {
                            "question_id": 1,
                            "answer": "Blue"
                        },
                        {
                            "question_id": 2,
                            "answer": "Daily"
                        },
                        {
                            "question_id": 3,
                            "answer": "More customization options"
                        }
                    ]
                }
            ]
        }
    }

class AnswerResponse(BaseModel):
    message: str
    data: List[Answer]

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "message": "Answers submitted successfully",
                    "data": [
                        {
                            "question_id": 1,
                            "answer": "Blue"
                        },
                        {
                            "question_id": 2,
                            "answer": "Daily"
                        }
                    ]
                }
            ]
        }
    }