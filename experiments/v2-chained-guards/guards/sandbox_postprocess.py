import re
from typing import Tuple, List, Dict

# Keywords we consider sensitive; add more as needed.
SENSITIVE_KEYWORDS = [
    "password",
    "passwd",
    "secret",
    "api_key",
    "api-key",
    "apikey",
    "token",
    "access_token",
    "ssn",
    "social security number",
]

# Patterns to capture "keyword : value", "keyword = value", 'keyword "value"', "keyword is value"
# We capture the keyword (group 1) and the value (group 2).
_PATTERNS = [
    # password: value  OR password = value
    r'(?i)\b(' + r'|'.join(map(re.escape, SENSITIVE_KEYWORDS)) + r')\b\s*[:=]\s*["\']?([^\s"\'<>`]+)["\']?',
    # my password is value  OR the token is "value"
    r'(?i)\b(?:my|the)?\s*(' + r'|'.join(map(re.escape, SENSITIVE_KEYWORDS)) + r')\b\s*(?:is|was)\s*["\']?([^\s"\'<>`]+)["\']?',
    # JSON-like "password": "value"  (handles quotes and spaces)
    r'(?i)["\'](' + r'|'.join(map(re.escape, SENSITIVE_KEYWORDS)) + r')["\']\s*:\s*["\']([^"\']+)["\']',
    # key=value as a single token (already covered above, but keep as fallback)
    r'(?i)\b(' + r'|'.join(map(re.escape, SENSITIVE_KEYWORDS)) + r')=([^\s"\'<>`]+)',
]

# compile for performance
_COMPILED = [re.compile(p) for p in _PATTERNS]


def _replace_match_with_redaction(text: str, match: re.Match) -> Tuple[str, Dict]:
    """
    Replace the captured sensitive value with [REDACTED] while preserving the surrounding text.
    Returns (new_text_fragment, metadata) where metadata contains keyword and original value.
    """
    keyword = match.group(1)
    value = match.group(2)
    # Build replacement: keep the keyword and a marker, redact the value
    # We'll replace only the value portion in the match span to preserve punctuation/format.
    start, end = match.span(0)
    full_match = text[start:end]

    # Replace the value occurrence inside the matched substring.
    # Use a small heuristic to find the value inside the matched substring (safe because group 2 exists)
    # Create a redacted fragment that mirrors original spacing/punctuation.
    redacted_fragment = full_match.replace(value, "[REDACTED]")

    metadata = {"keyword": keyword.lower(), "original_value": value}
    return redacted_fragment, metadata


def sandbox_postprocess(response: str) -> Tuple[str, List[Dict[str, str]]]:
    """
    Redact sensitive values from the response.

    Returns:
        - redacted_response (str): response with sensitive values replaced by [REDACTED]
        - redactions (list of dict): each dict contains 'keyword' and 'original_value' that was redacted
    """
    text = response
    redactions: List[Dict[str, str]] = []

    # Iterate patterns and progressively replace matches.
    # We use a loop to allow multiple different sensitive tokens in the string.
    for pattern in _COMPILED:
        # For each match in the current text, replace and record metadata.
        # Use finditer on the current text (we will rebuild text as we replace)
        offset = 0
        new_text_parts = []
        last_end = 0
        for m in pattern.finditer(text):
            # m.span() gives indices in current text
            start, end = m.span()
            # append text between last_end and start
            new_text_parts.append(text[last_end:start])
            redacted_fragment, metadata = _replace_match_with_redaction(text, m)
            new_text_parts.append(redacted_fragment)
            redactions.append(metadata)
            last_end = end
        new_text_parts.append(text[last_end:])
        text = "".join(new_text_parts)

    # Extra safety: redact long-looking base64-like or high-entropy tokens (optional heuristic)
    # e.g., strings of length >= 20 with mix of letters/digits/+/
    def _entropy_redact(s: str) -> Tuple[str, List[Dict[str, str]]]:
        extra_redacts = []
        def repl(m):
            token = m.group(0)
            extra_redacts.append({"keyword": "high_entropy_token", "original_value": token})
            return "[REDACTED]"
        # crude regex for long tokens (20+ chars) of letters/digits/+/=/_/-
        pattern = re.compile(r'\b[A-Za-z0-9_\-+/=]{20,}\b')
        new_s, n = pattern.subn(repl, s)
        return new_s, extra_redacts

    text, extra = _entropy_redact(text)
    redactions.extend(extra)

    return text, redactions