"""
Input guardrails.
  1. Refuse the banned topics (cats/dogs, horoscopes/zodiac, Taylor Swift).
  2. Refuse attempts to read or change the system prompt.
Completion: DONE
"""

import re

# Banned topics
_RESTRICTED = {
    "cats and dogs": r"\b(cat|cats|kitten|feline|dog|dogs|puppy|canine)\b",
    "horoscopes and zodiac signs": (
        r"\b(horoscope|zodiac|astrolog\w*|aries|taurus|gemini|leo|virgo|libra|"
        r"scorpio|sagittarius|capricorn|aquarius|pisces)\b"
    ),
    "Taylor Swift": r"\b(taylor\s+swift|swiftie)\b",
}

# System-prompt attacks
_PROMPT_ATTACK = re.compile(
    r"(system\s*prompt|initial\s+instructions|your\s+instructions|"
    r"ignore\s+(all\s+)?(previous|prior)|reveal\s+your\s+(prompt|instructions)|"
    r"what\s+(are|were)\s+you\s+told|repeat\s+your\s+(system\s+)?prompt|"
    r"(change|update|replace|forget)\s+your\s+(system\s+)?(prompt|instructions)|"
    r"you\s+are\s+now\b|new\s+instructions?)",
    re.IGNORECASE,
)

# Return the label of a banned topic if the text mentions one, else None
def restricted_topic(text: str):
    for label, pattern in _RESTRICTED.items():
        if re.search(pattern, text, re.IGNORECASE):
            return label
    return None

def prompt_attack(text: str) -> bool:
    return bool(_PROMPT_ATTACK.search(text))