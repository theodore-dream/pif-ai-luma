import openai

def generate_poem_prompt(input_text, creative_prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"{creative_prompt}: {input_text}",
        max_tokens=500,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response.choices[0].text
