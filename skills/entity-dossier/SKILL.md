---
name: entity-dossier
description: Build a composite picture of an Israeli company or organisation by running registry, filings, litigation, media and permit lookups together and reconciling them into one sourced report. Use on "research this company", "due diligence", "full picture of X", "composite report", "dossier".
---

# Entity dossier

For companies, organisations and projects. Not for profiling private people.

1. **Identity first** (`company-lookup`): legal name, number, status, registered office, parent, former names.
   Everything else keys off this. Stop and ask if two entities fit.
2. **In parallel**, names only, no topic filter:
   `court-case-lookup` · `media-scan` · `public-filings` · safety orders (Kav LaOved,
   `work-accidents.kavlaoved.org.il`) · for a building project `parcel-lookup` and `jerusalem-building-file-lookup`.
3. **Second pass** on what stood out, plus the place, plan and project names.
4. **Reconcile** in one timeline. Where sources disagree, show both. Order of weight: court record and filing,
   registry, official database, index, press, company statement.
5. **Report**: one-paragraph picture; identity and ownership; money; litigation; regulatory and safety; media;
   timeline; what's unverified; what wasn't searched. Each line has a source, a date and
   READ / INDEX ONLY / HEADLINE ONLY / INFERRED. Use `israel-foi` for what isn't public.

Never merge similar names without a matching number, call an allegation a finding, or treat an empty search
as a clean record. Publishing the report is the user's decision, ideally after legal review.
