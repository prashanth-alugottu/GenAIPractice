import os
from dotenv import load_dotenv
load_dotenv()
import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO

client = genai.Client()
st.title("Image Generation with Gemini")
user_prompt = st.text_input("Enter a prompt for image generation:")
if st.button("Generate Image"):
    if not user_prompt:
        st.warning("Please enter a prompt.")
    else:
        try:
            with st.spinner("Generating image..."):
                response = client.models.generate_content(
                    model="gemini-2.0-flash-exp-image-generation",
                    contents=user_prompt,
                    config=types.GenerateContentConfig(
                        response_modalities=['Text','Image']
                    )
            )
            st.subheader("Generated Image:")
            for part in response.candidates[0].content.parts:
                if part.text is not None:
                    st.write("Text:", part.text)
                elif part.inline_data is not None:
                    image=Image.open(BytesIO(part.inline_data.data))
                    st.image(image, caption="Generated Image")
        except Exception as e:
            st.error(f"Error during image generation: {e}")

