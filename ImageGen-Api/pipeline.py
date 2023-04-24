from diffusers import DiffusionPipeline
import datetime
from accelerate import Accelerator

accelerator = Accelerator()

repo_id = "PublicPrompts/All-In-One-Pixel-Model"
pipe = DiffusionPipeline.from_pretrained(repo_id)
pipe.to("mps")

# Recommended if your computer has < 64 GB of RAM
pipe.enable_attention_slicing()

# Tokenize the text prompt
prompt = "simple pixel art character portrait of a frog with a white background"

# Generate images
image = pipe(prompt).images[0]

current_timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
image.save(f"/images/image-{current_timestamp}.png")