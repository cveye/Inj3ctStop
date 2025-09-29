from typing import Tuple
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# load distilgpt2 once at import
_tokenizer = AutoTokenizer.from_pretrained("distilgpt2")
_model = AutoModelForCausalLM.from_pretrained("distilgpt2")

SUSPICIOUS_KEYWORDS = ["ignore previous", "password", "secret", "delete all"]


def llm_self_check(text: str) -> Tuple[bool, str]:
    """
    Returns (is_malicious, explanation).
    Uses distilgpt2 perplexity + keyword checks.
    """
    lowered = text.lower()
    for kw in SUSPICIOUS_KEYWORDS:
        if kw in lowered:
            return True, f"keyword:{kw}"

    # compute perplexity
    inputs = _tokenizer(text, return_tensors="pt")
    with torch.no_grad():
        loss = _model(**inputs, labels=inputs["input_ids"]).loss
    ppl = torch.exp(loss).item()

    # threshold is tunable —> higher perplexity = more suspicious
    if ppl > 80 and len(inputs["input_ids"][0]) < 10:
        return True, f"high-perplexity:{ppl:.1f}"
    return False, f"ok:{ppl:.1f}"
