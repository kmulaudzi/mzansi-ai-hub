"""
Mzansi AI Hub
Heritage Intelligence Engine

Response Generation Capability

Base Generation Provider
"""

from abc import ABC, abstractmethod


class BaseGenerationProvider(ABC):
    """
    Contract for response-generation technologies.

    A generation provider is responsible for communicating
    with a specific model technology.

    Examples
    --------
    - Hugging Face local model
    - OpenAI API
    - Anthropic API
    - Google Gemini
    - future internally hosted model

    The Response Generation Engine should not need to know
    how the underlying model generates text.
    """

    @abstractmethod
    def generate(
        self,
        prompt: str,
    ) -> str:
        """
        Generate text from a grounded prompt.

        Parameters
        ----------
        prompt:
            Fully constructed grounded prompt.

        Returns
        -------
        str
            Generated natural-language response.
        """

        raise NotImplementedError