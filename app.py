import streamlit as st
import requests
import io
from PIL import Image
import time
import os

# --- Configuration ---
# API setup
HF_TOKEN = st.secrets["HF_TOKEN"] # <--- APNA TOKEN YAHAN DALEIN
# Hum stabilityai ka Stable Video Diffusion model use kar rahe hain
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

# --- Website UI Setup ---
st.set_page_config(page_title="Magic Product Video", page_icon="🚀", layout="wide")

st.markdown("""
<style>
    .big-font { font-size:30px !important; font-weight: bold; color: #4CAF50;}
    .sales-text { font-size:18px !important; color: #555; }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="big-font">🚀 Magic Product Video Generator</p>', unsafe_allow_html=True)
st.markdown('<p class="sales-text">Apni product ki tasveer upload karein, aur AI use ek exciting motion video mein badal dega jo sales barhane mein madad karegi.</p>', unsafe_allow_html=True)

# --- Sidebar for help ---
with st.sidebar:
    st.header("Kaise Use Karein?")
    st.markdown("""
    1.  Product ki *saaf tasveer* upload karein (Preferably with clear background).
    2.  'Generate Video' button dabayein.
    3.  AI 1-2 minute lega video banane mein.
    4.  Video download karein aur use social media par lagayein!
    """)

# --- Main App Logic ---
col1, col2 = st.columns(2)

uploaded_file = None

with col1:
    st.subheader("1. Tasveer Upload Karein")
    uploaded_file = st.file_uploader("Choose a product image...", type=["jpg", "png", "jpeg"])
    
    if uploaded_file is not None:
        # Display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image', use_column_width=True)

with col2:
    st.subheader("2. Aapki Video")
    generate_btn = st.button("Generate Exciting Video ✨", type="primary")

    if generate_btn and uploaded_file is not None:
        with st.spinner('AI Jadu kar raha hai... Isme 1-3 minute lag sakte hain...'):
            try:
                # Convert image to bytes for API
                img_bytes = io.BytesIO()
                image.save(img_bytes, format=image.format)
                img_bytes = img_bytes.getvalue()

                # Send request to Hugging Face API
                response = requests.post(API_URL, headers=headers, data=img_bytes)
                
                # Check if API is still loading the model
                if response.status_code == 503:
                    st.warning("AI Model abhi 'neend' se jag raha hai (loading). Please 2 minute baad dobara try karein.")
                elif response.status_code == 200:
                    # Video is successfully generated (it comes as bytes)
                    video_bytes = response.content
                    
                    # Save video locally
                    video_filename = f"generated_video_{int(time.time())}.mp4"
                    with open(video_filename, "wb") as f:
                        f.write(video_bytes)
                    
                    st.success("Video Tayyar Hai!")
                    # Display the video
                    st.video(video_bytes)
                    
                    # Download button
                    with open(video_filename, "rb") as f:
                        st.download_button(
                            label="Download Video",
                            data=f,
                            file_name=video_filename,
                            mime="video/mp4"
                        )
                    # Clean up local file after display
                    os.remove(video_filename)
                else:
                    st.error(f"Error: API ne response nahi diya. Status Code: {response.status_code}")
                    st.write(response.text) # For debugging

            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")
                
    elif generate_btn and uploaded_file is None:
        st.warning("Please pehle ek tasveer upload karein.")

st.markdown("---")
st.caption("Powered by Stable Video Diffusion (Hugging Face) | Banaya gaya hai Streamlit se.")
