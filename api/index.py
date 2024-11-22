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
    allow_methods=["*"],
    allow_headers=["*"]
)

openai.api_key = os.getenv("OPENAI_API_KEY")

class Prompt(BaseModel):
    prompt: str

@app.get("/")
def home():
    with open('index.html') as f:
        return HTMLResponse(f.read())

@app.post("/generate")
async def generate(prompt: Prompt):
    try:
        response = openai.images.generate(
            model="dall-e-3",
            prompt=prompt.prompt,
            size="1024x1024",
            n=1
        )
        return {"image_url": response.data[0].url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
