from openai import OpenAI
from jester.settings import settings 
from prompts import GPTParsedResume, ScoreCard, Prompts
from pypdf import PdfReader
import docx
import os 

client = OpenAI(api_key=settings.openai_key)  

def extract_file_content(file_path: str) -> tuple[str, int]:
    file_extension = os.path.splitext(file_path)[1].lower()

    if file_extension == ".pdf":
        return extract_pdf_content(file_path)
    elif file_extension == ".docx":
        return extract_docx_content(file_path)
    else:
        raise ValueError("Unsupported file format. Please provide a PDF or DOCX file.")

def extract_pdf_content(pdf_path: str) -> tuple[str, int]:

    reader = PdfReader(pdf_path)

    num_pages = len(reader.pages)

    text = ""
    for page in reader.pages:
        text += page.extract_text(extraction_mode="layout") + "\n"

    return text, num_pages

def extract_docx_content(file_path) -> tuple[str, int]:
    doc = docx.Document(file_path)
    text = ""

    for para in doc.paragraphs:
        text += para.text + "\n"
    
    # Estimate page count (since DOCX files don't have a concept of pages like PDFs)
    # This is a rough estimate and may not be accurate for complex layouts.
    num_pages = max(1, len(text) // 2000)  # Assuming an average of 2000 characters per page

    return text, num_pages

def parse_resume(contents: str) -> GPTParsedResume:
    prompts = Prompts(resume_content=contents)

    completion = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[
            {"role": "system", "content": prompts.instruction_content},
            {"role": "user", "content": contents},
        ],
        response_format=GPTParsedResume,
    )

    return completion.choices[0].message.parsed, contents

