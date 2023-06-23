from modules.logger import setup_logger
from flask import Flask, request, jsonify, session
from flask_cors import CORS, cross_origin
import openai
from modules import openai_api_service, db_service, config, luma_write
import datetime
import random
from decimal import Decimal
from time import sleep
import uuid

#start logger
logger = setup_logger(__name__)
logger.info("Logger is set up and running.")

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

from decimal import Decimal

def handle_option_a(entropy):
    # Implement game logic for Option A
    # Decrease entropy by .1, not going below 0
    entropy = max(Decimal('0.0'), entropy - Decimal('0.1'))
    # Return a result (e.g., a string containing game text)
    return entropy
    

def handle_option_b(entropy):
    # Implement game logic for Option B
    # Increase entropy by .1, not going above 1
    entropy = min(Decimal('1.0'), entropy + Decimal('0.1'))
    # Return a result (e.g., a string containing game text)
    return entropy
    

# no flask endpoint, simply a function that writes to the oled using luma
def handle_game():
    logger.debug("starting game session....")

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
        entropy = handle_option_a(entropy)
        level += 1
        logger.debug(f"Option A chosen. entropy decreased by .1. Current entropy level: {entropy}")
    
    elif choice == "Option B":
        entropy = handle_option_b(entropy)
        level += 1
        logger.debug(f"Option B chosen. entropy increased by .1. Current entropy level: {entropy}")

    # Save the updated game state to the database
    db_service.save_game(session_id, level, entropy)
    logger.debug(f"saving updated game state, state is currently session, level, entropy: {session_id, level, entropy}")

    # Return the updated game text data to luma to display on the screen
    luma_write(gametext)
  
    logger.debug("sent to luma")
   

if __name__ == "__main__":
    handle_game()