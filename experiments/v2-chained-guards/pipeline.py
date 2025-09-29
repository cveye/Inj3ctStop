import time
from typing import Dict, Any
from guards.prefilter import prefilter_check
from guards.embedding_check import embedding_check
from guards.llm_self_check import llm_self_check
from guards.sandbox_postprocess import sandbox_postprocess

DEFAULT_LAYERS = [
    "prefilter",
    "embedding_check",
    "llm_self_check",
    "sandbox_postprocess",
]

class ChainedGuardsPipeline:
    def __init__(self, layers=None):
        self.layers = layers or DEFAULT_LAYERS

    def run(self, prompt: str) -> Dict[str, Any]:
        results = {"prompt": prompt, "start_ts": time.time(), "layers": [], "final": {}}

        if "prefilter" in self.layers:
            mal, reason = prefilter_check(prompt)
            results["layers"].append({"layer": "prefilter", "malicious": mal, "reason": reason})
            if mal:
                return self._final(results, "blocked", reason)

        if "embedding_check" in self.layers:
            mal, sim = embedding_check(prompt)
            results["layers"].append({"layer": "embedding_check", "malicious": mal, "sim": sim})
            if mal:
                return self._final(results, "flagged", f"low_sim:{sim:.3f}")

        if "llm_self_check" in self.layers:
            mal, explanation = llm_self_check(prompt)
            results["layers"].append({"layer": "llm_self_check", "malicious": mal, "explanation": explanation})
            if mal:
                return self._final(results, "flagged", explanation)

        raw_response = f"[LLM] safe answer to: {prompt}"

        if "sandbox_postprocess" in self.layers:
            processed, redactions = sandbox_postprocess(raw_response)
            results["layers"].append({"layer": "sandbox_postprocess", "redactions": redactions})
            return self._final(results, "delivered", processed)

        return self._final(results, "delivered", raw_response)

    def _final(self, results: Dict[str, Any], status: str, payload: str):
        results["final"] = {"status": status}
        if status == "delivered":
            results["final"]["response"] = payload
        else:
            results["final"]["reason"] = payload
        results["latency_ms"] = int((time.time() - results["start_ts"]) * 1000)
        return results