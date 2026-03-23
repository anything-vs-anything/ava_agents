#!/usr/bin/env python3
"""
Atlas cycle helper: manages run folders and data/state.json.
Does not call external APIs or post to any platform.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
STATE_PATH = DATA / "state.json"
RUNS = DATA / "runs"

PHASES = [
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


def load_state() -> dict:
    if not STATE_PATH.exists():
        return {}
    return json.loads(STATE_PATH.read_text(encoding="utf-8"))


def save_state(state: dict) -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")


def ensure_dirs() -> None:
    RUNS.mkdir(parents=True, exist_ok=True)
    (DATA / "memory").mkdir(parents=True, exist_ok=True)
    (DATA / "schemas").mkdir(parents=True, exist_ok=True)


def cmd_new_run(_args: argparse.Namespace) -> int:
    ensure_dirs()
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_dir = RUNS / run_id
    run_dir.mkdir(parents=True, exist_ok=False)
    (run_dir / "context_profiles").mkdir(exist_ok=True)

    state = load_state()
    state.update(
        {
            "run_id": run_id,
            "phase": "atlas_plan",
            "human_cleared": False,
            "last_tick": datetime.now(timezone.utc).isoformat(),
            "notes": f"Run folder: {run_dir.relative_to(ROOT)}",
        }
    )
    save_state(state)

    print(f"Created run {run_id}")
    print(f"Directory: {run_dir}")
    print("Next: in Cursor, use @agents/prompts/atlas.md and plan this cycle.")
    return 0


def cmd_status(_args: argparse.Namespace) -> int:
    ensure_dirs()
    state = load_state()
    if not state:
        print("No state.json yet. Run: python3 scripts/run_atlas_cycle.py new-run")
        return 0
    print(json.dumps(state, indent=2))
    rid = state.get("run_id")
    phase = state.get("phase")
    if rid:
        print(f"\nRun path: {RUNS / rid}")
    if phase and phase != "idle":
        try:
            i = PHASES.index(phase)
            nxt = PHASES[i + 1] if i + 1 < len(PHASES) else "(end)"
        except ValueError:
            nxt = "(run new-run if starting fresh)"
        print(f"Suggested next phase after current ({phase}): {nxt}")
    elif phase == "idle":
        print("Suggested next step: python3 scripts/run_atlas_cycle.py new-run")
    return 0


def cmd_set_phase(args: argparse.Namespace) -> int:
    ensure_dirs()
    if args.phase not in PHASES:
        print(f"Unknown phase. Choose one of: {', '.join(PHASES)}", file=sys.stderr)
        return 1
    state = load_state()
    if not state.get("run_id"):
        print("No active run. Run new-run first.", file=sys.stderr)
        return 1
    state["phase"] = args.phase
    state["last_tick"] = datetime.now(timezone.utc).isoformat()
    if args.phase == "human_review":
        state["human_cleared"] = False
    save_state(state)
    print(f"Phase set to {args.phase}")
    return 0


def cmd_human_ok(_args: argparse.Namespace) -> int:
    ensure_dirs()
    state = load_state()
    state["human_cleared"] = True
    state["phase"] = "sentinel"
    state["last_tick"] = datetime.now(timezone.utc).isoformat()
    save_state(state)
    print("Marked human_cleared=true and advanced phase to sentinel.")
    return 0


def cmd_tick(_args: argparse.Namespace) -> int:
    """Daily hook: ensure dirs exist and refresh last_tick (for launchd / cron)."""
    ensure_dirs()
    state = load_state()
    state["last_tick"] = datetime.now(timezone.utc).isoformat()
    save_state(state)
    print("tick:", state["last_tick"])
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description="Atlas cycle state helper")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("new-run", help="Create a new run id and folder").set_defaults(func=cmd_new_run)
    sub.add_parser("status", help="Print state.json").set_defaults(func=cmd_status)
    sub.add_parser("tick", help="Update last_tick (for scheduled jobs)").set_defaults(func=cmd_tick)

    sp = sub.add_parser("set-phase", help="Set current phase in state.json")
    sp.add_argument("phase", choices=PHASES)
    sp.set_defaults(func=cmd_set_phase)

    sub.add_parser("human-ok", help="After human review, advance to sentinel").set_defaults(func=cmd_human_ok)

    args = p.parse_args()
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
