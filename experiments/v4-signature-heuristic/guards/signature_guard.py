from __future__ import annotations
from typing import Dict, Any, List, Tuple
import json
import regex as re
from pathlib import Path

_SIGS: List[Dict[str, Any]] = []
_COMPILED = []

# The LEET table is fun
_LEET_TABLE = str.maketrans({
    "0": "o", "1": "i", "3": "e", "4": "a", "5": "s", "7": "t", "8": "b", "9": "g",
    "@": "a", "$": "s"
})

def _load_signatures() -> None:
    global _SIGS, _COMPILED
    if _SIGS:
        return
    
    here = Path(__file__).resolve()
    candidates = [
        here.parent.parent / "signatures.json",                  # .../v4-signature-heuristic/signatures.json
        here.parent.parent.parent / "signatures.json",           # fallback if run deeper
    ]

    sig_path = next((p for p in candidates if p.exists()), None)
    if sig_path is None:
        raise FileNotFoundError(
            f"Could not find signatures.json in expected locations: {candidates}"
        )

    with open(sig_path, "r", encoding="utf-8") as f:
        _SIGS = json.load(f)
    _COMPILED = [(s, re.compile(s["pattern"])) for s in _SIGS]

def _normalize_leet(s: str) -> str:
    s2 = s.lower().translate(_LEET_TABLE)
    # replace non-word with space, collapse spaces
    s2 = re.sub(r"[^\p{L}\p{N}\s]+", " ", s2)
    s2 = re.sub(r"\s+", " ", s2).strip()
    return s2

def signature_guard(text: str) -> Tuple[float, Dict[str, Any]]:
    """
    Returns (risk_score in [0,1], details).
    risk_score is severity-weighted signal of how many signatures matched.
    Also checking for Leets to make it leet resilient
    """
    _load_signatures()
    texts = [text, _normalize_leet(text)]
    
    matches = []
    total_sev = 0.0
    max_sev = 0.0

    for candidate in texts:
        for sig, cre in _COMPILED:
            hits = list(cre.finditer(candidate))
            if not hits:
                continue
            sev = float(sig.get("severity", 0.5))
            matches.append({
                "id": sig["id"],
                "category": sig.get("category", "other"),
                "count": len(hits),
                "severity": sev,
                "normalized": (candidate is not text)  # mark if matched in normalized
            })
            total_sev += sev * len(hits)
            max_sev = max(max_sev, sev)

    # Normalize: squash via 1 - exp(-x) to keep bounded in [0,1)
    # and add a small boost for the strongest single hit.
    import math
    base = 1.0 - math.exp(-total_sev)
    risk = min(1.0, base * 0.7 + max_sev * 0.3)

    details = {
        "matches": matches,
        "total_severity": float(total_sev),
        "strongest": float(max_sev)
    }
    return float(risk), details