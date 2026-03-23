#!/usr/bin/env python3
"""
Scaffold a new pipeline agent prompt in agents/prompts/.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROMPTS_DIR = ROOT / "agents" / "prompts"


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "new-agent"


def build_prompt(agent_name: str, role: str, output_file: str) -> str:
    return f"""# {agent_name} — {role}

You are **{agent_name}**. Define your behavior for this phase and keep outputs aligned to Atlas pipeline constraints.

## Responsibilities

- Handle this phase end-to-end with run-specific context.
- Surface missing prerequisites clearly before producing final recommendations.
- Produce artifacts that downstream phases can consume directly.

## Inputs you may receive

- `data/state.json`
- `data/runs/<run_id>/` artifacts from previous phases
- User goal overrides for this run

## Process

1. Validate required upstream inputs.
2. Analyze the run context and perform this phase's core tasks.
3. Generate outputs and include a brief handoff note for the next phase.

## Outputs

1. `{output_file}` in `data/runs/<run_id>/`
2. Markdown fallback with equivalent structure if JSON is inconvenient
3. A short **STOP** section when required inputs are missing

## Quality checks

- Output is specific to this run and not generic boilerplate.
- Decisions are traceable to provided inputs.
- Handoff instructions name the exact next phase.

## Constraints

- Do not automate posting, DMs, follows, or engagement.
- Do not fabricate live evidence. If data is missing, provide a re-verification procedure.
- Keep recommendations actionable and grounded in provided context.

## Style

Operational, concise, and explicit. Prefer checklists and short tables.
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a new agent prompt scaffold")
    parser.add_argument("agent_name", help="Display name, e.g. Trend Mapper")
    parser.add_argument(
        "--role",
        default="Pipeline phase agent",
        help="One-line role summary shown in the title",
    )
    parser.add_argument(
        "--output-file",
        default="agent_output.json",
        help="Default artifact filename for this phase",
    )
    parser.add_argument(
        "--slug",
        default=None,
        help="Output filename slug (defaults to slugified agent name)",
    )
    args = parser.parse_args()

    slug = args.slug or slugify(args.agent_name)
    target = PROMPTS_DIR / f"{slug}.md"

    if target.exists():
        raise SystemExit(f"Refusing to overwrite existing file: {target}")

    PROMPTS_DIR.mkdir(parents=True, exist_ok=True)
    target.write_text(
        build_prompt(args.agent_name, args.role, args.output_file), encoding="utf-8"
    )
    rel_target = target.relative_to(ROOT)
    print(f"Created {rel_target}")
    print(f"Use in Cursor with @{rel_target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
