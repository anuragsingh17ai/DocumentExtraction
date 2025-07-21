import io
import os
import httpx # Use httpx for async requests
import pdfplumber
import bibtexparser

# --- Internal helper functions for reading from memory ---

def _read_text_from_pdf_from_memory(file_bytes: bytes) -> str:
    """Reads text from a PDF file's bytes."""
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        text = "".join([page.extract_text() or "" for page in pdf.pages])
    return text

def _read_text_from_md_from_memory(file_bytes: bytes) -> str:
    """Reads text from a Markdown file's bytes."""
    return file_bytes.decode("utf-8")

async def _read_text_from_bib_from_memory_async(file_bytes: bytes) -> str:
    """Parses BibTeX bytes, downloads the linked PDF asynchronously, and extracts its text."""
    bibtex_text = file_bytes.decode("utf-8")
    bib_db = bibtexparser.loads(bibtex_text)
    if not bib_db.entries:
        raise ValueError("No entries found in BibTeX")

    entry = bib_db.entries[0]
    url = entry.get("url")
    if not url or not url.endswith(".pdf"):
        raise ValueError("No valid PDF URL found in BibTeX")

    # Asynchronously download the PDF content
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        pdf_bytes = response.content

    # Reuse the in-memory PDF reader
    return _read_text_from_pdf_from_memory(pdf_bytes)

# --- Main dispatcher function ---

async def read_file_from_memory_async(file_bytes: bytes, extension: str) -> str:
    """
    Dispatcher that reads file content from memory based on the file extension.
    This function is async to handle the BibTeX case.
    """
    extension = extension.lower()
    if extension == ".pdf":
        return _read_text_from_pdf_from_memory(file_bytes)
    elif extension == ".md":
        return _read_text_from_md_from_memory(file_bytes)
    elif extension == ".bib":
        return await _read_text_from_bib_from_memory_async(file_bytes)
    else:
        # Fallback for plain text files
        try:
            return file_bytes.decode("utf-8")
        except UnicodeDecodeError:
            raise ValueError(f"Unsupported file extension: {extension}, and could not decode as plain text.")