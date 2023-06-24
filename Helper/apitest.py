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

logging.basicConfig(level=logging.INFO)
openai.api_key = os.getenv("OPENAI_API_KEY")

abstract_concepts = ["sensuality", "grace", "mundanity", "transcendence", "mortality", "morality", "transience",]
linguistic_styles = ["metaphor", "simile", "Personification", "allegory", "idiom", "Anachronism" ]

#array of abstract objects goes here

def openai_api_call(creative_prompt):

# var setup and print
    abstract_concept = random.choice(abstract_concepts)

# API call
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            #{"role": "user", "content": creative_prompt},
            {"role": "user", "content": "Step 1: Produce three different versions of a poem that about: " + creative_prompt + ". Each poem can be three or four lines long" + "Each version should have a different structure - rhyme, free verse, sonnet, haiku, etc. Explain the changes made for each iteration before printing the result for each step."},
            {"role": "user", "content": "Step 2: Iterate over each version, revising and modifying to reduce consistency and introduce variation in the language, while maintaining coherence. Alter the tone and mood of each version."},
            {"role": "user", "content": "Step 3: The chosen abstract concept is: " + abstract_concept + ". Next you evaluate the revisions and determine which most closely has a deep connection to then chosen concept, or could most elegantly be modified to fit the concept."},
            {"role": "user", "content": "Step 4: Create a new poem that is two to four lines long with the following parameters: Revise the selected poem to subtly weave in the chosen concept."},
            {"role": "user", "content": "Step 5: Create a new poem that is two to four lines long with the following parameters: Revise the selected poem to to enhance the connection to the abstract concept."},
            {"role": "user", "content": "Step 6: Create a new poem that is two to four lines long with the following parameters: Review this list of linguistic devices: "  + ', '.join(linguistic_styles) + ". Determine which linguistic device would most contribute to the poem. Revise the poem to incorporate the chosen linguistic device"},
            {"role": "user", "content": "Step 7: Create a new poem that is two to four lines long with the following parameters: Introduce variation to reduce overall consistency in tone, language use, and sentence structure."},
        ],
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=1.2,
    )
    # Extracting information
    
    api_response = response['choices'][0]['message']
    model = response.model
    role = api_response['role']
    finish_reason = response.choices[0].finish_reason
    print(f"finish_reason: {finish_reason}")

    print(f"abstract_concept: {abstract_concept}")
    print(f"creative_prompt: {creative_prompt}")

    # Get current timestamp
    current_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return api_response

def promptgen():
    creative_prompt = "a glimpse through the veil and you pierce me in blue eyes, in stained sheets, in annoyed looks, in moments of ecstasy and in panic"
    return creative_prompt

def poetry_gen_rosemary(creative_prompt):
    print("log: starting peom generation")
    print(f"running poetry_gen_rosemary with prompt: {creative_prompt}")
    api_response = openai_api_call(creative_prompt)
    return api_response

def apitest():
    promptgen()
    api_response = poetry_gen_rosemary(promptgen())
    if api_response['role'] == "assistant":  # only passing on assistant's messages
        api_response_content = api_response['content'].strip()
    else:
        api_response_syscontent = api_response['system'].strip()  # put into a var for later use 
    print("-" * 30)
#    print(f"api_response: {api_response}")
    print("-" * 30)
    num_tokens = num_tokens_from_messages([api_response])
    print(f"Number of tokens: {num_tokens}")
    print("-" * 30)
    print(api_response_content)

def num_tokens_from_messages(messages, model="gpt-3.5-turbo"):
  """Returns the number of tokens used by a list of messages."""
  try:
      encoding = tiktoken.encoding_for_model(model)
  except KeyError:
      encoding = tiktoken.get_encoding("cl100k_base")
  if model == "gpt-3.5-turbo":  # note: future models may deviate from this
      num_tokens = 0
      for message in messages:
          num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
          for key, value in message.items():
              num_tokens += len(encoding.encode(value))
              if key == "name":  # if there's a name, the role is omitted
                  num_tokens += -1  # role is always required and always 1 token
      num_tokens += 2  # every reply is primed with <im_start>assistant
      return num_tokens
  else:
      raise NotImplementedError(f"""num_tokens_from_messages() is not presently implemented for model {model}.
  See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens.""")

if __name__ == "__main__":
    apitest()