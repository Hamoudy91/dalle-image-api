import streamlit as st
import openai
import requests
from PIL import Image
from io import BytesIO
import os

# Configure OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_image(prompt):
    try:
        response = openai.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            n=1
        )
        return response.data[0].url
    except Exception as e:
        st.error(f"Error generating image: {str(e)}")
        return None

def main():
    st.set_page_config(page_title="AI Image Generator", page_icon="🎨", layout="wide")
    
    # Custom CSS
    st.markdown("""
        <style>
        .stTextInput > div > div > input {
            font-size: 20px;
        }
        .stButton > button {
            font-size: 20px;
            padding: 10px 24px;
            background-color: #FF4B4B;
            color: white;
            border-radius: 8px;
        }
        .title {
            text-align: center;
            color: #FF4B4B;
            font-size: 50px;
            margin-bottom: 30px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Title
    st.markdown("<h1 class='title'>✨ AI Image Generator ✨</h1>", unsafe_allow_html=True)

    # Create two columns
    col1, col2 = st.columns([2, 3])

    with col1:
        st.markdown("### Enter your prompt")
        prompt = st.text_area("", height=150, placeholder="Describe the image you want to create...")
        
        if st.button("Generate Image 🎨"):
            if prompt:
                with st.spinner("Creating your masterpiece..."):
                    image_url = generate_image(prompt)
                    if image_url:
                        # Save URL to session state
                        st.session_state.image_url = image_url
                        st.session_state.last_prompt = prompt
            else:
                st.warning("Please enter a prompt first!")

    with col2:
        st.markdown("### Generated Image")
        # Display image if it exists in session state
        if 'image_url' in st.session_state:
            try:
                response = requests.get(st.session_state.image_url)
                img = Image.open(BytesIO(response.content))
                st.image(img, caption=f"Prompt: {st.session_state.last_prompt}", use_column_width=True)
                
                # Download button
                st.download_button(
                    label="Download Image 💾",
                    data=response.content,
                    file_name="generated_image.png",
                    mime="image/png"
                )
            except Exception as e:
                st.error(f"Error displaying image: {str(e)}")

if __name__ == "__main__":
    main()
