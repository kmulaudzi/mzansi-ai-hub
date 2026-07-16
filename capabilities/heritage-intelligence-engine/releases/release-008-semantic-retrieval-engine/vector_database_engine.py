"""
Mzansi AI Hub
Heritage Intelligence Engine

Release 007 - Vector Database Engine

FAISS Vector Database Implementation
"""

from copy import deepcopy
from typing import Any, Dict, List

import faiss
import numpy as np


class VectorDatabaseEngine:
    """
    Build and search a FAISS vector index.

    Architectural contract
    ----------------------
    build_index(embedded_chunks)
        Store embedded chunks in a searchable vector index.

    search(query_embedding, top_k)
        Retrieve the nearest embedded chunks.

    FAISS is only the implementation behind this contract.
    The rest of the Heritage Intelligence Engine does not need
    to know how FAISS works internally.
    """

    def __init__(self):
        """
        Initialise an empty vector database.

        State
        -----
        index
            FAISS searchable vector index.

        embedded_chunks
            Original chunks whose embeddings were added to the index.

            Their list position is aligned with the vector position
            inside the FAISS index.

        embedding_dimension
            Number of values in each embedding vector.
        """

        self.index = None
        self.embedded_chunks: List[Dict] = []
        self.embedding_dimension = None

    def build_index(
        self,
        embedded_chunks: List[Dict],
    ) -> None:
        """
        Build a searchable FAISS index from embedded chunks.

        Startup flow
        ------------
        Embedded chunks
            ↓
        Extract vectors
            ↓
        Convert to float32 NumPy matrix
            ↓
        Normalize vectors
            ↓
        Build FAISS inner-product index
            ↓
        Add vectors to index
        """

        if not embedded_chunks:
            raise ValueError(
                "VectorDatabaseEngine requires at least "
                "one embedded chunk."
            )

        vectors = []

        for chunk in embedded_chunks:
            embedding = chunk.get("embedding")

            if embedding is None:
                raise ValueError(
                    "Every chunk must contain an embedding."
                )

            vectors.append(embedding)

        # FAISS expects a two-dimensional float32 NumPy array:
        #
        # [
        #     [vector 1],
        #     [vector 2],
        #     [vector 3],
        # ]
        vector_matrix = np.asarray(
            vectors,
            dtype=np.float32,
        )

        if vector_matrix.ndim != 2:
            raise ValueError(
                "Embeddings must form a two-dimensional matrix."
            )

        self.embedding_dimension = vector_matrix.shape[1]

        # Normalize each vector to length 1.
        #
        # After normalization, inner product behaves like
        # cosine similarity.
        faiss.normalize_L2(vector_matrix)

        # IndexFlatIP performs exact maximum inner-product search.
        self.index = faiss.IndexFlatIP(
            self.embedding_dimension
        )

        self.index.add(vector_matrix)

        # Store copies so later searches can safely enrich results
        # without modifying the original input objects.
        self.embedded_chunks = [
            deepcopy(chunk)
            for chunk in embedded_chunks
        ]

    def search(
        self,
        query_embedding: Any,
        top_k: int,
    ) -> List[Dict]:
        """
        Retrieve nearest-neighbour chunks from the FAISS index.

        Search-time flow
        ----------------
        Query embedding
            ↓
        Convert to float32 matrix
            ↓
        Normalize query vector
            ↓
        FAISS search
            ↓
        Vector positions + similarity scores
            ↓
        Enriched heritage chunks
        """

        if self.index is None:
            raise RuntimeError(
                "Vector index has not been built. "
                "Call build_index() before search()."
            )

        if top_k <= 0:
            raise ValueError(
                "top_k must be greater than zero."
            )

        query_vector = np.asarray(
            query_embedding,
            dtype=np.float32,
        )

        # A single embedding normally has shape:
        #
        # (384,)
        #
        # FAISS expects:
        #
        # (number_of_queries, embedding_dimension)
        #
        # Therefore we reshape it to:
        #
        # (1, 384)
        if query_vector.ndim == 1:
            query_vector = query_vector.reshape(
                1,
                -1,
            )

        if query_vector.ndim != 2:
            raise ValueError(
                "Query embedding must be one vector."
            )

        if query_vector.shape[1] != self.embedding_dimension:
            raise ValueError(
                "Query embedding dimension does not match "
                "the vector index dimension."
            )

        faiss.normalize_L2(query_vector)

        # Never request more neighbours than the index contains.
        result_count = min(
            top_k,
            len(self.embedded_chunks),
        )

        similarity_scores, neighbour_indexes = (
            self.index.search(
                query_vector,
                result_count,
            )
        )

        results = []

        # FAISS returns two matrices because it supports searching
        # multiple queries at once.
        #
        # We submitted one query, so we use row zero.
        for similarity, chunk_index in zip(
            similarity_scores[0],
            neighbour_indexes[0],
        ):
            # FAISS may use -1 when no neighbour is available.
            if chunk_index < 0:
                continue

            result = deepcopy(
                self.embedded_chunks[chunk_index]
            )

            result["similarity"] = float(
                similarity
            )

            result["vector_index"] = int(
                chunk_index
            )

            results.append(result)

        return results