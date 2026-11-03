"""Weak-label sector classification and content-based recommendation.

Source sectors are mapped into broad project sectors and used as weak labels.
This makes the exercise reproducible, but the scores measure agreement with
source taxonomy, not truth about an idea or its commercial prospects.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "models" / "sector_classifier.joblib"
METRICS_PATH = ROOT / "models" / "model_metrics.json"

# Ordered, explicit mapping from source labels into the project's broad classes.
SECTOR_TERMS = {
    "Financial Technology": ("financial", "bank", "insurance", "payment", "fintech", "lending", "investment", "venture capital", "accounting", "wealth", "credit"),
    "Healthcare": ("health", "medical", "hospital", "pharma", "biotech", "wellness", "diagnostic", "clinical", "medicine", "care"),
    "Education Technology": ("education", "educational", "edtech", "learning", "school", "university", "training", "tutor"),
    "Retail and E-commerce": ("retail", "ecommerce", "e-commerce", "consumer goods", "shopping", "marketplace", "fashion", "apparel", "wholesale"),
    "Food and Beverage": ("food", "beverage", "restaurant", "agriculture", "agritech", "farm", "dairy", "grocery", "meat", "snack"),
    "Climate and Energy": ("climate", "energy", "renewable", "solar", "cleantech", "clean tech", "environment", "sustainability", "electric power", "recycling"),
    "Enterprise Software and AI": ("software", "technology", "saas", "artificial intelligence", "enterprise", "internet", "cloud", "information technology", "computer", "semiconductor", "data"),
    "Transport and Mobility": ("transport", "automotive", "mobility", "logistics", "shipping", "aviation", "travel", "delivery", "vehicle"),
    "Media and Entertainment": ("media", "entertainment", "gaming", "music", "film", "television", "publishing", "content", "sports"),
    "Real Estate and Construction": ("real estate", "property", "construction", "housing", "building", "infrastructure"),
}


def canonical_sector(value: str) -> str:
    text = re.sub(r"[^a-z0-9]+", " ", (value or "").lower()).strip()
    if not text:
        return "Other / Unclassified"
    hits = [(sum(1 for term in terms if term in text), label) for label, terms in SECTOR_TERMS.items()]
    best = max(hits, default=(0, "Other / Unclassified"))
    return best[1] if best[0] else "Other / Unclassified"


def build_corpus(companies: list[dict], funding: list[dict], profiles: dict[str, dict], global_startups: list[dict] | None = None) -> list[dict]:
    """Build one document per normalized company name; exclude label fields from text.

    Cross-source name deduplication reduces train/test leakage when the same entity
    appears in the public-company snapshot and a startup funding catalog. Exact
    name matching is conservative: aliases and transliterations can still remain.
    """
    rows: list[dict] = []
    seen: set[str] = set()

    def name_key(value: str) -> str:
        return re.sub(r"[^a-z0-9]+", "", (value or "").casefold())

    for company in companies:
        key = name_key(company.get("name", ""))
        if not key or key in seen:
            continue
        seen.add(key)
        profile = profiles.get(company["name"].casefold(), {})
        label = canonical_sector(company.get("industry", ""))
        description = profile.get("description", "")
        text = " ".join(filter(None, (company.get("name"), description, profile.get("industry", ""))))
        if text.strip():
            rows.append({"text": text, "label": label, "name": company["name"], "source": company.get("source", "public company")})
    for startup in funding:
        key = name_key(startup.get("name", ""))
        if not key or key in seen:
            continue
        seen.add(key)
        # Sub-industry and remarks enrich descriptions; the broad vertical supplies the weak label.
        label = canonical_sector(startup.get("industry", ""))
        text = " ".join(filter(None, (startup.get("name"), startup.get("subIndustry"), startup.get("remarks"))))
        if text.strip():
            rows.append({"text": text, "label": label, "name": startup["name"], "source": startup.get("source", "startup funding")})
    for startup in global_startups or []:
        key = name_key(startup.get("name", ""))
        if not key or key in seen:
            continue
        seen.add(key)
        # Use the sector as a weak target only; keep it out of model text to avoid label leakage.
        label = canonical_sector(startup.get("industry", ""))
        text = str(startup.get("modelText") or startup.get("name", ""))
        if text.strip():
            rows.append({"text": text, "label": label, "name": startup["name"], "source": startup.get("source", "global startup funding")})
    return rows


def load_bundle():
    if not MODEL_PATH.exists():
        return None
    try:
        return joblib.load(MODEL_PATH)
    except (OSError, ValueError, EOFError):
        return None


def load_metrics() -> dict:
    if not METRICS_PATH.exists():
        return {"status": "not_trained", "message": "Install requirements and run python3 -m ml.train to build and evaluate models."}
    try:
        return json.loads(METRICS_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {"status": "unavailable", "message": "Model metrics could not be read."}


def recommend(query: str, records: list[dict], limit: int = 12) -> list[dict]:
    """TF-IDF cosine retrieval; this recommends similar records, not investments."""
    docs = []
    for record in records:
        profile = record.get("companyProfile") or {}
        docs.append(str(record.get("recommendationText") or " ".join(str(record.get(k, "") or "") for k in ("name", "industry", "subIndustry", "remarks", "round"))) + " " + str(profile.get("description", "")))
    if not docs or not query.strip():
        return []
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words="english", min_df=1, sublinear_tf=True)
    matrix = vectorizer.fit_transform([query] + docs)
    scores = cosine_similarity(matrix[0:1], matrix[1:]).ravel()
    ranked = scores.argsort()[::-1]
    result = []
    for idx in ranked:
        if scores[idx] <= 0 or len(result) >= limit:
            break
        record = dict(records[int(idx)])
        record["matchScore"] = round(float(scores[idx]), 3)
        record["matchPercent"] = round(float(scores[idx]) * 100, 1)
        record["matchMethod"] = "TF-IDF cosine similarity"
        result.append(record)
    return result
