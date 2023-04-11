from modules.logger import setup_logger
from flask import Flask, request, jsonify
import openai
from modules import openai_api_service, db_service, config
import datetime

# using python built in logger to setup logging
logger = setup_logger("app")

# Load OpenAI API key
openai.api_key = config.openai_api_key

# Initialize the Flask app
app = Flask(__name__)

# sets up the api endpoint for the front end to call
@app.route("/api/submit-text", methods=["POST"])
def generate_poem():
    if not request.is_json:
        return "Invalid request, data must be in JSON format.", 400

    input_text = request.json.get("input_text")

    # Call the OpenAI API to generate a poem based on the user input
    response = openai_api_service.generate_poem_prompt(input_text, config.creative_prompt)

    # Extracting information
    generated_poem = response.choices[0].message['content']
    model = response.model
    role = response.choices[0].message['role']
    finish_reason = response.choices[0].finish_reason

    # Save the poem to the database
    db_service.save_poem_to_database(generated_poem)

    # Return the generated poem in the HTTP response
    return jsonify({"poem": generated_poem})

print("Testing the database connection...")
db_service.test_db_connection()

if __name__ == "__main__":
    print("Running the app...")
    app.run(host="app", port=5000, debug=True)
