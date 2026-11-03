"""Add public Wikidata profiles to the Forbes company snapshot by exact English label.

Wikidata is supplemental context, not an authoritative source of financials.
This script keeps provenance and captures only returned, non-empty facts.
"""
from __future__ import annotations

import csv
import gzip
import json
import time
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data" / "raw" / "Forbes_2000_Companies_2025.csv"
OUTPUT = ROOT / "data" / "wikidata_company_profiles.json.gz"
ENDPOINT = "https://query.wikidata.org/sparql"
USER_AGENT = "VentureInsight/1.0 (https://github.com/ArshSharma21/venture-insight)"
BATCH_SIZE = 100


def value(binding: dict, key: str) -> str:
    return binding.get(key, {}).get("value", "").strip()


def query(labels: list[str]) -> list[dict]:
    values = " ".join(json.dumps(label, ensure_ascii=False) + "@en" for label in labels)
    sparql = f'''SELECT ?match ?item
      (SAMPLE(?desc) AS ?description) (SAMPLE(?website) AS ?website)
      (SAMPLE(?founded) AS ?founded) (SAMPLE(?hqLabel) AS ?headquarters)
      (SAMPLE(?countryLabel) AS ?country) (SAMPLE(?industryLabel) AS ?industry)
      (SAMPLE(?employees) AS ?employees) (SAMPLE(?revenue) AS ?revenue)
      (SAMPLE(?ticker) AS ?ticker) (SAMPLE(?exchangeLabel) AS ?exchange)
    WHERE {{
      VALUES ?match {{ {values} }}
      ?item rdfs:label ?match . FILTER(LANG(?match) = "en")
      OPTIONAL {{ ?item schema:description ?desc . FILTER(LANG(?desc) = "en") }}
      OPTIONAL {{ ?item wdt:P856 ?website }}
      OPTIONAL {{ ?item wdt:P571 ?founded }}
      OPTIONAL {{ ?item wdt:P159 ?hq }}
      OPTIONAL {{ ?item wdt:P17 ?countryItem }}
      OPTIONAL {{ ?item wdt:P452 ?industryItem }}
      OPTIONAL {{ ?item wdt:P1128 ?employees }}
      OPTIONAL {{ ?item wdt:P2139 ?revenue }}
      OPTIONAL {{ ?item wdt:P249 ?ticker }}
      OPTIONAL {{ ?item wdt:P414 ?exchangeItem }}
      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en" .
        ?hq rdfs:label ?hqLabel . ?countryItem rdfs:label ?countryLabel .
        ?industryItem rdfs:label ?industryLabel . ?exchangeItem rdfs:label ?exchangeLabel . }}
    }} GROUP BY ?match ?item'''
    url = ENDPOINT + "?" + urllib.parse.urlencode({"query": sparql, "format": "json"})
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/sparql-results+json"})
    with urllib.request.urlopen(request, timeout=90) as response:
        payload = json.load(response)
    result = []
    for row in payload["results"]["bindings"]:
        item_url = value(row, "item")
        result.append({
            "companyLabel": value(row, "match"), "wikidataId": item_url.rsplit("/", 1)[-1],
            "description": value(row, "description"), "website": value(row, "website"),
            "founded": value(row, "founded")[:10], "headquarters": value(row, "headquarters"),
            "country": value(row, "country"), "industry": value(row, "industry"),
            "employees": value(row, "employees"), "revenue": value(row, "revenue"),
            "ticker": value(row, "ticker"), "exchange": value(row, "exchange"),
            "matchMethod": "exact English label; verify identity before relying on this profile",
            "source": "Wikidata CC0", "sourceUrl": "https://www.wikidata.org/wiki/" + item_url.rsplit("/", 1)[-1],
        })
    return result


def main() -> None:
    with INPUT.open(encoding="utf-8-sig", newline="") as source:
        companies = list(csv.DictReader(source, delimiter=";"))
    labels = list(dict.fromkeys(row["Company"].strip() for row in companies if row.get("Company", "").strip()))
    profiles: list[dict] = []
    for start in range(0, len(labels), BATCH_SIZE):
        profiles.extend(query(labels[start:start + BATCH_SIZE]))
        if start + BATCH_SIZE < len(labels):
            time.sleep(1.2)
    # Keep the strongest exact-label candidate per source company; retain source URL for auditing.
    by_label: dict[str, list[dict]] = {}
    for profile in profiles:
        by_label.setdefault(profile["companyLabel"], []).append(profile)
    chosen = []
    for label, candidates in by_label.items():
        candidates.sort(key=lambda p: sum(bool(p[k]) for k in ("description", "website", "founded", "headquarters", "industry", "employees", "ticker")), reverse=True)
        chosen.append(candidates[0])
    payload = json.dumps({
        "source": "Wikidata Query Service", "license": "CC0", "retrieved": date.today().isoformat(),
        "matchedLabels": len(chosen), "candidateRecords": len(profiles),
        "identityWarning": "Exact labels can be ambiguous; treat entries as candidate matches and verify before use.",
        "profiles": chosen,
    }, ensure_ascii=False, separators=(",", ":")) + "\n"
    with OUTPUT.open("wb") as raw, gzip.GzipFile(fileobj=raw, mode="wb", mtime=0) as compressed:
        compressed.write(payload.encode("utf-8"))
    print(f"Wrote {len(chosen)} exact-label profile candidates for {len(labels)} companies to {OUTPUT}")


if __name__ == "__main__":
    main()
