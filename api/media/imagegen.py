from google import genai
from google.genai import types
from io import BytesIO
from PIL import Image
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API"))

def generate_image_from_prompt(prompt: str, tags: str) -> Image.Image:
    response = client.models.generate_images(
        model="imagen-4.0-generate-preview-06-06",
        prompt=prompt,
        config=types.GenerateImagesConfig(
            number_of_images=1,
            aspect_ratio="1:1"
        )
    )
    img_bytes = response.generated_images[0].image.image_bytes
    img = Image.open(BytesIO(img_bytes))
    return img

# img = generate_image_from_prompt("A cyberpunk cityscape at night with neon lights and rain")
# img.save("output.png")
