# Data files

The raw files in `raw/` are kept as downloaded, with their original field names and values. The application reads them into standardized in-memory records at startup; no company facts are joined across sources.

## Global public companies

- File: `raw/Forbes_2000_Companies_2025.csv`
- Source: [Forbes — The Global 2000 Companies, 2025 (Kaggle)](https://www.kaggle.com/datasets/ellimaaac/forbes-the-global-2000-companies-2025)
- License shown on Kaggle: CC0 Public Domain
- Coverage: 2,000 large public companies; 8 fields for rank, company, headquarters country, industry, sales, profit, assets and market value.
- Period: latest 12 months available to Forbes as of 25 April 2025. Currency is USD billions.
- Format: semicolon-delimited CSV despite the `.csv` extension.
- Limits: annual snapshot, not a financial time series; excludes many smaller and private firms; no detailed business descriptions or liabilities.

## Indian startup funding

- File: `raw/startup_funding.csv`
- Source: [Indian Startup Funding (Kaggle)](https://www.kaggle.com/datasets/sudalairajkumar/indian-startup-funding)
- License shown in Kaggle dataset metadata: CC0 Public Domain
- Coverage: 3,044 historical funding records with startup, vertical/subvertical, city, date, investor, round/type, amount and remarks fields.
- Period: valid dates span 2 Jan 2015–13 Jan 2020 in this downloaded version (3,036 of 3,044 rows have a parseable date). Amounts are USD when present.
- Limits: funding events are not revenue, profit, or valuation; dates, categories, names and amounts may be missing or inconsistent; not a current startup directory.

## Retrieval and handling

Retrieved from Kaggle on 3 November 2026 after account sign-in. The dashboard preserves each dataset as its own source and shows the source period. Funding and company financials are not merged. Public-company profit margin is calculated from the source's reported sales and profit; other displayed company financial values are source fields.
