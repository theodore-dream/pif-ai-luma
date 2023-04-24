from modules.logger import setup_logger
from flask import Flask, request, jsonify, session
from flask_cors import CORS, cross_origin
import openai
from modules import openai_api_service, db_service, config
import datetime
import random
from time import sleep

## setup level functions into another file is a longer term goal

#level_functions = {
#   1: level1,
#    2: level2,
#    # ...
#    10: level10,
#}

#start logger
logger = setup_logger(__name__)
logger.info("Logger is set up and running.")

# using python built in logger to setup logging
#logger = setup_logger("app")

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
    opening_text = "Welcome to the text-based adventure game! Would you like to start?\n"
    creative_prompt = "Welcome the player to the game in a single sentence. Welcome them in an such a way that is unexpected, smug, or pedantic"
    api_response = openai_api_service.openai_api_call("", creative_prompt)
    gametext = api_response + opening_text
    return gametext

def level2_handle_level():
    # should already have current game state from python because we just read it from the database
    # check current danger level
    if current_state.danger > 0:
        creative_prompt = "Describe a swarm of tiny creatures approaching, like a colony of ants or a flock of birds."
    if current_state.danger > 3:
        creative_prompt = "Describe a group of small creatures approaching, like a pack of wolves or a school of piranhas."
    if current_state.danger > 5:
        creative_prompt = "Describe a herd of large creatures approaching, like a stampede of elephants or a pod of whales."
    if current_state.danger > 8:
        creative_prompt = "Describe a massive creature approaching, like a giant dragon or a towering Godzilla-like monster."

    api_response = openai_api_service.openai_api_call("", creative_prompt)
    level_text = "You are a guard stationed in a remote outpost. You see a " + api_response + "rapidly approaching. They're headed to the city. You need to arrive to the castle and warn the king. What do you do?"
    gametext = level_text
    return gametext

# This function is designed to be modular so that it can be used for any game state transaction
# Save the prompt, game text, options, and other game state data to the database
# This needs to be updated so that only the data this is available is saved, otherwise skip
def save_game_state(session_id, level, danger, creative_prompt, api_response):
    db_service.write_to_database(session_id, level, danger, "prompt", creative_prompt)
    db_service.write_to_database(session_id, level, danger, "gametext", api_response)
    db_service.write_to_database(session_id, level, danger, "player-optiona", "Option A")
    db_service.write_to_database(session_id, level, danger, "player-optionb", "Option B")

# before we start the game, but after defining the sessions functions, we set level functions
level_functions = {
    1: level1_handle_level,
    2: level2_handle_level,
}

# sets up the api endpoint for the front end to call
# Add this new route to handle the game start and user choices
@app.route("/api/game", methods=["POST"])
def handle_game():
    if not request.is_json:
        return "Invalid request, data must be in JSON format.", 400

    choice = request.json.get("choice")
    session_id = request.json.get("session_id")
    
    if not session.get("game_state"):
        session["game_state"] = {
            "level": 1,
            "danger": random.randint(1, 10)
        }
    
    game_state = session["game_state"]
    level = game_state["level"]
    danger = game_state["danger"]
    
    if choice == "make a choice":
        # this is a do nothing option, just wait for the user to make a choice A or B" 
        sleep(5)
        print("waiting for user to make a choice...")
        logger.info("logger reporting, waiting for user to make a choice...")
        sleep(20)

    elif choice == "Option A" or choice == "Option B":
        # Get the game state data from the database
        game_state = db_service.read_from_database(session_id, level, danger, "*")
        # Determine the current state based on level and danger... need to figure out how to use it 
        print(game_state)
        
        # Run the function corresponding to the current level
        if level in level_functions:
            gametext = level_functions[level]()
            level += 1
        else:
            return jsonify({"gametext": "Invalid level. An error has occurred!", "choices": [], "level": level, "danger": danger})

        # Save the updated game state to the database
        save_game_state(session_id, level, danger, "", gametext)

        # Return the updated game text data to the frontend to display it
        return jsonify({"game_text": gametext})
    else:
        # This should not happen unless a condition occurs to end the game 
        return jsonify({"gametext": "An error has occurred in backend!", "choices": []})
    
# This start_game function allows for the Flask API route to return session_id and player-option (a or b)
@app.route("/api/submit-text", methods=["POST"])
def start_game():
    if not request.is_json:
        return "Invalid request, data must be in JSON format.", 400

    input_text = request.json.get("player-option")
    session_id = request.json.get("session_id")

    return jsonify({"game_text": config.initial_game_text, "choices": config.initial_choices})

#print("Testing the database connection...")
#db_service.test_db_connection()

if __name__ == "__main__":
    print("Running the app...")
    app.run(host="0.0.0.0", port=5000, debug=True)
