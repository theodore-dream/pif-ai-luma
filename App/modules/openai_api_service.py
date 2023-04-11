import openai
import logging
import datetime
from modules.logger import setup_logger

logger = setup_logger("openai_api_service")


def generate_poem_prompt(input_text, creative_prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates poems."},
            {"role": "user", "content": f"{creative_prompt}: {input_text}"}
        ],
        max_tokens=500,
        n=1,
        stop=None,
        temperature=0.5,
    )

    # Extracting information
    generated_poem = response['choices'][0]['message']['content'].strip()
    model = response.model
    role = response.choices[0].message['role']
    finish_reason = response.choices[0].finish_reason

    # Get current timestamp
    current_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Logging details
    logger.info("Generated Poem:")
    logger.info(generated_poem)
    logger.info("\nDetails:")
    logger.info(f"Model: {model}")
    logger.info(f"Role: {role}")
    logger.info(f"Finish Reason: {finish_reason}")
    logger.info(f"Timestamp: {current_timestamp}")

    return generated_poem


