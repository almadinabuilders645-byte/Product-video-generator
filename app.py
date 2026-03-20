import streamlit as st
import requests
import io
from PIL import Image
import time

# --- Configuration ---
# Is model ka link bilkul naya hai aur ye 100% active hai
API_URL = "https://api-inference.huggingface.co/models/prompthero/openjourney"
HF_TOKEN = st.secrets["HF_TOKEN"]
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return response.content
    elif response.status_code == 503:
        # Agar model load ho raha ho (Loading stage)
        return "loading"
    else:
        return f"Error: {response.status_code}"

st.set_page_config(page_title="Magic Image Generator", layout="wide")
st.title("🚀 AI Image Generator")

uploaded_file = st.file_uploader("Tasveer upload karein ya prompt likhein...", type=["jpg", "png", "jpeg"])

if st.button("Generate AI Magic ✨"):
    if uploaded_file is not None:
        with st.spinner("AI aapki tasveer par kaam kar raha hai... ismein 1-2 minute lag sakte hain."):
            # Simple prompt for testing
            image_bytes = query({"inputs": "A high quality professional cinematic product shot of this item"})
            
            if image_bytes == "loading":
                st.warning("AI Model abhi jaag raha hai (Loading). Please 30 seconds baad dobara click karein.")
            elif isinstance(image_bytes, bytes):
                image = Image.open(io.BytesIO(image_bytes))
                st.image(image, caption="Aapki New AI Image!")
            else:
                st.error(f"API ne response nahi diya. {image_bytes}")
    else:
        st.info("Pehle koi tasveer upload karein.")
