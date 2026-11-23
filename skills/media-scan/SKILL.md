---
name: media-scan
description: Scan Israeli media for coverage of a company, project or organisation - Google News plus the main Hebrew and English outlets - and produce a dated, sourced coverage list. CLI, no key. Use on "media coverage of X", "what's been written about this company", "news scan", "sikur tikshoret".
---

# Media scan

```bash
uv run ${CLAUDE_PLUGIN_ROOT}/skills/media-scan/scripts/media_scan.py "<exact name>" \
  --alias "<English name>" "<brand>" --sites [--extra תביעה בטיחות]
```

Verified 2026-11-23: Google News RSS answers scripts and dates every item; each query returns at most 100.

`--sites` adds 14 queries per name and found nothing extra on the 2026-11-23 test; use it for well-covered names.

1. Run exact names first, **no topic words**. Add `--extra` only in a second pass.
2. Scan the project name and the parent as separate runs. A subsidiary is often covered under the group name.
3. Google matches the article body, not just the headline. An off-topic headline can hide the key
   sentence (a safety list naming the company), so open anything with `name_in_headline: false` before dropping it.
4. Read the article. Use the browser or `exa` fetch; respect paywalls (headline and standfirst only, marked so).
5. Report per item: date, outlet, title, one-line paraphrase, how the entity features
   (subject / mentioned / list), READ or HEADLINE ONLY. Group wire copies and reposts as one story.

Press claims are claims: check numbers against filings and case outcomes against the court record.
Company-supplied advertorial (תוכן שיווקי) gets its own label. Zero results is not zero coverage.
