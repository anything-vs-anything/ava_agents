# Dependency Audit — Atlas Agents

**Date:** 2026-03-23  
**Branch:** `cursor/dependency-updates-plan-3717`  
**Scope:** Full repository scan for outdated, deprecated, or vulnerable packages.

---

## Executive Summary

This repository has **zero managed third-party dependencies**. All Python scripts use only the standard library, the single HTML page loads fonts from a CDN stylesheet link, and there are no dependency manifests (`requirements.txt`, `package.json`, `pyproject.toml`, etc.) anywhere in the tree.

**No updates are required.** The sections below document exactly what was audited and provide forward-looking recommendations for when dependencies are introduced.

---

## Audit Methodology

1. Searched the full file tree for every standard dependency manifest format: `package.json`, `yarn.lock`, `package-lock.json`, `requirements.txt`, `setup.py`, `setup.cfg`, `pyproject.toml`, `Pipfile`, `Pipfile.lock`, `Gemfile`, `go.mod`, `Cargo.toml`, `pom.xml`, `build.gradle`, `Dockerfile`, `docker-compose.yml`, `.github/workflows/*.yml`.
2. Inspected all Python files for `import` / `from` statements to identify any third-party module usage.
3. Scanned HTML files for CDN `<script>` tags with pinned versions.
4. Checked JSON schemas for external specification references.

---

## Inventory of External References

### Python scripts (3 files)

| File | Imports | Third-party? |
|------|---------|-------------|
| `scripts/run_atlas_cycle.py` | `argparse`, `json`, `os`, `sys`, `datetime`, `pathlib` | No — all stdlib |
| `scripts/pipeline_automation.py` | `argparse`, `json`, `sys`, `datetime`, `pathlib` | No — all stdlib |
| `scripts/create_agent_prompt.py` | `argparse`, `re`, `pathlib` | No — all stdlib |

**Minimum Python version required:** 3.10+ (uses `X | Y` union type syntax in type hints).

### HTML (`web/index.html`)

| Resource | Type | Pinned version? |
|----------|------|----------------|
| `https://fonts.googleapis.com/css2?family=DM+Sans:...&family=Fraunces:...` | Google Fonts stylesheet | No pin — Google serves the latest font files automatically |

No `<script>` tags. No JavaScript dependencies.

### JSON Schema (`data/schemas/scout_discoveries.schema.json`)

| Reference | Purpose |
|-----------|---------|
| `https://json-schema.org/draft/2020-12/schema` | Meta-schema identifier (specification URL, not a library) |

This is the current draft and does not require updating.

### VS Code tasks (`.vscode/tasks.json`)

Invokes `python3 scripts/*.py` — no external tooling beyond the Python interpreter.

---

## Findings

| Category | Count | Action needed |
|----------|-------|---------------|
| Outdated packages | 0 | None |
| Deprecated packages | 0 | None |
| Vulnerable packages | 0 | None |
| Missing dependency manifests | — | See recommendations |

---

## Recommended Update Plan

**Smallest safe update plan: no code changes required.**

The repository is dependency-free by design. The recommended actions below are preventive, not corrective.

### 1. Add a `requirements.txt` (low priority)

Even though only stdlib modules are used today, pinning the Python version helps collaborators and CI:

```
# No third-party packages required.
# Python >= 3.10 is needed for type-hint syntax used in scripts/.
```

### 2. Pin Python version for tooling (low priority)

Consider adding a `.python-version` file (for `pyenv` users) containing `3.10` or later, so contributors use a compatible interpreter.

### 3. If dependencies are added later

When the project eventually pulls in third-party packages:

- Create `pyproject.toml` (preferred over `requirements.txt` for new projects) with pinned ranges.
- Run `pip-audit` or `safety check` in CI to catch vulnerabilities.
- Use Dependabot or Renovate for automated update PRs.

---

## Conclusion

No dependency updates are needed. The codebase is lightweight and stdlib-only, which eliminates supply-chain risk entirely. The external Google Fonts reference is auto-updating and does not require manual version management.
