# backend/build_corpus.py

import json
import os
from pathlib import Path
from typing import List, Dict

import numpy as np
from openai import OpenAI

from backend.config import OPENAI_API_KEY, OPENAI_EMBEDDING_MODEL

client = OpenAI(api_key=OPENAI_API_KEY)

RAW_DIR = Path("data/raw")
OUT_PATH = Path("data/processed/cpf_corpus.jsonl")


def load_raw_documents() -> List[Dict]:
    docs: List[Dict] = []

    for path in RAW_DIR.glob("*.md"):
        with path.open("r", encoding="utf-8") as f:
            text = f.read()

        # Very simple header parsing
        title = "Untitled"
        topic = "general"
        source = ""

        lines = text.splitlines()
        body_lines = []

        for line in lines:
            if line.startswith("# Title:"):
                title = line.replace("# Title:", "").strip()
            elif line.startswith("# Topic:"):
                topic = line.replace("# Topic:", "").strip()
            elif line.startswith("# Source:"):
                source = line.replace("# Source:", "").strip()
            else:
                body_lines.append(line)

        body = "\n".join(body_lines).strip()

        docs.append(
            {
                "id": path.stem,
                "title": title,
                "topic": topic,
                "source": source,
                "text": body,
            }
        )

    return docs


def chunk_text(text: str, max_chars: int = 800) -> List[str]:
    """
    Simple character-based chunking with paragraph awareness.
    """
    paragraphs = text.split("\n\n")
    chunks: List[str] = []
    current = ""

    for para in paragraphs:
        if len(current) + len(para) + 2 <= max_chars:
            current += ("\n\n" if current else "") + para
        else:
            if current:
                chunks.append(current.strip())
            current = para

    if current:
        chunks.append(current.strip())

    return chunks


def embed_texts(texts: List[str]) -> List[List[float]]:
    resp = client.embeddings.create(
        model=OPENAI_EMBEDDING_MODEL,
        input=texts,
    )
    return [item.embedding for item in resp.data]


def build_corpus():
    os.makedirs(OUT_PATH.parent, exist_ok=True)

    docs = load_raw_documents()
    print(f"Loaded {len(docs)} raw documents.")

    all_records = []

    for doc in docs:
        chunks = chunk_text(doc["text"], max_chars=800)

        # Embed in batches if needed; here we do all chunks for this doc
        embeddings = embed_texts(chunks)

        for i, (chunk, emb) in enumerate(zip(chunks, embeddings)):
            record = {
                "doc_id": doc["id"],
                "chunk_id": f"{doc['id']}_chunk_{i}",
                "title": doc["title"],
                "topic": doc["topic"],
                "source": doc["source"],
                "text": chunk,
                "embedding": emb,
            }
            all_records.append(record)

    # Write JSONL
    with OUT_PATH.open("w", encoding="utf-8") as f:
        for rec in all_records:
            f.write(json.dumps(rec) + "\n")

    print(f"Wrote {len(all_records)} chunks to {OUT_PATH}")


if __name__ == "__main__":
    build_corpus()
