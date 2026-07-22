"""
Mzansi AI Hub
Heritage Intelligence Engine

Release 010 - Response Generation Application

Knowledge Communication Capability
"""

from response_generation_engine import ResponseGenerationEngine


class ResponseGenerationApplication:
    """
    Orchestrates the Knowledge Communication capability.

    Responsibilities
    ----------------
    - Validate capability inputs.
    - Coordinate the Response Generation Engine.
    - Return a standard capability result.

    This application does NOT:
    - Retrieve documents
    - Build embeddings
    - Construct context
    - Load AI models
    - Present information to users
    """

    def __init__(
        self,
        response_generation_engine: ResponseGenerationEngine,
    ):
        """
        Initialise the application.

        Parameters
        ----------
        response_generation_engine : ResponseGenerationEngine
            Engine responsible for generating grounded responses.
        """

        self.response_generation_engine = response_generation_engine

    def execute(
        self,
        question: str,
        context: str,
    ) -> dict:
        """
        Execute the Knowledge Communication capability.

        Parameters
        ----------
        question : str
            User question.

        context : str
            Prepared context supplied by another capability.

        Returns
        -------
        dict
            Standard capability result.
        """

        answer = self.response_generation_engine.generate_response(
            query=question,
            context=context,
        )

        return {
            "success": True,
            "capability": "Knowledge Communication",
            "release": "010",
            "question": question,
            "context": context,
            "answer": answer,
            "confidence": None,
        }