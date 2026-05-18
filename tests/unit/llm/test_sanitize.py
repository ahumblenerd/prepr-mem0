from __future__ import annotations

from prepr_mem0.llm.sanitize import extract_json, normalize_facts, remove_code_blocks


def test_strips_markdown_fences_with_json_tag():
    raw = '```json\n{"facts": ["a"]}\n```'
    assert remove_code_blocks(raw) == '{"facts": ["a"]}'


def test_strips_markdown_fences_with_no_tag():
    raw = '```\n{"facts": ["a"]}\n```'
    assert remove_code_blocks(raw) == '{"facts": ["a"]}'


def test_returns_input_when_no_fences():
    raw = '{"facts": ["a"]}'
    assert remove_code_blocks(raw) == '{"facts": ["a"]}'


def test_strips_think_tags():
    raw = '<think>let me consider...</think>\n{"facts": ["a"]}'
    assert remove_code_blocks(raw).strip() == '{"facts": ["a"]}'


def test_strips_think_tags_inside_fences():
    raw = '```json\n<think>reasoning</think>\n{"facts": []}\n```'
    out = remove_code_blocks(raw)
    assert "<think>" not in out
    assert "{" in out


def test_normalize_facts_handles_bare_strings():
    assert normalize_facts(["foo", "bar"]) == ["foo", "bar"]


def test_normalize_facts_handles_fact_dicts():
    assert normalize_facts([{"fact": "foo"}, {"text": "bar"}]) == ["foo", "bar"]


def test_normalize_facts_drops_unknown_shapes():
    assert normalize_facts([{"unknown": "x"}, "ok"]) == ["ok"]


def test_normalize_facts_empty():
    assert normalize_facts([]) == []
    assert normalize_facts(None) == []


def test_extract_json_from_fenced():
    raw = '```json\n{"memory": []}\n```'
    assert extract_json(raw) == '{"memory": []}'


def test_extract_json_from_braces():
    raw = 'noise before {"memory": [{"id": "0"}]} noise after'
    assert extract_json(raw) == '{"memory": [{"id": "0"}]}'


def test_extract_json_passthrough_when_no_match():
    raw = "not json at all"
    assert extract_json(raw) == "not json at all"
