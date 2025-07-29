import streamlit as st
import requests
import io

st.markdown("# 📝 In-Place PDF Text Edit (via PDF.co API)")
st.caption("⚡ True PDF text editing—preserves layout, fonts, and all selectable text using PDF.co API.")

# --- PUT YOUR API KEY HERE ---
PDFCO_API_KEY = "sashindra126@gmail.com_0CnfpyoBLB5Dsv3bdu621HlFuoQGdUn4tpFetuDR5uMHob1Lsprg7sRDfdE317TK"   # <-- Replace this with your actual API key, keep the quotes

uploaded = st.file_uploader("Upload PDF", type="pdf")
if uploaded:
    # Save PDF to temporary file to upload to PDF.co storage
    with st.spinner("Uploading PDF to PDF.co..."):
        files = {'file': uploaded}
        stor_headers = {"x-api-key": PDFCO_API_KEY}
        stor_url = "https://api.pdf.co/v1/file/upload/get-presigned-url?contenttype=application/pdf&name=uploaded.pdf"
        presigned_resp = requests.get(stor_url, headers=stor_headers)
        if presigned_resp.status_code == 200 and presigned_resp.json()["error"] == False:
            upload_url = presigned_resp.json()["presignedUrl"]
            file_url = presigned_resp.json()["url"]
            put_resp = requests.put(upload_url, data=uploaded, headers={"Content-Type": "application/pdf"})
        else:
            st.error("Failed to get upload URL from PDF.co. Check your API key / credits.")
            st.stop()
    st.success("PDF file uploaded.")

    # Ask user for find/replace details
    st.markdown("## 👇 Text Replacement")
    find_text = st.text_input("Text to replace (case sensitive, as it appears in the PDF):")
    replace_text = st.text_input("Replace with (your new text):")
    page_indexes = st.text_input(
        "Pages to perform replace (e.g. `0`, `0-1,3` or leave empty for all pages):",
        value=""
    )
    if st.button("Edit PDF Text (in place)"):
        with st.spinner("Editing PDF text with PDF.co, please wait..."):
            endpoint = "https://api.pdf.co/v1/pdf/edit/replace-text"
            payload = {
                "url": file_url,
                "searchString": find_text,
                "replaceString": replace_text,
                "name": "edited.pdf",
                "pages": page_indexes,
            }
            headers = {"x-api-key": PDFCO_API_KEY, "Content-Type": "application/json"}
            api_resp = requests.post(endpoint, headers=headers, json=payload)
            if api_resp.ok and not api_resp.json().get("error"):
                download_url = api_resp.json().get("url")
                # Download the edited PDF and serve to user
                edited_pdf = requests.get(download_url).content
                st.success("PDF text edited! Download below ⬇️")
                st.download_button(
                    label="Download Edited PDF",
                    data=edited_pdf,
                    file_name="edited_inplace.pdf",
                    mime="application/pdf"
                )
            else:
                st.error(f"PDF.co error: {api_resp.text}")

st.info("""
- **Limitation:** Find/replace is *case sensitive* and replaces all matches on chosen pages.
- **Supported by PDF.co API:** True in-place PDF edits with original layout preserved.
- **No changes made if 'Text to replace' is not found in the PDF content.
""")
