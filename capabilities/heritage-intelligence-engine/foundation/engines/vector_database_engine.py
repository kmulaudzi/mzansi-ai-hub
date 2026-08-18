"""
Mzansi AI Hub
Heritage Intelligence Engine

Foundation

Vector Database Engine

FAISS implementation behind the platform's
Vector Database architectural contract.
"""

import json

from copy import deepcopy
from pathlib import Path
from typing import Any, Dict, List

import faiss
import numpy as np


class VectorDatabaseEngine:
    """
    Build, search, save, and load a FAISS vector index.

    Architectural contract
    ----------------------
    build_index(embedded_chunks)
        Build searchable vector intelligence.

    search(query_embedding, top_k)
        Retrieve nearest semantic neighbours.

    save(index_path, chunks_path)
        Persist prepared vector intelligence.

    load(index_path, chunks_path)
        Restore previously prepared intelligence.

    FAISS remains an implementation detail behind this engine.
    """

    def __init__(self):
        self.index = None

        self.embedded_chunks: List[Dict] = []

        self.embedding_dimension = None

    def build_index(
        self,
        embedded_chunks: List[Dict],
    ) -> None:
        """
        Build a searchable FAISS index.
        """

        if not embedded_chunks:
            raise ValueError(
                "VectorDatabaseEngine requires at least "
                "one embedded chunk."
            )

        vectors = []

        for chunk in embedded_chunks:
            embedding = chunk.get(
                "embedding"
            )

            if embedding is None:
                raise ValueError(
                    "Every chunk must contain an embedding."
                )

            vectors.append(
                embedding
            )

        vector_matrix = np.asarray(
            vectors,
            dtype=np.float32,
        )

        if vector_matrix.ndim != 2:
            raise ValueError(
                "Embeddings must form a "
                "two-dimensional matrix."
            )

        self.embedding_dimension = (
            vector_matrix.shape[1]
        )

        faiss.normalize_L2(
            vector_matrix
        )

        self.index = faiss.IndexFlatIP(
            self.embedding_dimension
        )

        self.index.add(
            vector_matrix
        )

        # -----------------------------------------------------
        # Keep searchable chunk metadata in memory.
        #
        # The embedding itself is no longer required after
        # it has been inserted into FAISS, so we deliberately
        # remove it from the stored metadata.
        # -----------------------------------------------------

        self.embedded_chunks = []

        for chunk in embedded_chunks:

            stored_chunk = deepcopy(
                chunk
            )

            stored_chunk.pop(
                "embedding",
                None,
            )

            self.embedded_chunks.append(
                stored_chunk
            )

    def search(
        self,
        query_embedding: Any,
        top_k: int,
    ) -> List[Dict]:
        """
        Retrieve nearest semantic neighbours.
        """

        if self.index is None:
            raise RuntimeError(
                "Vector index has not been built or loaded."
            )

        if top_k <= 0:
            raise ValueError(
                "top_k must be greater than zero."
            )

        query_vector = np.asarray(
            query_embedding,
            dtype=np.float32,
        )

        if query_vector.ndim == 1:
            query_vector = (
                query_vector.reshape(
                    1,
                    -1,
                )
            )

        if query_vector.ndim != 2:
            raise ValueError(
                "Query embedding must be one vector."
            )

        if (
            query_vector.shape[1]
            != self.embedding_dimension
        ):
            raise ValueError(
                "Query embedding dimension does not "
                "match vector index dimension."
            )

        faiss.normalize_L2(
            query_vector
        )

        result_count = min(
            top_k,
            len(self.embedded_chunks),
        )

        (
            similarity_scores,
            neighbour_indexes,
        ) = self.index.search(
            query_vector,
            result_count,
        )

        results = []

        for similarity, chunk_index in zip(
            similarity_scores[0],
            neighbour_indexes[0],
        ):
            if chunk_index < 0:
                continue

            result = deepcopy(
                self.embedded_chunks[
                    chunk_index
                ]
            )

            result["similarity"] = float(
                similarity
            )

            result["vector_index"] = int(
                chunk_index
            )

            results.append(
                result
            )

        return results

    def save(
        self,
        index_path: Path,
        chunks_path: Path,
    ) -> None:
        """
        Persist the FAISS index and associated chunk metadata.
        """

        if self.index is None:
            raise RuntimeError(
                "Cannot save an empty vector index."
            )

        index_path = Path(
            index_path
        )

        chunks_path = Path(
            chunks_path
        )

        index_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        chunks_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        faiss.write_index(
            self.index,
            str(index_path),
        )

        chunks_path.write_text(
            json.dumps(
                self.embedded_chunks,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

    def load(
        self,
        index_path: Path,
        chunks_path: Path,
    ) -> int:
        """
        Restore a persisted FAISS index and chunk metadata.

        Returns
        -------
        int
            Number of searchable chunks restored.
        """

        index_path = Path(
            index_path
        )

        chunks_path = Path(
            chunks_path
        )

        if not index_path.exists():
            raise FileNotFoundError(
                f"FAISS index not found: {index_path}"
            )

        if not chunks_path.exists():
            raise FileNotFoundError(
                f"Chunk metadata not found: {chunks_path}"
            )

        self.index = faiss.read_index(
            str(index_path)
        )

        self.embedded_chunks = json.loads(
            chunks_path.read_text(
                encoding="utf-8"
            )
        )

        self.embedding_dimension = (
            self.index.d
        )

        if (
            self.index.ntotal
            != len(self.embedded_chunks)
        ):
            raise RuntimeError(
                "Persisted FAISS index and chunk metadata "
                "contain different numbers of records."
            )

        return len(
            self.embedded_chunks
        )