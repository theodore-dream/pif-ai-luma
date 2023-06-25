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
from urllib.request import Request, urlopen

logging.basicConfig(level=logging.INFO)
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_abstract_concept():
    abstract_concepts = [
        "amusement",
        "beauty",
        "bliss",
        "charm",
        "chaos",
        "cheerfulness",
        "courage",
        "delight",
        "despair",
        "destiny",
        "dreams",
        "ecstasy",
        "enlightenment",
        "eternity",
        "faith",
        "freedom",
        "frolic",
        "gaiety",
        "giddiness",
        "glee",
        "gleefulness",
        "grace",
        "hope",
        "humor",
        "ingenuity",
        "innocence",
        "jollity",
        "joviality",
        "justice",
        "knowledge",
        "lightheartedness",
        "liveliness",
        "memory",
        "merriment",
        "mirth",
        "mischief",
        "morality",
        "mortality",
        "mundanity",
        "passion",
        "pep",
        "playfulness",
        "quaintness",
        "radiance",
        "redemption",
        "sensuality",
        "serenity",
        "silliness",
        "solitude",
        "sparkle",
        "spirituality",
        "sprightliness",
        "time",
        "transcendence",
        "transience",
        "truth",
        "vivacity",
        "whimsy",
        "wisdom",
        "wit",
        "zest"
    ]
    # Pick a random abstract_concept
    selected_abstract_concept = random.choice(abstract_concepts)
    return selected_abstract_concept

def setup_lang_device():
    language_devices = {
        "metaphor": "a figure of speech in which a word or phrase is applied to an object or action to which it is not literally applicable.",
        "simile": "a figure of speech involving the comparison of one thing with another thing of a different kind, used to make a description more emphatic or vivid.",
        "personification": "the attribution of a personal nature or human characteristics to something non-human, or the representation of an abstract quality in human form.",
        "allegory": "a story, poem, or picture that can be interpreted to reveal a hidden meaning, typically a moral or political one.",
        "idiom": "a group of words established by usage as having a meaning not deducible from those of the individual words (e.g., rain cats and dogs, see the light).",
        "anachronism": "a thing belonging or appropriate to a period other than that in which it exists, especially a thing that is conspicuously old-fashioned.",
        "hyperbole": "exaggerated statements or claims not meant to be taken literally.",
        "irony": "the expression of one's meaning by using language that normally signifies the opposite, typically for humorous or emphatic effect.",
        "oxymoron": "a figure of speech in which apparently contradictory terms appear in conjunction (e.g., bittersweet, living death).",
        "synecdoche": "a figure of speech in which a part is made to represent the whole or vice versa.",
        "alliteration": "the occurrence of the same letter or sound at the beginning of adjacent or closely connected words.",
        "assonance": "the repetition of the sound of a vowel or diphthong in non-rhyming stressed syllables.",
        "consonance": "the recurrence of similar sounds, especially consonants, in close proximity.",
        "enjambment": "the continuation of a sentence without a pause beyond the end of a line, couplet, or stanza.",
        "caesura": "a break between words within a metrical foot, a pause near the middle of a line."
}
    # Pick a random language device
    selected_lang_device = random.choice(list(language_devices.keys()))
    return selected_lang_device

def build_persona():
    personas = {
        "Bob": "Bob weaves complex metaphors into his poetry, often reflecting on his past experiences with a melancholic but hopeful tone. His mind, a labyrinth of profound thoughts and intricate connections, delves into the depths of the human experience, seeking to capture the essence of life's fleeting moments in the tapestry of his verses. As he sits in his study, surrounded by weathered books and faded photographs, Bob's gaze drifts into the distance, his eyes shining with the flicker of inspiration. He contemplates the world through a lens tinted with nostalgia, the memories of his youth mingling with the dreams of what is yet to come. The weight of time rests upon his weary shoulders, but it does not deter his fervor for introspection..",
        "Alice": "Alice, a beautiful young girl with curly blonde hair, loves to write uplifting and cheery poetry, that may have a dark or an ironic twist.",
        "Reginald": "Reginald, an eccentric oil tycoon of immeasurable wealth, indulges in a style that is luxuriant and opulent, echoing his extravagance. His prose frequently revolves around themes of desire and excess, reflecting an insatiable hunger for the boundless and a dissatisfaction with the mundane.",
        "Beatrice": "Beatrice, an anxious heiress shadowed by an unshakeable paranoia, crafts her writings with a sense of urgency and uncertainty. The underlying theme in her stories is the existential dread of imagined threats, using suspense as a tool to articulate her constant state of anxiety and fear.",
        "Mortimer": "Mortimer, an eccentric scientist, presents his writings in a structured, albeit unpredictable manner. His prose, rich with the motifs of innovation and chaos, embodies his passion for scientific discovery as well as his nonchalance towards the disorder left in his wake. His writings often culminate in a profound sense of detachment, a testament to his aloof and peculiar character.",
        #"Daisy": "Daisy, a passionate high school student deeply interested in science and astronomy, creates poems filled with wonder and awe, often using vivid imagery to paint celestial landscapes.",
        #"Edward": "Edward, a world-renowned chef with a thirst for adventure, infuses his poetry with rich culinary metaphors and cultural allusions, his verses embodying the vibrant flavors and textures he experiences in his travels.",
        #"Fiona": "Fiona, a tech entrepreneur with a love for the great outdoors, writes concise and insightful poetry that contrasts the structured logic of code with the wild unpredictability of nature."
}
    # Pick a random persona
    selected_persona = random.choice(list(personas.keys()))
    return selected_persona

def openai_api_call(creative_prompt, persona, lang_device, abstract_concept):

# API call
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            #{"role": "user", "content": creative_prompt},
            {"role": "system", "content": persona },
            {"role": "user", "content": "Step 1: Produce three different versions of a poem inspired by the following: " + creative_prompt + ". Each poem can be three or four lines long" + "Each version should have a different structure - rhyme, free verse, sonnet, haiku, etc. Explain the changes made for each iteration before printing the result for each step."},
            {"role": "user", "content": "Step 2: The chosen abstract concept is: " + abstract_concept + ". Next you evaluate the revisions and determine which most closely has a deep connection to then chosen concept, or could most elegantly be modified to fit the concept."},
            {"role": "user", "content": "Step 3: Create a new poem that is two to four lines long with the following parameters: Revise the selected poem to subtly weave in the chosen concept."},
            {"role": "user", "content": "Step 4: Create a new poem that is two to four lines long with the following parameters: Thinking of yourself and your own personal writing style, revise the selected poem to more closely match your style."},
            {"role": "user", "content": "Step 5: Create a new poem that is two to four lines long with the following parameters: Consider how you could use this linguistic device: "  + lang_device + ". Revise the poem to incorporate the linguistic device"},
            {"role": "user", "content": "Step 6: Create a single new poem that is two to four lines long with the following parameters: Think of all the changes you've made. Think of how you've grown. Make one more poem."},
             
             # Introduce variation to reduce overall consistency in tone, language use, and sentence structure."},
        ],
        max_tokens=2000,
        n=1,
        stop=None,
        temperature=1.0,
    )
    
    # print information about api call
    print(f"persona: {persona}")
    print(f"abstract_concept: {abstract_concept}")
    print(f"creative_prompt: {creative_prompt}")
    return response

def get_random_word():
    url="https://svnweb.freebsd.org/csrg/share/dict/words?revision=61569&view=co"
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})

    web_byte = urlopen(req).read()
    webpage = web_byte.decode('utf-8')
    all_words = webpage.split("\n")
    return random.choice(all_words)

def parse_response():
    creative_prompt = get_random_word()
    abstract_concept = get_abstract_concept()
    persona = build_persona()
    lang_device = setup_lang_device()
    print(f"running pif_poetry_generator with prompt: {creative_prompt}")
    api_response = openai_api_call(creative_prompt, persona, lang_device, abstract_concept)
    if api_response['choices'][0]['message']['role'] == "assistant":
        api_response_content = api_response['choices'][0]['message']['content'].strip()
    else:
        api_response_syscontent = api_response['system'].strip()  # put into a var for later use 
    print("-" * 30)

    print(f"Prompt tokens: {api_response['usage']['prompt_tokens']}")
    print(f"Completion tokens: {api_response['usage']['completion_tokens']}")
    print(f"Total tokens: {api_response['usage']['total_tokens']}")

    print("-" * 30)
    print(api_response_content)

if __name__ == "__main__":
    parse_response()