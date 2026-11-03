# Data files

Raw files in `raw/` retain their source field names and values. The Fliar sample is fetched locally by a pinned/checksummed downloader and is omitted from Git because its CC BY-NC license is separate from the project code. The application reads available files into standardized in-memory records at startup. The Forbes list is enriched with a separate, supplemental Wikidata profile file using exact English company-name labels; that identity match is a candidate and must be checked before relying on it.

## Global public companies

- File: `raw/Forbes_2000_Companies_2025.csv`
- Source: [Forbes — The Global 2000 Companies, 2025 (Kaggle)](https://www.kaggle.com/datasets/ellimaaac/forbes-the-global-2000-companies-2025)
- License shown on Kaggle: CC0 Public Domain
- Coverage: 2,000 large public companies; 8 fields for rank, company, headquarters country, industry, sales, profit, assets and market value.
- Period: latest 12 months available to Forbes as of 25 April 2025. Currency is USD billions.
- Format: semicolon-delimited CSV despite the `.csv` extension.
- Limits: annual snapshot, not a financial time series; excludes many smaller and private firms; no detailed business descriptions or liabilities.

## Supplemental company profiles

- File: `wikidata_company_profiles.json.gz` (gzip-compressed JSON used by the local app)
- Source: [Wikidata Query Service](https://query.wikidata.org/), structured data released under CC0.
- Retrieved: 3 November 2026 by `enrich_wikidata.py`, matching exact English labels against the 2,000 company names.
- Coverage: 1,275 candidate profile records (out of 2,000 input companies); 1,235 descriptions, 1,122 websites, 1,103 founding dates, 1,049 headquarters, 919 industry tags, 401 employee counts, 397 revenue facts, 921 exchange labels, and 25 ticker values.
- Fields: description, website, founding date, headquarters, country, industry tags, employee count, revenue fact, ticker, exchange, Wikidata item ID and source URL.
- Limits: community-maintained and unevenly populated; exact labels can be ambiguous; employee and revenue fact dates/units can be absent. The dashboard does not display revenue facts whose currency and reporting context are not clear. Verify identity and any fact directly at its linked Wikidata item. This profile source supplements the Forbes record and does not replace audited filings.

## Supplemental dated financial facts

- File: `wikidata_financial_facts.json.gz` (gzip-compressed JSON used by the local app)
- Source: Wikidata Query Service (CC0), queried for dated claims of revenue, net profit, total assets, and total liabilities for the matched profile candidates.
- Coverage: 8,578 dated claims across 417 matched company profiles: 3,934 revenue, 3,962 net-profit, and 682 total-assets claims. No dated total-liabilities claims were returned in this retrieval.
- Units and reported periods are retained per source claim; the dashboard never converts these values or combines them with Forbes figures.
- Limits: community-entered claims can be sparse, conflicting, or unverified; these should be treated as leads and checked against original filings. Only dated claims with an explicit currency/unit are captured. This is not a substitute for audited statements.
- Rebuild profile candidates with `python3 data/enrich_wikidata.py`; rebuild financial claims with `python3 data/enrich_financial_facts.py`. Both use the public Wikidata Query Service and a descriptive User-Agent. Outputs are compressed to keep the repository small.

## Indian startup funding

- File: `raw/startup_funding.csv`
- Source: [Indian Startup Funding (Kaggle)](https://www.kaggle.com/datasets/sudalairajkumar/indian-startup-funding)
- License shown in Kaggle dataset metadata: CC0 Public Domain
- Coverage: 3,044 historical funding records with startup, vertical/subvertical, city, date, investor, round/type, amount and remarks fields.
- Period: valid dates span 2 Jan 2015–13 Jan 2020 in this downloaded version (3,036 of 3,044 rows have a parseable date). Amounts are USD when present.
- Limits: funding events are not revenue, profit, or valuation; dates, categories, names and amounts may be missing or inconsistent; not a current startup directory.

## Global startup funding sample

- Expected local file: `raw/global_startup_funding_sample.csv` (ignored by Git; restored with `python3 data/download_global_startup_funding.py`).
- Source: [Fliar Research — Global Startup Funding Rounds 2019–2026](https://github.com/Busineessfree/global-startup-funding).
- License: CC BY-NC 4.0, attribution Fliar Research / Fliar BI; this dataset may be used only for non-commercial purposes under its stated license.
- Pinned version: source commit `225b3e0e84e5ed4a45b5311b20760930cfde9c72`; SHA-256 `1f1602f2a8266418899457527aec906ab32f8e19b97375c06f673492ee7e03f0`.
- Coverage: 20,227 funding events, dated Jan 2019–Jun 2026 according to the source; 11,853 profile-level recommendation entities after importer fallback keys. The source calls this a fixed 25% sample of 80,911 events. Parsed data has 137 country values and 69 sector labels.
- Fields include event ID, company name/domain, location, sector, founded year, date, stage, amount, amount check status, investor, news excerpt, news URL and Fliar profile URL.
- Amount handling: the dashboard shows a numeric value only when the source marks the event `verified`; unchecked, failed-check, and undisclosed amounts remain unavailable. The sample has 15,951 events with verified amounts.
- Limits: this is a sample of reported funding events, not all startups or operating companies. News excerpts can describe an announcement rather than the startup's complete product. 42 source events have no profile URL; the importer uses domain/name fallback keys. The full dataset and updates require Fliar API access. It overlaps the India history period, so record counts across sources are not a count of unique global rounds.
- Rebuild/download with `python3 data/download_global_startup_funding.py`; the script pins the source commit and verifies the checksum before writing.

## Retrieval and handling

The Kaggle datasets were retrieved on 3 November 2026 after account sign-in. Funding and company financials remain separate. The Wikidata join is exact-name only and is visibly labeled supplemental. Public-company profit margin is calculated from the source's reported sales and profit; other displayed company financial values are source fields.
