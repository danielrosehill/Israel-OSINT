---
name: court-case-lookup
description: Find Israeli court cases involving a company or other party from public case indexes, then compile a sourced case file. Two stages - list every case by exact party name, then open the interesting ones. Use on "has this company been sued", "court cases against X", "litigation history", "psak din", "tove'a / nitba", "beit mishpat".
---

# Court-case lookup by party name

Verified 2026-11-23. **Cast wide first.** A topic-filtered search found 1 case for a contractor; the same
name unfiltered found 43. Never put the subject in the stage-1 query.

## Stage 1: find the indexes, list everything

1. Exact legal name from `company-lookup`, with and without בע"מ, former names, group companies.
   Similar names are often different companies: match registry numbers before merging.
2. Google in a real browser (generic search APIs return almost no Israeli case law):
   `"<name>"`, `"<name>" נתבעת תובעת`, `"<name>" ("פסק דין" OR נגד)`, then `site:<index> "<name>"`.
3. Read the party's own page on each index:

| Index | Use | Access |
|---|---|---|
| תולעת המשפט `xn----8hcborozt8bdd.xn--9dbq2a` | **Best.** `/צד-להליך/<exact name>` lists a party's cases; `/תיק/<number>` gives parties, judge, type, result, hearings | browser, wait ~6 s; some rows paid |
| LawBuzz `lawbuzz.co.il/?s=<name>` | judgments containing a phrase | scriptable; loose matching; full text paid |
| judgments.org.il, verdicts.co.il | decisions, criminal verdicts | free |
| psakdin.co.il, lite.takdin.co.il | judgments, partial text | free part; psakdin crawl-delay 2 s |
| giluy-naot.org.il, psikan.com, law-mate.com, dinrega.com | recent decisions, some full PDFs | mostly free |
| supremedecisions.court.gov.il | Supreme Court, official | free |
| checkid.co.il | case list on a company profile | refuses scripts |
| Nevo, Takdin | full databases | paid |
| Net HaMishpat | official portal | the user completes any captcha |

Normal access only: no login, paywall or captcha workarounds.

## Stage 2: pick, read, compile

- Prefixes: ת"א civil, ת"ק small claims, תא"ק/תא"מ fast track, ת"צ class action, ת"פ criminal, חע"מ by-law fines,
  עת"מ administrative petition, סע"ש/ס"ע/ד"מ labour, ע"א/עע"מ appeals.
- Open: the state or a regulator as a party, neighbours and house committees, class actions, petitions, recent ones.
- Also search the **place and plan number**: the ruling that matters may not name the party.
- Record: number, court, parties and role, status, result, date, source, READ / INDEX ONLY / PAYWALLED, PDF sha256.

## Reading honestly

- An index is not the court; note the page's update date. "Open" may be stale.
- A conviction may later be undone: compare ticket and file numbers before writing "convicted".
- Nothing found means nothing indexed. AI search summaries are leads only.
- Leave private opponents' names out unless they matter. Look up a private person only for a stated legitimate
  reason, never to build a profile, and beware of namesakes. Not legal advice.
