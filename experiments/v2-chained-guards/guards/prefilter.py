import re
from typing import Tuple

BLACKLIST_PATTERNS = [
    r"(?i)ignore previous instructions",
    r"(?i)delete all",
    r"(?i)sudo",
]


def prefilter_check(text: str) -> Tuple[bool, str]:
    """Return (is_malicious, reason). True means malicious detected."""
    for p in BLACKLIST_PATTERNS:
        if re.search(p, text):
            return True, f"blacklist-match: {p}"
    return False, "pass"
