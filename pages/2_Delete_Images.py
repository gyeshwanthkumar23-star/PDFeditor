import streamlit as st
import io
from PyPDF2 import PdfReader, PdfWriter
import pdfplumber
from PIL import Image, ImageDraw

st.markdown("# 🧹 Delete All Images (per page, keep layout/text)")
uploaded = st.file_uploader("Upload PDF", type="pdf")
if uploaded:
    pdf_bytes = uploaded.read()
    reader = PdfReader(io.BytesIO(pdf_bytes))
    num_pages = len(reader.pages)
    page = st.number_input("Page number", 0, num_pages-1, 0)
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf_doc:
        page_obj = pdf_doc.pages[page]
        base_img = page_obj.to_image(resolution=150).original.convert('RGB')
        images = page_obj.images
        page_height = page_obj.height
        for img in images:
            x0, y0, x1, y1 = img['x0'], img['top'], img['x1'], img['bottom']
            y0_img = page_height - y1
            y1_img = page_height - y0
            ImageDraw.Draw(base_img).rectangle([x0, y0_img, x1, y1_img], fill='white')
        buff = io.BytesIO()
        base_img.save(buff, format='PDF')
        buff.seek(0)
        new_page = PdfReader(buff).pages[0]
    if st.button("Remove Images & Download PDF"):
        writer = PdfWriter()
        for i in range(num_pages):
            if i == page:
                writer.add_page(new_page)
            else:
                writer.add_page(reader.pages[i])
        out = io.BytesIO()
        writer.write(out)
        st.download_button("Download PDF", out.getvalue(), file_name="images_deleted.pdf")
    st.image(base_img, caption="Preview with images removed")
