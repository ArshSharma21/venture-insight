# Data Source Research — Candidate Inventory

**Research date:** 2026-11-03  
**Status:** candidates only; no dataset has been selected, downloaded, or integrated.

## Confirmed project scope

- Geography: India and global markets.
- Industries: all industries.
- Exact course syllabus: still awaited; the current syllabus mapping is provisional.

## Candidate source matrix

| Source | Potential use | Coverage and limits | Due diligence before use |
| --- | --- | --- | --- |
| [India OGD — Company Master Data](https://www.data.gov.in/catalog/company-master-data) | Indian company registry identity and profile fields, including CIN, name, status, class/category, capital fields, registration date, and state | Companies registered with India's Registrar of Companies; the catalog does not establish a unified global view or full startup financial statements | Inspect the current archive/API schema, completeness, update cadence, and Government Open Data License-India conditions |
| [SEC EDGAR APIs](https://www.sec.gov/search-filings/edgar-application-programming-interfaces) | Financial filing facts for companies reporting to the SEC; possible listed-company financial analysis | Public filers, including some foreign issuers; not all global companies or private startups. Structured XBRL and reporting periods vary | Choose specific endpoints and concepts; preserve period/unit metadata; follow SEC fair-access and user-agent requirements |
| [UK Companies House API](https://developer.company-information.service.gov.uk/) | UK company identity, status, registered records, and filings | UK companies within the Companies Act scope; not global coverage. API authentication is required | Review terms, API limits, data fields, and account/key requirements before connecting or collecting |
| [Kaggle — StartUp Investments (Crunchbase)](https://www.kaggle.com/datasets/arindam235/startup-investments-crunchbase) | Potential company/funding features for startup exploration or recommendation | Community-hosted dataset; age, geography, completeness, and source rights are not established by this initial inspection | Inspect the actual files, provenance, license, field definitions, and redistribution terms before any download/use |
| [Kaggle — Indian Business Listings](https://www.kaggle.com/datasets/japnoor69/indian-business-listings-dataset) | Possible Indian business discovery and category/search data | Community-hosted listings; may be businesses rather than startups and may not contain financials | Inspect data source, collection method, license, privacy implications, fields, duplicates, and freshness |

## Findings so far

No single inspected candidate covers all Indian and global companies across every industry with comparable company profiles, funding, revenue, profit/loss, and market attributes. The official sources are jurisdiction-specific; Kaggle candidates may fill selected gaps, but they need file-level provenance and license review.

The likely data design is therefore a small set of source-specific records with explicit geography and provenance, not a claim of complete global coverage. Financial charts should appear only for sources and companies with actual financial filings. Missing values remain unavailable; funding is not revenue.

## Selection gate

Before download or integration, inspect each shortlisted dataset's actual schema and terms. Then select sources against the verified syllabus and the project's demonstration requirements. Any API key, account creation, paid source, or additional permission will be handled separately before use.

## References

- Government of India, [Company Master Data](https://www.data.gov.in/catalog/company-master-data).
- U.S. Securities and Exchange Commission, [EDGAR Application Programming Interfaces](https://www.sec.gov/search-filings/edgar-application-programming-interfaces) and [Accessing EDGAR Data](https://www.sec.gov/search-filings/edgar-search-assistance/accessing-edgar-data).
- Companies House, [API overview](https://developer.company-information.service.gov.uk/) and [Getting started](https://developer.company-information.service.gov.uk/get-started).
- Kaggle dataset listings linked in the candidate matrix; item metadata and file contents are pending inspection.
