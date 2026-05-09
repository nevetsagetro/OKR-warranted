"""Query-time filter extraction.

Parses a natural-language question to derive structured pre-filters
(country ISO codes, sender types, regulation types) that narrow the
retrieval search space before BM25 + vector scoring.

No provider is involved. This is a fast, heuristic-only operation.
"""

import re
from dataclasses import dataclass, field


@dataclass
class QueryFilters:
    """Structured filters extracted from a user question."""
    iso_codes: list[str] = field(default_factory=list)
    sender_types: list[str] = field(default_factory=list)
    regulation_types: list[str] = field(default_factory=list)

    @property
    def has_filters(self) -> bool:
        return bool(self.iso_codes or self.sender_types or self.regulation_types)


# Sender type keyword → tag value
_SENDER_TYPE_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"\balphanumeric\b|\balpha[\s-]?numeric\b|\bsender[\s-]?id\b", re.I), "alphanumeric"),
    (re.compile(r"\bshort[\s-]?code\b", re.I), "short_code"),
    (re.compile(r"\btoll[\s-]?free\b", re.I), "toll_free"),
    (re.compile(r"\blong[\s-]?code\b|\bvirtual[\s-]?number\b", re.I), "long_code"),
]

# Regulation type keyword → tag value
_REGULATION_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"\bregist(?:er|ration|ered)\b|\bpre[\s-]?regist", re.I), "registration"),
    (re.compile(r"\bopt[\s-]?out\b|\bunsubscribe\b|\bstop\b", re.I), "opt_out"),
    (re.compile(r"\bcontent\s+restriction\b|\bprohibited\b|\bforbidden\b|\bcannot\s+send\b", re.I), "content"),
    (re.compile(r"\bcomplian(?:ce|t)\b|\bdlt\b|\btemplate\b", re.I), "compliance"),
]


def extract_query_filters(
    question: str,
    country_index: dict[str, str],
) -> QueryFilters:
    """Extract pre-filter tags from a natural-language question.

    Args:
        question: The user's question.
        country_index: Mapping of lowercase country name / alias / ISO → uppercase ISO code.
                       Built at retriever load time from indexed block tags.
    Returns:
        QueryFilters with extracted tags. All lists are deduplicated.
    """
    lowered = question.lower()
    filters = QueryFilters()

    # ── Geo / country ──────────────────────────────────────────────────────────
    # 1. Bare ISO codes already present in the question (e.g. "ES", "US")
    for match in re.finditer(r"\b([A-Z]{2})\b", question):
        token = match.group(1)
        if _is_sender_id_phrase(question, match.start(), match.end()):
            continue
        if token.lower() in country_index:
            iso = country_index[token.lower()]
            if iso not in filters.iso_codes:
                filters.iso_codes.append(iso)
    if re.search(r"\bu\.?s\.?\b", question, flags=re.IGNORECASE) and "us" in country_index:
        iso = country_index["us"]
        if iso not in filters.iso_codes:
            filters.iso_codes.append(iso)

    # 2. Country names from the index (longest match first to handle "United States" before "States")
    sorted_keys = sorted(country_index.keys(), key=len, reverse=True)
    matched_spans: list[tuple[int, int]] = []

    for key in sorted_keys:
        if len(key) < 3:
            continue
        for match in re.finditer(r"\b" + re.escape(key) + r"\b", lowered):
            start, end = match.span()
            # Skip if overlapping with a longer already-matched span
            if any(s <= start < e or s < end <= e for s, e in matched_spans):
                continue
            iso = country_index[key]
            if iso and iso not in filters.iso_codes:
                filters.iso_codes.append(iso)
            matched_spans.append((start, end))

    # ── Sender type ────────────────────────────────────────────────────────────
    for pattern, tag in _SENDER_TYPE_PATTERNS:
        if pattern.search(question) and tag not in filters.sender_types:
            filters.sender_types.append(tag)

    # ── Regulation type ────────────────────────────────────────────────────────
    for pattern, tag in _REGULATION_PATTERNS:
        if pattern.search(question) and tag not in filters.regulation_types:
            filters.regulation_types.append(tag)

    return filters


def _is_sender_id_phrase(question: str, start: int, end: int) -> bool:
    """Avoid treating the "ID" in "sender ID" as Indonesia's ISO code."""
    if question[start:end] != "ID":
        return False
    before = question[max(0, start - 16):start].lower()
    after = question[end:end + 2].lower()
    return bool(re.search(r"\bsender[\s-]*$", before) or after == "s")
