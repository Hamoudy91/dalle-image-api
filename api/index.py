from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
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

# Get API key from environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("No OpenAI API key found in environment variables")

openai.api_key = OPENAI_API_KEY

class ImagePrompt(BaseModel):
    prompt: str

@app.get("/")
def read_root():
    return {"message": "Image Generation API"}

@app.post("/generate-image")
async def generate_image(prompt_data: ImagePrompt):
    if not prompt_data.prompt:
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")
    
    try:
        response = openai.images.generate(
            prompt=prompt_data.prompt,
            n=1,
            size="1024x1024"
        )
        
        if not response.data:
            raise HTTPException(status_code=500, detail="No image generated")
            
        return JSONResponse(content={"image_url": response.data[0].url})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
