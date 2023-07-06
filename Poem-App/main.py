from modules.logger import setup_logger
from flask import Flask, request, jsonify, session
from flask_cors import CORS, cross_origin
import openai
from modules import openai_api_service, db_service, setup_utils, poem_gen, luma_write, intro_vars
import datetime
import random
from decimal import Decimal, ROUND_DOWN
from time import sleep
import uuid
import time

#start logger
logger = setup_logger("main.py")
logger.info("Logger is set up and running.")

# maybe flash the entropy level on the screen for a second or two, along with a random persona?
def poetry_game_intro(entropy):
    logger.debug("starting introduction")
    opening_text1 = intro_vars.opening_text1
    opening_text2 = intro_vars.opening_text2 
    opening_text3  = intro_vars.opening_text3 
    print()
    luma_write.luma_write(opening_text1, 5)
    luma_write.luma_write(opening_text2, 2)
    luma_write.luma_write(opening_text3, 2)
    logger.debug("opening text written to luma")
    creative_prompt = "Welcome the player to the poetry game in a single sentence. Welcome them in an such a way that is unexpected, smug, or pedantic"
    api_response = openai_api_service.openai_api_call("", creative_prompt, entropy)
    # print information about api_response data type
    print("api_response type = " + str(type(api_response)))
    # this is the text that gets saved to the DB, I guess whatever is custom
    print(opening_text1)
    print(api_response)
    gametext = api_response 
    return gametext

def poetry_gen_loop(entropy):
    # check current entropy level
    #api_response = openai_api_service.openai_api_call("", creative_prompt, entropy)
    #level_text = "Your poem is " + api_response + "--end poem--"
    gametext = poem_gen.parse_response(entropy)
    print("gametext = " + gametext)
    return gametext

def handle_option_a(entropy):
    # Implement game logic for Option A
    # Decrease entropy by .1, not going below 0
    entropy = max(Decimal('0.0'), entropy - Decimal('0.1'))
    # Return a result (e.g., a string containing game text)
    return entropy
    

def handle_option_b(entropy):
    # Implement game logic for Option B
    # Increase entropy by .1, not going above 1
    #entropy = min(1.0, float(entropy) + 0.1)
    entropy = min(Decimal('1.0'), entropy + Decimal('0.1'))
    # Return a result (e.g., a string containing game text)
    return entropy
    

def run_game():
    # running game 
    persona, session_state, gametext, entropy, session_id = maintain_game_state()
    # first lets get the game status 

    #if choice is None:
    #    # this is a do nothing option, just wait for the user to make a choice A or B" 
    #    sleep(1)
    #    print("waiting for user to make a choice...")
    #    logger.info("logger reporting, waiting for user to make a choice...")

    # Run the intro function or the poetry loop 
    if session_state == "new":
        gametext = poetry_game_intro(entropy)
        logger.debug(f"poetry game intro starting now...")
        session_state = "active"
        db_service.write_to_database(session_id, session_state, entropy)
        
    elif session_state == "active":
        logger.debug(f"runing poetry_gen_loop, current entropy is: {entropy}")
        gametext = poetry_gen_loop(float(entropy))
        db_service.write_to_database(session_id, session_state, entropy)

    # placeholder 
    choice = "Option B"

    if choice == "Option A":
        entropy = handle_option_a(entropy)
        logger.debug(f"Option A chosen. entropy decreased by .1. Current entropy level: {entropy}")
        db_service.write_to_database(session_id, session_state, entropy)
    
    elif choice == "Option B":
        entropy = handle_option_b(entropy)
        logger.debug(f"Option B chosen. entropy increased by .1. Current entropy level: {entropy}")
        db_service.write_to_database(session_id, session_state, entropy)


    # Save the updated game state to the database
    #db_service.save_game(session_id, level, entropy)
    #logger.debug(f"saving updated game state, state is currently session, level, entropy: {session_id, level, entropy}")

    # Return the updated game text data to luma to display on the screen
    luma_write.luma_write(gametext, 30)
    logger.debug("sent to luma")
    logger.debug("gametext is" + gametext)



def maintain_game_state():
    # latest game status
    logger.debug("running game status check....")

    # check for ID on filesystem, very rudementary version of a config file/system
    # can only create new sessions for first implementation, not resume old ones
    session_id = setup_utils.get_or_create_uuid()
    print("session_id = " + session_id)

    # temporarily for all new games, no initial session state
    logger.debug(f"reading session data from DB: {session_id}")
    persona, session_state, gametext, entropy, session_id = db_service.read_from_database(session_id)
    logger.debug(
        "Session data after read from DB - Session ID: {}, Persona: {}, Session State: {}, Game Text: {}, Entropy: {}".format(
            session_id, persona, session_state, gametext, entropy
        )
    )

    # If session_state is None, it means an active game session was not found, lets create one and save it
    if session_state is None:
        session_state = "new"
        # entropy is a random decimal from 0.00 to 1.00 with 1-2 decimal places
        entropy = Decimal(str(random.uniform(0.0, 0.9))).quantize(Decimal('0.00'), rounding=ROUND_DOWN)
        # lets save initial game state 
        db_service.write_to_database(session_id, session_state, entropy)

    return persona, session_state, gametext, entropy, session_id, 

if __name__ == "__main__":
   
   # temporarily using this hacky approach
   try:
        while True:
            run_game()
            time.sleep(1)  # optional delay if you want to run the function with intervals
   except KeyboardInterrupt:
            print("\nProgram has been stopped by the user.")

# main interaction is just left and right button increasing and decreasing entropy 

