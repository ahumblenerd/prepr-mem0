"""Deterministic embedding stub.

The chaos-test demo needs reproducible vectors without depending on a real
embedding provider. SHA-256 of the text seeds an RNG that produces a unit
vector of dimension `EMBED_DIM`. Same text → same vector → cosine self-similarity
of 1.0. Swap for a real embedder (OpenRouter, OpenAI, etc.) by changing
`embed_text` only — call sites and DB schema stay identical.
"""

from __future__ import annotations

import hashlib
import math
import random

EMBED_DIM = 1536


def embed_text(text: str) -> list[float]:
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    seed = int(digest[:16], 16)
    rng = random.Random(seed)  # noqa: S311  # nosec B311 — reproducibility is the point
    raw = [rng.gauss(0.0, 1.0) for _ in range(EMBED_DIM)]
    norm = math.sqrt(sum(x * x for x in raw))
    return [x / norm for x in raw]
