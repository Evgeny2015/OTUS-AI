from fastapi import APIRouter, HTTPException
from app.models.sample import SampleData, SampleResponse

router = APIRouter(
    prefix="/sample",
    tags=["sample"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=SampleResponse, summary="Get sample data",
         description="Retrieve sample data with predefined values")
async def get_sample():
    """Get sample data"""
    response = SampleResponse(
        message="This is a sample response",
        data=SampleData(id=1, name="Sample Item")
    )
    return response

@router.post("/", response_model=SampleResponse, summary="Create sample item",
          description="Create a new sample item with the provided data")
async def create_sample(sample_data: SampleData):
    """Create a new sample item"""
    return SampleResponse(
        message="Sample item created successfully",
        data=sample_data
    )