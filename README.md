# Venture Insight

Venture Insight is a local market research dashboard for exploring startup ideas, finding related companies, and comparing reported business and funding data. Its first release covers a broad global snapshot of large public companies and a separate historical dataset of Indian startup funding rounds.

## Start the local dashboard

Requires Python 3.9 or newer. The full dashboard uses scikit-learn and the pinned global startup sample.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python3 data/download_global_startup_funding.py
python -m ml.train
python app.py
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000). Stop the server with `Ctrl+C`.

### Refresh or retrain the classifier

After updating the source files, repeat the download/checksum step and retrain:

```bash
python3 data/download_global_startup_funding.py
python -m ml.train
```

Training compares Multinomial Naive Bayes, Logistic Regression, and Linear SVM. It selects the model with the highest validation macro-F1, saves it under `models/`, and exposes evaluation metrics in the Idea Explorer. Model artifacts are generated locally and are not committed. Without training, the dashboard visibly falls back to the keyword baseline.

## Features

- Search and filter 2,000 public companies by name, industry, and country.
- View a company profile with rank, location, industry, sales, profit/loss, assets, market value, and calculated profit margin.
- View supplemental company descriptions, official websites, founding dates, additional industries, headquarters, employee facts, tickers, and exchanges where an exact-name Wikidata profile is available.
- Review dated Wikidata claims for revenue, net profit, assets, and liabilities in reported currencies when available; these remain separate from the Forbes snapshot.
- Explore an idea with a trained text classifier (or explicit keyword-rule baseline) and a separate TF-IDF cosine-similarity recommender.
- Compare classifier accuracy and macro-F1 on a stratified held-out sample; inspect the weak-label and evaluation caveats in the interface.
- Search source-separated Indian and global funding records by company, investor, location, or sector.
- Retrieve up to 12 startup profiles across the global funding sample and India-only legacy records; every recommendation has a dedicated 0–100 text-similarity column and source link.
- View an industry sales chart and major-company rankings.
- See source and period labels with data limitations throughout the interface.

## Sources and limits

The idea explorer indexes a pinned global funding sample with 20,227 funding events and 11,853 imported recommendation profiles from that sample, in addition to 2,177 India-only startup entities from the legacy source in this local snapshot. The global source is CC BY-NC 4.0, so it is for non-commercial use only. It is fetched locally by `python3 data/download_global_startup_funding.py` and is not stored in this repository. The source license, date range, quality checks, and reviewed alternatives are documented in [`data/SOURCES.md`](data/SOURCES.md) and [`web/sources.html`](web/sources.html).

The financial source is the [Forbes Global 2000 2025 Kaggle dataset](https://www.kaggle.com/datasets/ellimaaac/forbes-the-global-2000-companies-2025), listed as CC0. It contains a latest-12-month financial snapshot available as of 25 April 2025; it is not a current live feed or a multi-year trend. Supplemental profiles are exact-name candidates from the CC0 [Wikidata Query Service](https://query.wikidata.org/): 1,275 profiles matched, and 8,578 dated revenue, net profit, and asset claims were found across 417 companies. These community-maintained claims remain separate from the Forbes snapshot and retain their source currency and dates. The India startup source is [Indian Startup Funding on Kaggle](https://www.kaggle.com/datasets/sudalairajkumar/indian-startup-funding), listed as CC0; its downloaded records span 2015–2020 and show fundraising events, not operating results. See [`data/README.md`](data/README.md) and [`docs/DATA_SOURCE_RESEARCH.md`](docs/DATA_SOURCE_RESEARCH.md) for provenance and limitations.

The 2026 Forbes Kaggle dataset was reviewed but is not included because its page specifies a separate license/permissions process. This repository keeps the redistributable 2025 source. The available sources do not provide complete descriptions or financial histories for every company, especially private startups. The interface labels fields absent from its sources as unavailable rather than filling them with guesses.

## Data science methods and boundaries

The classifier maps Forbes industry and India/global startup funding sectors into broad project sectors. These mapped source categories are **weak labels**, not manually verified labels. Features use company/startup names and available profile descriptions, sub-industry text, remarks and global funding-news excerpts; the global source sector is excluded from its feature text to avoid direct label leakage. A fixed random seed and stratified 60/20/20 train/validation/test split make model selection and final evaluation reproducible. Accuracy and macro-F1 describe agreement with the weak labels on the untouched test partition; they do not measure whether an idea is correctly classified in reality. The interface distinguishes this fitted classifier from the readable keyword-rule baseline.

Recommendations use TF-IDF vectorization and cosine similarity to retrieve records whose available text resembles the user's description; the text-similarity score is scaled to a 0–100 display and is not a match probability. This retrieval method is separate from classification. It does not infer market size, recommend investments, or establish direct competitors. See [`docs/ML_METHODOLOGY.md`](docs/ML_METHODOLOGY.md).

## Project pipeline

See [`docs/ROADMAP.md`](docs/ROADMAP.md) for the staged delivery plan, [`docs/PRODUCT_REQUIREMENTS.md`](docs/PRODUCT_REQUIREMENTS.md) for the product scope, and [`docs/DATA_SOURCE_RESEARCH.md`](docs/DATA_SOURCE_RESEARCH.md) for the reviewed-source decision log. Syllabus mapping is excluded at the user's direction.
