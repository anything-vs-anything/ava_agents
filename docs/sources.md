# Research sources: Reddit and X

Scout, Context Extractor, and Smith should treat **Reddit** and **X** as the **primary** surfaces for discovering argument-dense communities and for drafting native prompts. Other sources are optional unless the user expands scope.

## Reddit

- **Unit of analysis:** subreddit (`r/...`) plus its culture, sidebar/wiki rules, and recurring thread types.
- **Discovery patterns:** search within Reddit; related subreddits; “controversial” or high-comment threads in candidate subs; megathreads where debates cluster.
- **Record in artifacts:** canonical subreddit name, link to subreddit or representative thread (when sharing externally is appropriate), and **rules summary** (flair, text-post norms, bans on topics).

## X

- **Unit of analysis:** there is no 1:1 subreddit analog. Use a clear **anchor** per candidate, e.g.:
  - **X Communities** (when relevant to the niche),
  - a small set of **high-signal accounts** or **lists** that repeatedly host comparisons,
  - or a **documented search / filter pattern** (e.g. recurring hashtag + quality heuristics) that reliably surfaces “vs / rank / pick one” discourse.
- **Record in artifacts:** anchor type, names/handles or query description, and how a human would **re-verify** live (no fabricated posts).

## Compliance and ethics (read-only research)

- Respect **Reddit** and **X** terms of service, API/usage rules, and rate limits. Prefer **official APIs** or **normal client use** the human controls—not scraping paywalled or logged-in-only content at scale.
- **Do not** automate posting, DMs, follows, or engagement. Research and drafting only; the human posts if they choose.
- **Do not** target harassment, brigading, or coordinated manipulation. Sentinel diagnostics should flag moderation and community backlash risks honestly.

## Split between platforms

Default Scout expectation: **roughly half** of candidate communities from **Reddit** and **half from X** (adjust if the user specifies a skew). Summarize the actual split in each `scout_discoveries` file.
