import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

# Define the function
def create_poem():
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "you create poems"},
            {"role": "user", "content": "create a poem"}
        ],
        functions=[
            {
                "name": "create_poem",
                "description": "generated poetry",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "poem": {
                            "type": "string",
                            "description": "a poem"
                        },
                    },
                    "required": ["poem"]
                }
            }
        ],
        function_call="auto",
        temperature=1.2,
    )
    message = completion.choices[0].message
    function_used = hasattr(message, "function_call")
    print(message)
    return message.function_call.arguments if function_used else message.content

def test_create_poem():
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Create a poem about love"}], # include the keyword in the user message
        max_tokens=3600,
        n=1,
        stop=None,
        temperature=1.2,
        functions=[create_poem]
    )
    # Return API response
    print(response['choices'][0]['message']['content'])
    return response

create_poem()
