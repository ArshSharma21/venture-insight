# Venture Insight — Development Roadmap

This roadmap is staged so each phase produces a reviewable result before the next begins. The user asked to complete the project from the shared brief without waiting for syllabus material; syllabus mapping is outside this delivery.

## Current implementation status

- Product scope and staged plan recorded.
- Two Kaggle datasets downloaded, schema inspected, and provenance documented.
- Standard-library Python API and responsive dashboard implemented.
- Idea exploration uses transparent keyword sector rules and keyword similarity. This is a prototype research aid, not a validated predictive model.
- Localhost startup command is `python3 app.py` and the dashboard URL is `http://127.0.0.1:8000`.
- Local browser review completed for the overview, idea explorer, and paginated company explorer.
- Full source, raw datasets, dashboard, and documentation are synced to the private repository.

## Phase 0 — Project setup

**Goal:** establish the repository and record the project brief.

- Create and verify the private GitHub repository.
- Record the project objective, development stages, and data integrity rules.
- Keep the workspace free of unverified datasets and fabricated dashboard metrics.

**Gate:** repository and project baseline are visible locally and on GitHub.

## Phase 1 — Requirements capture

**Goal:** turn the shared brief and confirmed scope into a checked list of requirements.

- Confirm target market, intended user, and initial industry coverage.
- Proceed from the shared brief without waiting for syllabus material.
- Define the smallest useful localhost demonstration.
- Record out-of-scope features and constraints.

**Gate:** user-reviewed scope and a defined localhost demonstration.

## Phase 2 — Dataset research and selection

**Status: complete for the first local release.** The selected sources support an initial, clearly bounded release.

- Identify candidate startup, company, and financial datasets on Kaggle/open data platforms.
- Inspect actual files, fields, dates, geography, completeness, and duplicate patterns.
- Record publisher, dataset URL, license/terms, retrieval date, and known limitations.
- Select a dataset only after confirming the fields support the required analyses.

**Gate met:** source pages and downloaded schemas/limits are recorded in `data/README.md`.

## Phase 3 — Data engineering

**Status: implemented.** The application reads source-specific raw files and normalizes fields in memory.

- Preserve source data separately from processed data when terms allow.
- Normalize column names and types; standardize company names and categories.
- Handle missingness explicitly and deduplicate with documented rules.
- Validate row counts, ranges, key fields, and transformation output.
- Generate a data dictionary and source lineage notes.

**Gate met for demo:** units, null handling and source boundaries are explicit. A separate persisted clean-data export can be added in a later iteration.

## Phase 4 — Exploratory analysis and data science

**Status: prototype implemented.** Dashboard aggregates and charts are source-backed; idea classification and similarity are transparent keyword methods.

- Perform exploratory data analysis and visualizations.
- Classify company or idea sectors only with supported labels and evaluate the model.
- Recommend similar companies from idea text and available business/sector fields; explain matches.
- Establish clear prediction targets before training regressors.
- Compare appropriate baselines and candidate models; report evaluation metrics.
- Apply clustering and content-based similarity only to meaningful, available features.
- Explain limitations and avoid interpreting association as causation.

**Gate:** initial analyses are described with limitations. A trained predictive model and held-out evaluation remain future work because the available input data does not contain rich business descriptions or validated idea-success labels.

## Phase 5 — API and storage

**Status: implemented.** `app.py` serves JSON endpoints and static files using Python's standard library.

- Select lightweight local storage after reviewing schema and data size.
- Define endpoints for search, company detail, comparisons, aggregate analytics, and recommendations.
- Return data provenance, missing values, and prediction metadata with results.

**Gate met for demo:** company, funding, overview, and idea endpoints read the checked-in source files.

## Phase 6 — Web dashboard

**Status: implemented.** `web/` contains the responsive dashboard, company explorer, profile details, funding browser, charts, and idea explorer.

- Idea search and filters.
- Company explorer and profile.
- Competitor comparison and financial analytics where source data exists.
- Market visualizations and recommendations tied to actual records.
- Clear labels for unavailable, estimated, and predicted values.

**Gate met:** core pages loaded in the local browser and the company explorer pagination was reviewed.

## Phase 7 — Integration and validation

**Goal:** review the full path from source data to the visible dashboard.

- Trace displayed values to source records or model outputs.
- Validate search, filters, comparisons, empty states, and error handling.
- Review model metrics and descriptions for accuracy.
- Document known gaps and reproducible setup steps.

**Gate met for demo:** the API and dashboard were manually exercised in the browser; this is not a formal automated test suite.

## Phase 8 — Localhost demonstration

**Goal:** run the application locally in a browser.

- Provide setup and run commands.
- Start backend and frontend services.
- Open and verify the local URL and core demonstration path.
- Prepare a short walkthrough using the selected data.

**Final result:** a working localhost showcase plus reproducible project documentation.

## Decision log

- Project name: Venture Insight.
- Repository: `ArshSharma21/venture-insight` (private).
- Initial market: India and global markets.
- Initial industry coverage: all industries.
- Framework: Python standard library API and static HTML/CSS/JavaScript.
- Data sources: Forbes Global 2000 (2025 snapshot) and Indian Startup Funding (2015–2020).
- Syllabus mapping: excluded from current delivery at the user's direction.
- Initial repository state: no dataset or application code existed in the workspace.
