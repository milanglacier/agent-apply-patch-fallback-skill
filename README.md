# Apply Patch Fallback

A fallback file editing tool for agent without native file editing capabilities.

## Purpose

This skill exists primarily for use with **Codex CLI** when using a **non-GPT
model**. Codex's native `apply_patch` tool only works with GPT models (see
[openai/codex#16397](https://github.com/openai/codex/issues/16397)).

When using Codex with other models (e.g., Kimi, GLM etc.), this fallback
provides file editing capabilities through a Python script that applies patches
in a standardized format.

## When to Use This Tool

- Using Codex CLI with a non-GPT model (Claude, Gemini, etc.)

## Quick Start

The `apply_patch` script must be available in your PATH or current directory:

```bash
cp scripts/apply_patch /usr/local/bin/
chmod +x /usr/local/bin/apply_patch
```

Or use it directly:

```bash
./scripts/apply_patch patch.txt
```

## Documentation

- Full documentation: See `SKILL.md`
- Technical reference: See `references/README.md`
- Test examples: See `test/` directory
