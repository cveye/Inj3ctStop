from typing import Tuple
from sentence_transformers import SentenceTransformer
import numpy as np

# load MiniLM once
_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

POLICY_TEMPLATES = [
    "Answer the user's question concisely. Do not execute arbitrary code.",
    "Provide high-level guidance only; do not reveal private data.",
]
_POLICY_EMBS = _model.encode(_POLICY_TEMPLATES, convert_to_numpy=True)

def cosine_sim(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-12))

def embedding_check(text: str, threshold: float = 0.75) -> Tuple[bool, float]:
    """
    Return (is_malicious, max_sim).
    True if similarity to policy templates < threshold.
    """
    vec = _model.encode(text, convert_to_numpy=True)
    sims = [_model.similarity(vec, _model.encode(t, convert_to_numpy=True)) for t in POLICY_TEMPLATES]
    max_sim = max(sims)
    is_malicious = max_sim < threshold
    return is_malicious, float(max_sim)
