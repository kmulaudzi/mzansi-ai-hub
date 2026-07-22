"""
Mzansi AI Hub
Heritage Intelligence Engine

Release 003 - Document Intelligence

Markdown Document Provider
"""

from pathlib import Path
from typing import Dict, List

from .base_provider import BaseProvider


class MarkdownProvider(BaseProvider):
    """
    Loads Markdown files and converts them into
    the platform's standard document structure.
    """

    def __init__(self, source_path: str):
        self.source_path = Path(source_path)

    def load_documents(self) -> List[Dict]:
        """
        Load all Markdown documents from the configured directory.

        Returns
        -------
        List[Dict]
            Documents containing filename, title, content,
            source type and source path.
        """

        if not self.source_path.exists():
            raise FileNotFoundError(
                f"Markdown source directory does not exist: "
                f"{self.source_path}"
            )

        if not self.source_path.is_dir():
            raise NotADirectoryError(
                f"Markdown source path is not a directory: "
                f"{self.source_path}"
            )

        documents = []

        for file_path in sorted(self.source_path.glob("*.md")):
            content = file_path.read_text(
                encoding="utf-8"
            ).strip()

            if not content:
                continue

            first_line = content.splitlines()[0]

            title = first_line.replace("#", "").strip()

            documents.append(
                {
                    "filename": file_path.name,
                    "title": title,
                    "content": content,
                    "source_type": "markdown",
                    "source_path": str(file_path),
                }
            )

        return documents