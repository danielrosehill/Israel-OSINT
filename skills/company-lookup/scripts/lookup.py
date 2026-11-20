#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""Look up Israeli registered entities in the open registrar datasets on data.gov.il.

Usage:
    uv run lookup.py company 514744887          # exact, by company number
    uv run lookup.py company "monday.com"       # free text (Hebrew or English)
    uv run lookup.py amuta 580000016            # amutot (NPO) registry
    uv run lookup.py amuta "name words"
    uv run lookup.py deletion 514398262         # companies flagged for strike-off
    uv run lookup.py pledges 510627409          # registered charges (shiabud) events

Add --json for raw records. Datasets are periodic snapshots, not the live register.
"""
import argparse, json, sys, urllib.error, urllib.parse, urllib.request

BASE = "https://data.gov.il/api/3/action/datastore_search"
RES = {
    "company": ("f004176c-b85f-4542-8901-7b3176f9a054", "מספר חברה"),
    "amuta": ("be5b7935-3922-45d4-9638-08871b17ec95", "מספר עמותה"),
    "deletion": ("0fd312bb-68c9-4647-b186-60c3e7b4f6f7", "מספר התאגיד"),
    "pledges": ("28780ab5-3ef1-44c7-8377-da82c0aa6781", "מספר תאגיד"),
}


def get(params):
    url = BASE + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "israel-osint-plugin/0.1"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            body = r.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        sys.exit(f"HTTP {e.code}: the resource id may have rotated (re-resolve with package_show) "
                 "or the request hit the portal's generic error page.")
    except urllib.error.URLError as e:
        sys.exit(f"Connection error: {e.reason}")
    try:
        d = json.loads(body)
    except json.JSONDecodeError:
        sys.exit("Non-JSON response (HTML error page or AccessDenied XML): not data. Check resource id.")
    if not d.get("success"):
        sys.exit(f"API error: {d.get('error')}")
    return d["result"]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("kind", choices=RES)
    ap.add_argument("query", help="9-digit number or free text")
    ap.add_argument("--limit", type=int, default=5)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    rid, numfield = RES[a.kind]
    q = a.query.strip().replace("-", "")
    if q.isdigit() and len(q) >= 8:
        params = {"resource_id": rid, "filters": json.dumps({numfield: int(q)}), "limit": a.limit}
    else:
        params = {"resource_id": rid, "q": a.query, "limit": a.limit}
    res = get(params)
    recs = [{k: v for k, v in r.items() if k != "_full_text"} for r in res["records"]]
    if a.json:
        print(json.dumps({"total": res["total"], "records": recs}, ensure_ascii=False, indent=2))
        return
    print(f"{res['total']} match(es); showing {len(recs)}. Snapshot data: confirm on the official register before relying on it.\n")
    for r in recs:
        for k, v in r.items():
            if v not in ("", None):
                print(f"  {k}: {v}")
        print()
    if res["total"] == 0:
        print("No match. Try the Hebrew name, the company number, or another registry (partnerships, "
              "cooperatives and some entities are not in this dataset). Names use ~ for quotes: בע~מ.")


if __name__ == "__main__":
    main()
