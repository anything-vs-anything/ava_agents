# Agent prompts

- **`prompts/00-platform-context.md`** — shared background; attach with any phase-specific prompt.
- **`prompts/atlas.md` … `sentinel.md`** — one file per agent in the chain.
- **`templates/human-review-packet.md`** — what the human fills before any real-world post.

In Cursor, reference files with `@agents/prompts/scout.md` (etc.) so the model loads the full instruction set.
