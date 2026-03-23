# Atlas Human-Readable Run Report

## Run Summary

- **Run ID:** `20260323T164718Z`
- **Mode:** Live verification pass (public web only)
- **Overall status:** Completed through `atlas_learn` with human gate enforced
- **Posting activity:** None (no automated posting executed)

## Atlas Orchestration Notes

- Reddit evidence was directly verified from live public thread pages.
- X validation was partial in this environment due direct-post retrieval limits.
- Pipeline continued with conservative confidence handling and explicit human checks.

## Scout Findings (Discovery)

### Candidate 1: `r/buildapc` (Reddit, technology)

- **Evidence link:** https://www.reddit.com/r/buildapc/comments/1rswv1f/best_gpu_to_buy_at_every_budget_in_2026_price_to/
- **Why it matters:** clear compare-and-choose behavior with high-volume opposing recommendations.
- **Signals observed:**
  - explicit budget-tier comparison request
  - many replies defending different GPU picks
  - recurring A-vs-B framing (`RX 9070 XT` vs `RTX 5070 Ti`)
- **Viability:** `viable`
- **Reason:** active argument culture and concrete comparison rituals.

### Candidate 2: `r/NFL_Draft` (Reddit, sports)

- **Evidence link:** https://www.reddit.com/r/NFL_Draft/comments/1r373ou/mansoor_delane_or_jermod_mccoy_as_cb1/
- **Why it matters:** direct binary prospect comparison with sustained disagreement.
- **Signals observed:**
  - binary framing in title
  - ceiling-vs-safety arguments
  - injury-risk weighting in decisions
- **Viability:** `viable`
- **Reason:** repeatable debate format with defensible positions.

### Candidate 3: `X AI tool comparison cluster` (X, technology)

- **Anchor:** search pattern (`site:x.com + ai coding + vs + thread`)
- **Viability:** `uncertain`
- **Reason:** no direct live post verification captured in this run.

## Judge Outcomes (Qualification)

- **Approved (`Good`):**
  - `r/buildapc`
  - `r/NFL_Draft`
- **Watchlist (`Risky`):**
  - `X AI tool comparison cluster`
- **Top strike:** `r/buildapc`
- **Judge note:** approvals were limited to directly verifiable public evidence.

## Context Extractor Highlights

### `r/buildapc` profile

- **Tone:** technical, price-sensitive, comparative
- **Debate primitives:** value vs premium features, new vs used, ecosystem tradeoffs
- **Common trigger:** pricing shifts and budget recommendation threads

### `r/NFL_Draft` profile

- **Tone:** argumentative, scouting-centric, injury-risk aware
- **Debate primitives:** upside vs reliability, recent tape vs prior peak
- **Common trigger:** new mocks, combine/pro-day news

## Smith Outputs (Prompt Drafts)

### Prompt `live-r-buildapc-001`

- **Title:** Value Debate (2026): RX 9070 XT or RTX 5070 Ti for a fixed $1000 GPU budget?
- **Goal:** force explicit tradeoff reasoning (raster, RT, efficiency, resale, drivers)
- **Duplicate risk:** `medium`

### Prompt `live-r-nfl-draft-001`

- **Title:** CB1 Debate: Elite upside with injury risk vs safer year-to-year consistency?
- **Goal:** structure floor/ceiling and risk-threshold arguments
- **Duplicate risk:** `medium`

## Quality Gate Result

- **Result:** `pass_with_fixes`
- **Passes:**
  - native tone
  - stakes and depth
- **Warnings:**
  - duplicate topic risk
  - partial source verification (Reddit strong, X partial)
- **Required fixes before posting:**
  - re-check community rules and weekly thread policy
  - run 48-72h duplicate scan
  - gather direct X anchors before any X attempt

## Human Review Status

- **Reviewer:** pending
- **Checklist completion:** pending (all critical pre-post checks still open)
- **Decision for this run:** no real-world posting executed

## Sentinel Diagnostics

- **Mode:** `live_verification_no_post`
- **Outcome metrics:** not available (no posts were made)
- **Primary drivers:**
  - no live execution
  - strongest verification confidence on Reddit
  - X evidence remained indirect
- **Recommended next action:** run one narrow human pilot on a single Reddit target, then perform a dedicated direct-X verification pass.

## Practical Next Steps

1. Complete human review checklist for one target (`r/buildapc` preferred).
2. Run recency/duplicate checks immediately before posting.
3. Execute one human-posted pilot and record Sentinel metrics at 15m, 1h, and 24h.
4. Run a separate X-only evidence pass with direct post URLs before approving X strikes.
