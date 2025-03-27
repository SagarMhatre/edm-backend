from flask import Flask, jsonify, request
import os
from datetime import datetime, timezone
import requests

MCQUERY_API_URL=os.getenv('MCQUERY_API_URL')
MCQUERY_API_KEY=os.getenv('MCQUERY_API_KEY')
MCQUERY_API_KEY_HEADER=os.getenv('MCQUERY_API_KEY_HEADER')

app = Flask(__name__)

@app.route('/questionset/batch', methods=['POST'])
def create_questionset_with_questions():
    data = request.json

    # Extract questionset details
    questionset_id = data['questionsetid']
    name = data['name']
    description = data['description']
    questions = data['questions']

    # Insert into questionsets table
    questionset_item = {
        'questionsetId': questionset_id,
        'name': name,
        'description': description,
        'timestamp': datetime.now(timezone.utc).isoformat()
    }

    """
    We now make an API call 

    POST <MCQUERY_API_URL>/questionset/batch HTTP/1.1
    Content-Type: application/json
    <MCQUERY_API_KEY_HEADER>: <MCQUERY_API_KEY>
    Host: kong-5e30d406e3usadj2j.kongcloud.dev
    Content-Length: 741

    {
    "questionsetid": "dynamodb-basics-2503151722",
    "name": "DynamoDB Advanced Use Cases Quiz 3",
    "description": "A set of questions to test knowledge on advanced features and use cases of Amazon DynamoDB.",
    "questions": [
        {
        "text": "How do DynamoDB transactions ensure atomicity and consistency?",
        "choices": [
            {
            "text": "By allowing multiple operations to be executed atomically with ACID guarantees.",
            "targetedResponse": "Correct! DynamoDB transactions ensure all-or-nothing execution of multiple operations, maintaining atomicity and consistency.",
            "isCorrect": true
            }
        ],
        "tags": [
            "acid",
            "dynamodb",
            "atomicity"
        ]
        }
    ]
    }
    """

    # Prepare the headers and payload for the API call
    headers = {
        'Content-Type': 'application/json',
        MCQUERY_API_KEY_HEADER: MCQUERY_API_KEY
    }
    payload = {
        "questionsetid": questionset_id,
        "name": name,
        "description": description,
        "questions": questions
    }

    # Make the API call
    response = requests.post(MCQUERY_API_URL, headers=headers, json=payload)

    # Check if the API call was successful
    if response.status_code != 201:
        return jsonify({"error": "Failed to create questionset", "details": response.json()}), response.status_code

    # Return the API response
    return jsonify(response.json()), response.status_code

@app.route('/static/<path:filename>', methods=['GET'])
def serve_static(filename):
    return send_from_directory(os.path.join(app.root_path, 'static'), filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)