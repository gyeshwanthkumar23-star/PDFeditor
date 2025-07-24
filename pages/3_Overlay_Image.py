import streamlit as st
import io
from PyPDF2 import PdfReader, PdfWriter
import pdfplumber
from PIL import Image

st.markdown("# 🖼️ Overlay/Add Image to PDF Page")
st.caption("Add an image overlay (PNG/JPG) at a position of your choice.")

uploaded_pdf = st.file_uploader("Upload PDF", type="pdf")
uploaded_image = st.file_uploader("Upload image (PNG/JPG)", type=["png", "jpg"])

if uploaded_pdf and uploaded_image:
    pdf_bytes = uploaded_pdf.read()
    reader = PdfReader(io.BytesIO(pdf_bytes))
    num_pages = len(reader.pages)
    page_num = st.number_input("Page number", 0, num_pages-1, 0)
    x = st.number_input("X position (px)", 0, 2000, 50)
    y = st.number_input("Y position (px)", 0, 2000, 50)
    if st.button("Overlay Image on Page"):
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf_doc:
            page = pdf_doc.pages[page_num]
            base = page.to_image(resolution=150).original.convert("RGB")
            img = Image.open(uploaded_image).convert("RGBA")
            base.paste(img, (x, y), img)
            buf = io.BytesIO()
            base.save(buf, format="PDF")
            buf.seek(0)
            new_page = PdfReader(buf).pages[0]
        writer = PdfWriter()
        for i in range(num_pages):
            if i == page_num:
                writer.add_page(new_page)
            else:
                writer.add_page(reader.pages[i])
        out = io.BytesIO()
        writer.write(out)
        st.download_button("Download PDF with Image Overlay", data=out.getvalue(), file_name="image_overlay.pdf")
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf_doc:
        st.image(pdf_doc.pages[page_num].to_image(resolution=150).original, caption="Preview")
