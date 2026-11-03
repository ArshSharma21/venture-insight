# Venture Insight

Venture Insight is a startup idea research dashboard. A user enters an idea, finds similar companies and market activity, explores company profiles, compares available financials, and sees data-backed recommendations.

The project brief calls for a working local web application backed by reproducible data preparation and data science workflows. Company financials and predictions must be traceable to their sources; unavailable figures will be shown as unavailable instead of being invented. Funding raised is a financing event, not revenue or profit. Private-company financials may not be publicly available.

## Project status

**Stage 1 — product brief captured; dataset selection pending.** The user wants an idea search, company research, financial analysis, visualization, classification, and recommendation workflow, using Kaggle/open data where suitable. The user asked to proceed without syllabus mapping. No dataset has yet been downloaded or integrated.

## Planned development pipeline

1. **Confirm requirements** — use the shared brief and the user's confirmed scope: India and global markets, all industries; do not block on syllabus material.
2. **Select data sources** — review public datasets, schemas, licenses, coverage, and any contact/API requirements before integrating them.
3. **Build the data pipeline** — preserve source data, document provenance, clean and standardize records, and validate processed output.
4. **Develop the data science layer** — exploratory analysis, visualization, supervised models, clustering, and content-based recommendations where supported by the selected data.
5. **Build the API and storage** — expose company search, profiles, comparisons, analytics, and model results through a Python service.
6. **Build the web dashboard** — implement idea search, company explorer, company profiles, competitor comparisons, market analytics, and recommendations.
7. **Integrate and validate** — connect real processed data and model outputs to the interface; check source attribution and missing-data behavior.
8. **Run locally** — provide reproducible setup instructions and demonstrate the complete application on localhost.

See [`docs/PRODUCT_REQUIREMENTS.md`](docs/PRODUCT_REQUIREMENTS.md) for the user journeys and data requirements, [`docs/ROADMAP.md`](docs/ROADMAP.md) for phase gates, and [`docs/DATA_SOURCE_RESEARCH.md`](docs/DATA_SOURCE_RESEARCH.md) for candidate datasets and their limits.

## Proposed technical direction

The shared brief proposed Python for data processing and the API, with a web frontend. The framework will be chosen after confirming the actual data and local runtime. No dependencies have been installed.

## Data integrity rules

- Keep a source and retrieval note for each dataset.
- Do not treat funding raised as revenue.
- Do not invent unavailable company financials.
- Distinguish observed values, estimates, and model outputs in both the API and dashboard.
- Only claim predictive performance after evaluating the model on appropriate held-out data.
- Review dataset terms and website rules before collection or redistribution.

## Local development

Local run commands will be added after the application stack and dependencies are selected and implemented.

## License

No software license has been selected. The repository remains private while the project scope and data sources are being established.
