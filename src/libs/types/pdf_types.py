from typing import TypedDict, List, Union

class FileMetadata(TypedDict):
    file_name: str
    file_time: str

class DocumentMetadata(TypedDict):
    format: str
    title: str
    author: str
    subject: str
    keywords: str
    last_modified: str
    name: str
    is_pdf: bool
    language: str
    page_count: int
    toc: List[dict[str, Union[str, int]]]

class TextBlock(TypedDict):
    x1: float
    y1: float
    x2: float
    y2: float
    text: str
    block_no: int
    line_no: int

class ImageInfo(TypedDict):
    number: int
    bbox: List[float]
    transform: List[float]
    width: int
    height: int
    colorspace: int
    cs_name: str
    xres: int
    yres: int
    bpc: int
    size: int

class PageText(TypedDict):
    page_number: int
    text: str
    text_blocks: List[tuple[float, float, float, float, str, int, int]] # 원본: List[TextBlock]
    label: str
    link: List[dict[str, str]]
    images: List[List[Union[int, str]]]
    image_info: List[ImageInfo] # 원본: List[ImageInfo]

class ParsedContent(TypedDict):
    document_id: str
    full_text: str
    page_texts: List[PageText]

class PDFDocumentData(TypedDict):
    file_metadata: FileMetadata
    document_metadata: DocumentMetadata
    parsed_content: ParsedContent