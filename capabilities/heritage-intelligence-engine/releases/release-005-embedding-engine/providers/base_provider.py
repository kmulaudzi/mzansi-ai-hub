"""
Mzansi AI Hub
Heritage Intelligence Engine

Release 003 - Document Intelligence

Base Provider Contract
"""

from abc import ABC, abstractmethod
from typing import Dict, List


class BaseProvider(ABC):
    """
    Abstract base class for all document providers.

    Every provider must know how to load documents
    from one specific data source.

    Examples
    --------
    - MarkdownProvider
    - PDFProvider
    - ImageProvider
    - AudioProvider
    """

    @abstractmethod
    def load_documents(self) -> List[Dict]:
        """
        Load documents from a data source.

        Returns
        -------
        List[Dict]

        Each document must follow this structure:

        {
            "filename": "...",
            "title": "...",
            "content": "..."
        }
        """
        pass