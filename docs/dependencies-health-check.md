# Dependencies Health Check

**Date:** 2026-03-23
**Python runtime tested:** 3.12.3
**Scope:** Full repository audit — Python scripts, HTML assets, JSON schemas, shell scripts, CI/CD

---

## Executive Summary

This repository has **zero third-party package dependencies**. All three Python
scripts rely exclusively on the standard library. The single HTML page loads two
Google Fonts via CDN but includes no JavaScript libraries. There are no lockfiles,
no CI workflows, and no Docker images to audit.

**Risk level: Minimal.** The recommendations below are preventive hardening, not
urgent fixes.

---

## Audit Details

### 1. Python Scripts

| File | Imports | Third-party? |
|------|---------|-------------|
| `scripts/run_atlas_cycle.py` | `argparse`, `json`, `os`, `sys`, `datetime`, `pathlib` | No |
| `scripts/pipeline_automation.py` | `argparse`, `json`, `sys`, `datetime`, `pathlib` | No |
| `scripts/create_agent_prompt.py` | `argparse`, `re`, `pathlib` | No |

All scripts use `from __future__ import annotations` and PEP 604 union syntax
(`Path | None`). Under `__future__` annotations this compiles on Python 3.7+,
but **Python >= 3.10 is recommended** for full runtime support of the union type
syntax if annotations are ever evaluated at runtime (e.g., by type-checking tools
or frameworks that inspect signatures).

**Findings:** No outdated, deprecated, or vulnerable packages.

### 2. Web Assets (`web/index.html`)

| Resource | Source | Risk |
|----------|--------|------|
| DM Sans (font) | `fonts.googleapis.com/css2` | Low — Google Fonts CSS2 API is stable; no deprecation announced |
| Fraunces (font) | `fonts.googleapis.com/css2` | Low — same API |

No JavaScript frameworks, no CSS frameworks, no `<script>` tags.

**Findings:** The CSS2 API is the current recommended Google Fonts endpoint. The
`v1` CSS API is the one with a deprecation trajectory. No action needed.

### 3. JSON Schemas

| File | Schema dialect |
|------|----------------|
| `data/schemas/scout_discoveries.schema.json` | `https://json-schema.org/draft/2020-12/schema` |

Draft 2020-12 is the latest stable JSON Schema specification. No upgrade needed.

### 4. Shell & Tooling

| File | Notes |
|------|-------|
| `scripts/install_launchd.sh` | macOS-only `launchctl` helper; uses `sed`, POSIX-portable |
| `scripts/com.atlas.cycle.plist.example` | Hardcodes `/usr/bin/python3`; safe on macOS where system Python 3 ships |
| `.vscode/tasks.json` | v2.0.0 schema; invokes `python3` on helper scripts |

**Findings:** No deprecated commands. The `launchctl load/unload` verbs are
deprecated on macOS 13+ in favor of `launchctl bootstrap/bootout`, but this is
informational only — the legacy verbs still function.

### 5. CI/CD & Docker

No `.github/workflows/`, `.gitlab-ci.yml`, `Dockerfile`, or `docker-compose.yml`
files exist. Nothing to audit.

---

## Recommendations

### Safe — implement now (no breaking changes)

1. **Add `python_requires` metadata.** Create a minimal `pyproject.toml` or
   `.python-version` file documenting `>= 3.10` so future contributors (and
   tools like `pyright`, `mypy`, `ruff`) target the correct version.

2. **Pin Google Fonts with `font-display: swap`.** Already present in the URL
   (`&display=swap`). No change needed.

3. **Add a repeatable health-check script** (`scripts/check_deps.py`) that
   future contributors can run to re-audit imports and flag any new third-party
   packages.

### Low priority — nice-to-have

4. **Modernize `install_launchd.sh`** to use `launchctl bootstrap` when running
   on macOS 13+. Non-urgent; the legacy API still works.

5. **Consider self-hosting fonts** if offline usage or build reproducibility
   becomes important. Currently not needed.

### No action required

- JSON Schema draft 2020-12 — current
- VS Code tasks.json v2.0.0 — current
- All Python standard library imports — stable across 3.10+

---

## Re-running This Audit

```
python3 scripts/check_deps.py
```

The script scans all `.py` files for imports and reports any that are not in the
Python standard library. Run it whenever new scripts are added.
