---
name: public-filings
description: Read Israeli public-company filings (TASE Maya, ISA Magna, investor-relations pages) for financials, backlog, legal proceedings, environmental and safety disclosures, including about private subsidiaries of a listed parent. Use on "company financials", "annual report", "doch tkufati", "what do the filings say about X", "Maya".
---

# Public filings

A private company is often visible through its **listed parent or bond issuer**. Confirm the chain in a filing,
not from a similar name.

## Sources, in order

1. Investor-relations page (דוחות כספיים): direct PDFs, scriptable. Easiest.
2. Maya (`maya.tase.co.il`): immediate reports, search by company. JavaScript app, use the browser.
3. Magna (`magna.isa.gov.il`): ISA archive, older reports. Browser.
4. Not listed: registrar extract (paid, the user pays) via `company-lookup`. Private accounts are usually not public.

## Reading a periodic report (דוח תקופתי)

`pdftotext report.pdf` then search by page. Hebrew PDFs carry bidi marks: strip U+200E/F, U+202A-E, U+2066-9
before matching, and look at the page itself before relying on a miss.

| Want | Look for |
|---|---|
| Holdings | תרשים אחזקות; רשימת חברות מוחזקות |
| Financials | דוח רווח והפסד, תזרים, צבר הזמנות |
| Litigation | הליכים משפטיים (points to a note, often 28ג); תביעות |
| Environment, noise | סיכונים סביבתיים ודרכי ניהולם |
| Safety | הוראות בטיחות; רשיונות (סיווג קבלני) |
| Going concern | עסק חי; הפניית תשומת לב |

Every figure: currency, unit (אלפי/מיליוני ש"ח), as-of date, page, URL, and filed / company-stated / press.
No estimates: write "not disclosed". A project missing from a parent's report usually means below its
materiality line. Save the PDF's sha256. Not investment advice.
