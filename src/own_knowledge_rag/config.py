from pathlib import Path

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CANONICAL_TERMS_VERSION = "telecom-v1.0"

CANONICAL_TERM_GROUPS = {
    "sender_identity": [
        "alphanumeric sender id",
        "dynamic sender id",
        "generic sender id",
        "numeric sender id",
        "registered sender id",
        "shared sender id",
        "sender id preservation",
        "sender id replacement",
        "sender registration",
        "whitelisted sender id",
    ],
    "numbering": [
        "short code",
        "dedicated short code",
        "shared short code",
        "long code",
        "toll-free number",
        "virtual mobile number",
        "local number",
        "national number",
        "international number",
        "dialing code",
        "mcc",
        "mnc",
        "number portability",
    ],
    "messaging_capabilities": [
        "sms",
        "two-way sms",
        "one-way sms",
        "mms",
        "rcs",
        "concatenated sms",
        "message concatenation",
        "unicode sms",
        "flash sms",
        "delivery receipt",
        "inbound messaging",
        "outbound messaging",
    ],
    "registration_and_compliance": [
        "pre-registration",
        "brand registration",
        "campaign registration",
        "kyc",
        "letter of authorization",
        "business verification",
        "regulatory approval",
        "operator approval",
        "government approval",
        "use case approval",
        "traffic vetting",
        "content template approval",
    ],
    "policy_and_consent": [
        "opt-in",
        "opt-out",
        "consent requirement",
        "unsubscribe requirement",
        "stop keyword",
        "help keyword",
        "quiet hours",
        "do not disturb",
        "content restriction",
        "prohibited content",
        "marketing restriction",
        "transactional traffic",
        "promotional traffic",
        "political traffic",
        "financial traffic",
        "gambling content",
        "adult content",
        "phishing prevention",
    ],
    "operations": [
        "provisioning time",
        "throughput",
        "rate limit",
        "message encoding",
        "sms encoding",
        "validity period",
        "delivery window",
        "routing",
        "direct connection",
        "grey route",
        "operator filtering",
        "traffic suspension",
        "service availability",
    ],
}

CANONICAL_TERMS = sorted({term for terms in CANONICAL_TERM_GROUPS.values() for term in terms})

class Settings(BaseSettings):
    source_dir: Path = Field(default=Path("data/raw"), alias="OKR_SOURCE_DIR")
    work_dir: Path = Field(default=Path("data/work"), alias="OKR_WORK_DIR")
    mapping_provider: str = Field(default="local", alias="OKR_MAPPING_PROVIDER")
    mapping_model: str = Field(default="heuristic-v1", alias="OKR_MAPPING_MODEL")
    mapping_batch_size: int = Field(default=16, alias="OKR_MAPPING_BATCH_SIZE")
    mapping_batch_delay_ms: int = Field(default=0, alias="OKR_MAPPING_BATCH_DELAY_MS")
    mapping_text_char_limit: int = Field(default=600, alias="OKR_MAPPING_TEXT_CHAR_LIMIT")
    mapping_prompt_mode: str = Field(default="full", alias="OKR_MAPPING_PROMPT_MODE")
    mapping_retry_missing_results: bool = Field(default=True, alias="OKR_MAPPING_RETRY_MISSING_RESULTS")
    embedding_provider: str = Field(default="local", alias="OKR_EMBEDDING_PROVIDER")
    embedding_model: str = Field(
        default="BAAI/bge-small-en-v1.5",
        alias="OKR_EMBEDDING_MODEL",
    )
    embedding_device: str = Field(default="cpu", alias="OKR_EMBEDDING_DEVICE")
    embedding_dimensions: int | None = Field(default=None, alias="OKR_EMBEDDING_DIMENSIONS")
    vector_backend: str = Field(default="local", alias="OKR_VECTOR_BACKEND")
    vector_collection: str = Field(default="own-knowledge-rag", alias="OKR_VECTOR_COLLECTION")
    qdrant_url: str = Field(default="http://localhost:6333", alias="OKR_QDRANT_URL")
    qdrant_api_key: str | None = Field(default=None, alias="OKR_QDRANT_API_KEY")
    reranker_provider: str = Field(default="none", alias="OKR_RERANKER_PROVIDER")
    reranker_model: str = Field(
        default="cross-encoder/ms-marco-MiniLM-L-6-v2",
        alias="OKR_RERANKER_MODEL",
    )
    reranker_top_n: int = Field(default=10, alias="OKR_RERANKER_TOP_N")
    rrf_lexical_weight: float = Field(default=1.0, alias="OKR_RRF_LEXICAL_WEIGHT")
    rrf_vector_weight: float = Field(default=1.0, alias="OKR_RRF_VECTOR_WEIGHT")
    arm_k_multiplier: int = Field(default=3, alias="OKR_ARM_K_MULTIPLIER")
    max_blocks_per_document: int = Field(default=2, alias="OKR_MAX_BLOCKS_PER_DOCUMENT")
    generation_provider: str = Field(default="none", alias="OKR_GENERATION_PROVIDER")
    generation_model: str = Field(default="gpt-4o-mini", alias="OKR_GENERATION_MODEL")
    generation_model_allowlist: list[str] = Field(
        default_factory=lambda: ["gpt-4o-mini", "gpt-4o", "gpt-4.1-mini", "gpt-4.1"],
        alias="OKR_GENERATION_MODEL_ALLOWLIST",
    )
    provider_model_probe_enabled: bool = Field(default=False, alias="OKR_PROVIDER_MODEL_PROBE_ENABLED")
    generation_max_evidence: int = Field(default=5, alias="OKR_GENERATION_MAX_EVIDENCE")
    query_cache_enabled: bool = Field(default=True, alias="OKR_QUERY_CACHE_ENABLED")
    top_k: int = Field(default=5, ge=0, le=10, alias="OKR_TOP_K")
    min_answer_score: float = Field(default=0.18, alias="OKR_MIN_ANSWER_SCORE")
    min_answer_overlap_ratio: float = Field(default=0.2, alias="OKR_MIN_ANSWER_OVERLAP_RATIO")
    tier0_score_threshold: float = Field(default=0.75, alias="OKR_TIER0_SCORE_THRESHOLD")
    tier2_score_threshold: float = Field(default=0.55, alias="OKR_TIER2_SCORE_THRESHOLD")
    chunk_size: int = Field(default=800, alias="OKR_CHUNK_SIZE")
    chunk_overlap: int = Field(default=120, alias="OKR_CHUNK_OVERLAP")
    max_file_bytes: int = Field(default=10 * 1024 * 1024, alias="OKR_MAX_FILE_BYTES")
    api_host: str = Field(default="127.0.0.1", alias="OKR_API_HOST")
    api_port: int = Field(default=8000, alias="OKR_API_PORT")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True,
    )

    @model_validator(mode="after")
    def validate_thresholds_and_models(self) -> "Settings":
        self.source_dir = self._resolve_project_path(self.source_dir)
        self.work_dir = self._resolve_project_path(self.work_dir)
        if not self.tier0_score_threshold > self.tier2_score_threshold > self.min_answer_score:
            raise ValueError(
                "Answer thresholds must satisfy "
                "OKR_TIER0_SCORE_THRESHOLD > OKR_TIER2_SCORE_THRESHOLD > OKR_MIN_ANSWER_SCORE."
            )
        if self.generation_provider == "openai" and self.generation_model not in self.generation_model_allowlist:
            allowed = ", ".join(self.generation_model_allowlist)
            raise ValueError(
                f"Generation model '{self.generation_model}' is not in "
                f"OKR_GENERATION_MODEL_ALLOWLIST: {allowed}."
            )
        return self

    @staticmethod
    def _resolve_project_path(path: Path) -> Path:
        return path if path.is_absolute() else PROJECT_ROOT / path

    @property
    def hf_model(self) -> str:
        return self.embedding_model

    @property
    def hf_device(self) -> str:
        return self.embedding_device
