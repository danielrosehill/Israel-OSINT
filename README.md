# Israel OSINT

Open-source intelligence on Israeli organisations and public records: establish who and what an entity officially is, using public registers, and say clearly what is confirmed versus a snapshot.

## Skills

- `entity-dossier`: runs the skills below together and reconciles them into one sourced report.
- `court-case-lookup`: every indexed court case for a party, then a case file.
- `media-scan`: Israeli news coverage, dated and sourced. CLI, no key.
- `public-filings`: Maya, Magna and investor-relations reports, including a private subsidiary via its listed parent.
- `company-lookup`: Companies Registrar, amutot, strike-off and registered-charge data via the open datasets on data.gov.il; statuses, the breach flag, stale-filing signals, entity types and where each type is registered. Script: `skills/company-lookup/scripts/lookup.py` (`uv run`).

- `parcel-lookup`: address or lat/lon → gush/helka with neighbouring parcels, and gush/helka → location, outline, status, legal area. CLI `skills/parcel-lookup/scripts/parcel.py` (`uv run`, no key). National cadastre layer plus the Jerusalem municipal layer.
- `jerusalem-building-file-lookup`: Jerusalem building permits, building-violation files, pre-permit requests and conservation opinions per gush/helka from the municipality's GIS info hub (metadata only; documents need FOI or in-person inspection). Pairs with `israel-foi`.

## Backlog (not built)

Likely next skills, in rough order: amuta financial profile (turnover, staff, funders from GuideStar and the amutot dataset); gazette (Reshumot) notice search; insolvency docket check; NBCTF sanctions screening; public procurement and tender records; Tabu extract ordering (18 ₪, official site; reading is in `rtl-skills:read-israeli-forms`); planning records for cities other than Jerusalem.

## Complementary plugins

- `research-space` (osint and deep-research variants) and `legal-investigative` (OSINT investigation workspace, evidence logging, redaction): use them to run and document an investigation; this plugin supplies the Israel-specific sources.
- `israel-foi` ([Israel-FOI-Plugin](https://github.com/danielrosehill/Israel-FOI-Plugin)): when the record you need isn't public, file an FOI request with the authority that holds it.
- `digital-evidence`: hashing and timestamping captured records.
- `israel-open-data` ([Israel-Open-Data-Plugin](https://github.com/danielrosehill/Israel-Open-Data-Plugin)): general data.gov.il querying and quirks; this plugin's datasets are served by the same portal.

## Limits

No credit scoring, no litigation history, no foreign registries, no public beneficial-owner register exists in Israel (per the upstream source, not re-verified). Data is a periodic snapshot: confirm on the official register before legal or financial decisions. Unofficial; not affiliated with any government body.

Install: `claude plugins install israel-osint@danielrosehill`. See [THIRD_PARTY.md](THIRD_PARTY.md).
