from typing import Type
from pydantic import BaseModel
from crewai.tools import BaseTool
from PyPDF2 import PdfReader
import logging

logger = logging.getLogger(__name__)

class CVReaderToolInput(BaseModel):
    file_path: str

class CVReaderTool(BaseTool):
    name: str = "CV Reader Tool"
    description: str = (
        "A tool for reading both TXT and PDF CV files. "
        "It can handle both plain text files and PDF files, "
        "skipping any password-protected PDFs."
    )
    args_schema: Type[BaseModel] = CVReaderToolInput

    def _run(self, file_path: str) -> str:
        try:
            if file_path.endswith('.pdf'):
                with open(file_path, 'rb') as pdf_file:
                    reader = PdfReader(pdf_file)
                    if reader.is_encrypted:
                        return f"Error: PDF file {file_path} is password protected and cannot be read."
                    
                    text = ""
                    for page in reader.pages:
                        text += page.extract_text() + "\n"
                    return text
            else:
                # Read text file
                with open(file_path, 'r') as txt_file:
                    return txt_file.read()
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {str(e)}")
            return f"Error reading file {file_path}: {str(e)}" 