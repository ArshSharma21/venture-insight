"""Local Venture Insight dashboard and data API."""
from __future__ import annotations

import csv
import gzip
import json
import math
import re
from collections import Counter, defaultdict
from datetime import datetime
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

try:
    from ml.pipeline import load_bundle, load_metrics, recommend as content_recommend
except ImportError:  # The dashboard still runs before optional ML dependencies are installed.
    load_bundle = lambda: None
    load_metrics = lambda: {"status": "not_trained", "message": "Install requirements and train the classifier to enable ML."}
    content_recommend = None

ROOT = Path(__file__).resolve().parent
RAW = ROOT / "data" / "raw"
WEB = ROOT / "web"
WIKIDATA_PATH = ROOT / "data" / "wikidata_company_profiles.json.gz"
WIKIDATA_FINANCIALS_PATH = ROOT / "data" / "wikidata_financial_facts.json.gz"
GLOBAL_STARTUP_PATH = RAW / "global_startup_funding_sample.csv"
STOP = {"the", "and", "for", "with", "from", "that", "this", "into", "your", "our", "are", "was", "you", "can", "all", "how", "what", "who", "its", "their", "about", "business", "company", "companies", "startup", "startups", "idea", "ideas", "market", "platform", "app", "service", "services"}


def tokens(value: str) -> list[str]:
    return [t for t in re.findall(r"[a-z0-9]+", (value or "").lower()) if len(t) > 1 and t not in STOP]


def number(value: str | None) -> float | None:
    if not value:
        return None
    value = value.strip().replace(",", "").replace("$", "")
    if value.lower() in {"", "n/a", "na", "-", "undisclosed", "unknown"}:
        return None
    try:
        parsed = float(value)
        return parsed if math.isfinite(parsed) else None
    except ValueError:
        return None


def clean_text(value: str | None, fallback: str = "") -> str:
    value = (value or "").strip()
    return fallback if value.lower() in {"nan", "none", "null", "n/a", "na", "-"} else value


def read_csv(path: Path, delimiter: str | None = None) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as file:
        if delimiter is None:
            delimiter = ";" if path.name.startswith("Forbes") else ","
        return list(csv.DictReader(file, delimiter=delimiter))


companies: list[dict] = []
funding: list[dict] = []
for row in read_csv(RAW / "Forbes_2000_Companies_2025.csv"):
    sales, profit = number(row.get("Sales ($B)")), number(row.get("Profit ($B)"))
    companies.append({
        "rank": int(number(row.get("Rank")) or 0), "name": row.get("Company", "").strip(),
        "location": row.get("Headquarters", "").strip(), "industry": row.get("Industry", "Unspecified").strip() or "Unspecified",
        "sales": sales, "profit": profit, "assets": number(row.get("Assets ($B)")),
        "marketValue": number(row.get("Market Value ($B)")),
        "profitMargin": round(profit / sales * 100, 1) if profit is not None and sales else None,
        "source": "Forbes Global 2000 / Kaggle 2025", "period": "Latest 12 months available as of 25 Apr 2025", "currency": "USD billions",
    })

for row in read_csv(RAW / "startup_funding.csv"):
    amount_raw = (row.get("Amount in USD") or "").strip()
    amount = number(amount_raw)
    date_text = (row.get("Date dd/mm/yyyy") or "").strip()
    try:
        date_iso = datetime.strptime(date_text, "%d/%m/%Y").date().isoformat()
    except ValueError:
        date_iso = None
    funding.append({
        "name": clean_text(row.get("Startup Name"), "Unnamed startup"), "industry": clean_text(row.get("Industry Vertical"), "Not specified"),
        "subIndustry": clean_text(row.get("SubVertical")), "location": clean_text(row.get("City  Location")),
        "date": date_iso, "investors": clean_text(row.get("Investors Name"), "Not disclosed"),
        "round": clean_text(row.get("InvestmentnType"), "Not specified"), "amount": amount,
        "remarks": clean_text(row.get("Remarks")), "source": "Indian Startup Funding / Kaggle",
    })

global_startup_funding: list[dict] = []
if GLOBAL_STARTUP_PATH.exists():
    for row in read_csv(GLOBAL_STARTUP_PATH):
        status = clean_text(row.get("amount_status")).lower()
        try:
            date_iso = datetime.strptime(clean_text(row.get("announced_date")), "%Y-%m-%d").date().isoformat()
        except ValueError:
            date_iso = None
        global_startup_funding.append({
            "roundId": clean_text(row.get("round_id")), "name": clean_text(row.get("company_name"), "Unnamed startup"),
            "domain": clean_text(row.get("company_domain")), "country": clean_text(row.get("country")),
            "city": clean_text(row.get("city")), "industry": clean_text(row.get("sector"), "Not specified"),
            "foundedYear": int(number(row.get("founded_year")) or 0) or None,
            "date": date_iso, "round": clean_text(row.get("stage"), "Not specified"),
            # Surface an amount only when the source explicitly marks its check as verified.
            "amount": number(row.get("amount_usd")) if status == "verified" else None,
            "amountStatus": status or "not specified", "leadInvestor": clean_text(row.get("lead_investor")),
            "investors": clean_text(row.get("lead_investor"), "Not disclosed"),
            "investorCount": int(number(row.get("investor_count")) or 0),
            "newsExcerpt": clean_text(row.get("news_excerpt")), "newsSource": clean_text(row.get("news_source")),
            "newsUrl": clean_text(row.get("news_url")),
            "profileUrl": clean_text(row.get("fliar_profile_url")),
            "location": ", ".join(v for v in (clean_text(row.get("city")), clean_text(row.get("country"))) if v),
            "source": "Fliar Radar / Global Startup Funding sample (CC BY-NC 4.0)",
        })


def normalized_key(value: str) -> str:
    return "".join(re.findall(r"[a-z0-9]+", (value or "").casefold()))


def global_startup_profiles() -> list[dict]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for row in global_startup_funding:
        # The source profile path is the best available entity key; domain/name are fallbacks.
        profile_key = urlparse(row["profileUrl"]).path.rstrip("/").casefold()
        key = profile_key or row["domain"].casefold() or f"{normalized_key(row['name'])}:{row['country'].casefold()}"
        grouped[key].append(row)
    profiles = []
    for entries in grouped.values():
        entries.sort(key=lambda r: r["date"] or "", reverse=True)
        latest = entries[0]
        excerpts = list(dict.fromkeys(r["newsExcerpt"] for r in entries if r["newsExcerpt"]))[:6]
        context = " ".join(excerpts)
        profiles.append({
            "name": latest["name"], "domain": latest["domain"], "industry": latest["industry"],
            "location": ", ".join(v for v in (latest["city"], latest["country"]) if v) or "Location not recorded",
            "country": latest["country"], "foundedYear": latest["foundedYear"], "round": latest["round"],
            "date": latest["date"], "amount": latest["amount"], "amountStatus": latest["amountStatus"],
            "leadInvestor": latest["leadInvestor"], "roundCount": len(entries),
            "contextSnippet": latest["newsExcerpt"], "recommendationText": " ".join((latest["name"], latest["industry"], context)),
            "modelText": " ".join((latest["name"], context)),
            "profileUrl": latest["profileUrl"], "sourceUrl": latest["newsUrl"] or latest["profileUrl"], "newsSource": latest["newsSource"],
            "recordType": "global startup", "source": latest["source"],
        })
    return profiles


global_startup_companies = global_startup_profiles()

wikidata_profiles: dict[str, dict] = {}
if WIKIDATA_PATH.exists():
    try:
        with gzip.open(WIKIDATA_PATH, "rt", encoding="utf-8") as source:
            payload = json.load(source)
        wikidata_profiles = {p["companyLabel"].casefold(): p for p in payload.get("profiles", [])}
    except (OSError, json.JSONDecodeError, KeyError):
        wikidata_profiles = {}
wikidata_financials: dict[str, list[dict]] = defaultdict(list)
if WIKIDATA_FINANCIALS_PATH.exists():
    try:
        with gzip.open(WIKIDATA_FINANCIALS_PATH, "rt", encoding="utf-8") as source:
            payload = json.load(source)
        for fact in payload.get("facts", []):
            wikidata_financials[fact["wikidataId"]].append(fact)
    except (OSError, json.JSONDecodeError, KeyError):
        wikidata_financials = defaultdict(list)


def classify_idea(text: str) -> list[dict]:
    """Transparent keyword baseline; scores are rule signals, not probabilities."""
    rules = {
        "Financial Technology": ["payment", "bank", "credit", "loan", "finance", "fintech", "insurance", "wallet", "invest"],
        "Healthcare": ["health", "medical", "doctor", "clinic", "patient", "diagnosis", "medicine", "pharma"],
        "Education Technology": ["learn", "education", "student", "school", "course", "tutor", "teaching"],
        "Retail and E-commerce": ["retail", "shop", "commerce", "grocery", "marketplace", "shopping", "delivery", "parlour", "parlor", "gelato"],
        "Food and Beverage": ["food", "restaurant", "farm", "agriculture", "crop", "grocery", "supply chain", "ice cream", "gelato", "dessert", "parlour", "parlor", "cafe", "bakery", "beverage"],
        "Climate and Energy": ["climate", "energy", "solar", "renewable", "electric", "battery", "carbon", "recycle"],
        "Enterprise Software and AI": ["software", "saas", "artificial intelligence", " ai ", "automation", "data", "cloud", "developer"],
        "Transport and Mobility": ["transport", "mobility", "vehicle", "automotive", "travel", "logistics", "ride"],
        "Media and Entertainment": ["media", "content", "music", "video", "gaming", "entertainment", "creator"],
        "Real Estate and Construction": ["real estate", "property", "housing", "construction", "building"],
    }
    lowered = f" {text.lower()} "
    scores = []
    for label, terms in rules.items():
        score = sum(1 for term in terms if (f" {term.strip()} " in lowered if " " in term else term in tokens(text)))
        if score:
            scores.append((label, score))
    if not scores:
        return []
    total = sum(score for _, score in scores)
    return [{"label": label, "signal": round(score / total, 2)} for label, score in sorted(scores, key=lambda item: (-item[1], item[0]))[:3]]


def idea_records() -> list[dict]:
    """Build established public-company records for the separate comparator results."""
    records = []
    for item in companies:
        record = dict(item)
        record["recordType"] = "public company"
        record["companyProfile"] = wikidata_profiles.get(item["name"].casefold())
        if record["companyProfile"]:
            record["historicalFacts"] = wikidata_financials.get(record["companyProfile"]["wikidataId"], [])
        record["recommendationText"] = " ".join((record["name"], record["industry"], record["location"], (record["companyProfile"] or {}).get("description", "")))
        records.append(record)
    return records


def india_startup_profiles() -> list[dict]:
    """Collapse repeated Indian funding events to one startup recommendation."""
    grouped: dict[str, list[dict]] = defaultdict(list)
    for event in funding:
        grouped[normalized_key(event["name"])].append(event)
    global_india_names = {normalized_key(row["name"]) for row in global_startup_companies if row["country"].casefold() == "india"}
    result = []
    for key, events in grouped.items():
        if not key or key in global_india_names:
            continue
        events.sort(key=lambda r: r["date"] or "", reverse=True)
        latest = events[0]
        descriptions = list(dict.fromkeys(r["subIndustry"] + " " + r["remarks"] for r in events if r["subIndustry"] or r["remarks"]))[:5]
        text = " ".join((latest["name"], latest["industry"], " ".join(descriptions)))
        result.append({
            "name": latest["name"], "industry": latest["industry"], "subIndustry": latest["subIndustry"],
            "location": latest["location"] or "India", "country": "India", "date": latest["date"],
            "round": latest["round"], "amount": latest["amount"], "leadInvestor": latest["investors"],
            "roundCount": len(events), "contextSnippet": latest["subIndustry"] or latest["remarks"],
            "recommendationText": text, "recordType": "India startup", "source": "Indian Startup Funding / Kaggle (2015–2020)",
            "sourceUrl": "https://www.kaggle.com/datasets/sudalairajkumar/indian-startup-funding",
        })
    return result


india_startup_companies = india_startup_profiles()
startup_recommendation_records = global_startup_companies + india_startup_companies
_PUBLIC_RETRIEVAL_RECORDS = None


def public_company_recommendations(query: str, limit: int = 8) -> list[dict]:
    global _PUBLIC_RETRIEVAL_RECORDS
    if _PUBLIC_RETRIEVAL_RECORDS is None:
        _PUBLIC_RETRIEVAL_RECORDS = idea_records()
    if content_recommend:
        return content_recommend(query, _PUBLIC_RETRIEVAL_RECORDS, limit)
    return _legacy_idea_matches(query, limit)


def startup_recommendations(query: str, limit: int = 12) -> list[dict]:
    if content_recommend:
        return content_recommend(query, startup_recommendation_records, limit)
    return _legacy_idea_matches(query, limit)


def _legacy_idea_matches(query: str, limit: int = 12) -> list[dict]:
    q = set(tokens(query))
    if not q:
        return []
    predictions = classify_idea(query)
    labels = {item["label"] for item in predictions}
    sector_terms = {
        "Food and Beverage": {"food", "drink", "tobacco", "restaurants", "leisure", "retail", "wholesale"},
        "Retail and E-commerce": {"retail", "wholesale", "food", "markets"},
        "Financial Technology": {"banking", "insurance", "financials"},
        "Healthcare": {"health", "care", "biotechnology", "pharmaceuticals"},
        "Enterprise Software and AI": {"software", "technology", "semiconductors"},
        "Transport and Mobility": {"transportation", "automotive"},
    }
    scored = []
    for item in funding:
        text = " ".join((item["name"], item["industry"], item["subIndustry"], item["remarks"], item["round"]))
        words = set(tokens(text))
        overlap = len(q & words)
        sector_text = set(tokens(item["industry"] + " " + item["subIndustry"]))
        sector_match = any(bool(sector_terms.get(label, set()) & sector_text) for label in labels)
        score = overlap / max(1, len(q)) + (0.25 if sector_match else 0)
        if score > 0:
            scored.append((score, item, sorted(q & words), sector_match, overlap / max(1, len(q))))
    for item in companies:
        profile = wikidata_profiles.get(item["name"].casefold(), {})
        profile_text = " ".join((profile.get("description", ""), profile.get("industry", "")))
        words = set(tokens(item["name"] + " " + item["industry"] + " " + item["location"] + " " + profile_text))
        overlap = len(q & words)
        sector_text = set(tokens(item["industry"]))
        sector_match = any(bool(sector_terms.get(label, set()) & sector_text) for label in labels)
        score = overlap / max(1, len(q)) + (0.25 if sector_match else 0)
        if score > 0:
            scored.append((score, item, sorted(q & words), sector_match, overlap / max(1, len(q))))
    scored.sort(key=lambda hit: (-hit[0], hit[1]["name"]))
    result = []
    seen_startups = set()
    for _rank_score, item, terms, sector_match, text_overlap in scored:
        if len(result) >= limit:
            break
        if "amount" in item:
            key = "".join(tokens(item["name"]))
            if key and key in seen_startups:
                continue
            if key:
                seen_startups.add(key)
        record = dict(item)
        record["matchScore"] = round(text_overlap, 2)
        record["matchedTerms"] = terms
        record["sectorMatch"] = sector_match
        record["recordType"] = "startup funding" if "amount" in item else "public company"
        if record["recordType"] == "public company":
            record["companyProfile"] = wikidata_profiles.get(record["name"].casefold())
            if record["companyProfile"]:
                record["historicalFacts"] = wikidata_financials.get(record["companyProfile"]["wikidataId"], [])
        result.append(record)
    return result


CLASSIFIER_BUNDLE = load_bundle()


def ml_classify(text: str) -> list[dict]:
    if not text.strip() or not CLASSIFIER_BUNDLE:
        return []
    model = CLASSIFIER_BUNDLE["pipeline"]
    classes = model.classes_
    if hasattr(model, "predict_proba"):
        values = model.predict_proba([text])[0]
    else:
        values = model.decision_function([text])[0]
    return [{"label": str(classes[i]), "score": round(float(values[i]), 4), "scoreType": "model score"} for i in values.argsort()[::-1][:3]]


def overview() -> dict:
    industries = Counter(c["industry"] for c in companies)
    countries = Counter(c["location"].split(",")[-1].strip() for c in companies)
    sector_finance = defaultdict(lambda: {"companies": 0, "sales": 0.0, "profit": 0.0, "marketValue": 0.0})
    for c in companies:
        s = sector_finance[c["industry"]]
        s["companies"] += 1
        for key in ("sales", "profit", "marketValue"):
            s[key] += c[key] or 0
    top_sectors = sorted(({"industry": key, **value} for key, value in sector_finance.items()), key=lambda x: x["sales"], reverse=True)[:10]
    startup_sectors = Counter((f["industry"] or "Unspecified") for f in funding)
    india_records = sum("india" in c["location"].lower() for c in companies)
    known_amounts = [r["amount"] for r in funding if r["amount"] is not None]
    return {
        "companyCount": len(companies), "startupRounds": len(funding) + len(global_startup_funding),
        "startupProfiles": len(startup_recommendation_records), "globalFundingRounds": len(global_startup_funding),
        "globalStartupProfiles": len(global_startup_companies), "globalCountries": len(countries),
        "industries": len(industries), "indiaPublicCompanies": india_records,
        "totalSales": round(sum(c["sales"] or 0 for c in companies), 1),
        "totalProfit": round(sum(c["profit"] or 0 for c in companies), 1),
        "averageFunding": round(sum(known_amounts) / len(known_amounts), 0) if known_amounts else None,
        "fundingWithAmount": len(known_amounts),
        "topSectors": top_sectors, "startupSectors": [{"industry": k, "count": v} for k, v in startup_sectors.most_common(12)],
        "topCompanies": sorted(companies, key=lambda c: c["sales"] or 0, reverse=True)[:8],
        "period": "Forbes snapshot: latest 12 months available as of 25 Apr 2025",
    }


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(WEB), **kwargs)

    def do_GET(self):
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)
        if parsed.path == "/api/model":
            return self.send_json({"metrics": load_metrics(), "activeModel": CLASSIFIER_BUNDLE.get("name") if CLASSIFIER_BUNDLE else None, "mlAvailable": bool(CLASSIFIER_BUNDLE)})
        if parsed.path == "/api/overview":
            return self.send_json(overview())
        if parsed.path == "/api/companies":
            term = params.get("q", [""])[0].lower().strip()
            industry = params.get("industry", [""])[0]
            country = params.get("country", [""])[0]
            rows = [r for r in companies if (not term or term in (r["name"] + " " + r["industry"] + " " + r["location"]).lower()) and (not industry or r["industry"] == industry) and (not country or country in r["location"])]
            page = max(0, int(params.get("page", ["0"])[0] or 0))
            page_size = 50
            return self.send_json({"rows": rows[page * page_size:(page + 1) * page_size], "total": len(rows), "page": page, "pageSize": page_size, "industries": sorted({r["industry"] for r in companies}), "countries": sorted({r["location"].split(",")[-1].strip() for r in companies})})
        if parsed.path == "/api/company":
            name = params.get("name", [""])[0].casefold()
            found = next((r for r in companies if r["name"].casefold() == name), None)
            if found:
                found = dict(found)
                found["companyProfile"] = wikidata_profiles.get(found["name"].casefold())
                if found["companyProfile"]:
                    found["historicalFacts"] = wikidata_financials.get(found["companyProfile"]["wikidataId"], [])
            return self.send_json(found or {"error": "Company not found in this source."}, 200 if found else 404)
        if parsed.path == "/api/idea":
            query = params.get("q", [""])[0][:240]
            method = params.get("method", ["ml"])[0]
            use_ml = method != "rules" and bool(CLASSIFIER_BUNDLE)
            classifications = ml_classify(query) if use_ml else classify_idea(query)
            startup_matches = startup_recommendations(query)
            company_matches = public_company_recommendations(query)
            return self.send_json({
                "query": query, "method": "ml" if use_ml else "rules",
                "classifierName": CLASSIFIER_BUNDLE["name"] if use_ml else "Keyword rules (baseline)",
                "classifications": classifications, "ruleBaseline": classify_idea(query),
                "mlComparison": ml_classify(query), "startupMatches": startup_matches,
                "companyMatches": company_matches,
                "catalog": {"startupProfiles": len(startup_recommendation_records), "globalStartupProfiles": len(global_startup_companies), "globalFundingRounds": len(global_startup_funding), "indiaHistoricalRounds": len(funding), "countries": len({r['country'] for r in global_startup_companies if r['country']})},
                "recommendationMethod": "TF-IDF cosine similarity" if content_recommend else "Keyword overlap fallback",
                "modelNote": ("ML sector classifier trained on source taxonomy weak labels; model scores are not commercial-success probabilities." if use_ml else "Keyword rules baseline. Install dependencies and train to enable the ML classifier."),
            })
        if parsed.path == "/api/funding":
            term = params.get("q", [""])[0].lower()
            sector = params.get("industry", [""])[0]
            scope = params.get("scope", ["all"])[0]
            india_rows = [{**r, "market": "India", "currency": "USD", "sourceUrl": "https://www.kaggle.com/datasets/sudalairajkumar/indian-startup-funding"} for r in funding]
            global_rows = [{**r, "market": "Global", "currency": "USD", "remarks": r["newsExcerpt"], "sourceUrl": r["newsUrl"] or r["profileUrl"]} for r in global_startup_funding]
            rows = (india_rows if scope == "india" else global_rows if scope == "global" else india_rows + global_rows)
            rows = [r for r in rows if (not term or term in " ".join(str(v) for v in r.values()).lower()) and (not sector or sector == r["industry"])]
            rows.sort(key=lambda r: r["date"] or "", reverse=True)
            page = max(0, int(params.get("page", ["0"])[0] or 0))
            page_size = 50
            return self.send_json({"rows": rows[page * page_size:(page + 1) * page_size], "total": len(rows), "page": page, "pageSize": page_size, "scope": scope, "industries": sorted({r["industry"] for r in rows if r["industry"]}), "indiaRounds": len(india_rows), "globalRounds": len(global_rows), "withAmount": sum(r["amount"] is not None for r in rows)})
        return super().do_GET()

    def send_json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False, allow_nan=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        print("[%s] %s" % (self.log_date_time_string(), fmt % args))


if __name__ == "__main__":
    server = ThreadingHTTPServer(("127.0.0.1", 8000), Handler)
    print("Venture Insight running at http://127.0.0.1:8000")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping Venture Insight")
        server.server_close()
