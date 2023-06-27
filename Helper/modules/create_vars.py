import random
import nltk
from nltk.corpus import wordnet as wn
import openai
import os
from nltk.probability import FreqDist

# setup logger
from modules.logger import setup_logger
logger = setup_logger('create_vars')

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

    # Get the list of file IDs in the web text corpus.
    fileids = nltk.corpus.webtext.fileids()

    # Randomly select a file ID.
    random_fileid = random.choice(fileids)

    # Get raw text from the randomly selected file.
    raw_text = nltk.corpus.webtext.raw(random_fileid)

    # Tokenize the raw text.
    tokens = nltk.word_tokenize(raw_text)

    # Tag the tokens with their parts of speech.
    tagged = nltk.pos_tag(tokens)

    # Filter to get only the nouns (NN), adjectives (JJ), adverbs (RB), 
    # personal pronouns (PRP), possessive pronouns (PRP$), and coordinating conjunctions (CC).
    nouns = [word for word, pos in tagged if pos in ['NN', 'NNS'] and word.isalpha()]
    adjectives = [word for word, pos in tagged if pos in ['JJ', 'JJR', 'JJS'] and word.isalpha()]
    adverbs = [word for word, pos in tagged if pos in ['RB', 'RBR', 'RBS'] and word.isalpha()]
    pronouns = [word for word, pos in tagged if pos in ['PRP', 'PRP$'] and word.isalpha()]
    conjunctions = [word for word, pos in tagged if pos == 'CC' and word.isalpha()]

    # Get the frequency distribution of the words.
    fdist_nouns = FreqDist(nouns)
    fdist_adj = FreqDist(adjectives)
    fdist_adv = FreqDist(adverbs)
    fdist_pronouns = FreqDist(pronouns)
    fdist_conjunctions = FreqDist(conjunctions)

    # Filter to get only the common words.
    common_nouns = [word for word in set(nouns) if fdist_nouns[word] > 3]
    common_adj = [word for word in set(adjectives) if fdist_adj[word] > 3]
    common_adv = [word for word in set(adverbs) if fdist_adv[word] > 3]
    common_pronouns = [word for word in set(pronouns) if fdist_pronouns[word] > 3]
    common_conjunctions = [word for word in set(conjunctions) if fdist_conjunctions[word] > 3]

    # Select a random word from each category.
    random_noun = random.choice(common_nouns)
    random_adj = random.choice(common_adj)
    random_adv = random.choice(common_adv)
    random_pronoun = random.choice(common_pronouns)
    random_conjunction = random.choice(common_conjunctions)

    webtext_words = f'{random_noun} {random_adj} {random_adv} {random_pronoun} {random_conjunction}'
    logger.debug(f"webtext words are: {webtext_words}")

    # This section pulls words from wordnet
    word_types = [wn.NOUN, wn.VERB, wn.ADJ, wn.ADV]
    wordnet_words = []

    for word_type in word_types:
        # Select a subset of synsets
        all_synsets = list(wn.all_synsets(word_type))
        sample_size = max(200, min(500, len(all_synsets)))
        selected_synsets = random.sample(all_synsets, sample_size)

    # sample_size will be between 200 and 500 inclusive, unless all_synsets has fewer than 200 elements, in which case sample_size will be the size of all_synsets.
    for synset in selected_synsets:
        word = synset.name().split('.')[0]
        wordnet_words.append(word)

    # Remove duplicates
    wordnet_words = list(set(wordnet_words))

    # Select a random word from each word type.
    random_noun = random.choice([word for word in wordnet_words if wn.synsets(word, wn.NOUN)])
    random_verb = random.choice([word for word in wordnet_words if wn.synsets(word, wn.VERB)])
    random_adj = random.choice([word for word in wordnet_words if wn.synsets(word, wn.ADJ)])
    random_adv = random.choice([word for word in wordnet_words if wn.synsets(word, wn.ADV)])

    wordnet_words_string = f'{random_noun} {random_verb} {random_adj} {random_adv}'
    logger.debug(f"wordnet words are: {wordnet_words_string}")

    # combine both webtext and wordnet words
    combined_string = webtext_words + " " + wordnet_words_string
    logger.debug(f"combined words are: {combined_string}")
    return combined_string

def gen_creative_prompt(text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "Create a short sentence inspired by the following words: "
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
    
    creative_prompt = response['choices'][0]['message']['content']
    return creative_prompt

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
    selected_persona = random.choice(list(personas["poets"].keys()))
    return selected_persona
