# backend/vector_store.py

import json
from pathlib import Path
from typing import List, Dict, Optional

import numpy as np
from openai import OpenAI

from backend.config import OPENAI_API_KEY, OPENAI_EMBEDDING_MODEL

client = OpenAI(api_key=OPENAI_API_KEY)

CORPUS_PATH = Path("data/processed/cpf_corpus.jsonl")

# Simple global cache (loaded once per process)
_EMBEDDINGS_MATRIX: Optional[np.ndarray] = None
_RECORDS: List[Dict] = []


def _load_corpus():
    global _EMBEDDINGS_MATRIX, _RECORDS

    if _EMBEDDINGS_MATRIX is not None:
        return

    if not CORPUS_PATH.exists():
        raise RuntimeError(
            f"Corpus file not found at {CORPUS_PATH}. "
            "Run backend.build_corpus first."
        )

    records: List[Dict] = []
    embeddings = []

    with CORPUS_PATH.open("r", encoding="utf-8") as f:
        for line in f:
            rec = json.loads(line)
            records.append(rec)
            embeddings.append(rec["embedding"])

    _RECORDS = records
    _EMBEDDINGS_MATRIX = np.array(embeddings, dtype="float32")


def _ensure_corpus_loaded():
    if _EMBEDDINGS_MATRIX is None:
        _load_corpus()


def embed_query(text: str) -> np.ndarray:
    resp = client.embeddings.create(
        model=OPENAI_EMBEDDING_MODEL,
        input=[text],
    )
    return np.array(resp.data[0].embedding, dtype="float32")


def retrieve(
    query: str,
    k: int = 5,
    topic_filter: Optional[str] = None,
) -> List[Dict]:
    """
    Retrieve top-k relevant chunks for the given query.
    Optionally filter by topic (e.g. 'retirement_sums', 'withdrawals').
    """
    _ensure_corpus_loaded()

    assert _EMBEDDINGS_MATRIX is not None

    query_vec = embed_query(query)

    # Cosine similarity
    emb_matrix = _EMBEDDINGS_MATRIX
    dot = emb_matrix @ query_vec
    norms = np.linalg.norm(emb_matrix, axis=1) * np.linalg.norm(query_vec)
    sims = dot / (norms + 1e-8)

    # Sort indices by similarity
    idxs = np.argsort(-sims)  # descending

    results: List[Dict] = []

    for idx in idxs:
        rec = _RECORDS[idx]
        if topic_filter and rec.get("topic") != topic_filter:
            continue
        results.append(rec)
        if len(results) >= k:
            break

    return results
