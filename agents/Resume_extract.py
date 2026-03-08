from pypdf import PdfReader
from io import BytesIO

def parse_resume(state: dict) -> dict:
    uploaded_file = state.get("resume_file")

    if uploaded_file is None:
        raise ValueError("resume_file missing in state")

    # Streamlit UploadedFile → bytes → BytesIO
    pdf_bytes = uploaded_file.read()
    pdf_stream = BytesIO(pdf_bytes)

    reader = PdfReader(pdf_stream)

    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"

    return {
        **state,
        "resume_text": text
    }
