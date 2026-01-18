from pydantic import BaseModel
from typing import Optional

class SampleData(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "name": "Sample Item",
                    "description": "A sample item for testing"
                }
            ]
        }
    }

class SampleResponse(BaseModel):
    message: str
    data: SampleData

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "message": "This is a sample response",
                    "data": {
                        "id": 1,
                        "name": "Sample Item",
                        "description": "A sample item for testing"
                    }
                }
            ]
        }
    }