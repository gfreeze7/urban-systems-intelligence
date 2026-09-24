from ai.ai_briefing import build_evidence_context, build_prompt
from src.analytics.bi_reporting import (
    build_bi_dataset,
    validate_bi_dataset,
)


def test_ai_context_contains_evidence_and_limitations():
    context = build_evidence_context()

    assert "SUPPORTED" in context
    assert "COMPLICATED" in context
    assert "CONTRADICTED" in context
    assert "UNRESOLVED" in context
    assert "Limitation:" in context


def test_ai_prompt_contains_guardrails_and_question():
    question = "What does the evidence say about urban systems?"

    prompt = build_prompt(question)

    assert question in prompt
    assert "Do not invent evidence." in prompt
    assert "Do not claim causation" in prompt
    assert "ONLY the supplied Project 3 evidence" in prompt


def test_bi_dataset_has_expected_grain():
    dataset = build_bi_dataset()

    assert len(dataset) == 770
    assert not dataset.duplicated(["year", "csa2010"]).any()


def test_bi_dataset_passes_validation():
    dataset = build_bi_dataset()

    assert validate_bi_dataset(dataset) is True