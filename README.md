# Atlas Agents — guerrilla seeding workspace

Marketing research and **prompt preparation** for introducing a **battle comparison** ritual into communities that already debate—while keeping **humans** as the only posting authority.

## Start here

1. Read **`AGENTS.md`** for how to run agents in Cursor. Discovery defaults to **Reddit** and **X** — see **`docs/sources.md`**.
2. Project rules live in **`.cursor/rules/atlas-seeding-system.mdc`** (constraints + pipeline).
3. Per-agent instructions: **`agents/prompts/`** (attach with `@` in Composer).
4. Canonical spec: **`agentic_seeding_master_prompt_revised_final.pdf`**

## Commands

```bash
python3 scripts/run_atlas_cycle.py new-run   # create data/runs/<id>/ and state
python3 scripts/run_atlas_cycle.py status  # show phase + paths
python3 scripts/run_atlas_cycle.py set-phase scout
python3 scripts/run_atlas_cycle.py human-ok  # after human review packet
```

## Cursor tasks

**Terminal → Run Task** → `Atlas: new run`, `Atlas: cycle status`, etc. (see `.vscode/tasks.json`).

## Scheduled reminder (macOS)

`scripts/install_launchd.sh` installs a daily **`tick`** (updates timestamps only; no network). Edit the plist to change the time.

## Agent map (browser)

Open **`web/index.html`** in your browser for a simple pipeline view and links to each agent Markdown file. Cursor does not list custom agents in its own web UI; this page is local to the repo.
