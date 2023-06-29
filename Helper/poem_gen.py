import datetime
import random
from decimal import Decimal
from time import sleep
import uuid
import tiktoken

import logging
import datetime
import os
import openai
import nltk
from modules import create_vars
from nltk.probability import FreqDist

from modules.logger import setup_logger

#start logger
logger = setup_logger("poem_gen")
logger.info("Logger is set up and running.")

nltk.download('wordnet')
from nltk.corpus import wordnet as wn

logging.basicConfig(level=logging.INFO)
openai.api_key = os.getenv("OPENAI_API_KEY")

def api_create_poem(steps_to_execute, creative_prompt, persona, lang_device, abstract_concept, randomness_factor):

    all_steps = {
        0: {"role": "system", "content": persona },
        #0: {"role": "system", "content": "you create poetry." },
        1: {"role": "user", "content": "Step 1: Produce three different versions of a poem inspired by the following: " + creative_prompt + ". Each poem can be three or four lines long. Each version should have a different structure - rhyme, free verse, sonnet, haiku, etc. Explain the changes made for each iteration before printing the result for each step."},
        2: {"role": "user", "content": "Step 2: The chosen abstract concept is: " + abstract_concept + ". Next you evaluate the revisions and determine which most closely has a deep connection to then chosen concept, or could most elegantly be modified to fit the concept."},
        3: {"role": "user", "content": "Step 3: Create a new poem that is two to four lines long with the following parameters: Revise the selected poem to subtly weave in the chosen concept."},
        4: {"role": "user", "content": "Next Step: Create a new poem that is two to four lines long with the following parameters: Revise the selected poem to more closely match your own personality and writing technique."},
        5: {"role": "user", "content": "Next Step: Create a new poem that is two to four lines long with the following parameters: Consider how you could use this linguistic device: "  + lang_device + ". Revise the poem to incorporate the linguistic device"},
        6: {"role": "user", "content": "Next Step: Create a single new poem that is two to four lines long with the following parameters: Introduce variation to reduce overall consistency in tone, language use, and sentence structure."},
    }

    steps_for_api = [all_steps[step] for step in steps_to_execute]
    i = 0
    for i, step in enumerate(steps_for_api):
        logger.debug("Step %d: %s", i+1, step)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=steps_for_api,
        max_tokens=2000,
        n=1,
        stop=None,
        temperature=(2 * randomness_factor),
    )

    
    # print information about api call
    logging.debug(f"persona: {persona}")
    logging.debug(f"abstract_concept: {abstract_concept}")
    logging.debug(f"creative_prompt: {creative_prompt}")
    return response

def parse_response():
    # set a randomness factor between 0 and 1. Placeholder, will be logic for the buttons
    randomness_factor = 0.6
    creative_prompt = create_vars.gen_creative_prompt(create_vars.gen_random_words(randomness_factor), randomness_factor)
    abstract_concept = create_vars.get_abstract_concept()
    persona = create_vars.build_persona()
    lang_device = create_vars.get_lang_device()
    logger.debug(f"lang_device is: {lang_device}")
    logger.debug(f"abstract_concept is: {abstract_concept}")
    logger.debug(f"randomness factor is: {randomness_factor}")
    logger.debug(f"==========================")
    logger.debug(f"running pif_poetry_generator with prompt: {creative_prompt}")



    # set the number of steps you want here
    api_response = api_create_poem([0, 1, 2, 3],creative_prompt, persona, lang_device, abstract_concept, randomness_factor)
    if api_response['choices'][0]['message']['role'] == "assistant":
        api_response_content = api_response['choices'][0]['message']['content'].strip()
    else:
        api_response_syscontent = api_response['system'].strip()  # put into a var for later use 
    print("-" * 30)

    logger.info(f"Prompt tokens: {api_response['usage']['prompt_tokens']}")
    logger.info(f"Completion tokens: {api_response['usage']['completion_tokens']}")
    logger.info(f"Total tokens: {api_response['usage']['total_tokens']}")

    logger.info(f"api_response_content: {api_response_content}")

    print("-" * 30)
    logger.debug("poem_gen completed successfully")
    #return api_response_content

if __name__ == "__main__":
    parse_response()

    ## variables overview - goals
    ## build_persona - bad, needs more work / further testing, only seems to perhaps be effective with very few steps, 1-2 steps tops 
    ## get_random_words - OK, creates too many words, needs to be fewer words, create an entropy variable from 0-1 and use that to determine how many words to create
    ## get_abstract_concept - good, needs more work, the words are showing up too much in the poetry, use nltk to find synonyms and use those instead
    ## get_lang_device - seems good but needs more testing
    ## ?incorporate the lyrics api into the poetry generator? prob save for a stage 2 
    ## poetic_goal ? - set up a new variable that defines a poetic goal

    ## other assorted ideas
    ## ====================
    ## seed the database with a script that pulls from nltk and compiles lists of words
    ## could use nltk to find synonyms for the words in the abstract concept list to seed that to the DB
    ## could find a list of meme related words somewhere, create categories, tags, individual columns or tables, etc.