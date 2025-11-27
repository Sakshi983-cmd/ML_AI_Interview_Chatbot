from langchain_community.document_loaders import PyPDFLoader
import os

def extract_text_from_pdf(file):
    path = f"./temp_{file.name}"
    with open(path, "wb") as f:
        f.write(file.getvalue())
    loader = PyPDFLoader(path)
    pages = loader.load()
    os.remove(path)
    return "\n".join([page.page_content for page in pages])
