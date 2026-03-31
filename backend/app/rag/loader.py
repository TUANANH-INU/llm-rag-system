"""
Document Loader for PDF and Web sources
"""

from pathlib import Path
from typing import Any, Dict, List

import pypdf
import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel


class Document(BaseModel):
    """Document model"""

    content: str
    metadata: Dict[str, Any]


class PDFLoader:
    """Load documents from PDF files"""

    @staticmethod
    def load(file_path: str) -> List[Document]:
        """Load PDF file and extract text"""
        documents = []
        try:
            with open(file_path, "rb") as file:
                reader = pypdf.PdfReader(file)
                for page_num, page in enumerate(reader.pages):
                    text = page.extract_text()
                    if text.strip():
                        documents.append(Document(content=text, metadata={"source": file_path, "page": page_num + 1, "type": "pdf"}))
        except Exception as e:
            raise Exception(f"Error loading PDF {file_path}: {str(e)}")

        return documents


class WebLoader:
    """Load documents from web URLs"""

    @staticmethod
    def load(url: str) -> List[Document]:
        """Load webpage and extract text"""
        documents = []
        try:
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "html.parser")

            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()

            # Get text
            text = soup.get_text(separator=" ", strip=True)

            if text.strip():
                documents.append(Document(content=text, metadata={"source": url, "type": "web"}))
        except Exception as e:
            raise Exception(f"Error loading URL {url}: {str(e)}")

        return documents


class DocumentLoader:
    """Main document loader"""

    @staticmethod
    def load_pdf(file_path: str) -> List[Document]:
        """Load from PDF"""
        return PDFLoader.load(file_path)

    @staticmethod
    def load_web(url: str) -> List[Document]:
        """Load from web URL"""
        return WebLoader.load(url)

    @staticmethod
    def load_directory(directory: str) -> List[Document]:
        """Load all PDFs from a directory"""
        documents = []
        pdf_files = Path(directory).glob("*.pdf")

        for pdf_file in pdf_files:
            documents.extend(PDFLoader.load(str(pdf_file)))

        return documents
