import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API token from environment
api_token = os.getenv("HUGGINGFACE_API_TOKEN")

# Function to call Hugging Face Inference API
def translate_text(text, model_name):
    api_url = f"https://api-inference.huggingface.co/models/{model_name}"
    headers = {"Authorization": f"Bearer {api_token}"}
    payload = {"inputs": text}

    response = requests.post(api_url, headers=headers, json=payload)
    if response.status_code == 200:
        result = response.json()
        return result[0]['translation_text']
    else:
        return f"Error: {response.status_code} - {response.text}"

# Streamlit app interface
def main():
    st.title("Text Translation App")
    st.write("Translate text using Hugging Face's Inference API.")

    # Input text
    text = st.text_area("Enter text to translate:")

    # Language selection
    language_options = {
        "English to French": "Helsinki-NLP/opus-mt-en-fr",
        "French to English": "Helsinki-NLP/opus-mt-fr-en",
        "English to German": "Helsinki-NLP/opus-mt-en-de",
        "German to English": "Helsinki-NLP/opus-mt-de-en",
        # Add more language pairs as needed
    }
    language_pair = st.selectbox("Select translation direction:", list(language_options.keys()))
    model_name = language_options[language_pair]

    if st.button("Translate"):
        if not text:
            st.warning("Please enter text to translate.")
        else:
            with st.spinner("Translating..."):
                translation = translate_text(text, model_name)
            st.success("Translation completed!")
            st.write("### Translated Text:")
            st.write(translation)

if __name__ == "__main__":
    main()
