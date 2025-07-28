import base64
import streamlit as st

def set_image_as_background(image_path):
    with open(image_path, "rb") as img_file:
        data = img_file.read()
    encoded = base64.b64encode(data).decode()
    css = f"""
    <style>
    .stApp {{
        background: url("data:image/png;base64,{encoded}");
        background-size: fit;
        background-position: center center;
        background-attachment: fixed;
        color: gray;
        font-family: 'Segoe UI', 'Arial', sans-serif;
    }}
    .stApp::before {{
        content: "";
        position: fixed;
        inset: 0;
        z-index: -1;
        background: gray;
        pointer-events: none;
        min-width: 100vw;
        min-height: 100vh;
    }}
    h1, h2, h3, h4, h5, h6 {{
        color: #4371d7 !important;
        text-shadow: 1px 2px 7px rgba(130,150,200,0.11);
        letter-spacing: 1px;
    }}
    .block-container {{
        background: rgba(255,255,255,0.93);
        border-radius: 22px;
        margin-top: 2.5rem;
        color: #232046;
        border: 1.3px solid #6893d240;
        box-shadow: 0 8px 32px rgba(100,130,255,0.10);
    }}
    section[data-testid="stSidebar"] {{
        background: black !important;
        color: #213;
        border-radius: 10px;
    }}
    .stAlert, .stInfo, .stSuccess {{
        background-color: black !important;
        color: #1c2a3c !important;
        border-radius: 13px;
    }}
    a, .stActionButton, .stDownloadButton {{
        color: #4371d7 !important;
        font-weight: 600;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Place your image in 'assets/background.png' (you may change filename/extension as needed)
set_image_as_background("assets/background.png")

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
