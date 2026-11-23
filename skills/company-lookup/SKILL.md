---
name: company-lookup
description: Look up an Israeli company, amuta (NPO) or other registered entity from the open registrar data: status, breach flag, last annual report, strike-off notices, charges; plus entity-type guidance. Use on "look up this Israeli company", "chevra", "company number 51...", "Rasham HaChevarot", "is this amuta registered", "Israeli due diligence".
---

# Israeli company and entity lookup

First skill of the Israel-OSINT plugin: establish what an Israeli organisation officially is, from public registers. Not credit scoring, not litigation search, not foreign registries.

## Route that an agent can execute

The Israel Corporations Authority (ICA) search page is a human web form. Use the Ministry of Justice open datasets on data.gov.il instead (free, no key). Helper: `scripts/lookup.py` (stdlib, `uv run`):

```
uv run scripts/lookup.py company 514744887        # exact by number
uv run scripts/lookup.py company "monday.com"      # free text, Hebrew or English
uv run scripts/lookup.py amuta 580000016           # amutot registry
uv run scripts/lookup.py deletion <number>         # flagged for strike-off
uv run scripts/lookup.py pledges <number>          # registered charges (shiabud) events
```

| Subcommand | Dataset slug | Resource id | Rows (2026-11-20) |
|---|---|---|---|
| `company` | `ica_companies` | `f004176c-b85f-4542-8901-7b3176f9a054` | not counted |
| `amuta` | amutot registry | `be5b7935-3922-45d4-9638-08871b17ec95` | 76,146 |
| `deletion` | `ica-deletion` | `0fd312bb-68c9-4647-b186-60c3e7b4f6f7` | 9,308 |
| `pledges` | `ica-changes` | `28780ab5-3ef1-44c7-8377-da82c0aa6781` | 563,663 |

All four confirmed returning real records on 2026-11-20 (monday.com 514744887 resolved; free-text "monday.com" returned it and the Foundation 516948726). Resource ids rotate on republication: if a call returns an HTML 404 or AccessDenied, re-resolve with `package_show?id=<slug>`. General API behaviour and quirks: the `data-gov-il` skill in the Israel-Open-Data plugin.

Company record fields worth reading: `מספר חברה` (number), `שם חברה` (Hebrew name), `שם באנגלית`, `סוג תאגיד`, `סטטוס חברה`, `מפרה` (breach flag), `שנה אחרונה של דוח שנתי (שהוגש)` (last filed annual report year; a stale year is a red flag before formal breach), `תאריך התאגדות`, `מגבלות` (limited or not), `חברה ממשלתית`, address fields (`שם עיר`, `שם רחוב`, `מספר בית`).

## Procedure

1. Resolve the entity by **number** when you have one; else search the Hebrew name, then the English name. Registry names use `~` for quotes (`בע~מ`), so searching `בע"מ` finds nothing. English names are inconsistently filled and often differ from the trading name: an English-only miss proves nothing.
2. Read status and breach flag. Statuses: active (pe'ila), in liquidation (be-piruq), struck off (nimekhqa), in breach of law (mufrat hok; unpaid annual fees, missing reports). Checking only "active" misses breach.
3. Check `deletion` (strike-off pending) and, if relevant, `pledges` (charges registered or released against the number).
4. Report with the snapshot caveat: the datasets are periodic dumps. For any signing, lending or litigation decision, confirm on the official ICA search (https://ica.justice.gov.il/GenericCorporarionInfo/SearchCorporation?unit=8) or a paid extract (https://ica.justice.gov.il/Request/OpenRequest?rt=CompanyExtract; fee shown on the form).

## Where each entity type lives

- Companies (prefix 51-, 9 digits): `ica_companies`, above. Company number is not the tax ID (mispar osek).
- Amutot (58-) and public-benefit companies (CHL"Tz, in the companies data with a "(חל~צ)" suffix): amutot dataset above and GuideStar https://www.guidestar.org.il (free extracts). Amutot records carry financial turnover, staff and volunteers.
- Partnerships (55-): not in the companies dataset, but the registrar publishes a **separate partnerships dataset** on data.gov.il, resource `139aa193-fabb-4f6b-a71b-0bb40fd73eb2` ("מאגר שותפויות - רשם החברות"; fields: מספר שותפות, שם, status, city/street/house/postcode, **אצל** care-of). Query it with the same `datastore_search` call (`q=<number or name>`). Verified 2026-11-23 on a limited partnership (55…): active, registered office plus care-of line. Paid official extract: https://ica.justice.gov.il/Request/OpenRequest?rt=PartnershipExtract.
- **Registered office for formal letters:** use the registry's address fields *and* the `אצל` (care-of) line, not a directory or marketing address. A business directory can find the number, but confirm the address in the registry.
- Cooperatives (57-): own registry.
- Sole traders (osek patur/morsheh): Tax Authority VAT registration, not a registrar entity.
- See `references/entity-types.md` for the full table, prefixes and fees.

## Beyond the registrar (pointers, not covered by the script)

- Official gazette (liquidation notices, creditor calls): https://www.gov.il/he/Departments/DynamicCollectors/gazette-official
- Insolvency Commissioner dockets for cases from 2019-09-15: https://insolvency.justice.gov.il/poshtim/main/tikim/wfrmlisttikim.aspx (older files stay under the legacy Apotropos Klali).
- Counter-Terrorism Law designations (NBCTF): https://nbctf.mod.gov.il/en/Minister%20Sanctions/Designation/Pages/downloads.aspx
- Listed companies' disclosures: Maya (maya.tase.co.il). Licensed financial entities: ISA (isa.gov.il) and the Capital Market Authority.
- **No public UBO register.** As of the upstream author's August 2026 check the law was still pre-enactment and a future registry is not planned to be public. Do not promise beneficial-owner lookup; closest signals are a paid extract's directors/shareholders, annual reports and Maya for listed companies. Not re-verified here.

## Examples

- "Look up monday.com": `company 514744887` gives public company, active, incorporated 13/03/2012, Yitzhak Sadeh 6, Tel Aviv-Yafo, last annual report 2026 (snapshot 2026-11-20). Never quote a company number from memory; resolve it.
- "Which entity type should a freelancer use": see `references/entity-types.md`; osek patur/morsheh vs Ltd, fees marked 2026 must be verified at ica.justice.gov.il.

## Sources

Adapted from [israeli-company-lookup](https://github.com/skills-il/government-services/tree/972fb0be9f960ad534ee6dc13881c9468280b0ed/israeli-company-lookup) by Skills IL (MIT). Changes: reoriented from entity-type advice to lookup (the upstream script only printed static tables; replaced by a working `lookup.py` over four open datasets, tested 2026-11-20); added the strike-off, charges and amutot datasets; dropped the registration walkthrough, the static-table script, the coverage checklist and Hebrew variant. Entity-type reference kept as upstream wrote it (2026 fees unverified here).
