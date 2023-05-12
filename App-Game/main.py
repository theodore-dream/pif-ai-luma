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

def poetry_game_intro(entropy):
    logger.debug("starting introduction")
    opening_text = " Welcome to the poetry game! Would you like to start?\n"
    creative_prompt = "Welcome the player to the poetry game in a single sentence. Welcome them in an such a way that is unexpected, smug, or pedantic"
    api_response = openai_api_service.openai_api_call("", creative_prompt, entropy)
    gametext = api_response + opening_text
    return gametext

def poetry_gen_apollo(level, entropy):
    logger.debug("starting peom generation")
    # should already have current game state from python because we just read it from the database
    # check current entropy level
    if entropy > 0:
        creative_prompt = "make a poem."
    if entropy > .3:
        creative_prompt = "make an interesting poem"
    if entropy > .5:
        creative_prompt = "make a strange poem."
    if entropy > .7:
        creative_prompt = "make a really really weird and random poem."

    logger.debug(f"runing poetry_gen_apollo, current entropy is: {entropy}")
    api_response = openai_api_service.openai_api_call("", creative_prompt, entropy)
    level_text = "Your poem is " + api_response + "--end poem--"
    gametext = level_text
    return gametext

def handle_option_a(entropy):
    # Implement game logic for Option A
    # Decrease entropy by .1, not going below 0
    entropy = max(0, entropy - .1)
    # Return a result (e.g., a string containing game text)
    return entropy
    #return f"Option A chosen. entropy decreased by .1. Current entropy level: {entropy}"

def handle_option_b(entropy):
    # Implement game logic for Option B
    # Increase entropy by 1, not going above 1
    entropy = min(1, entropy + .1)
    # Return a result (e.g., a string containing game text)
    return entropy
    #return f"Option B chosen. entropy increased by .1. Current entropy level: {entropy}"

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

    # Initialize level and entropy variables
    level = None
    entropy = None

    # this section is for initial game setup, or in active game, collect the game state
    
    # Read the game state data from the database
    if session_id != "":
        session_id, level, entropy = db_service.read_from_database(session_id)
        logger.debug(f"checking session ID... found existing session: {session_id}")

    if session_id is "":
        session_id = str(uuid.uuid4())

    # If level and entropy are not None, it means a game session was found in the database
    if level is not None and entropy is not None:
        logger.debug(f"identified existing session_id: {session_id}")

    # If level is None, it means a game session was not found, lets create one and save it
    if level is None:
        level = 1
        entropy = random.uniform(.1, .9)
        db_service.write_to_database(session_id, level, entropy)

    logger.debug(f"Session after checking game_state: {session_id}")
    logger.debug(f"game_state: level, entropy: {level, entropy}")
    
    #if choice is None:
    #    # this is a do nothing option, just wait for the user to make a choice A or B" 
    #    sleep(1)
    #    print("waiting for user to make a choice...")
    #    logger.info("logger reporting, waiting for user to make a choice...")

    # Run the function corresponding to the current level
    if level == 1:
        gametext = poetry_game_intro(entropy)
        logger.debug(f"poetry game intro starting now...")
        
    elif level >= 2:
        gametext = poetry_gen_apollo(level, entropy)
        logger.debug(f"now running level 2...")

    if choice == "Option A":
        handle_option_a(entropy)
        level += 1
    
    elif choice == "Option B":
        handle_option_a(entropy)
        level += 1

    # Save the updated game state to the database
    db_service.save_game(session_id, level, entropy)
    logger.debug(f"saving updated game state, state is currently session, level, entropy: {session_id, level, entropy}")

    # Return the updated game text data to the frontend to display it
    return jsonify({"gametext": gametext, "session_id": session_id})
    logger.debug("sent to frontend")
        
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
