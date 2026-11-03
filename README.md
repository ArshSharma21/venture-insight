# Venture Insight

Venture Insight is a student data science project for exploring startup ideas, researching existing companies, comparing competitors, and surfacing potential market opportunities.

The project brief calls for a working local web application backed by reproducible data preparation and data science workflows. Company financials and predictions must be traceable to their sources; unavailable figures will be shown as unavailable instead of being invented.

## Project status

**Stage 0 — repository and plan established.** The current workspace began empty. This repository starts from the requirements in the shared project brief; it does not yet contain a validated dataset or a running application.

## Planned development pipeline

1. **Confirm requirements and syllabus** — validate project scope, required course topics, and demonstration needs.
2. **Inspect data sources** — find candidate public datasets, review their schemas, licenses, and coverage, then select a source before downloading or integrating it.
3. **Build the data pipeline** — preserve source data, document provenance, clean and standardize records, and validate processed output.
4. **Develop the data science layer** — exploratory analysis, visualization, supervised models, clustering, and content-based recommendations where supported by the selected data.
5. **Build the API and storage** — expose company search, profiles, comparisons, analytics, and model results through a Python service.
6. **Build the web dashboard** — implement idea search, company explorer, company profiles, competitor comparisons, market analytics, and recommendations.
7. **Integrate and validate** — connect real processed data and model outputs to the interface; check source attribution and missing-data behavior.
8. **Run locally** — provide reproducible setup instructions and demonstrate the complete application on localhost.

See [`docs/ROADMAP.md`](docs/ROADMAP.md) for phase gates, [`docs/SYLLABUS_MAPPING.md`](docs/SYLLABUS_MAPPING.md) for the provisional course-topic mapping, and [`docs/DATA_SOURCE_RESEARCH.md`](docs/DATA_SOURCE_RESEARCH.md) for initial source candidates and limits.

## Proposed technical direction

The shared brief proposed Python for data processing and the API, with a web frontend. The exact framework and dependency versions will be selected after environment and syllabus requirements are confirmed. No dependencies have been installed yet.

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
