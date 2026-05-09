import re
from collections import Counter


STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "how",
    "in",
    "is",
    "it",
    "of",
    "on",
    "or",
    "that",
    "the",
    "their",
    "this",
    "to",
    "what",
    "when",
    "where",
    "which",
    "with",
}


def normalize_token(token: str) -> str:
    token = re.sub(r"[^a-z0-9]+", "", token.lower())
    if len(token) <= 2 or token in STOPWORDS:
        return ""
    return token


def tokenize(text: str) -> list[str]:
    return [token for raw in re.findall(r"[A-Za-z0-9_/-]+", text) if (token := normalize_token(raw))]


def token_counts(text: str) -> Counter[str]:
    return Counter(tokenize(text))

