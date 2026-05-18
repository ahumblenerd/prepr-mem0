"""LLM layer: OpenRouter client + Mem0 prompts + parsing.

Two public entry points wrap the two LLM calls in `Memory.add()`:

- `extract_facts(messages, agent_id=None)` -> list[str]
- `decide_actions(facts, neighbors_per_fact)` -> list[DecidedAction]

Everything underneath runs through httpx so respx can intercept it in tests.
"""
