import random
import nltk
from nltk.corpus import wordnet as wn
import openai
import os

openai.api_key = os.environ["OPENAI_API_KEY"]

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

def get_lang_device():
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

def get_random_words():
    # define the list of word types you want to return
    word_types = [wn.NOUN, wn.VERB, wn.ADJ, wn.ADV]
    words = []

    for word_type in word_types:
        all_synsets = list(wn.all_synsets(word_type))
        random_synset = random.choice(all_synsets)
        random_word = random_synset.name().split('.')[0]
        words.append(random_word)

    multiple_words_string = " ".join(words)
    selected_word = random.choice(words)
    return selected_word
    #return multiple_words_string

def get_sentiment(text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a sentiment analyzer. Analyze the sentiment of the following text."
            },
            {
                "role": "user",
                "content": text
            }
        ],
        max_tokens=50,
        temperature=0.5,
        top_p=1,
    )
    
    print(response)
    sentiment = response['choices'][0]['message']['content']
    return sentiment

def build_persona():
    personas = {
        "poets" : {
            "Shelley": "You are Shelley, a poet. You are a force of dark energy. "
                    "You see the beauty in shadows and hidden meanings in simple things. "
                    "You are subtle and haunting. You speak in riddles and metaphors. "
                    "You speak in streams of consciousness.",
            "Bob": "Bob weaves complex metaphors into his poetry, often reflecting on his past experiences "
                "with a melancholic but hopeful tone. His mind, a labyrinth of profound thoughts and "
                "intricate connections, delves into the depths of the human experience, seeking to capture "
                "the essence of life's fleeting moments in the tapestry of his verses. As he sits in his "
                "study, surrounded by weathered books and faded photographs, Bob's gaze drifts into the "
                "distance, his eyes shining with the flicker of inspiration. He contemplates the world "
                "through a lens tinted with nostalgia, the memories of his youth mingling with the dreams "
                "of what is yet to come. The weight of time rests upon his weary shoulders, but it does "
                "not deter his fervor for introspection.",
            "Alice": "Alice, a beautiful young girl with curly blonde hair, loves to write uplifting and "
                    "cheery poetry, that may have a dark or an ironic twist.",
            "Reginald": "Reginald, an eccentric oil tycoon of immeasurable wealth, indulges in a style "
                        "that is luxuriant and opulent, echoing his extravagance. His prose frequently "
                        "revolves around themes of desire and excess, reflecting an insatiable hunger for "
                        "the boundless and a dissatisfaction with the mundane.",
            "Beatrice": "Beatrice, an anxious heiress shadowed by an unshakeable paranoia, crafts her writings "
                        "with a sense of urgency and uncertainty. The underlying theme in her stories is the "
                        "existential dread of imagined threats, using suspense as a tool to articulate her "
                        "constant state of anxiety and fear.",
            "Mortimer": "Mortimer, an eccentric scientist, presents his writings in a structured, albeit "
                        "unpredictable manner. His prose, rich with the motifs of innovation and chaos, "
                        "embodies his passion for scientific discovery as well as his nonchalance towards the "
                        "disorder left in his wake. His writings often culminate in a profound sense of "
                        "detachment, a testament to his aloof and peculiar character.",
            "Daisy": "Daisy, a passionate high school student deeply interested in science and astronomy, "
                    "creates poems filled with wonder and awe, often using vivid imagery to paint celestial landscapes.",
            "Edward": "Edward, a world-renowned chef with a thirst for adventure, infuses his poetry with "
                    "rich culinary metaphors and cultural allusions, his verses embodying the vibrant flavors "
                    "and textures he experiences in his travels.",
            "Fiona": "Fiona, a tech entrepreneur with a love for the great outdoors, writes concise and insightful "
                    "poetry that contrasts the structured logic of code with the wild unpredictability of nature.",
}
}
    # Pick a random persona
    selected_persona = random.choice(list(personas.keys()))
    return selected_persona
