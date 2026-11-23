---
name: jerusalem-building-file-lookup
description: Look up Jerusalem building permits and planning records for a parcel (gush/helka) from the municipality's public GIS info hub - permit files and status, building-violation files, pre-permit information requests, conservation opinions, plans. Use on "who is building at <address> Jerusalem", "permit status for gush X helka Y", "tik binyan", "is there a building violation on this plot", before an FOI request.
---

# Jerusalem building-file lookup (jergisinfohub)

The Jerusalem Municipality's public "מידע תכנוני" hub serves per-parcel records as
JSON. Use it to find who holds a permit, what kind it is, when it was issued or renewed,
and whether violation files exist. Then decide what still needs an FOI request
(`israel-foi:jerusalem-municipality-foi`) or an in-person file inspection.

Verified 2026-11-23 in Claude in Chrome.

## What it gives and what it doesn't

- **Gives:** metadata per record: file number, opening date, request type, status and
  status date, use, applicant, address.
- **Doesn't give:** documents. No permit text, conditions, plans, acoustic or
  environmental reports, correspondence. For those, use FOI or inspect the building
  file in person at the licensing department.

## Access

- UI: `https://jergisinfohub.jerusalem.muni.il/UI/GisMeidaT/index.html`
- API: `GET /Services/api/MetaDataObjectsDetails/{objectId}?gush={gush}&helka={helka}`
  Companions: `/Services/api/GetGeneralInfo`, `/MetaDataObjects`, `/MetaDataFields/{id}`.
- **Plain curl / server-side fetch gets 403** (Akamai). Open the UI page in a real
  browser tab, then call the API with a same-origin `fetch()` from that page
  (`javascript_tool`). No login, no captcha.
- Response: `{gisDataObject: [...rows], gisObjectID, gisObjectName, gisObjectAlias, ...}`.
  Return only the fields you need. Raw dumps can trip the tool's output filter.

| objectId | Layer | Useful row fields |
|---|---|---|
| `1` | רישוי בניה (building permits) | `tik_num`, `taarih_ptiha` (opened), `sug_bakasha` (type), `r_status`, `r_taarih_status`, `p_taarih_status`, `shimush` (use), `mevakesh` (applicant), `address` |
| `6` | עבירות בניה (building violations) | file no., date, source (e.g. תלונה), status, closed date, offence type |
| `14` | מידע להיתר (pre-permit information requests) | file no., type, status, date, requester |
| `84` | חוות דעת שימור (conservation opinions) | id, case type, status, date, related permit/plan |
| `12` | תב"ע (plans) | |
| `13` | מגרשים / ייעודי קרקע (plots / land use) | |
| `16` | תצ"ר (parcellation plans) | |

Permit sub-files: `YYYY/NNNN.00` is the original application, and `.01`, `.02`, … are later
requests on the same file (excavation, additions, **חידוש היתר** = permit renewal).
Status `הופק-הוצא היתר בניה` = permit issued. `p_taarih_status` is a second, undocumented
date. Report it as such, don't interpret it.

## Getting gush/helka from an address

Use the municipal ArcGIS parcels layer (public, ITM / EPSG:2039):
`https://services3.arcgis.com/jeqc1A7OfE9m4EPO/arcgis/rest/services/helkot1225/FeatureServer/0/query`
(fields `GUSH_NO`, `PARCEL_NO`). Query by geometry from a geocoded point, or ask the user
for gush/helka from a contract or tax bill (ארנונה).

## Recipe

```js
const j = await (await fetch('/Services/api/MetaDataObjectsDetails/1?gush=30074&helka=447')).json();
j.gisDataObject.map(r => [r.tik_num, r.sug_bakasha, r.r_status, r.r_taarih_status, r.mevakesh].join(' | '));
```

Then repeat for `6`, `14` and `84`. Filter by `tik_num` prefix for one file, or by status date
for "anything new since <date>" (dates are `DD/MM/YYYY`; compare as `YYYYMMDD`).

## Reading the results carefully

- No violation file is **not** evidence that no complaints were made. Noise and nuisance
  complaints go to environment and enforcement units, not to this layer.
- The applicant (`mevakesh`) is usually the developer or owner entity. Confirm its legal
  identity and registered office with `company-lookup` (companies and partnerships
  datasets) before writing to it.
- Each record is a snapshot of the municipal system. Note the lookup date.
