import streamlit as st
import io
from PyPDF2 import PdfReader, PdfWriter

st.markdown("# ✂️ Extract Pages from PDF")
st.caption("Select specific pages to save them as a new PDF.")

uploaded_pdf = st.file_uploader("Upload PDF", type="pdf")
if uploaded_pdf:
    reader = PdfReader(uploaded_pdf)
    num_pages = len(reader.pages)
    sel_pages = st.multiselect("Select pages to extract (0-based)", range(num_pages))
    if st.button("Extract Pages"):
        writer = PdfWriter()
        for i in sel_pages:
            writer.add_page(reader.pages[i])
        out = io.BytesIO()
        writer.write(out)
        st.download_button("Download Extracted PDF", data=out.getvalue(), file_name="extracted.pdf")
