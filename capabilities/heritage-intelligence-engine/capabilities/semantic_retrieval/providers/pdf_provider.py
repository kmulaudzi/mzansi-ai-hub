"""
Mzansi AI Hub
Heritage Intelligence Engine

Semantic Retrieval Capability

PDF Document Provider
"""

from pathlib import Path
from typing import Dict, List

from .base_provider import BaseProvider


class PDFProvider(BaseProvider):
    """
    Load PDF pages and convert them into the platform's
    standard document structure.

    Each PDF page becomes its own internal document.

    This preserves a natural source boundary and prevents
    the Chunking Engine from creating chunks that span
    unrelated pages.
    """

    def __init__(
        self,
        source_path: str,
    ):
        self.source_path = Path(source_path)

    def load_documents(
        self,
    ) -> List[Dict]:
        """
        Load text from all configured PDFs.

        Returns
        -------
        List[Dict]
            One standardized document per PDF page.

        Document structure
        ------------------
        {
            "filename": str,
            "title": str,
            "content": str,
            "source_type": "pdf",
            "source_path": str,
            "page_number": int
        }
        """

        import pymupdf

        if not self.source_path.exists():
            raise FileNotFoundError(
                "PDF source directory does not exist: "
                f"{self.source_path}"
            )

        if not self.source_path.is_dir():
            raise NotADirectoryError(
                "PDF source path is not a directory: "
                f"{self.source_path}"
            )

        documents = []

        for file_path in sorted(
            self.source_path.glob("*.pdf")
        ):
            pdf = pymupdf.open(file_path)

            title = (
                file_path.stem
                .replace("_", " ")
                .replace("-", " ")
                .title()
            )

            for page_index, page in enumerate(
                pdf,
                start=1,
            ):
                content = page.get_text(
                    "text"
                ).strip()

                if not content:
                    continue

                documents.append(
                    {
                        "filename": file_path.name,
                        "title": title,
                        "content": content,
                        "source_type": "pdf",
                        "source_path": str(
                            file_path
                        ),
                        "page_number": page_index,
                    }
                )

            pdf.close()

        return documents