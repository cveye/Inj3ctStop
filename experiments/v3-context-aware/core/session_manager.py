from typing import List, Dict, Optional

class SessionManager:
    """
    Keeps a rolling window of recent conversation turns.
    Each turn = {"user": "...", "model": "..."}.
    """
    def __init__(self, window: int = 3):
        self.window = window
        self._history: List[Dict[str, str]] = []

    def add_turn(self, user_input: str, model_output: str) -> None:
        self._history.append({"user": user_input, "model": model_output})
        if len(self._history) > self.window:
            self._history = self._history[-self.window:]

    def reset(self) -> None:
        self._history.clear()

    def history(self) -> List[Dict[str, str]]:
        return list(self._history)

    def context_text(self) -> str:
        if not self._history:
            return ""
        parts = []
        for h in self._history:
            parts.append(f"User: {h['user']}")
            parts.append(f"Model: {h['model']}")
        return " \n".join(parts)