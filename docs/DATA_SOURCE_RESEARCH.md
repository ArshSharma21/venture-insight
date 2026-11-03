# Data Source Research — Candidate Inventory

**Research date:** 2026-11-03  
**Status:** Kaggle candidates inspected at the listing/metadata level; the user must confirm the proposed dataset bundle before files are downloaded. No dataset has been integrated.

## Confirmed project scope

- Geography: India and global markets.
- Industries: all industries.
- Preferred data platform: Kaggle/open datasets, as described by the user.
- Syllabus material: not required for current delivery, at the user's direction.

## Candidate source matrix

| Source | Potential use | Coverage and limits | Due diligence before use |
| --- | --- | --- | --- |
| [Kaggle — Indian Startup Funding](https://www.kaggle.com/datasets/sudalairajkumar/indian-startup-funding) | India startup discovery, sector trends, funding history, investors, and classification labels | About 3,044 funding records; fields include date, startup, vertical/sub-vertical, city, investors, investment type, amount, and remarks. This is historical funding data, not company revenue/profit or full business descriptions. Kaggle metadata lists CC0 Public Domain; records are older and contain missing fields | After approval, inspect the downloaded CSV schema, date range, missingness, duplicate rounds, and amount parsing; preserve attribution and source dates |
| [Kaggle — Financial Data S&P 500 Companies](https://www.kaggle.com/datasets/pierrelouisdanieau/financial-data-sp500-companies) | Company financial profiles and visual comparison of public companies | About 502 companies and four 2020–2021 reporting dates; includes total revenue, net income, gross profit, operating income, expenses, and related metrics. U.S.-listed large companies only; data is stale. Kaggle lists CC0 Public Domain | After approval, inspect CSV units, reporting-period meaning, missingness, and source lineage (dataset says scraped from Yahoo Finance API) |
| [Kaggle — New York Stock Exchange fundamentals](https://www.kaggle.com/datasets/dgawlik/nyse) | Company descriptions/sectors and historical annual fundamentals | NYSE/S&P 500-oriented; prices and fundamentals are mainly 2010–2016. Dataset lists CC0 Public Domain. Older and does not represent all private companies or all countries | Compare schema and financial field definitions to the S&P 500 quarterly candidate; avoid combining inconsistent period definitions without explicit provenance |
| [Kaggle — LinkedIn Job Postings (2023–2024)](https://www.kaggle.com/dsv/9200871) | Company descriptions, industry, headquarters, and employee-size context for companies with postings | Broad job-posting snapshot; company set is limited to employers present in the postings. Dataset page lists CC BY-SA 4.0 and references scraper code; this is not a complete company directory and has no audited company financials | Requires a separate license/provenance review before use; include only the company-profile file if approved, and retain required attribution/share-alike terms |

## Findings so far

No single inspected candidate covers all Indian and global companies across every industry with comparable company profiles, funding, revenue, profit/loss, and market attributes. Kaggle candidates can demonstrate complementary views but will not make coverage complete.

An initial Kaggle-based demonstration could combine India startup funding records with S&P 500 financials. That would support idea/sector exploration and financial charts, but the company sets and measures do not overlap consistently. A separate company-description dataset could improve the “what does this business do?” profile, but the inspected LinkedIn dataset is licensed CC BY-SA 4.0 and needs specific user approval. Every chart and company field must stay attached to its own source and coverage limits.

The India OGD catalog lists company identity and registry fields, but this is not a comparable global financial statements dataset. Its catalog preview reports 3,738,721 records, while the downloadable resource's file size and a lightweight API path were not established. The SEC says its public APIs need no authentication or API key and include submissions and XBRL facts; automated access guidance asks clients to declare a user agent with a contact email.

## Selection gate

Before download or integration, confirm the exact dataset bundle, then inspect the downloaded files' actual schema and terms. Make coverage limits visible. Do not mix datasets into a single financial time series unless their entities, units, and reporting periods match. The LinkedIn CC BY-SA candidate requires separate approval before use.

## References

- Kaggle dataset listings linked in the candidate matrix; downloadable files still need local schema inspection.
- Kaggle [dataset guidance](https://www.kaggle.com/docs/datasets) for supported files and metadata.
- The Indian Startup Funding dataset's Kaggle listing and an IBM Skills Network course document both indicate CC0; the current Kaggle metadata is the controlling license to check when obtaining the files.
