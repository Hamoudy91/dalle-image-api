from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import openai
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
logger.info(f"API Key present: {bool(OPENAI_API_KEY)}")
openai.api_key = OPENAI_API_KEY

class ImagePrompt(BaseModel):
    prompt: str

@app.post("/generate-image")
async def generate_image(prompt_data: ImagePrompt):
    logger.info(f"Received prompt: {prompt_data.prompt}")
    try:
        response = openai.images.generate(
            prompt=prompt_data.prompt,
            n=1,
            size="1024x1024"
        )
        logger.info(f"OpenAI response: {response}")
        return {"image_url": response.data[0].url}
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
