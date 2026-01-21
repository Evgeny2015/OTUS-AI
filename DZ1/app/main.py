from fastapi import FastAPI
from app.api.routes import sample, questions, answers
from app.core.config import settings

app = FastAPI(
    title=settings.app_name,
    description="A simple API built with FastAPI",
    version="1.0.0"
)

app.include_router(sample.router, prefix="/api/v1")
app.include_router(questions.router, prefix="/api/v1")
app.include_router(answers.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Welcome to the Sample API"}