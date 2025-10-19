from __future__ import annotations
from typing import Dict, Any, Tuple
import math
import numpy as np

# Optional perplexity via distilgpt2
try:
    import torch
    from transformers import AutoTokenizer, AutoModelForCausalLM
    _tok = AutoTokenizer.from_pretrained("distilgpt2")
    _mdl = AutoModelForCausalLM.from_pretrained("distilgpt2")
    _HAS_PPL = True
except Exception:
    _HAS_PPL = False
    _tok = None
    _mdl = None

def _char_entropy(text: str) -> float:
    if not text:
        return 0.0
    # Character-level Shannon entropy
    import collections
    counts = collections.Counter(text)
    probs = np.array([c/len(text) for c in counts.values()], dtype=float)
    H = float(-np.sum(probs * np.log2(probs + 1e-12)))
    # Normalize by max entropy for len alphabet approx (cap 6 bits ~ typical ASCII subset)
    return float(min(1.0, H / 6.0))

def _ppl_score(text: str) -> float:
    """
    Returns normalized perplexity score in [0,1].
    If model unavailable, returns 0.0 (neutral).
    """
    if not _HAS_PPL or not text.strip():
        return 0.0
    with torch.no_grad():
        inputs = _tok(text, return_tensors="pt")
        loss = _mdl(**inputs, labels=inputs["input_ids"]).loss  # per-token NLL
        ppl = torch.exp(loss).item()
    # Map perplexity to 0..1 using a soft curve; clamp at 1000
    ppl_c = min(1000.0, max(0.0, ppl))
    # Convert to 0..1 (log scale), tuneable
    return float(math.log1p(ppl_c) / math.log1p(1000.0))

def _length_score(text: str) -> float:
    # very long prompts can carry injection blobs
    n = len(text)
    # smooth step around 200 chars; cap near 600+
    if n <= 50:
        return 0.0
    if n >= 600:
        return 1.0
    return float((n - 50) / (600 - 50))

def heuristic_guard(text: str, weights: Dict[str, float] | None = None) -> Tuple[float, Dict[str, Any]]:
    """
    Combines multiple behavioral signals into a risk score in [0,1].
    scores:
      - entropy_score: unusual character distribution
      - ppl_score: model finds text odd/unpredictable
      - length_score: longer inputs are riskier (blobs)
    """
    w = {"entropy": 0.30, "ppl": 0.40, "length": 0.30}
    if weights:
        w.update(weights)

    ent = _char_entropy(text)
    ppl = _ppl_score(text)
    ln  = _length_score(text)

    risk = w["entropy"] * ent + w["ppl"] * ppl + w["length"] * ln
    details = {
        "entropy_score": float(ent),
        "ppl_score": float(ppl),
        "length_score": float(ln),
        "weights": {k: float(v) for k, v in w.items()}
    }
    return float(min(1.0, max(0.0, risk))), details