# Agent prompts

- **`prompts/00-platform-context.md`** — shared background; attach with any phase-specific prompt.
- **`prompts/atlas.md` … `sentinel.md`** — one file per agent in the chain.
- **`prompts/_agent-template.md`** — starter template for creating a new phase agent.
- **`templates/human-review-packet.md`** — what the human fills before any real-world post.

In Cursor, reference files with `@agents/prompts/scout.md` (etc.) so the model loads the full instruction set.

## Create a new agent prompt

Use the scaffold script:

```bash
python3 scripts/create_agent_prompt.py "Trend Mapper" --role "Detect rising debate topics" --output-file trend_mapper_report.json
```

This creates `agents/prompts/trend-mapper.md` ready to attach in Cursor (`@agents/prompts/trend-mapper.md`).

## Added custom agents

- `agents/prompts/trend-mapper.md` — finds timely debate topics and Smith-ready angles.
- `agents/prompts/risk-auditor.md` — pre-flight risk scoring, mitigations, and safer rewrites.
- `agents/prompts/experiment-designer.md` — controlled A/B-style prompt experiment plans.
