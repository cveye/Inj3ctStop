from . import logger

DISALLOWED_KEYWORDS = {"bypass", "exploit", "bomb", "hack", "illicit", "password", "credentials", "attack"}

def response_verifier(resp_text):
    lowered = resp_text.lower()
    for kw in DISALLOWED_KEYWORDS:
        if kw in lowered:
            logger.error("Response flagged due to keyword: %s", kw)  # 🚨 red in terminal
            return False, f"disallowed_keyword:{kw}"
    return True, "ok"