"""
Resume Parser Module

Extracts text, bullets, and structure from PDF/DOCX resumes.
Uses smart parsing to handle ANY resume format.
"""

import io
from typing import Dict, List, Any
from app.smart_parser import parse_resume_smart


def parse_resume(content: bytes, content_type: str) -> Dict[str, Any]:
    """
    Parse a resume file and extract structured data.

    Args:
        content: File content as bytes
        content_type: MIME type (application/pdf or application/vnd.openxmlformats-officedocument.wordprocessingml.document)

    Returns:
        Dictionary with:
            - text: Full text content
            - bullets: List of bullet points
            - sections: Dict mapping section names to content
            - contact_info: Dict with email, phone, etc.

    TODO: Implement parsing logic using:
        - pdfplumber for PDF files
        - python-docx for DOCX files
    """

    if content_type == "application/pdf":
        return parse_pdf(content)
    elif "wordprocessingml" in content_type:
        return parse_docx(content)
    else:
        raise ValueError(f"Unsupported content type: {content_type}")


def parse_pdf(content: bytes) -> Dict[str, Any]:
    """
    Parse PDF resume using pdfplumber.

    Extracts text from all pages and uses smart parser to structure it.
    """
    try:
        import pdfplumber
    except ImportError:
        # Fallback if pdfplumber not installed
        return {
            "text": "ERROR: pdfplumber not installed",
            "bullets": [],
            "sections": {},
            "contact_info": {}
        }

    # Extract text from PDF
    text = ""
    with pdfplumber.open(io.BytesIO(content)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    # Use smart parser to structure the text
    return parse_resume_smart(text)


def parse_docx(content: bytes) -> Dict[str, Any]:
    """
    Parse DOCX resume using python-docx.

    Extracts text from all paragraphs and uses smart parser.
    """
    try:
        from docx import Document
    except ImportError:
        return {
            "text": "ERROR: python-docx not installed",
            "bullets": [],
            "sections": {},
            "contact_info": {}
        }

    # Extract text from DOCX
    doc = Document(io.BytesIO(content))
    text = ""

    for paragraph in doc.paragraphs:
        if paragraph.text.strip():
            text += paragraph.text + "\n"

    # Use smart parser to structure the text
    return parse_resume_smart(text)


def extract_bullets(text: str) -> List[str]:
    """
    Extract bullet points from text.

    Identifies lines that start with:
        - Bullet characters: •, -, *, ○, ▪
        - Numbers: 1., 2., etc.
        - Common action verbs

    TODO: Improve bullet detection logic
    """

    bullets = []
    lines = text.split('\n')

    bullet_chars = ['•', '-', '*', '○', '▪', '▫', '■', '□']

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Check if line starts with bullet character
        if any(line.startswith(char) for char in bullet_chars):
            bullets.append(line.lstrip('•-*○▪▫■□ '))
            continue

        # Check if line starts with number (1., 2., etc.)
        if line[0].isdigit() and '.' in line[:3]:
            bullets.append(line.split('.', 1)[1].strip())
            continue

    return bullets


def clean_text(text: str) -> str:
    """
    Clean and normalize resume text.

    - Remove extra whitespace
    - Normalize line breaks
    - Remove special characters that might interfere with parsing
    """

    # Remove multiple spaces
    text = ' '.join(text.split())

    return text
