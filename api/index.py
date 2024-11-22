from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# More flexible API key handling
openai.api_key = os.environ.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")

class ImagePrompt(BaseModel):
    prompt: str

@app.post("/generate-image")
async def generate_image(prompt_data: ImagePrompt):
    if not openai.api_key:
        return {"error": "API key not configured"}
    try:
        response = openai.images.generate(
            prompt=prompt_data.prompt,
            n=1,
            size="1024x1024"
        )
        return {"image_url": response.data[0].url}
    except Exception as e:
        return {"error": str(e)}
