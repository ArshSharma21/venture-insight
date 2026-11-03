"""Harvest dated Wikidata financial statement claims for matched company candidates."""
from __future__ import annotations

import json
import gzip
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROFILE_FILE = ROOT / "data" / "wikidata_company_profiles.json.gz"
OUTPUT = ROOT / "data" / "wikidata_financial_facts.json.gz"
ENDPOINT = "https://query.wikidata.org/sparql"
USER_AGENT = "VentureInsight/1.0 (https://github.com/ArshSharma21/venture-insight)"
BATCH_SIZE = 200


def fetch(qids: list[str]) -> list[dict]:
    entities = " ".join("wd:" + qid for qid in qids)
    sparql = f'''SELECT ?item ?companyLabel ?metric ?amount ?unitLabel ?period WHERE {{
      VALUES ?item {{ {entities} }}
      VALUES (?statementPredicate ?valuePredicate ?metric) {{
        (p:P2139 psv:P2139 "Revenue")
        (p:P2295 psv:P2295 "Net profit")
        (p:P2403 psv:P2403 "Total assets")
        (p:P2404 psv:P2404 "Total liabilities")
      }}
      ?item rdfs:label ?companyLabel; ?statementPredicate ?statement .
      FILTER(LANG(?companyLabel) = "en")
      ?statement ?valuePredicate ?quantity; pq:P585 ?period .
      ?quantity wikibase:quantityAmount ?amount; wikibase:quantityUnit ?unit .
      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en" . ?unit rdfs:label ?unitLabel }}
    }}'''
    url = ENDPOINT + "?" + urllib.parse.urlencode({"query": sparql, "format": "json"})
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/sparql-results+json"})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(request, timeout=90) as response:
                data = json.load(response)
            break
        except urllib.error.HTTPError as error:
            if error.code != 429 or attempt == 3:
                raise
            delay = int(error.headers.get("Retry-After", "30"))
            print(f"Wikidata asked us to slow down; waiting {delay}s before retry", flush=True)
            time.sleep(max(10, delay))
    output = []
    for row in data["results"]["bindings"]:
        item_url = row["item"]["value"]
        output.append({
            "wikidataId": item_url.rsplit("/", 1)[-1],
            "companyLabel": row["companyLabel"]["value"],
            "metric": row["metric"]["value"],
            "amount": row["amount"]["value"],
            "unit": row["unitLabel"]["value"],
            "period": row["period"]["value"][:10],
            "sourceUrl": "https://www.wikidata.org/wiki/" + item_url.rsplit("/", 1)[-1],
        })
    return output


def main() -> None:
    with gzip.open(PROFILE_FILE, "rt", encoding="utf-8") as source:
        profile_data = json.load(source)
    qids = list(dict.fromkeys(p["wikidataId"] for p in profile_data["profiles"] if p.get("wikidataId", "").startswith("Q")))
    facts: list[dict] = []
    for start in range(0, len(qids), BATCH_SIZE):
        facts.extend(fetch(qids[start:start + BATCH_SIZE]))
        payload = json.dumps({
            "source": "Wikidata Query Service", "license": "CC0", "retrieved": date.today().isoformat(),
            "inputProfiles": len(qids), "processedProfiles": min(start + BATCH_SIZE, len(qids)), "facts": facts,
            "limitations": "Claims are community-maintained and may be incomplete or conflicting. Values retain source currency units and reported dates; compare only compatible units and periods.",
        }, ensure_ascii=False, separators=(",", ":")) + "\n"
        with OUTPUT.open("wb") as raw, gzip.GzipFile(fileobj=raw, mode="wb", mtime=0) as compressed:
            compressed.write(payload.encode("utf-8"))
        print(f"Collected facts for {min(start + BATCH_SIZE, len(qids))} / {len(qids)} profile candidates", flush=True)
        if start + BATCH_SIZE < len(qids):
            time.sleep(5)
    print(f"Wrote {len(facts)} dated financial claims for {len(qids)} matched profiles to {OUTPUT}")


if __name__ == "__main__":
    main()
