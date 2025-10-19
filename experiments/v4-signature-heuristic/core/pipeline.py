from __future__ import annotations
import time
from typing import Dict, Any, Optional, List
from guards.signature_guard import signature_guard
from guards.heuristic_guard import heuristic_guard

DEFAULT_LAYERS: List[str] = ["signature_guard", "heuristic_guard"]
DEFAULT_WEIGHTS = {"signature": 0.6, "heuristic": 0.4}
DEFAULT_BLOCK_THRESHOLD = 0.6  # final risk over this -> flagged

class SignatureHeuristicPipeline:
    def __init__(self,
                 layers: Optional[List[str]] = None,
                 weights: Optional[Dict[str, float]] = None,
                 block_threshold: float = DEFAULT_BLOCK_THRESHOLD):
        self.layers = layers or DEFAULT_LAYERS
        self.weights = weights or DEFAULT_WEIGHTS
        self.block_threshold = float(block_threshold)

    def run(self, prompt: str) -> Dict[str, Any]:
        start = time.time()
        res: Dict[str, Any] = {
            "prompt": prompt,
            "layers": [],
            "final": {},
        }

        sig_score = 0.0
        heu_score = 0.0

        if "signature_guard" in self.layers:
            s, details = signature_guard(prompt)
            res["layers"].append({
                "layer": "signature_guard",
                "risk": float(s),
                "details": details
            })
            sig_score = float(s)

        if "heuristic_guard" in self.layers:
            h, details = heuristic_guard(prompt)
            res["layers"].append({
                "layer": "heuristic_guard",
                "risk": float(h),
                "details": details
            })
            heu_score = float(h)

        final_risk = self.weights["signature"] * sig_score + self.weights["heuristic"] * heu_score
        res["risk"] = float(final_risk)

        status = "flagged" if final_risk >= self.block_threshold else "delivered"
        res["final"] = {
            "status": status,
            "reason": "high_risk" if status == "flagged" else "ok",
        }
        res["latency_ms"] = int((time.time() - start) * 1000)
        return res