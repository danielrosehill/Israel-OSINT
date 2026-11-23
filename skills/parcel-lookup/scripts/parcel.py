#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Israel location -> cadastral block/parcel (gush/helka), and back.

  parcel.py "כיכר ספרא 1, ירושלים"        # address (geocoded via OpenStreetMap Nominatim)
  parcel.py --latlon 32.0753,34.7749        # point
  parcel.py --gush 30074 --helka 447        # reverse: centroid, area, status
  options: --radius 30 (metres, neighbours), --source national|jerusalem|auto

Sources (public ArcGIS REST, no key):
  national  : "חלקות קדסטר בישראל" (copy of the Survey of Israel cadastre, ~1.1M parcels,
              fields GUSH_NUM/PARCEL/STATUS_TEX/LOCALITY_N/LEGAL_AREA). Missing areas where
              land settlement is incomplete, e.g. central Jerusalem.
  jerusalem : Jerusalem Municipality "helkot1225" (GUSH_NO/PARCEL_NO), city-wide.
Output: JSON on stdout. Geocoded points are approximate - read `nearby`, not just `at_point`.
"""
import argparse
import json
import sys
import urllib.parse
import urllib.request

UA = "israel-osint-parcel-lookup/0.1 (+https://github.com/danielrosehill/Israel-OSINT)"
LAYERS = {
    "national": {
        "url": "https://services8.arcgis.com/JcXY3lLZni6BK4El/arcgis/rest/services/%D7%97%D7%9C%D7%A7%D7%95%D7%AA/FeatureServer/0",
        "gush": "GUSH_NUM", "helka": "PARCEL",
        "extra": ["STATUS_TEX", "LOCALITY_N", "LEGAL_AREA", "GUSH_SUFFI"],
        "note": "copy of the Survey of Israel cadastre (publisher on ArcGIS Online: sysdata); not the official MAPI service",
    },
    "jerusalem": {
        "url": "https://services3.arcgis.com/jeqc1A7OfE9m4EPO/arcgis/rest/services/helkot1225/FeatureServer/0",
        "gush": "GUSH_NO", "helka": "PARCEL_NO",
        "extra": [],
        "note": "Jerusalem Municipality parcel layer",
        # rough city envelope (lon/lat) - only consulted for points inside it
        "bbox": (35.07, 31.68, 35.30, 31.90),
    },
}


def get(url, params):
    q = url + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(q, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def geocode(address):
    res = get("https://nominatim.openstreetmap.org/search",
              {"q": address, "format": "json", "limit": 1, "countrycodes": "il", "addressdetails": 0})
    if not res:
        raise SystemExit(json.dumps({"error": f"address not found: {address}"}, ensure_ascii=False))
    r = res[0]
    return float(r["lat"]), float(r["lon"]), r.get("display_name"), r.get("type")


def norm(layer, attrs, name):
    L = LAYERS[name]
    out = {"gush": str(attrs.get(L["gush"])), "helka": str(attrs.get(L["helka"])), "source": name}
    for k in L["extra"]:
        if attrs.get(k) not in (None, ""):
            out[k.lower()] = attrs[k]
    return out


def query_point(name, lat, lon, radius):
    L = LAYERS[name]
    fields = ",".join([L["gush"], L["helka"], *L["extra"]])
    base = {"geometry": f"{lon},{lat}", "geometryType": "esriGeometryPoint", "inSR": 4326,
            "spatialRel": "esriSpatialRelIntersects", "outFields": fields,
            "returnGeometry": "false", "f": "json"}
    at = get(L["url"] + "/query", base).get("features", [])
    near = []
    if radius:
        near = get(L["url"] + "/query", {**base, "distance": radius, "units": "esriSRUnit_Meter"}).get("features", [])
    at_n = [norm(L, f["attributes"], name) for f in at]
    keys = {(p["gush"], p["helka"]) for p in at_n}
    near_n = [p for p in (norm(L, f["attributes"], name) for f in near) if (p["gush"], p["helka"]) not in keys]
    return at_n, near_n


def in_bbox(name, lat, lon):
    b = LAYERS[name].get("bbox")
    return b is None or (b[0] <= lon <= b[2] and b[1] <= lat <= b[3])


def lookup_point(lat, lon, radius, source):
    order = ["national", "jerusalem"] if source == "auto" else [source]
    tried = []
    for name in order:
        if source == "auto" and not in_bbox(name, lat, lon):
            continue
        at, near = query_point(name, lat, lon, radius)
        tried.append(name)
        if at or near:
            return {"source": name, "source_note": LAYERS[name]["note"], "at_point": at,
                    "nearby": near, "radius_m": radius, "tried": tried}
    return {"source": None, "at_point": [], "nearby": [], "radius_m": radius, "tried": tried,
            "hint": "no parcel layer covers this point; try a larger --radius or the municipality's own GIS"}


def reverse(gush, helka, source):
    order = ["national", "jerusalem"] if source == "auto" else [source]
    for name in order:
        L = LAYERS[name]
        gq = f"{L['gush']}={int(gush)}" if name == "national" else f"{L['gush']}='{gush}'"
        hq = f"{L['helka']}={int(helka)}" if name == "national" else f"{L['helka']}='{helka}'"
        d = get(L["url"] + "/query", {"where": f"{gq} AND {hq}", "outFields": ",".join([L["gush"], L["helka"], *L["extra"]]),
                                      "returnGeometry": "true", "returnCentroid": "true", "outSR": 4326, "f": "json"})
        feats = d.get("features", [])
        if not feats:
            continue
        f = feats[0]
        rings = (f.get("geometry") or {}).get("rings") or []
        pts = [p for r in rings for p in r]
        c = f.get("centroid") or ({"x": sum(p[0] for p in pts) / len(pts), "y": sum(p[1] for p in pts) / len(pts)} if pts else None)
        out = norm(L, f["attributes"], name)
        out.update(source_note=L["note"], parts=len(feats))
        if c:
            out["centroid"] = {"lat": round(c["y"], 6), "lon": round(c["x"], 6)}
        if pts:
            xs, ys = [p[0] for p in pts], [p[1] for p in pts]
            out["bbox"] = [round(min(xs), 6), round(min(ys), 6), round(max(xs), 6), round(max(ys), 6)]
        return out
    return {"error": f"gush {gush} helka {helka} not found in {order}"}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("address", nargs="?")
    ap.add_argument("--latlon")
    ap.add_argument("--gush")
    ap.add_argument("--helka")
    ap.add_argument("--radius", type=float, default=30)
    ap.add_argument("--source", choices=["auto", "national", "jerusalem"], default="auto")
    a = ap.parse_args()
    if a.gush and a.helka:
        print(json.dumps(reverse(a.gush, a.helka, a.source), ensure_ascii=False, indent=1))
        return
    if a.latlon:
        lat, lon = (float(x) for x in a.latlon.split(","))
        geo = {"input": a.latlon}
    elif a.address:
        lat, lon, disp, typ = geocode(a.address)
        geo = {"input": a.address, "geocoded": disp, "osm_type": typ}
    else:
        ap.error("give an address, --latlon, or --gush/--helka")
    res = lookup_point(lat, lon, a.radius, a.source)
    print(json.dumps({**geo, "lat": lat, "lon": lon, **res}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    sys.exit(main())
