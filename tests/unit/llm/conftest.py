"""Shared fixtures for LLM unit tests."""

from __future__ import annotations

import pytest

from prepr_mem0.llm.openrouter import reset_client_for_tests


@pytest.fixture(autouse=True)
def openrouter_env(monkeypatch):
    """Set a dummy API key + reset the SDK singleton so respx intercepts."""
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-key")
    reset_client_for_tests()
    yield
    reset_client_for_tests()
