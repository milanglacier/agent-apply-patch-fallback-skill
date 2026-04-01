# Apply Patch Fallback

A fallback file editing tool for agent without native file editing capabilities.

## Purpose

This skill exists primarily for use with **Codex CLI** when using a **non-GPT
model**. Codex's native `apply_patch` tool only works with GPT models (see
[openai/codex#16397](https://github.com/openai/codex/issues/16397)).

When using Codex with other models (e.g., Kimi, GLM etc.), this fallback
provides file editing capabilities through a Python script that applies patches
in a standardized format.

## Documentation

- Full documentation: See `SKILL.md`
- Test examples: See `test/` directory
