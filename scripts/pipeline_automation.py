#!/usr/bin/env python3
"""
Local automation helper for Atlas phase orchestration.
Prepares and validates pipeline state; never posts to platforms.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "data" / "state.json"
RUNS_PATH = ROOT / "data" / "runs"

PHASE_ORDER = [
    "atlas_plan",
    "scout",
    "judge",
    "context_extractor",
    "smith",
    "quality_gate",
    "human_review",
    "sentinel",
    "atlas_learn",
]

PHASE_META = {
    "atlas_plan": {"prompt": "agents/prompts/atlas.md", "artifact": "atlas_notes.md"},
    "scout": {"prompt": "agents/prompts/scout.md", "artifact": "scout_discoveries.json"},
    "judge": {"prompt": "agents/prompts/judge.md", "artifact": "judge_report.json"},
    "context_extractor": {
        "prompt": "agents/prompts/context-extractor.md",
        "artifact": "context_profiles/",
    },
    "smith": {"prompt": "agents/prompts/smith.md", "artifact": "smith_prompts.json"},
    "quality_gate": {
        "prompt": "agents/prompts/quality-gate.md",
        "artifact": "quality_gate.json",
    },
    "human_review": {
        "prompt": "agents/templates/human-review-packet.md",
        "artifact": "human_review_packet.md",
    },
    "sentinel": {"prompt": "agents/prompts/sentinel.md", "artifact": "sentinel_report.json"},
    "atlas_learn": {"prompt": "agents/prompts/atlas.md", "artifact": "atlas_notes.md"},
}


def load_state() -> dict:
    if not STATE_PATH.exists():
        return {}
    return json.loads(STATE_PATH.read_text(encoding="utf-8"))


def save_state(state: dict) -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    state["last_tick"] = datetime.now(timezone.utc).isoformat()
    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")


def run_dir(state: dict) -> Path | None:
    rid = state.get("run_id")
    if not rid:
        return None
    return RUNS_PATH / rid


def current_phase(state: dict) -> str:
    phase = state.get("phase")
    if phase in PHASE_ORDER:
        return phase
    return "idle"


def next_phase(phase: str) -> str:
    if phase not in PHASE_ORDER:
        return "atlas_plan"
    idx = PHASE_ORDER.index(phase)
    if idx + 1 >= len(PHASE_ORDER):
        return "atlas_plan"
    return PHASE_ORDER[idx + 1]


def artifact_exists(rundir: Path, phase: str) -> bool:
    artifact = PHASE_META[phase]["artifact"]
    target = rundir / artifact
    if artifact.endswith("/"):
        return target.exists() and any(target.iterdir())
    return target.exists()


def cmd_status(_args: argparse.Namespace) -> int:
    state = load_state()
    if not state:
        print("No state found. Run: python3 scripts/run_atlas_cycle.py new-run")
        return 0
    phase = current_phase(state)
    print(f"Run: {state.get('run_id')}")
    print(f"Phase: {phase}")
    print(f"Human cleared: {state.get('human_cleared', False)}")
    if phase in PHASE_ORDER:
        print(f"Next phase: {next_phase(phase)}")
    rd = run_dir(state)
    if rd:
        print(f"Run directory: {rd}")
    if rd and phase in PHASE_ORDER:
        ok = artifact_exists(rd, phase)
        status = "present" if ok else "missing"
        print(f"Current phase artifact ({PHASE_META[phase]['artifact']}): {status}")
    return 0


def cmd_guide(_args: argparse.Namespace) -> int:
    state = load_state()
    if not state.get("run_id"):
        print("No active run. Run: python3 scripts/run_atlas_cycle.py new-run")
        return 1
    phase = current_phase(state)
    if phase == "idle":
        print("State is idle. Set phase to atlas_plan or run new-run.")
        return 1
    meta = PHASE_META[phase]
    print(f"Current phase: {phase}")
    print(f"Attach prompt in Cursor: @{meta['prompt']}")
    print(f"Expected artifact: data/runs/<run_id>/{meta['artifact']}")
    print("Tip: use `python3 scripts/pipeline_automation.py validate` before advancing.")
    return 0


def cmd_validate(_args: argparse.Namespace) -> int:
    state = load_state()
    rd = run_dir(state)
    phase = current_phase(state)
    if not rd or phase == "idle":
        print("No active run/phase. Run new-run and set a phase first.", file=sys.stderr)
        return 1
    ok = artifact_exists(rd, phase)
    if not ok:
        print(f"Missing artifact for {phase}: {PHASE_META[phase]['artifact']}", file=sys.stderr)
        return 1
    if phase == "human_review" and not state.get("human_cleared", False):
        print("Human gate not cleared. Run: python3 scripts/run_atlas_cycle.py human-ok")
        return 1
    print(f"Validation passed for phase {phase}.")
    return 0


def cmd_advance(args: argparse.Namespace) -> int:
    state = load_state()
    rd = run_dir(state)
    phase = current_phase(state)
    if not rd or phase == "idle":
        print("No active run/phase. Run new-run first.", file=sys.stderr)
        return 1
    if not args.force and not artifact_exists(rd, phase):
        print(
            f"Cannot advance: missing artifact {PHASE_META[phase]['artifact']} for {phase}.",
            file=sys.stderr,
        )
        return 1
    if phase == "human_review" and not state.get("human_cleared", False):
        print("Cannot advance from human_review until human-ok is set.", file=sys.stderr)
        return 1
    nxt = next_phase(phase)
    state["phase"] = nxt
    save_state(state)
    print(f"Advanced from {phase} -> {nxt}")
    print(f"Next prompt: @{PHASE_META[nxt]['prompt']}")
    print(f"Expected artifact: data/runs/<run_id>/{PHASE_META[nxt]['artifact']}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Atlas local pipeline automation helper")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("status", help="Show run, phase, and artifact status").set_defaults(func=cmd_status)
    sub.add_parser("guide", help="Show what to run for current phase").set_defaults(func=cmd_guide)
    sub.add_parser("validate", help="Validate current phase outputs").set_defaults(func=cmd_validate)

    adv = sub.add_parser("advance", help="Advance to next phase after checks")
    adv.add_argument("--force", action="store_true", help="Advance even if artifact is missing")
    adv.set_defaults(func=cmd_advance)

    args = parser.parse_args()
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
