import io
from PyPDF2 import PdfReader

def extract_pdf_text(blob):
    # Download PDF file content as bytes
    pdf_bytes = blob.download_as_bytes()

    # Process PDF content
    pdf_file = io.BytesIO(pdf_bytes)
    pdf_reader = PdfReader(pdf_file)
    
    num_pages = len(pdf_reader.pages)
    text_content = ''
    for page_num in range(num_pages):
        page = pdf_reader.pages[page_num]
        text_content += page.extract_text()

    return text_content