"""Text extraction from documents using LangChain + ebooklib.

Supports PDF, EPUB, plain text, HTML, and Markdown.
"""

from __future__ import annotations

from pathlib import Path


def extract_text(path: str | Path) -> str:
    """Load a document and return its full text as a single string."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    suffix = path.suffix.lower()

    if suffix == ".epub":
        return _extract_epub(path)
    if suffix == ".txt":
        return path.read_text(encoding="utf-8")
    if suffix == ".pdf":
        return _extract_pdf(path)
    if suffix in (".html", ".htm"):
        return _extract_html(path)
    if suffix == ".md":
        return path.read_text(encoding="utf-8")

    raise ValueError(
        f"Unsupported file type: {suffix}. "
        f"Supported: .epub, .pdf, .txt, .html, .md"
    )


def _extract_epub(path: Path) -> str:
    """Extract text from EPUB using ebooklib + BeautifulSoup.

    Falls back to direct ZIP extraction for scanned/OCR epubs where
    ebooklib's ITEM_DOCUMENT enumeration misses page content.
    """
    import ebooklib
    from bs4 import BeautifulSoup
    from ebooklib import epub

    book = epub.read_epub(str(path), options={"ignore_ncx": True})
    texts: list[str] = []

    for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
        soup = BeautifulSoup(item.get_content(), "html.parser")
        text = soup.get_text(separator="\n", strip=True)
        if text:
            texts.append(text)

    result = "\n\n".join(texts)

    # Fallback: if ebooklib extracted very little, read HTML files from ZIP
    if len(result) < 500:
        import re
        import zipfile

        with zipfile.ZipFile(path) as zf:
            html_names = sorted(
                [n for n in zf.namelist() if re.search(r"page_\d+\.html$", n)],
                key=lambda n: int(re.search(r"page_(\d+)", n).group(1)),
            )
            texts = []
            for name in html_names:
                soup = BeautifulSoup(zf.read(name), "html.parser")
                text = soup.get_text(separator=" ", strip=True)
                if text:
                    texts.append(text)
            result = "\n\n".join(texts)

    return result


def _extract_pdf(path: Path) -> str:
    """Extract text from PDF via LangChain's community loader.

    Returns the text and detects scanned/image-based PDFs by checking
    if the extracted text is too short relative to page count.
    """
    from langchain_community.document_loaders import PyPDFLoader

    docs = PyPDFLoader(str(path)).load()
    text = "\n\n".join(doc.page_content for doc in docs)

    # Detect scanned PDFs: if text per page is very low, it's likely image-based
    if docs and len(text.strip()) < len(docs) * 100:
        raise ScannedPDFError(
            page_count=len(docs),
            extracted_chars=len(text.strip()),
            path=path,
        )

    return text


class ScannedPDFError(Exception):
    """Raised when a PDF appears to be scanned/image-based and needs OCR."""

    def __init__(self, page_count: int, extracted_chars: int, path: Path):
        self.page_count = page_count
        self.extracted_chars = extracted_chars
        self.path = path
        super().__init__(
            f"Scanned PDF detected: {path.name} has {page_count} pages "
            f"but only {extracted_chars} chars of text. "
            f"Use pdf_to_images() then OCR with Haiku vision."
        )


def pdf_to_images(path: str | Path, out_dir: str | Path, dpi: int = 200) -> list[Path]:
    """Convert a PDF to PNG images, one per page. Returns list of image paths."""
    import fitz

    path = Path(path)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    doc = fitz.open(str(path))
    image_paths = []
    for i, page in enumerate(doc):
        pix = page.get_pixmap(dpi=dpi)
        img_path = out_dir / f"page_{i:03d}.png"
        pix.save(str(img_path))
        image_paths.append(img_path)

    return image_paths


def _extract_html(path: Path) -> str:
    from bs4 import BeautifulSoup

    raw = path.read_text(encoding="utf-8")
    soup = BeautifulSoup(raw, "html.parser")
    return soup.get_text(separator="\n", strip=True)


def split_text(text: str, max_chars: int) -> list[str]:
    """Split text into chunks of roughly *max_chars*.

    Tries paragraph breaks (\\n\\n) first, falls back to line breaks (\\n),
    then splits oversized blocks by sentences as a last resort.
    """
    # First pass: split on \n\n
    raw_blocks = text.split("\n\n")

    # Explode any block that's still too large by splitting on \n
    blocks: list[str] = []
    for block in raw_blocks:
        if len(block) <= max_chars:
            blocks.append(block)
        else:
            # split on single newlines
            lines = block.split("\n")
            sub: list[str] = []
            sub_len = 0
            for line in lines:
                if sub_len + len(line) > max_chars and sub:
                    blocks.append("\n".join(sub))
                    sub = []
                    sub_len = 0
                sub.append(line)
                sub_len += len(line)
            if sub:
                blocks.append("\n".join(sub))

    # Second pass: accumulate blocks into chunks up to max_chars
    chunks: list[str] = []
    current: list[str] = []
    current_len = 0

    for block in blocks:
        block_len = len(block)
        if current_len + block_len > max_chars and current:
            chunks.append("\n\n".join(current))
            current = []
            current_len = 0
        current.append(block)
        current_len += block_len

    if current:
        chunks.append("\n\n".join(current))

    return chunks
