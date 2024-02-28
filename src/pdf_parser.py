import os
import uuid
from datetime import datetime
import fitz  # PyMuPDF
from libs.date_parser import parse_pdf_date
from libs.types.pdf_types import FileMetadata, DocumentMetadata, ParsedContent, PDFDocumentData, PageText
from libs.logger import Logger

class PDFParser:
    def __init__(self):
        self.logger = Logger()

    def parse_document(self, file_path: str) -> PDFDocumentData:
        try:
            self.logger.start("File Metadata Extraction")
            file_metadata: FileMetadata = self._get_file_metadata(file_path)
            self.logger.end()

            self.logger.start("Open PDF Document")
            with fitz.open(file_path) as doc:
                self.logger.end()

                self.logger.start("Document Metadata Extraction")
                document_metadata: DocumentMetadata = self._extract_document_metadata(doc)
                self.logger.end()

                self.logger.start("Text Content Extraction")
                parsed_content: ParsedContent = self._extract_text_content(doc)
                self.logger.end()

            return {
                "file_metadata": file_metadata,
                "document_metadata": document_metadata,
                "parsed_content": parsed_content,
            }
        except Exception as e:
            raise RuntimeError(f"Error parsing document: {e}")

    def _get_file_metadata(self, file_path: str) -> FileMetadata:
        try:
            file_stats = os.stat(file_path)
            return {
                "file_name": os.path.basename(file_path),
                "file_time": datetime.fromtimestamp(file_stats.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
            }
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Error retrieving file metadata: {e}")
        except Exception as e:
            raise RuntimeError(f"Unexpected error retrieving file metadata: {e}")

    def _extract_document_metadata(self, doc: fitz.Document) -> DocumentMetadata:
        metadata: dict[str, str] = doc.metadata  # type: ignore
        
        documentMetadata: DocumentMetadata = {
            "format": metadata.get("format", "Unknown"),
            "title": metadata.get("title", "Unknown"),
            "author": metadata.get("author", "Unknown"),
            "subject": metadata.get("subject", "Unknown"),
            "keywords": metadata.get("keywords", "Unknown"),
            "last_modified": parse_pdf_date(metadata.get("modDate", "Unknown")),
            "name": doc.name,  # file path # type: ignore
            "is_pdf": doc.is_pdf,
            "language": doc.language, # type: ignore
            "page_count": doc.page_count, # type: ignore
            "toc": doc.get_toc(), # type: ignore
        }
        return documentMetadata

    def _extract_text_content(self, doc: fitz.Document) -> ParsedContent:
        full_text: str = ""
        page_texts: list[PageText] = []
        for page_num in range(len(doc)):
            page = doc[page_num]
            page_data: PageText = {
                "page_number": page_num + 1,
                "text": page.get_text(), # type: ignore
                "text_blocks": page.get_text_blocks(), # type: ignore
                "label": page.get_label(), # type: ignore
                "link": page.get_links(), # type: ignore
                "images": page.get_images(), # type: ignore
                "image_info": page.get_image_info(), # type: ignore
            }
            full_text += page_data["text"]
            page_texts.append(page_data)

        return {
            "document_id": str(uuid.uuid4()),
            "full_text": full_text,
            "page_texts": page_texts,
        }
