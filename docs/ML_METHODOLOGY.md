# Classification and recommendation methods

## Two separate tasks

| Project task | Method | Input and output | How to interpret it |
|---|---|---|---|
| Sector classification | TF-IDF text features + selected supervised classifier | Idea text → ranked broad-sector scores | Model scores rank candidate sectors; they are not probabilities of success. |
| Baseline classification | Explicit keyword rules | Idea text → sectors with matching rule counts | Transparent comparison baseline; no fitting or training. |
| Similar-record recommendation | TF-IDF + cosine similarity | Idea and record text → nearest records | Retrieval relevance only; not proof of competition or business fit. |

## Training and comparison

The reproducible trainer maps the industry label in the Forbes snapshot and the vertical label in the Indian startup funding file into a broad sector taxonomy. These are weak labels: the program does not manually verify that a particular company's business belongs in the mapped class. The classification feature text uses company/startup names, available Wikidata descriptions and profile industry values, plus startup sub-industry/remarks and source-news excerpts from the global funding sample. Global source sectors also become weak target labels; their sector field is excluded from the model text. Source-level broad labels are the target; rows with fewer than five examples are left out of model fitting and evaluation.

The data is divided into 60% training, 20% validation, and a final 20% stratified test set. The comparison includes Multinomial Naive Bayes, Logistic Regression, and Linear SVM. The model with the highest validation macro-F1 is selected; each algorithm is then refit on the full 80% development partition and evaluated on the untouched 20% test partition. The rule baseline is scored on the same final test set. Accuracy gives overall agreement; macro-F1 weights each observed sector equally. Per-class scores and supports are saved in `models/model_metrics.json`.

Because labels are inherited from source categories, high scores mean that a model reproduces those categories on held-out examples. They do not prove that the categories are correct, and the holdout does not test performance on new real-world startup ideas. Do not interpret model scores as calibrated commercial probabilities, investment guidance, or startup-success forecasts. Review the displayed source data and match text.

## Retrieval recommendations

The recommender vectorizes the idea and each available company/startup record using TF-IDF unigrams and bigrams, then ranks by cosine similarity. Startup fundraising and public-company financials remain separate record types and retain their source context. Similarity is a text-retrieval score; it does not measure market share, sales equivalence, uniqueness, competition, or opportunity size. Classification selects a sector label; recommendation retrieves similar source records. Neither algorithm is used as a substitute for the other.

## Reproduce locally

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python3 data/download_global_startup_funding.py
python -m ml.train
python app.py
```
