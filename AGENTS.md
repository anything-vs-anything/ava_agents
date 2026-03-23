# Atlas Agents — how to run in Cursor

This repo encodes the **Agentic Guerrilla Seeding System** from `agentic_seeding_master_prompt_revised_final.pdf`. Use it to **research communities**, **qualify targets**, **draft native battle prompts**, **validate quality**, and **diagnose outcomes**—while keeping **humans** as the only posting authority.

## Sources

**Reddit** and **X** are the default surfaces for Scout through Smith: how to record anchors, platform mix, and compliance is documented in **`docs/sources.md`**. Scout outputs must tag each candidate with `source_platform` (`reddit` | `x`) per `data/schemas/scout_discoveries.schema.json`.

## Browser view of agents

Open **`web/index.html`** locally for a pipeline diagram and links to each prompt file. In **Cursor**, agents are used via **@** file references and **Rules**—there is no separate hosted “agents dashboard” for this project.

## Quick start (manual chain in Cursor)

1. Open **Composer** or **Chat** with this project as the workspace (so `.cursor/rules` apply).
2. Run the cycle helper to create/load state and see the current phase:
   - `python3 scripts/run_atlas_cycle.py status`
3. For each phase, attach the matching prompt file with `@` (e.g. `@agents/prompts/scout.md`) and paste any **inputs** the prompt asks for (or point the model at files under `data/`).
4. Save model outputs to the paths the prompt specifies (typically under `data/runs/<run_id>/`).

## Agent prompt files

| Phase | Prompt file | Primary artifacts |
|--------|----------------|-------------------|
| Atlas (orchestration) | `agents/prompts/atlas.md` | `data/state.json`, run folders |
| Scout | `agents/prompts/scout.md` | `scout_discoveries.json`, context packs |
| Judge | `agents/prompts/judge.md` | `judge_report.json` |
| Context Extractor | `agents/prompts/context-extractor.md` | `context_profiles/*.json` |
| Smith | `agents/prompts/smith.md` | `smith_prompts.json` |
| Quality Gate | `agents/prompts/quality-gate.md` | `quality_gate.json` |
| Human review | `agents/templates/human-review-packet.md` | filled packet Markdown |
| Sentinel | `agents/prompts/sentinel.md` | `sentinel_report.json` |

## “Automatic” operation in Cursor

Cursor does not ship a built-in cron for Composer. Practical automation:

1. **Project rules** — `.cursor/rules/atlas-seeding-system.mdc` is **always on** so every chat respects gates and ordering.
2. **Tasks** — `.vscode/tasks.json` defines one task per phase; run **Terminal → Run Task** and pick e.g. **Atlas: cycle status** or **Atlas: open Scout prompt**.
3. **Scheduled prep on macOS** — `scripts/com.atlas.cycle.plist.example` + `scripts/install_launchd.sh` install a daily job that runs `run_atlas_cycle.py tick` (bumps schedule, ensures folders). It **does not** call external APIs or post anywhere; it keeps the workspace ready for your Cursor session.

### Pipeline automation helper

Use `scripts/pipeline_automation.py` for local orchestration guardrails:

- `python3 scripts/pipeline_automation.py status` — run/phase + current artifact status
- `python3 scripts/pipeline_automation.py guide` — which prompt to attach and what file to produce
- `python3 scripts/pipeline_automation.py validate` — verify current phase output exists
- `python3 scripts/pipeline_automation.py advance` — move to next phase only when checks pass

`advance` blocks at `human_review` until you explicitly run:

- `python3 scripts/run_atlas_cycle.py human-ok`

This keeps human posting authority explicit and non-automated.

## Source document

Canonical spec: `agentic_seeding_master_prompt_revised_final.pdf` (also summarized in `docs/agentic_seeding_master_prompt.md`).
