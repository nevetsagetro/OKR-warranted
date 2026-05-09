from collections import Counter, defaultdict
from math import log

from own_knowledge_rag.models import KnowledgeBlock
from own_knowledge_rag.text import tokenize


class BM25Index:
    def __init__(self, blocks: list[KnowledgeBlock]) -> None:
        self._blocks = blocks
        self._doc_freqs: dict[str, int] = defaultdict(int)
        self._term_freqs: list[Counter[str]] = []
        self._doc_lengths: list[int] = []
        # block_id → list-index for O(1) candidate filtering
        self._id_to_index: dict[str, int] = {}

        for idx, block in enumerate(blocks):
            counts = Counter(tokenize(self._lexical_text(block)))
            self._term_freqs.append(counts)
            self._doc_lengths.append(sum(counts.values()))
            for term in counts:
                self._doc_freqs[term] += 1
            self._id_to_index[block.block_id] = idx

        self._avg_doc_len = sum(self._doc_lengths) / max(1, len(self._doc_lengths))

    def search(
        self,
        query: str,
        top_k: int = 20,
        candidate_ids: set[str] | None = None,
    ) -> list[tuple[KnowledgeBlock, float]]:
        """Search the index.

        Args:
            query: The question to score blocks against.
            top_k: Maximum number of results to return.
            candidate_ids: When provided, only score blocks whose block_id is
                           in this set.  This is the primary mechanism for
                           pre-filtering by semantic tags.
        """
        query_terms = tokenize(query)
        scored: list[tuple[KnowledgeBlock, float]] = []

        if candidate_ids is not None:
            # Fast path: score only the pre-filtered subset
            indices = [
                self._id_to_index[bid]
                for bid in candidate_ids
                if bid in self._id_to_index
            ]
        else:
            indices = range(len(self._blocks))  # type: ignore[assignment]

        for index in indices:
            score = self._score_block(index, query_terms)
            if score > 0:
                scored.append((self._blocks[index], score))

        scored.sort(key=lambda item: item[1], reverse=True)
        return scored[:top_k]

    def _score_block(self, index: int, query_terms: list[str], k1: float = 1.5, b: float = 0.75) -> float:
        counts = self._term_freqs[index]
        doc_len = self._doc_lengths[index]
        score = 0.0
        total_docs = max(1, len(self._blocks))

        for term in query_terms:
            freq = counts.get(term, 0)
            if freq == 0:
                continue
            doc_freq = self._doc_freqs.get(term, 0)
            idf = log(1 + (total_docs - doc_freq + 0.5) / (doc_freq + 0.5))
            denom = freq + k1 * (1 - b + b * (doc_len / max(1.0, self._avg_doc_len)))
            score += idf * ((freq * (k1 + 1)) / denom)
        return score

    @staticmethod
    def _lexical_text(block: KnowledgeBlock) -> str:
        section = " > ".join(block.section_path)
        row_key = block.metadata.get("row_key", "")
        row_values = block.metadata.get("row_values", "")
        structured_value = block.metadata.get("structured_value", "")
        clean_value = structured_value or BM25Index._row_value_for_lexical(row_values)
        document_kind = block.metadata.get("document_kind", "")
        
        # English-Only enriched fields for high-precision lexical matching
        questions = " ".join(block.hypothetical_questions)
        aliases = " ".join(block.local_aliases)
        enriched = block.enriched_text or ""
        canonical_terms = " ".join(block.canonical_terms)
        
        return (
            f"{block.document_id} {block.title} {section} "
            f"{row_key} {clean_value} {document_kind} "
            f"{row_values} "
            f"{enriched} {questions} {canonical_terms} {aliases} {block.text}"
        )

    @staticmethod
    def _row_value_for_lexical(row_values: str) -> str:
        for part in [item.strip() for item in row_values.split(";") if item.strip()]:
            if "=" not in part:
                continue
            label, value = [item.strip() for item in part.split("=", 1)]
            if label.lower() == "value" and value.lower() not in {"", "n/a", "---", "-----", "/", "unknown", "null"}:
                return value
        return ""
