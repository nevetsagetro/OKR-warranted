from dataclasses import dataclass, field


@dataclass(slots=True)
class ParsedDocument:
    document_id: str
    title: str
    source_path: str
    content_type: str
    text: str
    country: str = ""
    iso_code: str = ""
    encoding_detected: str = "utf-8"
    encoding_confidence: float = 1.0
    encoding_fallback: bool = False
    parse_warnings: list[str] = field(default_factory=list)


@dataclass(slots=True)
class KnowledgeBlock:
    block_id: str
    document_id: str
    title: str
    section_path: list[str]
    section_heading: str
    block_type: str
    text: str
    source_path: str
    start_anchor: str
    end_anchor: str
    block_index: int = 0
    char_offset: int = 0
    country: str = ""
    iso_code: str = ""
    reasoning: str = ""
    sender_types: list[str] = field(default_factory=list)
    channels: list[str] = field(default_factory=list)
    regulation_topics: list[str] = field(default_factory=list)
    answer_signal: str = ""
    summary: str = ""
    canonical_terms: list[str] = field(default_factory=list)
    hypothetical_questions: list[str] = field(default_factory=list)
    enriched_text: str = ""
    enrichment_provider: str = ""
    enrichment_model: str = ""
    enriched_at: str = ""
    local_aliases: list[str] = field(default_factory=list)
    quality_status: str = "ok"
    metadata: dict[str, str] = field(default_factory=dict)


@dataclass(slots=True)
class SearchHit:
    block: KnowledgeBlock
    score: float
    lexical_score: float = 0.0
    vector_score: float = 0.0


@dataclass(slots=True)
class Answer:
    question: str
    answer: str
    confidence: str
    evidence: list[SearchHit]
    tier: str = "refusal"
    query_intent: str = "lookup"
    cached: bool = False


@dataclass(slots=True)
class EvaluationCase:
    question: str
    expected_document_ids: list[str] = field(default_factory=list)
    expected_source_paths: list[str] = field(default_factory=list)
    expected_terms: list[str] = field(default_factory=list)
    expected_section_terms: list[str] = field(default_factory=list)
    expected_anchor_terms: list[str] = field(default_factory=list)
    expected_block_types: list[str] = field(default_factory=list)
    expected_sender_types: list[str] = field(default_factory=list)
    expected_metadata: dict[str, str] = field(default_factory=dict)
    expected_iso_code: str = ""
    forbid_document_ids: list[str] = field(default_factory=list)
    must_not_mix_documents: bool = False
    question_type: str = "factoid"
    should_refuse: bool = False


@dataclass(slots=True)
class EvaluationCaseResult:
    question: str
    expected_document_ids: list[str]
    expected_source_paths: list[str]
    expected_terms: list[str]
    expected_section_terms: list[str]
    expected_block_types: list[str]
    expected_sender_types: list[str]
    expected_metadata: dict[str, str]
    expected_iso_code: str
    question_type: str
    should_refuse: bool
    retrieved_document_ids: list[str]
    retrieved_sections: list[str]
    refusal_correct: bool
    retrieval_hit: bool
    evidence_hit: bool
    citation_hit: bool
    section_hit: bool
    answer_correct: bool
    document_precision_at_k: float
    answer_confidence: str
    block_type_hit: bool = False
    metadata_hit: bool = False
    country_match_at_1: bool = False
    foreign_evidence_present: bool = False
    forbidden_document_present: bool = False
    mixed_document_violation: bool = False
    routed_tier: str = "refusal"
    query_intent: str = "lookup"
    answer_cached: bool = False
    answer_text: str = ""
    failure_stage: str | None = None
    failure_reasons: list[str] = field(default_factory=list)


@dataclass(slots=True)
class EvaluationSummary:
    total_cases: int
    retrieval_recall_at_k: float
    evidence_hit_rate: float
    citation_accuracy: float
    document_precision_at_k: float
    no_answer_precision: float
    answer_correctness: float
    country_match_at_1: float = 0.0
    foreign_evidence_rate: float = 0.0
    wrong_country_answer_rate: float = 0.0
    diversity_enforcement_rate: float = 0.0
    answer_cache_hit_rate: float = 0.0
    cached_answer_count: int = 0
    tier_distribution: dict[str, int] = field(default_factory=dict)
    segment_breakdown: dict[str, dict[str, int | float]] = field(default_factory=dict)
    failure_analysis: dict[str, dict[str, int]] = field(default_factory=dict)
    fix_recommendations: dict[str, list[str]] = field(default_factory=dict)
    results: list[EvaluationCaseResult] = field(default_factory=list)


@dataclass(slots=True)
class CalibrationCandidate:
    min_score_threshold: float
    min_overlap_ratio: float
    tier0_score_threshold: float
    tier2_score_threshold: float
    no_answer_precision: float
    answer_correctness: float
    evidence_hit_rate: float
    retrieval_recall_at_k: float
    tier0_1_share: float
    tier2_share: float = 0.0
    refusal_share: float = 0.0


@dataclass(slots=True)
class CalibrationReport:
    recommended_min_score_threshold: float
    recommended_min_overlap_ratio: float
    recommended_tier0_score_threshold: float
    recommended_tier2_score_threshold: float
    total_cases: int = 0
    answerable_cases: int = 0
    refusal_cases: int = 0
    candidate_count: int = 0
    recommended_no_answer_precision: float = 0.0
    recommended_answer_correctness: float = 0.0
    recommended_evidence_hit_rate: float = 0.0
    recommended_retrieval_recall_at_k: float = 0.0
    recommended_tier0_1_share: float = 0.0
    recommended_tier2_share: float = 0.0
    recommended_refusal_share: float = 0.0
    meets_query_mix_target: bool = False
    candidates: list[CalibrationCandidate] = field(default_factory=list)
