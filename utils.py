from docx import Document
import fitz  # PyMuPDF
from logger import logger
import io

def extract_text_from_pdf(file_bytes):
    try:
        with fitz.open(stream=file_bytes, filetype="pdf") as doc:
            text = ""
            for page in doc:
                text += page.get_text()
        logger.info("PDF text extraction successful (%d bytes)", len(file_bytes))
        return text
    except Exception as e:
        logger.error("PDF extraction error: %s", str(e))
        return ""

def extract_text_from_docx(file_bytes):
    try:
        doc = Document(io.BytesIO(file_bytes))
        text = "\n".join([para.text for para in doc.paragraphs])
        logger.info("DOCX text extraction successful (%d bytes)", len(file_bytes))
        return text
    except Exception as e:
        logger.error("DOCX extraction error: %s", str(e))
        return ""

def extract_text(file_bytes, filename):
    filename_lower = filename.lower()
    if filename_lower.endswith(".pdf"):
        return extract_text_from_pdf(file_bytes)
    elif filename_lower.endswith(".docx"):
        return extract_text_from_docx(file_bytes)
    else:
        logger.warning("Unsupported file type: %s", filename)
        return ""
