from typing import Tuple
from sentence_transformers import SentenceTransformer
import numpy as np

# load MiniLM once
_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

POLICY_TEMPLATES = [
    "Answer the user's question concisely. Do not execute arbitrary code.",
    "Provide high-level guidance only; do not reveal private data.",
    "Provide factual responses to general knowledge questions.",
    "Do not reveal private data.",
    "what is your name or what is the capital of a country",
]
_POLICY_EMBS = _model.encode(POLICY_TEMPLATES, convert_to_numpy=True)

def cosine_sim(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-12))

def embedding_check(text: str, threshold: float = 0.4) -> Tuple[bool, float]:
    """
    Return (is_malicious, max_sim).
    True if similarity to policy templates < threshold.
    I cannot provide enough templates for the sake of demo, hence lowering threshold.
    """
    vec = _model.encode(text, convert_to_numpy=True)
    sims = [cosine_sim(vec, emb) for emb in _POLICY_EMBS]
    max_sim = max(sims)
    is_malicious = max_sim < threshold
    return bool(is_malicious), float(max_sim)
