import logging
from flask import Flask, jsonify, request
import os
from datetime import datetime, timezone
import requests

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

MCQUERY_API_URL = os.getenv('MCQUERY_API_URL')
MCQUERY_API_KEY = os.getenv('MCQUERY_API_KEY')
MCQUERY_API_KEY_HEADER = os.getenv('MCQUERY_API_KEY_HEADER')

app = Flask(__name__)

@app.route('/questionset/batch', methods=['POST'])
def create_questionset_with_questions():
    logging.info("Received request to create questionset with questions.")
    
    try:
        data = request.json
        logging.debug(f"Request JSON payload: {data}")

        # Extract questionset details
        questionset_id = data['questionsetid']
        name = data['name']
        description = data['description']
        questions = data['questions']
        logging.info(f"Extracted questionset details: ID={questionset_id}, Name={name}, Description={description}")

        # Insert into questionsets table
        questionset_item = {
            'questionsetId': questionset_id,
            'name': name,
            'description': description,
            'timestamp': datetime.now(timezone.utc).isoformat()
        }
        logging.debug(f"Questionset item prepared for insertion: {questionset_item}")

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
        logging.debug(f"API call headers: {headers}")
        logging.debug(f"API call payload: {payload}")

        # Make the API call
        logging.info(f"Making API call to {MCQUERY_API_URL}")
        response = requests.post(MCQUERY_API_URL, headers=headers, json=payload)
        logging.info(f"API call completed with status code: {response.status_code}")

        # Check if the API call was successful
        if response.status_code != 201:
            logging.error(f"Failed to create questionset. Response: {response.json()}")
            return jsonify({"error": "Failed to create questionset", "details": response.json()}), response.status_code

        # Return the API response
        logging.info("Questionset created successfully.")
        return jsonify(response.json()), response.status_code

    except Exception as e:
        logging.exception("An error occurred while processing the request.")
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

@app.route('/static/<path:filename>', methods=['GET'])
def serve_static(filename):
    return send_from_directory(os.path.join(app.root_path, 'static'), filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)