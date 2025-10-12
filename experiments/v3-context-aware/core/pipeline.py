import time
from typing import Dict, Any, Optional
from core.session_manager import SessionManager
from guards.context_guard import context_guard

DEFAULT_LAYERS = ["context_guard"]  # v3 focuses on context; you can add more later

class ContextAwarePipeline:
    def __init__(self, session: Optional[SessionManager] = None, layers=None):
        self.session = session
        self.layers = layers or DEFAULT_LAYERS

    def run(self, prompt: str) -> Dict[str, Any]:
        results = {"prompt": prompt, "start_ts": time.time(), "layers": [], "final": {}, "context": {}}

        history_text = self.session.context_text() if self.session else ""
        results["context"]["history_text"] = history_text

        if "context_guard" in self.layers:
            mal, reason, sim = context_guard(prompt, history_text)
            results["layers"].append({
                "layer": "context_guard",
                "malicious": bool(mal),
                "reason": reason,
                "similarity": float(sim),
            })
            if mal:
                return self._final(results, "flagged", reason)

        # Simulate "model answer"
        response = f"[LLM] safe answer to: {prompt}"

        # Update session AFTER decision (only if we have a session)
        if self.session:
            self.session.add_turn(prompt, response)

        return self._final(results, "delivered", response)

    def _final(self, results: Dict[str, Any], status: str, payload: str):
        results["final"] = {"status": status}
        if status == "delivered":
            results["final"]["response"] = payload
        else:
            results["final"]["reason"] = payload
        results["latency_ms"] = int((time.time() - results["start_ts"]) * 1000)
        return results