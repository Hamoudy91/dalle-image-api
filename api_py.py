from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import openai
import os

app = FastAPI()

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY", "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")

@app.get("/", response_class=HTMLResponse)
async def home():
    """
    Render the homepage with a simple text box for input.
    """
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AI Image Generator</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                text-align: center;
                margin: 0;
                padding: 0;
                background-color: #f4f4f4;
            }
            .container {
                margin-top: 100px;
                padding: 20px;
                background: white;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                width: 80%;
                max-width: 600px;
                margin-left: auto;
                margin-right: auto;
            }
            input[type="text"] {
                padding: 10px;
                width: 70%;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            button {
                padding: 10px 15px;
                color: white;
                background-color: #007BFF;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }
            button:hover {
                background-color: #0056b3;
            }
            .image-container {
                margin-top: 20px;
            }
            img {
                max-width: 100%;
                border-radius: 10px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>AI Image Generator</h1>
            <p>Describe what you want to see:</p>
            <form action="/generate-image" method="post">
                <input type="text" name="prompt" placeholder="Type your prompt here..." required>
                <button type="submit">Generate Image</button>
            </form>
            <div class="image-container">
                <p id="result"></p>
            </div>
        </div>
    </body>
    </html>
    """

@app.post("/generate-image", response_class=HTMLResponse)
async def generate_image(request: Request):
    """
    Generate an image based on the provided prompt.
    """
    form = await request.form()
    prompt = form.get("prompt")

    try:
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
        image_url = response['data'][0]['url']
        return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Generated Image</title>
        </head>
        <body>
            <div class="container">
                <h1>Generated Image</h1>
                <p>Prompt: {prompt}</p>
                <img src="{image_url}" alt="Generated Image">
                <br><br>
                <a href="/">Generate Another</a>
            </div>
        </body>
        </html>
        """
    except Exception as e:
        return f"<h1>Error:</h1><p>{str(e)}</p><a href='/'>Go Back</a>"
