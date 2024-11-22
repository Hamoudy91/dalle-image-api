from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
import os
from typing import List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

class ImagePrompt(BaseModel):
    prompt: str

class ImageSequence(BaseModel):
    prompts: List[str]

@app.get("/")
def read_root():
    return {"message": "Image Generation API"}

@app.post("/generate-image")
async def generate_image(prompt_data: ImagePrompt):
    try:
        response = openai.images.generate(
            prompt=prompt_data.prompt,
            n=1,
            size="1024x1024"
        )
        return {"image_url": response.data[0].url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-sequence")
async def generate_sequence(sequence_data: ImageSequence):
    try:
        urls = []
        for prompt in sequence_data.prompts:
            response = openai.images.generate(
                prompt=prompt,
                n=1,
                size="1024x1024"
            )
            urls.append(response.data[0].url)
        return {"image_urls": urls}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
