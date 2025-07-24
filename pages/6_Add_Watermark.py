import streamlit as st
import io
from PyPDF2 import PdfReader, PdfWriter
import pdfplumber
from PIL import Image, ImageDraw, ImageFont

st.markdown("# 💧 Add Watermark to Each Page")
st.caption("Overlay text watermark on every page (as background image).")

uploaded_pdf = st.file_uploader("Upload PDF", type="pdf")
watermark = st.text_input("Watermark text")
if uploaded_pdf and watermark:
    pdf_bytes = uploaded_pdf.read()
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf_doc:
        writer = PdfWriter()
        for page in pdf_doc.pages:
            img = page.to_image(resolution=150).original.convert("RGBA")
            draw = ImageDraw.Draw(img)
            font = ImageFont.load_default()
            w, h = img.size
            draw.text((w//3, h//2), watermark, fill=(255,30,30,125), font=font)
            img = img.convert("RGB")
            temp = io.BytesIO()
            img.save(temp, format="PDF")
            temp.seek(0)
            new_page = PdfReader(temp).pages[0]
            writer.add_page(new_page)
        buf = io.BytesIO()
        writer.write(buf)
        st.download_button("Download Watermarked PDF", data=buf.getvalue(), file_name="watermarked.pdf")
