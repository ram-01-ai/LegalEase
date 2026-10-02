import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


def generate_legal_document(
    document_type: str,
    parties: str,
    terms: str,
    effective_date: str
):

    prompt = f"""
You are a legal document drafting assistant.

Create a professional draft of the following legal document.

Document Type:
{document_type}

Parties Involved:
{parties}

Terms / Conditions:
{terms}

Effective Date:
{effective_date}

Requirements:
- Use clear and professional legal language.
- Include appropriate headings and clauses.
- Do not invent important facts that were not provided.
- Clearly identify missing information where necessary.
- This is a draft for review and not a substitute for advice from a qualified lawyer.

Generate only the legal document.
"""

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt
    )

    return response.text