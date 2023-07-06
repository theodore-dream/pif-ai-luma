import openai
import logging
import datetime
from modules.logger import setup_logger
import decimal

logger = setup_logger("openai_api_service")


def openai_api_call(input_text, creative_prompt, entropy):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a poet. Create a poem based on the following text "},
            {"role": "user", "content": f"{creative_prompt}: {input_text}"}
        ],
        max_tokens=500,
        n=1,
        stop=None,
        temperature=float((entropy * 2)),
    )

    # Extracting information
    api_response = response['choices'][0]['message']['content'].strip()
    api_response = f"\"{api_response}\""
    model = response.model
    role = response.choices[0].message['role']
    finish_reason = response.choices[0].finish_reason

    # Get current timestamp
    current_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Logging details
    logger.info("Generated Text:")
    logger.info(api_response)
    logger.info("\nDetails:")
    logger.info(f"Model: {model}")
    logger.info(f"Role: {role}")
    logger.info(f"Finish Reason: {finish_reason}")
    logger.info(f"Timestamp: {current_timestamp}")

    return api_response


