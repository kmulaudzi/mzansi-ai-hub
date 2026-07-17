"""
Mzansi AI Hub
Heritage Intelligence Engine

Release 003 - Document Intelligence

PDF Document Provider
"""

from pathlib import Path
from typing import Dict, List

from providers.base_provider import BaseProvider


class PDFProvider(BaseProvider):
    """
    Loads PDF files and converts them into the platform's
    standard document structure.
    """

    def __init__(self, source_path: str):
        self.source_path = Path(source_path)

    def load_documents(self) -> List[Dict]:
        """
        Load text from all PDFs in the configured directory.
        """

        import fitz

        if not self.source_path.exists():
            raise FileNotFoundError(
                f"PDF source directory does not exist: "
                f"{self.source_path}"
            )

        if not self.source_path.is_dir():
            raise NotADirectoryError(
                f"PDF source path is not a directory: "
                f"{self.source_path}"
            )

        documents = []

        for file_path in sorted(
            self.source_path.glob("*.pdf")
        ):
            pdf = fitz.open(file_path)

            page_text = []

            for page in pdf:
                text = page.get_text("text").strip()

                if text:
                    page_text.append(text)

            pdf.close()

            content = "\n\n".join(page_text).strip()

            if not content:
                continue

            documents.append(
                {
                    "filename": file_path.name,
                    "title": file_path.stem.replace(
                        "_",
                        " ",
                    ).replace(
                        "-",
                        " ",
                    ).title(),
                    "content": content,
                    "source_type": "pdf",
                    "source_path": str(file_path),
                }
            )

        return documents