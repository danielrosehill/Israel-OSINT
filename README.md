# Israel OSINT

Open-source intelligence on Israeli organisations and public records: establish who and what an entity officially is, using public registers, and say clearly what is confirmed versus a snapshot.

## Skills

- `company-lookup`: Companies Registrar, amutot, strike-off and registered-charge data via the open datasets on data.gov.il; statuses, the breach flag, stale-filing signals, entity types and where each type is registered. Script: `skills/company-lookup/scripts/lookup.py` (`uv run`).

## Backlog (not built)

Likely next skills, in rough order: amuta financial profile (turnover, staff, funders from GuideStar and the amutot dataset); gazette (Reshumot) notice search; insolvency docket check; NBCTF sanctions screening; listed-company disclosures (Maya/TASE); public procurement and tender records; land-registry and planning records; court decisions search.

## Complementary plugins

- `research-space` (osint and deep-research variants) and `legal-investigative` (OSINT investigation workspace, evidence logging, redaction): use them to run and document an investigation; this plugin supplies the Israel-specific sources.
- `digital-evidence`: hashing and timestamping captured records.
- `israel-open-data` ([Israel-Open-Data-Plugin](https://github.com/danielrosehill/Israel-Open-Data-Plugin)): general data.gov.il querying and quirks; this plugin's datasets are served by the same portal.

## Limits

No credit scoring, no litigation history, no foreign registries, no public beneficial-owner register exists in Israel (per the upstream source, not re-verified). Data is a periodic snapshot: confirm on the official register before legal or financial decisions. Unofficial; not affiliated with any government body.

Install: `claude plugins install israel-osint@danielrosehill`. See [THIRD_PARTY.md](THIRD_PARTY.md).
