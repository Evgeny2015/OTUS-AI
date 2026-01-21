import requests
import json

# Define the URL for the answers endpoint
url = "http://127.0.0.1:8000/api/v1/questions/answers"

# Define the answers data
answers_data = {
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

# Send the POST request
response = requests.post(url, json=answers_data)

# Print the response
print(f"Status Code: {response.status_code}")
print(f"Response: {response.json()}")