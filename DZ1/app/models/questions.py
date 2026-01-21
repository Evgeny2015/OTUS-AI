from pydantic import BaseModel
from typing import List, Optional

class Question(BaseModel):
    id: int
    text: str
    type: str  # text, multiple_choice, single_choice, etc.
    options: Optional[List[str]] = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "text": "What is your favorite color?",
                    "type": "multiple_choice",
                    "options": ["Red", "Blue", "Green", "Yellow"]
                }
            ]
        }
    }

class QuestionsResponse(BaseModel):
    message: str
    data: List[Question]

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "message": "Successfully retrieved questions",
                    "data": [
                        {
                            "id": 1,
                            "text": "What is your favorite color?",
                            "type": "multiple_choice",
                            "options": ["Red", "Blue", "Green", "Yellow"]
                        }
                    ]
                }
            ]
        }
    }