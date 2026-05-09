from dataclasses import dataclass


@dataclass(slots=True)
class QueryIntent:
    primary: str
    is_binary: bool
    is_count: bool
    is_duration: bool
    is_procedural: bool
    is_comparative: bool
    is_aggregate: bool
    is_file_reference: bool
    expects_refusal: bool


def analyze_query(question: str) -> QueryIntent:
    lowered = question.strip().lower()
    is_binary = lowered.startswith(("is ", "are ", "does ", "do ", "can ", "should ", "must "))
    is_count = "how many" in lowered or "count" in lowered or "number of" in lowered
    is_duration = "how long" in lowered or "how many weeks" in lowered or "how many days" in lowered
    is_procedural = any(
        phrase in lowered
        for phrase in ["how do i", "how to", "steps", "procedure", "process", "what should i do"]
    )
    is_comparative = any(
        phrase in lowered
        for phrase in ["compare", "difference", "versus", "vs ", "better than", "same as"]
    )
    is_aggregate = any(
        phrase in lowered
        for phrase in [
            "all countries",
            "all locales",
            "all markets",
            "countries requiring",
            "countries that",
            "countries with",
            "list countries",
            "list locales",
            "list markets",
            "markets that",
            "markets with",
            "what countries",
            "what locales",
            "which countries",
            "which locales",
            "which markets",
            "where are",
            "where is",
        ]
    )
    is_file_reference = ".json" in lowered or ".md" in lowered or "file" in lowered
    expects_refusal = any(
        phrase in lowered
        for phrase in ["in this corpus", "in this knowledge base", "do we have", "is there any"]
    )

    primary = "lookup"
    if is_procedural:
        primary = "procedural"
    elif is_comparative:
        primary = "comparative"
    elif is_aggregate:
        primary = "aggregate"
    elif is_count:
        primary = "count"
    elif is_duration:
        primary = "duration"
    elif is_binary:
        primary = "binary"

    return QueryIntent(
        primary=primary,
        is_binary=is_binary,
        is_count=is_count,
        is_duration=is_duration,
        is_procedural=is_procedural,
        is_comparative=is_comparative,
        is_aggregate=is_aggregate,
        is_file_reference=is_file_reference,
        expects_refusal=expects_refusal,
    )
