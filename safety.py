import re
from dataclasses import dataclass

@dataclass
class ScreenResult:
    blocked: bool
    model: str

SELF_HARM_TERMS = [r"\bkill myself\b", r"\bsuicide\b", r"\bself[- ]?harm\b", r"\bending it all\b"]
DANGEROUS_TERMS = [r"\bbomb\b", r"\bmake a weapon\b", r"\bpoison\b"]

def screen_text(text: str) -> ScreenResult:
    t = text.lower()
    for pat in DANGEROUS_TERMS:
        if re.search(pat, t):
            return ScreenResult(True, "regex-danger")
    return ScreenResult(False, "regex-ok")

def is_crisis(text: str):
    t = text.lower()
    for pat in SELF_HARM_TERMS:
        if re.search(pat, t):
            return True, "self-harm"
    return False, "none"
