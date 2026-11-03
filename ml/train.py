"""Train and compare sector models against the project's weak taxonomy labels."""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, f1_score
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import app  # noqa: E402
from ml.pipeline import MODEL_PATH, METRICS_PATH, build_corpus  # noqa: E402


def main() -> None:
    rows = build_corpus(app.companies, app.funding, app.wikidata_profiles)
    counts = Counter(row["label"] for row in rows)
    # Very small categories cannot support a stratified holdout and useful evaluation.
    rows = [row for row in rows if counts[row["label"]] >= 5]
    texts, labels = [r["text"] for r in rows], [r["label"] for r in rows]
    train_x, test_x, train_y, test_y = train_test_split(texts, labels, test_size=0.2, random_state=42, stratify=labels)
    algorithms = {
        "Multinomial Naive Bayes": MultinomialNB(alpha=0.5),
        "Logistic Regression": LogisticRegression(max_iter=1500, class_weight="balanced", random_state=42),
        "Linear SVM": LinearSVC(class_weight="balanced", random_state=42),
    }
    results = []
    best = None
    for name, estimator in algorithms.items():
        pipeline = Pipeline([("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=2, max_features=50000, sublinear_tf=True, stop_words="english")), ("classifier", estimator)])
        pipeline.fit(train_x, train_y)
        pred = pipeline.predict(test_x)
        result = {"name": name, "accuracy": round(float(accuracy_score(test_y, pred)), 4), "macroF1": round(float(f1_score(test_y, pred, average="macro", zero_division=0)), 4), "weightedF1": round(float(f1_score(test_y, pred, average="weighted", zero_division=0)), 4), "perClass": classification_report(test_y, pred, output_dict=True, zero_division=0)}
        result["perClass"] = {k: {metric: round(float(value), 4) for metric, value in v.items() if metric != "support"} | {"support": int(v.get("support", 0))} for k, v in result["perClass"].items() if isinstance(v, dict)}
        results.append(result)
        if best is None or result["macroF1"] > best["macroF1"]:
            best = {**result, "pipeline": pipeline}
    # Comparable keyword baseline: maps its output to the same held-out records.
    baseline_predictions = []
    for text, actual in zip(test_x, test_y):
        predictions = app.classify_idea(text)
        baseline_predictions.append(predictions[0]["label"] if predictions else "Other / Unclassified")
    baseline = {"name": "Keyword rules (baseline)", "accuracy": round(float(accuracy_score(test_y, baseline_predictions)), 4), "macroF1": round(float(f1_score(test_y, baseline_predictions, average="macro", zero_division=0)), 4), "weightedF1": round(float(f1_score(test_y, baseline_predictions, average="weighted", zero_division=0)), 4), "note": "Rule baseline; no fitted parameters."}
    results.insert(0, baseline)
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump({"pipeline": best["pipeline"], "name": best["name"], "labels": sorted(set(labels))}, MODEL_PATH)
    payload = {"status": "trained", "bestModel": best["name"], "selectionMetric": "held-out macro-F1", "holdout": {"fraction": 0.2, "seed": 42, "records": len(test_y)}, "corpus": {"records": len(rows), "trainingRecords": len(train_y), "labels": dict(sorted(Counter(labels).items())), "labelType": "weak labels mapped from Forbes industries and startup funding verticals"}, "algorithms": results, "caveat": "Scores measure agreement with mapped source taxonomy on a stratified holdout. They do not establish true sector fit, idea originality, or commercial success."}
    METRICS_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps({"status": payload["status"], "records": len(rows), "holdout": len(test_y), "bestModel": payload["bestModel"], "algorithms": [{"name": a["name"], "accuracy": a["accuracy"], "macroF1": a["macroF1"]} for a in results]}, indent=2))


if __name__ == "__main__":
    main()
