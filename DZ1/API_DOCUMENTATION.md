# API Documentation

## GET /api/v1/questions/

Retrieves a list of survey questions.

### Response
```json
{
  "message": "Successfully retrieved questions",
  "data": [
    {
      "id": 1,
      "text": "What is your favorite color?",
      "type": "multiple_choice",
      "options": ["Red", "Blue", "Green", "Yellow"]
    },
    // ... more questions
  ]
}
```

## POST /api/v1/answers

Submits answers to survey questions.

### Request Body
```json
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
```

### Response
```json
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
    },
    {
      "question_id": 3,
      "answer": "More customization options"
    }
  ]
}
```

### Notes
- Answers are stored in memory and will be lost when the server restarts
- The `answer` field can be a string for single answers or an array of strings for multiple selections