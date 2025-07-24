import base64
import streamlit as st

def get_base64_video(video_file):
    with open(video_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_mp4_as_background(video_path):
    video_base64 = get_base64_video(video_path)
    st.markdown(
        f"""
        <style>
        .stApp {{
            position: relative;
            min-height: 100vh;
            background: none !important;
            color: #fff;
            font-family: 'Segoe UI', 'Arial', sans-serif;
        }}
        #background-video {{
            position: fixed;
            top: 0; left: 0;
            width: 100vw;
            height: 100vh;
            min-width: 100vw;
            min-height: 100vh;
            object-fit: fit;  /* Stretches video to cover the viewport */
            z-index: -100;
            opacity: 1.0;
            pointer-events: none;
            background: black;
        }}
        </style>
        <video autoplay muted loop playsinline id="background-video">
            <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
        </video>
        """,
        unsafe_allow_html=True
    )

# Place your MP4 in 'assets/background.mp4'
set_mp4_as_background("assets/background.mp4")


# ---- Main Content ----

st.title("✨ Welcome to PDF Club")

st.markdown(
    """
    <p style='font-size:1.18rem;font-weight:500;'>
        <b>Edit PDFs visually, safely, and easily!</b>
        <br>
        <span style='color:#4371d7'>All tools work <b>right in your browser</b> with instant feedback.</span>
    </p>
    """, unsafe_allow_html=True
)

st.info("Choose a tool from the sidebar to get started.")

st.markdown("---")
st.markdown("""
<b>Features include:</b>
<ul>
    <li>Edit PDF text (overwrite a page)</li>
    <li>Remove all images from selected pages</li>
    <li>Overlay PNG/JPG images anywhere</li>
    <li>Delete, merge, or extract PDF pages</li>
    <li>Apply custom watermarks</li>
</ul>
""", unsafe_allow_html=True)

st.success("All processing happens locally in your browser — fast, safe, and private.")

st.markdown(
    "<center><b>PDF Editor Design by You, Powered by Python</b> 🦄</center>",
    unsafe_allow_html=True,
)
