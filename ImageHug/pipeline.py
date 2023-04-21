#from transformers import AutoTokenizer, AutoModelForCausalLM
from diffusers import DiffusionPipeline
#from accelerate import Accelerator

#accelerator = Accelerator()

repo_id = "PublicPrompts/All-In-One-Pixel-Model"
pipe = DiffusionPipeline.from_pretrained(repo_id)
pipe.to("mps")

# Recommended if your computer has < 64 GB of RAM
pipe.enable_attention_slicing()

# Tokenize the text prompt
prompt = "simple portrait with a blank background of an rpg character that is a monk"

# Generate images
image = pipe(prompt).images[0]

image.save("image3.png")