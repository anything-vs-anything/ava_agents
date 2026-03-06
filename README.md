# AvA Agents — Guerrilla Seeding Marketing Micro-Team

A four-agent AI architecture for running a guerrilla seeding marketing playbook. These agents are designed to run on **Kimi Claw** (OpenClaw-style local orchestration) with cheap API models, targeting **~$150–$300/month** (max $500) on standard hardware (Mac minis or mid-grade Mac laptops).

**Design principle:** Human approval for posting/DMs to avoid bans and brand damage. Agents produce copy-paste assets, ranked targets, and tracking; a single operator pushes the buttons.

---

## Agent Roster

| Agent | Type | Monthly Cost | Role in One Line |
|-------|------|--------------|------------------|
| **Ritual Scout** | Analyst | $35–$80 | Finds and ranks high-ritual communities that tolerate cold seeding. |
| **Battle Foundry** | Creative | $40–$120 | Generates native-feeling seed posts and Community Battle Starter Kits. |
| **Seeding Operator** | Executor | $30–$90 | Runs post → monitor → mod DM → handoff with minimal founder time. |
| **Signal Ops** | Monitor | $15–$60 | Tracks ritual adoption (repeat battles without you), not vanity engagement. |

**Optional automation glue (Make/Zapier):** $0–$20/mo  
**Total:** ~$120–$370/mo (under $500).

### Daily schedule

| Time        | Agent          | Purpose             |
| ----------- | -------------- | ------------------- |
| 5:00 AM     | Ritual Scout   | Find communities    |
| 5:30 AM     | Battle Foundry | Create battle packs |
| Every 2 hrs | Signal Ops     | Monitor adoption    |
| 6:30 AM     | Atlas          | Health check        |
| 6:45 AM     | Atlas          | Morning brief       |

---

## Agent 1 — Ritual Scout (Analyst)

**Role:** Finds and ranks “high-ritual” communities that will tolerate cold seeding and are likely to adopt recurring battles. Enforces targeting criteria (Argument Density, Cold Tolerance, Ritual Readiness) to avoid wasted shots (bans, dead threads, low adoption).

**Daily operations:**
- **Morning:** Scans 30–50 candidate communities (Reddit/Discord/FB/forums), scores them on a 10-factor rubric; acts when score ≥ threshold (e.g., 75/100).
- **Every 4 hours:** Monitors top 20 “in-play” communities for trending topics and seasonal hooks; acts on topic spikes (draft season, game release, city event).
- **EOD:** Outputs “Top 10 targets for tomorrow” with post-format constraints (karma gates, title rules, banned topics) and a recommended seed prompt.

**Tech stack:**
- **Model:** OpenAI gpt-4.1-mini (classification/scoring + synthesis).
- **Tools:** Browser automation (Playwright), lightweight scrapers; optional Reddit API; manual CSV import if APIs blocked.
- **Memory:** SQLite — community scores, post rules, prior outcomes; weights updated from performance (engagement + adoption).

**Self-improvement:** Auto-adjusts scoring weights from outcomes; A/B tests top-score vs wildcard; fire/replace if high scores yield low engagement or bans.

**Communication:** Sends daily target shortlist + constraints → **Battle Foundry**. Receives performance outcomes from **Signal Ops** to retrain scoring.

---

## Agent 2 — Battle Foundry (Creative)

**Role:** Generates native-feeling seed posts and “Community Battle Starter Kits” (copy/paste prompts + result templates) tailored to each target community’s culture and rules. Maximizes adoption without hand-writing everything.

**Daily operations:**
- **Daily:** Generates 10–20 seed posts matched to Scout’s targets; acts on new targets or trending hooks.
- **Twice daily:** Produces 3 variants per battle (safe/edgy/data-driven) and recommends best by community tone; acts when tone mismatch is flagged.
- **Daily:** Outputs “result follow-up” post copy (winner announcement + next battle teaser); acts when Signal Ops marks a thread as successful.

**Tech stack:**
- **Model:** OpenAI gpt-4.1-mini (quality copy); optional gpt-4.1-nano for bulk variants.
- **Tools:** Canva/Figma template links, local prompt library; optional simple branded image generation.
- **Memory:** SQLite — winning templates per niche; best hooks/titles.

**Self-improvement:** Learns per niche (titles, stakes framing, cadence); prunes low performers, promotes winners into default kit; fire/replace if templates get removed for “low effort” or miss engagement.

**Communication:** Receives targets + constraints from **Ritual Scout**. Sends final post copy + follow-up → **Seeding Operator**. Receives performance labels from **Signal Ops** to refine templates.

---

## Agent 3 — Seeding Operator (Executor)

**Role:** Turns assets into action: runs the Pilot-in-Public workflow (post → monitor → mod DM → handoff kit) with minimal founder time. Keeps seeding consistent, compliant, and repeatable.

**Daily operations:**
- **3×/day (e.g., 11am/4pm/9pm):** Prepares “ready-to-post queue” and requires human approval; acts when Foundry provides seeds and Scout marks them postable.
- **60–120 min after posting:** Checks early signals (comment velocity); acts when engagement passes threshold (e.g., 20 comments / 30 min) to trigger follow-up + mod DM script.
- **Daily:** Sends mod/admin outreach only after traction; acts when a thread hits “proof” thresholds (engagement + positive sentiment).

**Tech stack:**
- **Model:** gpt-4.1-mini (compliance checklists + DM drafting); nano for routine formatting.
- **Tools:** OpenClaw orchestration (task routing + schedules); Playwright for “open page, extract signals”; optional Zapier/Make for notifications.
- **Memory:** SQLite “campaign ledger” (where posted, copy, time, outcome); DM outcomes and mod responses.

**Self-improvement:** Learns best posting times and sequences per niche; ban-risk model increases human review when risk rises; fire/replace if it repeatedly causes removals/bans.

**Communication:** Pulls seed queue from **Battle Foundry** + constraints from **Ritual Scout**. Pushes outcome events → **Signal Ops**.

---

## Agent 4 — Signal Ops (Monitor)

**Role:** Measures what matters and prevents false positives. Tracks **ritual adoption** (repeat battles without you), not vanity engagement. Enforces “density before scale” and tells you where to double down.

**Daily operations:**
- **Every 2 hours:** Pulls metrics from campaign ledger; acts when a community crosses success thresholds (e.g., 2+ battles/week, mod buy-in, repeat participants).
- **Daily:** Flags failures and diagnoses why (removal reason, low velocity, tone mismatch); acts when a community underperforms 3 consecutive seeds.
- **Weekly:** Produces “Double Down / Pause / Exit” report for top 10 communities; acts when ROI rank changes.

**Tech stack:**
- **Model:** gpt-4.1-nano (summarization + outcome classification); mini for weekly insight synthesis.
- **Tools:** SQLite → simple dashboard (Metabase local or lightweight web); optional Google Sheets export.
- **Memory:** Per-community “ritual score” over time; allowlist/blacklist and recommended next actions.

**Self-improvement:** Recalibrates success thresholds by niche; A/B tests follow-up style and measures reactivation; fire/replace if reports don’t predict outcomes (e.g., “double down” but no adoption).

**Communication:** Receives event stream from **Seeding Operator**. Sends “what worked” labels → **Ritual Scout** (target scoring) and **Battle Foundry** (template tuning).

---

## Orchestration (OpenClaw)

- **Host:** One Mac mini or laptop as orchestrator.
- **Framework:** OpenClaw for scheduler/router + local tool calls (browser, DB).
- **Data spine:** Single SQLite database + optional daily CSV export to Google Sheets.
- **Later:** Entity resolve + changefeed when platform APIs are ready.

---

## Expected Output (30 Days)

With discipline (e.g., 5 communities max):

- **100–250** seeded battles posted (across 5 targets, with variants).
- **10–20** mod/admin conversations triggered only after traction.
- **2–5** communities running a weekly ritual without you (the real win).
- Reusable targeting engine + starter kits library (compounding assets).

---

## References

- **Models:** OpenAI gpt-4.1-mini / gpt-4.1-nano (see current API pricing).
- **Agent framework:** Kimi Claw / OpenClaw — local/open-source agent framework for orchestration and tool use.
- **Design doc:** “GPT Proposed 4 Agent AvA Mktg Architecture” — analyst (Scout), creative (Foundry), executor (Operator), monitor (Signal Ops), with 30-day build plans per agent.
