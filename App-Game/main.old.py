from modules.logger import setup_logger
from flask import Flask, request, jsonify, session
from flask_cors import CORS, cross_origin
import openai
from modules import openai_api_service, db_service, config
import datetime
import random
from time import sleep
import uuid

#start logger
logger = setup_logger(__name__)
logger.info("Logger is set up and running.")

# Load OpenAI API key
openai.api_key = config.openai_api_key

# Initialize the Flask app
app = Flask(__name__)
app.secret_key = "secret_key_phrase"
CORS(app, resources={r"/api/*": {"origins": "http://localhost:8080"}})

# Set up CORS headers
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

def level1_handle_level():
    logger.debug("starting Level 1")
    opening_text = "Welcome to the text-based adventure game! Would you like to start?\n"
    creative_prompt = "Welcome the player to the game in a single sentence. Welcome them in an such a way that is unexpected, smug, or pedantic"
    api_response = openai_api_service.openai_api_call("", creative_prompt)
    gametext = api_response + opening_text
    return gametext

def level2_handle_level(level, danger):
    logger.debug("starting Level 2")
    # should already have current game state from python because we just read it from the database
    # check current danger level
    if danger > 0:
        creative_prompt = "Describe a swarm of tiny creatures approaching, like a colony of ants or a flock of birds."
    if danger > 3:
        creative_prompt = "Describe a group of small creatures approaching, like a pack of wolves or a school of piranhas."
    if danger > 5:
        creative_prompt = "Describe a herd of large creatures approaching, like a stampede of elephants or a pod of whales."
    if danger > 8:
        creative_prompt = "Describe a massive creature approaching, like a giant dragon or a towering Godzilla-like monster."

    api_response = openai_api_service.openai_api_call("", creative_prompt)
    level_text = "You are a guard stationed in a remote outpost. You see a " + api_response + "rapidly approaching. They're headed to the city. You need to arrive to the castle and warn the king. What do you do?"
    gametext = level_text
    return gametext

def handle_option_a(danger):
    # Implement game logic for Option A
    # Decrease danger by 2, not going below 0
    danger = max(0, danger - 2)
    # Return a result (e.g., a string containing game text)
    return f"Option A chosen. Danger decreased by 2. Current danger level: {danger}"

def handle_option_b(danger):
    # Implement game logic for Option B
    # Increase danger by 2, not going above 10
    danger = min(10, danger + 2)
    # Return a result (e.g., a string containing game text)
    return f"Option B chosen. Danger increased by 2. Current danger level: {danger}"

# sets up the api endpoint for the front end to call
# Add this new route to handle the game start and user choices
@app.route("/api/game", methods=["POST"])
def handle_game():
    logger.debug("starting game session....")
    if not request.is_json:
        return "Invalid request, data must be in JSON format.", 400

    # pass the choice and active session_id from frontend to backend 
    choice = request.json.get("choice")
    session_id = request.json.get("session_id")

    # Initialize level and danger variables
    level = None
    danger = None

    # this section is for initial game setup, or in active game, collect the game state
    
    # Read the game state data from the database
    if session_id is not None:
        session_id, level, danger = db_service.read_from_database(session_id)
        logger.debug(f"checking session ID... is there a game state existing?: {session_id}")

    if session_id is None:
        session_id = str(uuid.uuid4())

    # If level and danger are not None, it means a game session was found in the database
    if level is not None and danger is not None:
        logger.debug(f"identified existing session_id: {session_id}")

    if level is None:
        level = 1
        danger = random.randint(1, 10)
        db_service.write_to_database(session_id, level, danger)

    logger.debug(f"Session after checking game_state: {session_id}")
    logger.debug(f"game_state: level, danger: {level, danger}")
    
    if choice is None:
        # this is a do nothing option, just wait for the user to make a choice A or B" 
        sleep(1)
        print("waiting for user to make a choice...")
        logger.info("logger reporting, waiting for user to make a choice...")

    # Run the function corresponding to the current level
    if level == 1:
        gametext = level1_handle_level()
        
    elif level == 2:
        gametext = level2_handle_level(level, danger)

    elif choice == "Option A":
        handle_option_a(danger)
        level += 1
    
    elif choice == "Option B":
        handle_option_a(danger)
        level += 1

        # Save the updated game state to the database
        db_service.write_to_database(session_id, level, danger)

    # Return the updated game text data to the frontend to display it
    return jsonify({"gametext": gametext, "session_id": session_id})
        
    #else:
    #    # This should not happen unless a condition occurs to end the game 
    #return jsonify({"gametext": "An error has occurred in backend!", "choices": []})
    
# This start_game function allows for the Flask API route to return session_id and player-option (a or b)
# this is currently doing nothing 
@app.route("/api/player-data", methods=["POST"])
def start_game():
    if not request.is_json:
        return "Invalid request, data must be in JSON format.", 400

    input_text = request.json.get("player-option")
    session_id = request.json.get("session_id")

    session_id = str(uuid.uuid4())
    return jsonify({"game_text": config.initial_game_text, "choices": config.initial_choices, "session_id": session_id})

#print("Testing the database connection...")
#db_service.test_db_connection()

if __name__ == "__main__":
    print("Running the app...")
    app.run(host="0.0.0.0", port=5000, debug=True)
