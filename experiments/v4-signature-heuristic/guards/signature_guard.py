from __future__ import annotations
from typing import Dict, Any, List, Tuple
import json
import regex as re
from pathlib import Path

_SIGS: List[Dict[str, Any]] = []
_COMPILED = []

def _load_signatures() -> None:
    global _SIGS, _COMPILED
    if _SIGS:
        return
    sig_path = Path(__file__).resolve().parents[1] / "signatures.json"
    with open(sig_path, "r", encoding="utf-8") as f:
        _SIGS = json.load(f)
    _COMPILED = [(s, re.compile(s["pattern"])) for s in _SIGS]

def signature_guard(text: str) -> Tuple[float, Dict[str, Any]]:
    """
    Returns (risk_score in [0,1], details).
    risk_score is severity-weighted signal of how many signatures matched.
    """
    _load_signatures()
    matches = []
    total_sev = 0.0
    max_sev = 0.0

    for sig, cre in _COMPILED:
        hits = list(cre.finditer(text))
        if not hits:
            continue
        matches.append({
            "id": sig["id"],
            "category": sig.get("category", "other"),
            "count": len(hits),
            "severity": float(sig.get("severity", 0.5))
        })
        # Simple aggregation: severity * count, and remember max severity hit
        total_sev += float(sig.get("severity", 0.5)) * len(hits)
        max_sev = max(max_sev, float(sig.get("severity", 0.5)))

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