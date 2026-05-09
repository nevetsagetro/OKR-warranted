from __future__ import annotations

from own_knowledge_rag.models import KnowledgeBlock
from own_knowledge_rag.retrieval_ablation import _block_type_hit, _metadata_hit, _weighted_rrf


def _block(block_id: str, text: str = "hello") -> KnowledgeBlock:
    return KnowledgeBlock(
        block_id=block_id,
        document_id=block_id,
        title=block_id,
        section_path=[block_id],
        section_heading=block_id,
        block_type="table_fact",
        text=text,
        source_path=f"{block_id}.md",
        start_anchor="",
        end_anchor="",
        metadata={"row_key": "Dialing code"},
        iso_code="ES",
    )


def test_weighted_rrf_combines_lexical_and_vector_ranks() -> None:
    first = _block("first")
    second = _block("second")
    third = _block("third")

    hits = _weighted_rrf(
        lexical_hits=[(first, 10.0), (second, 5.0)],
        vector_hits=[(third, 0.9), (second, 0.8)],
        lexical_weight=1.0,
        vector_weight=1.0,
    )

    assert {hit.block.block_id for hit in hits} == {"first", "second", "third"}
    assert hits[0].block.block_id == "second"
    assert hits[0].lexical_score == 5.0
    assert hits[0].vector_score == 0.8


def test_block_type_and_metadata_hits_are_detected() -> None:
    hit = _weighted_rrf([(_block("spain"), 1.0)], [], lexical_weight=1.0, vector_weight=0.0)[0]

    assert _block_type_hit(["table"], [hit]) is True
    assert _metadata_hit({"row_key": "Dialing code"}, [hit]) is True
    assert _metadata_hit({"row_key": "MCC"}, [hit]) is False
