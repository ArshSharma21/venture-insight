# Data Source Research — Candidate Inventory

**Research date:** 2026-11-03  
**Status:** two Kaggle datasets plus two Wikidata-derived company enrichment files are integrated. SEC access was researched, but automated requests from this environment are presently refused.

## Confirmed project scope

- Geography: India and global markets.
- Industries: all industries.
- Company types: startups and established large public companies.
- Preferred data platform: Kaggle/open datasets, as described by the user.
- Syllabus material: not required for current delivery, at the user's direction.

## Candidate source matrix

| Source | Potential use | Coverage and limits | Due diligence before use |
| --- | --- | --- | --- |
| [Kaggle — Forbes Global 2000 Companies 2025](https://www.kaggle.com/datasets/ellimaaac/forbes-the-global-2000-companies-2025) | Broad profile and financial comparison of established large public companies worldwide | 2,000 companies across countries and industries. Fields: rank, company, headquarters, industry, sales, profit, assets, and market value, in USD billions. Kaggle listing says CC0 Public Domain. A latest-12-month snapshot available as of 25 Apr 2025, not a financial time series; industry is not a full business description. CSV uses semicolon delimiters. | Downloaded on 3 Nov 2026, schema inspected, integrated in `app.py`; see `data/README.md` |
| [Kaggle — Indian Startup Funding](https://www.kaggle.com/datasets/sudalairajkumar/indian-startup-funding) | India startup discovery, sector trends, funding history, investors, and classification labels | 3,044 funding records; fields include date, startup, vertical/sub-vertical, city, investors, investment type, amount, and remarks. Historical funding data, not company revenue/profit or full business descriptions. Kaggle metadata lists CC0 Public Domain; records span 2015–2020 and contain missing fields. | Downloaded on 3 Nov 2026, schema inspected, integrated in `app.py`; see `data/README.md` |
| [Kaggle — Forbes Global 2000 Companies 2026](https://www.kaggle.com/datasets/ellimaaac/forbes-the-global-2000-companies-2026) | Newer broad public-company snapshot | 2,000 companies with the same core fields, latest 12 months available as of 15 May 2026. Kaggle lists “Other (specified in description)” and links to a Forbes permissions request. | Reviewed on 3 Nov 2026, not downloaded or included; use only after terms are clarified |
| [Wikidata Query Service](https://query.wikidata.org/) | Supplemental global company descriptions and dated reported financial claims | Exact English-name matching found 1,275 candidate profiles out of the 2,000 Forbes names. Available fields vary; claims are community-maintained and may be missing or ambiguous. The profile query exposes description, website, founding date, industry, headquarters, country, and employee facts. A second query captures dated revenue, net profit, assets, and liabilities only when a currency/unit is supplied. | Integrated as supplemental candidate data in `data/wikidata_company_profiles.json` and `data/wikidata_financial_facts.json`; identity and claims link back to Wikidata. |
| [SEC EDGAR APIs](https://www.sec.gov/search-filings/edgar-application-programming-interfaces) | Multi-year U.S. company filings and XBRL facts | Official API provides submissions, company facts, and bulk archives; no API key is required. Facts cover SEC filers and can contain periods, taxonomy differences, and restatements. | Public API researched; requests from this environment were rejected by SEC as an undeclared automated tool, even after adding the user-approved contact. No SEC facts were copied into the project. |
| [Kaggle — LinkedIn Job Postings (2023–2024)](https://www.kaggle.com/dsv/9200871) | Company descriptions, industry, headquarters, and employee-size context for companies with postings | Broad job-posting snapshot; company set is limited to employers present in postings. Dataset page lists CC BY-SA 4.0 and references scraper code; this is not a complete company directory and has no audited company financials | Requires separate user approval and provenance review; if approved, include only the company-profile file and retain attribution/share-alike terms |

## Findings

No single inspected candidate covers all Indian and global companies across every industry with comparable company profiles, funding, revenue, profit/loss, and market attributes. The Global 2000 candidate directly covers established large public firms across countries and sectors; the Indian startup dataset separately covers funding activity. Wikidata contributes candidate descriptions and dated financial claims, but it is uneven and community-maintained. Neither combination delivers complete global startup or company coverage.

The 2025 Global 2000 listing reports its snapshot from the latest 12 months available as of April 25, 2025. It supplies broad cross-country large-company coverage and four core financial measures, but not repeated history or detailed business descriptions. Wikidata supplements exact-name candidates and dated claims without merging their values into Forbes measures. The newer 2026 copy is not bundled because its terms point to a Forbes permissions process. The LinkedIn company-profile file could add descriptions and company-size context, but its CC BY-SA 4.0 terms and scraped provenance need the user's approval before use.

## Selection decision

Use the CC0 2025 Global 2000 and CC0 Indian Startup Funding file as the core, with exact-name Wikidata as visibly supplemental context. Keep funding and financial facts separate unless entity, currency, and reporting periods match. SEC is a strong future source for U.S. filing history if this network is permitted by SEC. The optional LinkedIn CC BY-SA candidate needs separate user approval.

## References

- Kaggle dataset listings linked in the candidate matrix; downloadable files still need local schema inspection.
- Kaggle [dataset guidance](https://www.kaggle.com/docs/datasets) for supported files and metadata.
- Forbes [2025 Global 2000 methodology](https://www.forbes.com/sites/andreamurphy/2025/06/12/how-we-crunch-the-numbers-the-2025-global-2000/) explains the ranking inputs and reporting snapshot.
