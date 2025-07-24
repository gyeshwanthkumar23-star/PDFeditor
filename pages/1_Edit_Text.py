import streamlit as st
import io
from PyPDF2 import PdfReader, PdfWriter
import pdfplumber
from PIL import Image, ImageDraw, ImageFont

st.markdown("# 📝 Edit PDF Text (Page Overwrite)")
st.caption("⚡ Overwrites a PDF page with your text (rasterized, layout/fonts lost).")

uploaded = st.file_uploader("Upload PDF", type="pdf")
if uploaded:
    pdf_bytes = uploaded.read()
    reader = PdfReader(io.BytesIO(pdf_bytes))
    num_pages = len(reader.pages)
    page = st.number_input("Select page to edit", 0, num_pages-1, 0)
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf_doc:
        old_text = pdf_doc.pages[page].extract_text() or ""
    new_text = st.text_area("Type new content for page", value=old_text)
    st.warning("This operation will overwrite the entire page as an image. All original layout, fonts, and links will be lost.")
    if st.button("Replace Page Text"):
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf_doc:
            base_img = pdf_doc.pages[page].to_image(resolution=150).original.convert("RGB")
            draw = ImageDraw.Draw(base_img)
            draw.rectangle([(0,0), base_img.size], fill="white")
            font = ImageFont.load_default()
            draw.text((24,28), new_text, fill="#233", font=font)
            buff = io.BytesIO()
            base_img.save(buff, format="PDF")
            buff.seek(0)
            new_page = PdfReader(buff).pages[0]
        writer = PdfWriter()
        for i in range(num_pages):
            if i == page:
                writer.add_page(new_page)
            else:
                writer.add_page(reader.pages[i])
        out = io.BytesIO()
        writer.write(out)
        st.download_button("Download Edited PDF", out.getvalue(), file_name="edited_text.pdf")
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf_doc:
        st.image(pdf_doc.pages[page].to_image(resolution=150).original, caption="Preview")
