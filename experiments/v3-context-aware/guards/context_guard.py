from typing import Tuple
import numpy as np
from sentence_transformers import SentenceTransformer
import re

_embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

OVERRIDE_PATTERNS = [
    r"(?i)\bignore previous\b",
    r"(?i)\bforget (?:earlier|previous)\b",
    r"(?i)\boverride (?:rules|instructions)\b",
    r"(?i)\breset (?:context|rules)\b",
]

def _cos(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-12))

def _extract_last_user(history_text: str) -> str:
    """
    History comes in lines like:
      User: ...
      Model: ...
    We want ONLY the last 'User: ...' segment to avoid diluting similarity
    with the synthetic model response.
    """
    last = ""
    for line in history_text.splitlines():
        if line.startswith("User:"):
            last = line[len("User:"):].strip()
    return last

def context_guard(new_prompt: str, history_text: str,
                  sim_threshold: float = 0.15) -> Tuple[bool, str, float]:
    """
    Returns (is_malicious, reason, similarity_to_last_user)

    Heuristics:
      - If explicit override keywords present -> malicious.
      - Else compare ONLY to the last user prompt (not the whole history).
      - Do not flag short follow-up questions purely on low similarity.
    """
    if not history_text.strip():
        return False, "no_context", 1.0
    
    lowered = new_prompt.lower()
    for pat in OVERRIDE_PATTERNS:
        if re.search(pat, lowered):
            return True, "explicit_override", 0.0


    last_user = _extract_last_user(history_text)
    if not last_user:
        return False, "no_user_turn", 1.0

    new_emb = _embedder.encode(new_prompt, convert_to_numpy=True)
    last_emb = _embedder.encode(last_user, convert_to_numpy=True)
    sim = _cos(new_emb, last_emb)

    # If it's a short follow-up question, don't flag based only on similarity.
    is_question = new_prompt.strip().endswith("?")
    token_count = len(new_prompt.split())
    if is_question and token_count <= 7:
        return False, f"followup_ok:{sim:.2f}", sim

    if sim < sim_threshold:
        return True, f"context_shift:{sim:.2f}", sim

    return False, f"ok:{sim:.2f}", sim