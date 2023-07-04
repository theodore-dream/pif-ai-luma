import time
import random
from decimal import Decimal
from time import sleep

import logging
import os
import openai
import nltk
from modules import create_vars
from nltk.probability import FreqDist
import json
from tenacity import retry, wait_random_exponential, stop_after_attempt


from modules.logger import setup_logger

#start logger
logger = setup_logger("poem_gen")
logger.info("Logger is set up and running.")

nltk.download('wordnet')
from nltk.corpus import wordnet as wn

logging.basicConfig(level=logging.INFO)
openai.api_key = os.getenv("OPENAI_API_KEY")

def api_poem_pipeline(creative_prompt, persona, randomness_factor, abstract_concept):
    logging.debug(f"creative_prompt: {creative_prompt}")
    step_1_poem = poem_step_1(creative_prompt, persona, randomness_factor)
    logger.debug (f"step_1_poem: {step_1_poem}")
    step_2_poem = poem_step_2(persona, randomness_factor, step_1_poem, abstract_concept)
    logger.debug (f"step_2_poem: {step_2_poem}")
    step_3_poem = poem_step_3(persona, randomness_factor, step_2_poem)
    logger.debug (f"step_3_poem: {step_3_poem}")
    return step_3_poem

@retry(wait=wait_random_exponential(min=1, max=40), stop=stop_after_attempt(3))
def poem_step_1(creative_prompt, persona, randomness_factor):
    MAX_RETRIES = 5  # Set max retry limit
    for i in range(MAX_RETRIES):
        #try:
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": persona + " You write a poem."},
                    {"role": "user", "content": "Produce a haiku inspired by the following words: " + creative_prompt + ""},
                    #{"role": "user", "content": "Explain why you created the poem the way you did."},
                ], 
                temperature=(randomness_factor * 2),
                max_tokens=2000,
            )

            if completion['choices'][0]['message']['role'] == "assistant":
                step_1_poem = completion['choices'][0]['message']['content'].strip()
            else:
                step_1_syscontent = api_response['system'].strip()  # put into a var for later use 
            print("-" * 30)
            print(step_1_poem)
            return step_1_poem

@retry(wait=wait_random_exponential(min=1, max=40), stop=stop_after_attempt(3))
def poem_step_2(persona, randomness_factor, step_1_poem, abstract_concept):
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": persona + " You write a poem based on parameters provided as well as input text to build on."},
                    {"role": "user", "content": "Create a new poem based on the input text that is two to four lines long with the following parameters. The chosen abstract concept is: " + abstract_concept + ". Revise the input text to subtly weave in the chosen concept."},
                    {"role": "user", "content": "Input text: " + step_1_poem},
                ],
                temperature=(randomness_factor * 2),
                max_tokens=2000,
            )

            if completion['choices'][0]['message']['role'] == "assistant":
                step_2_poem = completion['choices'][0]['message']['content'].strip()
            else:
                step_2_syscontent = completion['system'].strip()  # put into a var for later use 
            print("-" * 30)
            return step_2_poem

@retry(wait=wait_random_exponential(min=1, max=40), stop=stop_after_attempt(3))
def poem_step_3(persona, randomness_factor, step_2_poem):
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": persona + " You write a poem based on parameters provided as well as input text to build on."},
                    {"role": "user", "content": "Create a new poem based on the input text that is two to four lines long with the following parameters. Introduce variation to reduce overall consistency in tone, language use, and sentence structure."},
                    {"role": "user", "content": "Input text: " + step_2_poem},
                    {"role": "user", "content": "Explain why you created the poem the way you did."},
                ],
                temperature=(randomness_factor * 2),
                max_tokens=2000,
            )

            if completion['choices'][0]['message']['role'] == "assistant":
                step_3_poem = completion['choices'][0]['message']['content'].strip()
            else:
                step_3_syscontent = api_response['system'].strip()  # put into a var for later use 
            print("-" * 30)
            return step_3_poem


def api_create_poem(steps_to_execute, creative_prompt, persona, lang_device, abstract_concept, randomness_factor):

    # first we setup the steps for the api call, but now these need to be broken up into functions that can each be called as seperate api calls" 
    all_steps = {
        0: {"role": "system", "content": persona + " You write poems. Explicity state what step you are on and explain the changes made for each step before proceeding to the next step."},
        1: {"role": "user", "content": "Step 1: Produce three different versions of a poem inspired by the following: " + creative_prompt + ". Each poem can be three or four lines long. Each version should have a different structure - rhyme, free verse, sonnet, haiku, etc."},
        2: {"role": "user", "content": "Step 2: The chosen abstract concept is: " + abstract_concept + ". Next you evaluate the revisions and determine which most closely has a deep connection to then chosen concept, or could most elegantly be modified to fit the concept."},
        3: {"role": "user", "content": "Step 3: Create a new poem that is two to four lines long with the following parameters: Revise the selected poem to subtly weave in the chosen concept."},
        #4: {"role": "user", "content": "Step 4: Print five equals signs."},
        #5: {"role": "user", "content": "Step 5: Create a new poem that is two to four lines long with the following parameters: Introduce variation to reduce overall consistency in tone, language use, and sentence structure."},
        #4: {"role": "user", "content": "Step 4: Create a new poem that is two to four lines long with the following parameters: Revise the selected poem to achieve a poetic goal of expressing vivid imagery or evoking a specific emotion."},
        #5: {"role": "user", "content": "Step 5: Create a new poem that is two to four lines long with the following parameters: Consider how you could use this linguistic device: "  + lang_device + ". Revise the poem to incorporate the linguistic device"},
        
    }


    # steps need to be broken up anyways so will likely completely remove this logic 
    steps_for_api = [all_steps[step] for step in steps_to_execute]
    i = 0
    for i, step in enumerate(steps_for_api):
        logger.debug("Step %i: %s", i+1, step)


    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=steps_for_api,
        max_tokens=3600,
        n=1,
        stop=None,
        temperature=(2 * randomness_factor),
    )


    # print information about api call
    #logger.debug(f"persona: {persona}")
    #logger.debug(f"abstract_concept: {abstract_concept}")
    #logger.debug(f"creative_prompt: {creative_prompt}")
    return response



def parse_response():
    # set a randomness factor between 0 and 1. Placeholder, will be logic for the buttons
    randomness_factor = 0.8
    creative_prompt = create_vars.gen_creative_prompt(create_vars.gen_random_words(randomness_factor), randomness_factor)
    abstract_concept = create_vars.get_abstract_concept()
    persona = create_vars.build_persona()
    lang_device = create_vars.get_lang_device()

    logger.debug(f"persona is: {persona}")
    logger.debug(f"lang_device is: {lang_device}")
    logger.debug(f"abstract_concept is: {abstract_concept}")
    logger.debug(f"randomness factor is: {randomness_factor}")

    logger.debug(f"==========================")
    logger.debug(f"creative_starting_prompt: {creative_prompt}")

    poem_result = api_poem_pipeline(creative_prompt, persona, randomness_factor, abstract_concept)
    logger.debug(f"poem result:\n{poem_result}")


    # set the number of steps you want here
    #api_response = api_create_poem([0, 1, 2, 3],creative_prompt, persona, lang_device, abstract_concept, randomness_factor)
    #if api_response['choices'][0]['message']['role'] == "assistant":
    #    api_response_content = api_response['choices'][0]['message']['content'].strip()
    #else:
    #    api_response_syscontent = api_response['system'].strip()  # put into a var for later use 
    #print("-" * 30)

    #logger.info(f"Prompt tokens: {api_response['usage']['prompt_tokens']}")
    #logger.info(f"Completion tokens: {api_response['usage']['completion_tokens']}")
    #logger.info(f"Total tokens: {api_response['usage']['total_tokens']}")

    #logger.info(f"api_response_content: {api_response_content}")

    print("-" * 30)
    logger.debug("poem_gen completed successfully")
    #return api_response_content

if __name__ == "__main__":
    parse_response()


    # add tokens cost logging
    # remove the explanation for the poems its too much, useless tokens spend 
    # add proper retry logic again... I guess. Just add it to the whole thing. 

    # current issue is that there are 6 steps, 7 including the persona, and its too much complexity for the api to handle all of it
    # on the other hand the results are really good it seesm to only be going to step 3, maybe at this point I need to focus on
    # either I just want to output the final poem directly from the api but that could get dicey at different temperatures
    # alternatively I could use logic to modify the output from the api to get the final poem only. Will need to experiment on diff temps. 

    ## variables overview - goals
    ## build_persona - bad, needs more work / further testing, only seems to perhaps be effective with very few steps, 1-2 steps tops 
    ## get_random_words - happy with number of words because I modifed the api call to generate shorter sentence 
    ## get_abstract_concept - good, using a list and nltk to find synonyms
    ## delayed - poetic_goal ? - experimenting with this, seems like its stopping at step 3 and its step 4 now
    ## delayed - get_lang_device - seems good but needs more testing, might need to push this off for now, might be unnecesary, too much logic in a single prompt 
    ## delayed - ?incorporate the lyrics api into the poetry generator? prob save for a stage 2 

    ## other assorted ideas
    ## ====================
    ## seed the database with a script that pulls from nltk and compiles lists of words
    ## could use nltk to find synonyms for the words in the abstract concept list to seed that to the DB
    ## could find a list of meme related words somewhere, create categories, tags, individual columns or tables, etc.