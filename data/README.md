# Data directory

- **`state.json`** — current pipeline phase and run id (`scripts/run_atlas_cycle.py` updates this).
- **`runs/<run_id>/`** — per-cycle artifacts (`scout_discoveries.*`, `judge_report.*`, etc.).
- **`memory/`** — long-lived notes Atlas merges across runs (optional JSON or Markdown you maintain).
- **`schemas/`** — JSON Schema helpers for structured outputs.

Nothing here should contain secrets (passwords, tokens). Keep community URLs at a level you are comfortable storing locally.
