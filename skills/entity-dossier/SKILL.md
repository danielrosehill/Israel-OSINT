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
   For a contractor, query data.gov.il `datastore_search` by company number (verified 2026-11-23):
   fines `16d8510b-aee9-4223-aa26-263d2b7ca83a` (עיצומים כספיים על ליקויי בטיחות),
   active sites and registered executor `b072e36c-a53b-49e1-be08-4a608fcf4638` (search site or company name),
   closed sites `b9257d8f-f93a-4c7d-84dd-e4b0838eadaa`, contractors' register `4eb61bd6-18cf-4e7c-9f9c-e166dfa0a2d8`
   (omit its phone, email and staff fields). Searching by number also exposes former names.
   The registered executor can be the parent rather than the company on the hoarding. A fine's address
   may be a neighbouring site: do not attach it to a project without a match.
3. **Second pass** on what stood out, plus the place, plan and project names.
4. **Reconcile** in one timeline. Where sources disagree, show both. Order of weight: court record and filing,
   registry, official database, index, press, company statement.
5. **Report**: one-paragraph picture; identity and ownership; money; litigation; regulatory and safety; media;
   timeline; what's unverified; what wasn't searched. Each line has a source, a date and
   READ / INDEX ONLY / HEADLINE ONLY / INFERRED. Use `israel-foi` for what isn't public.

Never merge similar names without a matching number, call an allegation a finding, or treat an empty search
as a clean record. Publishing the report is the user's decision, ideally after legal review.
