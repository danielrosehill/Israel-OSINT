---
name: parcel-lookup
description: Turn an Israeli address or lat/lon into its cadastral block and parcel (gush/helka), with neighbouring parcels, or turn a gush/helka into its location, outline and legal area. CLI, no key. Use on "what's the gush helka of <address>", "which parcel is this", "where is gush X helka Y", before a Tabu extract, permit lookup or FOI request.
---

# Parcel lookup (location ↔ gush/helka)

The first step for anything land-related: Tabu extracts, building-permit lookups, planning
records, FOI requests. One CLI, JSON out, no API key. Verified 2026-11-23.

```bash
P=${CLAUDE_PLUGIN_ROOT}/skills/parcel-lookup/scripts/parcel.py
uv run $P "כיכר ספרא 1, ירושלים"          # address -> parcel at point + parcels within --radius
uv run $P --latlon 32.0753,34.7749         # point
uv run $P --gush 30074 --helka 447         # reverse -> centroid, bbox, status, legal area
#   --radius 30 (metres, default 30)  --source auto|national|jerusalem
```

## Sources

| Source | Coverage | Fields |
|---|---|---|
| `national`: "חלקות קדסטר בישראל" on ArcGIS Online (`services8.arcgis.com/JcXY3lLZni6BK4El/.../חלקות/FeatureServer/0`) | ~1.1M parcels nationwide. A copy of the Survey of Israel cadastre (publisher: `sysdata`), **not the official MAPI service**. Last edited around Sept 2026. | `GUSH_NUM`, `PARCEL`, `STATUS_TEX` (מוסדר / חדש רשום / …), `LOCALITY_N`, `LEGAL_AREA` (m²) |
| `jerusalem`: Jerusalem Municipality `helkot1225` | the whole city, **including central blocks missing from the national layer** (e.g. gush 30074, where settlement/registration is still in progress) | `GUSH_NO`, `PARCEL_NO` |

`auto` tries national first, then Jerusalem for points inside the city envelope. Add
other municipalities' public parcel layers to `LAYERS` in the script the same way.

Dead ends checked 2026-11-23: govmap's open WFS (`open.govmap.gov.il/geoserver/...`) returns
an HTML error page to scripts. The govmap API needs a token.

## Reading the result

- **Geocoding is approximate.** OpenStreetMap returns one point, at house level at best and
  sometimes only street or square level (check `osm_type`: `house` is best). That point can fall
  in the neighbouring street-facing parcel. Example: "כיכר ספרא 1, ירושלים" resolves only to the
  square, giving 30817/44 at the point and 30817/42 and /46 within 25 m. Always report
  `at_point` **and** `nearby`, and confirm against a document (contract, arnona bill, lease)
  before paying for an extract.
- An empty national result in an old city centre usually means unsettled or in-registration land
  (not "no parcel"). Fall back to the municipal layer, and expect the Tabu extract to carry
  a "בהליכי רישום / תיקון הסדר" notice.
- A sub-parcel (תת חלקה) for a flat in a condominium is **not** in these layers. It's in the
  Tabu extract, or ask the registry's call centre (*8653, ext. 7 then 1).

## Next steps it feeds

- Official extract: gov.il "הפקת נסח טאבו" (מקרקעין ברשת). As of 2026-11, a regular full extract
  costs 18 ₪ per parcel, emailed within minutes, and the user pays. Read the PDF with
  `rtl-skills:read-israeli-forms`.
- Jerusalem permits and violations for the parcel: `jerusalem-building-file-lookup`.
- Company behind the applicant or owner: `company-lookup`.
