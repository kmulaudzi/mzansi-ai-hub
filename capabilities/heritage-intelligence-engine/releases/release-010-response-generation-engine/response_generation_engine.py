"""
Response Generation Engine

This engine generates a grounded natural-language answer using:

1. A user question
2. Heritage context supplied by the Context Engine

The engine does not retrieve documents, create embeddings,
search FAISS, build context, or manage the user interface.
"""


class ResponseGenerationEngine:
    """
    Generates grounded answers from a question and supplied context.
    """

    def __init__(
        self,
        model,
        tokenizer,
        max_new_tokens: int = 200,
    ):
        """
        Initialise the Response Generation Engine.

        Parameters
        ----------
        model
            A Hugging Face text-generation model.

        tokenizer
            A Hugging Face tokenizer compatible with the model.

        max_new_tokens
            Maximum number of new tokens the model may generate.
        """

        if model is None:
            raise ValueError("A response-generation model is required.")

        if tokenizer is None:
            raise ValueError("A tokenizer is required.")

        if max_new_tokens <= 0:
            raise ValueError("max_new_tokens must be greater than zero.")

        self.model = model
        self.tokenizer = tokenizer
        self.max_new_tokens = max_new_tokens

    def _build_prompt(
        self,
        query: str,
        context: str,
    ) -> str:
        """
        Build the controlled prompt sent to the language model.

        The prompt instructs the model to answer only from the
        supplied heritage context.
        """

        clean_query = (query or "").strip()
        clean_context = (context or "").strip()

        return f"""
You are the Heritage Intelligence Engine.

Answer the user's question using only the supplied heritage context.

Do not use outside knowledge.

Do not invent names, dates, places, statistics, or events.

If the answer is not contained in the supplied context, respond exactly with:

The available heritage documents do not contain enough information to answer this question.

Keep the answer clear, factual, and concise.

Question:
{clean_query}

Heritage Context:
{clean_context}

Answer:
""".strip()

    def generate_response(
        self,
        query: str,
        context: str,
    ) -> str:
        """
        Generate a grounded answer.

        Parameters
        ----------
        query
            The user's heritage question.

        context
            The approved heritage context produced by the
            Context Engine.

        Returns
        -------
        str
            The generated answer.
        """

        clean_query = (query or "").strip()
        clean_context = (context or "").strip()

        if not clean_query:
            raise ValueError("The query cannot be empty.")

        if not clean_context:
            return (
                "The available heritage documents do not contain "
                "enough information to answer this question."
            )

        prompt = self._build_prompt(
            query=clean_query,
            context=clean_context,
        )

        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True,
        )

        outputs = self.model.generate(
            **inputs,
            max_new_tokens=self.max_new_tokens,
            do_sample=False,
        )

        response = self.tokenizer.decode(
            outputs[0],
            skip_special_tokens=True,
        )

        clean_response = response.strip()

        if not clean_response:
            return (
                "The available heritage documents do not contain "
                "enough information to answer this question."
            )

        return clean_response