import os
import uuid
import json

openai_api_key = os.environ["OPENAI_API_KEY"]

initial_game_text = "Welcome to the text-based adventure game! Would you like to start?"

def get_or_create_uuid():
    if os.path.exists('game_state.txt'):
        with open('game_state.txt', 'r') as file:
            game_state = json.load(file)
            game_uuid = game_state.get('uuid', None)
    else:
        game_uuid = str(uuid.uuid4())
        game_state = {'uuid': game_uuid}
        with open('game_state.txt', 'w') as file:
            json.dump(game_state, file)
    return game_uuid

