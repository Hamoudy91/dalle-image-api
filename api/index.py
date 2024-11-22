from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
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

openai.api_key = os.getenv("OPENAI_API_KEY")

class ImagePrompt(BaseModel):
    prompt: str

@app.get("/")
def read_root():
    with open('public/index.html', 'r') as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

@app.post("/generate-image")
async def generate_image(prompt_data: ImagePrompt):
    if not openai.api_key:
        raise HTTPException(status_code=500, detail="API key not configured")
    try:
        response = openai.images.generate(
            model="dall-e-3",
            prompt=prompt_data.prompt,
            n=1,
            size="1024x1024"
        )
        return {"image_url": response.data[0].url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
