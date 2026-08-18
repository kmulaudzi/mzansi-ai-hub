"""
Mzansi AI Hub
Heritage Intelligence Engine

Semantic Retrieval Capability

Retrieval Engine
"""

import hashlib
import json

from pathlib import Path
from typing import Dict, List

from foundation.engines.chunking_engine import ChunkingEngine
from foundation.engines.embedding_engine import EmbeddingEngine
from foundation.engines.vector_database_engine import (
    VectorDatabaseEngine,
)

from ..providers.base_provider import BaseProvider
from ..settings import (
    CHUNK_METADATA_PATH,
    INDEX_MANIFEST_PATH,
    VECTOR_INDEX_PATH,
)
from .retrieval_policy_engine import (
    RetrievalPolicyEngine,
)


class RetrievalEngine:
    """
    Coordinates knowledge preparation and
    policy-controlled semantic retrieval.

    Startup flow
    ------------
    Knowledge sources
        ↓
    Dataset fingerprint
        ↓
    Persistent intelligence valid?
        │
        ├── Yes
        │     ↓
        │   Load FAISS index
        │   Load chunk metadata
        │
        └── No
              ↓
            Providers
              ↓
            Documents
              ↓
            Chunking Engine
              ↓
            Chunks
              ↓
            Embedding Engine
              ↓
            Embedded Chunks
              ↓
            Vector Database Engine
              ↓
            Save FAISS index
            Save chunk metadata
            Save manifest

    Search-time flow
    ----------------
    User Query
        ↓
    Embedding Engine
        ↓
    Query Embedding
        ↓
    Vector Database Engine
        ↓
    Candidate Chunks
        ↓
    Retrieval Policy Engine
        ↓
    Approved Chunks
    """

    def __init__(
        self,
        providers: List[BaseProvider],
        chunking_engine: ChunkingEngine,
        embedding_engine: EmbeddingEngine,
        vector_database_engine: VectorDatabaseEngine,
        retrieval_policy_engine: RetrievalPolicyEngine,
    ):
        """
        Connect all dependencies required for retrieval.

        The Retrieval Engine does not create these components.
        They are assembled by the capability bootstrap and
        injected here.
        """

        if not providers:
            raise ValueError(
                "RetrievalEngine requires at least one provider."
            )

        self.providers = providers

        self.chunking_engine = (
            chunking_engine
        )

        self.embedding_engine = (
            embedding_engine
        )

        self.vector_database_engine = (
            vector_database_engine
        )

        self.retrieval_policy_engine = (
            retrieval_policy_engine
        )

        self.is_prepared = False

    # ============================================================
    # Persistent Intelligence Helpers
    # ============================================================

    def _get_source_files(
        self,
    ) -> List[Path]:
        """
        Discover the physical source files used by
        the configured providers.

        Returns
        -------
        List[Path]
            Sorted list of source files.
        """

        source_files = []

        for provider in self.providers:

            source_path = getattr(
                provider,
                "source_path",
                None,
            )

            if source_path is None:
                continue

            source_path = Path(
                source_path
            )

            if not source_path.exists():
                continue

            if source_path.is_file():
                source_files.append(
                    source_path
                )

                continue

            for file_path in source_path.rglob(
                "*"
            ):
                if file_path.is_file():
                    source_files.append(
                        file_path
                    )

        return sorted(
            source_files,
            key=lambda path: str(path),
        )

    def _calculate_dataset_fingerprint(
        self,
    ) -> str:
        """
        Calculate a deterministic fingerprint of the
        configured heritage knowledge sources.

        The fingerprint includes:

        - file path
        - file size
        - modification timestamp

        Therefore adding, deleting, replacing, or modifying
        a source document changes the fingerprint and causes
        prepare() to rebuild the semantic intelligence.
        """

        hasher = hashlib.sha256()

        source_files = (
            self._get_source_files()
        )

        for file_path in source_files:

            file_stat = file_path.stat()

            fingerprint_value = (
                f"{file_path.resolve()}"
                f"|{file_stat.st_size}"
                f"|{file_stat.st_mtime_ns}"
            )

            hasher.update(
                fingerprint_value.encode(
                    "utf-8"
                )
            )

        return hasher.hexdigest()

    def _persistent_index_exists(
        self,
    ) -> bool:
        """
        Check whether all required persisted
        semantic intelligence files exist.
        """

        return (
            VECTOR_INDEX_PATH.exists()
            and CHUNK_METADATA_PATH.exists()
            and INDEX_MANIFEST_PATH.exists()
        )

    def _load_manifest(
        self,
    ) -> Dict:
        """
        Load the persisted semantic index manifest.
        """

        if not INDEX_MANIFEST_PATH.exists():
            return {}

        try:

            return json.loads(
                INDEX_MANIFEST_PATH.read_text(
                    encoding="utf-8"
                )
            )

        except (
            json.JSONDecodeError,
            OSError,
        ):
            return {}

    def _save_manifest(
        self,
        dataset_fingerprint: str,
        chunk_count: int,
    ) -> None:
        """
        Save metadata describing the persisted index.
        """

        INDEX_MANIFEST_PATH.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        manifest = {
            "dataset_fingerprint": (
                dataset_fingerprint
            ),
            "chunk_count": chunk_count,
        }

        INDEX_MANIFEST_PATH.write_text(
            json.dumps(
                manifest,
                indent=2,
            ),
            encoding="utf-8",
        )

    def _can_restore_persistent_index(
        self,
        dataset_fingerprint: str,
    ) -> bool:
        """
        Determine whether the stored vector intelligence
        still matches the current dataset.
        """

        if not self._persistent_index_exists():
            return False

        manifest = self._load_manifest()

        stored_fingerprint = manifest.get(
            "dataset_fingerprint"
        )

        return (
            stored_fingerprint
            == dataset_fingerprint
        )

    # ============================================================
    # Knowledge Preparation
    # ============================================================

    def prepare(
        self,
    ) -> int:
        """
        Prepare the heritage semantic intelligence.

        If the knowledge sources have not changed since the
        last successful preparation, restore the persisted
        FAISS index instead of recomputing embeddings.

        If the source knowledge has changed, rebuild and
        persist the semantic intelligence.

        Returns
        -------
        int
            Number of searchable chunks.
        """

        dataset_fingerprint = (
            self._calculate_dataset_fingerprint()
        )

        # --------------------------------------------------------
        # FAST PATH
        #
        # Restore existing intelligence when the source dataset
        # has not changed.
        # --------------------------------------------------------

        if self._can_restore_persistent_index(
            dataset_fingerprint
        ):

            try:

                chunk_count = (
                    self.vector_database_engine.load(
                        index_path=VECTOR_INDEX_PATH,
                        chunks_path=CHUNK_METADATA_PATH,
                    )
                )

                self.is_prepared = True

                print(
                    "Loaded persistent semantic intelligence "
                    f"with {chunk_count} searchable chunks."
                )

                return chunk_count

            except (
                FileNotFoundError,
                RuntimeError,
                OSError,
            ):

                # If persisted intelligence is corrupt or
                # incomplete, fall through to a clean rebuild.
                pass

        # --------------------------------------------------------
        # REBUILD PATH
        #
        # Dataset changed, or no valid persisted intelligence
        # exists.
        # --------------------------------------------------------

        documents = []

        for provider in self.providers:

            provider_documents = (
                provider.load_documents()
            )

            documents.extend(
                provider_documents
            )

        chunks = (
            self.chunking_engine.chunk_documents(
                documents=documents
            )
        )

        embedded_chunks = (
            self.embedding_engine.embed_chunks(
                chunks=chunks
            )
        )

        self.vector_database_engine.build_index(
            embedded_chunks=embedded_chunks
        )

        chunk_count = len(
            embedded_chunks
        )

        # --------------------------------------------------------
        # Persist the newly prepared intelligence.
        # --------------------------------------------------------

        self.vector_database_engine.save(
            index_path=VECTOR_INDEX_PATH,
            chunks_path=CHUNK_METADATA_PATH,
        )

        self._save_manifest(
            dataset_fingerprint=dataset_fingerprint,
            chunk_count=chunk_count,
        )

        self.is_prepared = True

        print(
            "Built and persisted semantic intelligence "
            f"with {chunk_count} searchable chunks."
        )

        return chunk_count

    # ============================================================
    # Semantic Retrieval
    # ============================================================

    def retrieve(
        self,
        query: str,
        top_k: int,
    ) -> List[Dict]:
        """
        Retrieve and approve heritage knowledge.

        Parameters
        ----------
        query:
            User's natural-language query.

        top_k:
            Number of nearest-neighbour candidates requested
            from the Vector Database Engine.

        Returns
        -------
        List[Dict]
            Candidate chunks that passed the retrieval policies.
        """

        if not self.is_prepared:
            raise RuntimeError(
                "RetrievalEngine is not prepared. "
                "Call prepare() before searching."
            )

        # --------------------------------------------------------
        # Create the query embedding.
        # --------------------------------------------------------

        query_embedding = (
            self.embedding_engine.embed_text(
                text=query
            )
        )

        # --------------------------------------------------------
        # Retrieve nearest semantic candidates.
        #
        # The Vector Database finds mathematically close
        # neighbours. It does not decide whether they are
        # trustworthy or relevant enough to continue.
        # --------------------------------------------------------

        candidate_chunks = (
            self.vector_database_engine.search(
                query_embedding=query_embedding,
                top_k=top_k,
            )
        )

        # --------------------------------------------------------
        # Apply retrieval policies.
        # --------------------------------------------------------

        approved_chunks = (
            self.retrieval_policy_engine.apply(
                candidate_chunks=candidate_chunks
            )
        )

        return approved_chunks