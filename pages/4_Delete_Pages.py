import streamlit as st
import io
from PyPDF2 import PdfReader, PdfWriter

st.markdown("# 🗑️ Delete Pages from PDF")
st.caption("Remove any pages by selecting them below.")

uploaded_pdf = st.file_uploader("Upload PDF", type="pdf")
if uploaded_pdf:
    reader = PdfReader(uploaded_pdf)
    num_pages = len(reader.pages)
    del_pages = st.multiselect("Select Page(s) to Delete (0-based)", range(num_pages))
    if st.button("Delete Selected Pages"):
        writer = PdfWriter()
        for i in range(num_pages):
            if i not in del_pages:
                writer.add_page(reader.pages[i])
        out = io.BytesIO()
        writer.write(out)
        st.download_button("Download PDF (Pages Deleted)", data=out.getvalue(), file_name="pages_deleted.pdf")
