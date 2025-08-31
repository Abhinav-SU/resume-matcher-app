import io
from utils import extract_text_from_pdf, extract_text_from_docx, extract_text
from docx import Document
import fitz


def create_pdf_bytes(text: str) -> bytes:
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), text)
    pdf_bytes = doc.tobytes()
    doc.close()
    return pdf_bytes


def create_docx_bytes(text: str) -> bytes:
    buffer = io.BytesIO()
    doc = Document()
    doc.add_paragraph(text)
    doc.save(buffer)
    return buffer.getvalue()


def test_extract_text_from_pdf():
    text = "Hello PDF"
    pdf_bytes = create_pdf_bytes(text)
    extracted = extract_text_from_pdf(pdf_bytes).strip()
    assert extracted == text


def test_extract_text_from_docx():
    text = "Hello DOCX"
    docx_bytes = create_docx_bytes(text)
    extracted = extract_text_from_docx(docx_bytes).strip()
    assert extracted == text


def test_extract_text_dispatch_and_unsupported():
    pdf_text = "Pdf Content"
    pdf_bytes = create_pdf_bytes(pdf_text)
    assert extract_text(pdf_bytes, "file.pdf").strip() == pdf_text

    docx_text = "Docx Content"
    docx_bytes = create_docx_bytes(docx_text)
    assert extract_text(docx_bytes, "file.docx").strip() == docx_text

    assert extract_text(b"data", "file.txt") == ""
