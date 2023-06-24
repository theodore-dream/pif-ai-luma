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

def openai_api_call(creative_prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            #{"role": "user", "content": creative_prompt},
            {"role": "user", "content": "Step 1: Produce three different versions of a poem about" + creative_prompt + " Explain the changes made for each iteration."},
            {"role": "user", "content": "Step 2: Iterate over each version, revising and modifying to reduce consistency and increase entropy while maintaining a human-like feel."},
            {"role": "user", "content": "Step 3: Select one of the following themes: divinity, grundge, or beauty. Afterwards, evaluate the revisions and determine which most closely fits the theme."},
            {"role": "user", "content": "Step 4: Rework the poem to further incorporate the chosen theme."},
            {"role": "user", "content": "Step 5: Iterate over the selected poem to randomly select up to three lines and modify them to have more unexpected elements."},
        ],
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=1.0,
    )
    # Extracting information
    api_response = response['choices'][0]['message']
    model = response.model
    role = api_response['role']
    finish_reason = response.choices[0].finish_reason
    print(f"finish_reason: {finish_reason}")

    # Get current timestamp
    current_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return api_response

def promptgen():
    creative_prompt = "fleshy melons"
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