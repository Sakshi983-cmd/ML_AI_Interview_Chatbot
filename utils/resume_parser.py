from io import BytesIO
import PyPDF2

def extract_text_from_pdf(file):
    try:
        pdf_file = BytesIO(file.getvalue())
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        pdf_file.close()
        return text.strip()
    except Exception as e:
        return f"Parse error: {e}. Using dummy resume."
