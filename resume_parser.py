import io
from PyPDF2 import PdfReader


def extract_text(uploaded_file):
    """
    Extract text from an uploaded PDF file.
    """

    if uploaded_file is None:
        return ""

    try:
        # Read uploaded file
        file_bytes = uploaded_file.read()

        # Create PDF reader from memory
        pdf_file = io.BytesIO(file_bytes)
        reader = PdfReader(pdf_file)

        text = ""

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        return text.strip()

    except Exception as e:
        raise Exception(f"Could not extract resume text: {e}")