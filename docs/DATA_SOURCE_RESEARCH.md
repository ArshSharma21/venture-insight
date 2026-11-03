# Data Source Research and Audit

**Audit date:** 2026-11-03
**Purpose:** choose source-bounded startup records for idea search while keeping licenses, event/profile distinctions, and coverage limits visible.

## Integrated datasets

| Source | What is present | Rights and coverage | Treatment |
| --- | --- | --- | --- |
| [Fliar Research — Global Startup Funding Rounds 2019–2026](https://github.com/Busineessfree/global-startup-funding) | Pinned sample of 20,227 round events; importer groups it into 11,853 startup recommendation profiles. Source period Jan 2019–Jun 2026; parsed sample rows cover 137 countries and 69 sectors. Fields include name/domain, sector, country/city, founded year, funding stage/date, amount status, investor, news excerpt, article/profile URLs. | CC BY-NC 4.0, attribution Fliar Research / Fliar BI. Source describes this as a fixed 25% hashed company sample of 80,911 events. It is non-commercial; full dataset and updates require provider API access. | Pinned to source commit `225b3e0e84e5ed4a45b5311b20760930cfde9c72`, SHA-256 verified, downloaded locally via `data/download_global_startup_funding.py`; raw CSV excluded from Git. One profile-level recommendation per normalized profile path, with domain/name fallback. Events are kept separate in funding search. Only rows marked `verified` show an amount. |
| [Kaggle — Indian Startup Funding](https://www.kaggle.com/datasets/sudalairajkumar/indian-startup-funding) | 3,044 event rows, 2015–2020; company, vertical/sub-vertical, city, date, round, amount, investors and remarks. | Kaggle listing says CC0; historic, partial and missing fields. | Existing India dataset. Entity records not already in the global sample remain searchable/recommendable. Events may overlap the global 2019–2020 sample, so source event counts are never called a deduplicated total. |
| [Kaggle — Forbes Global 2000 Companies 2025](https://www.kaggle.com/datasets/ellimaaac/forbes-the-global-2000-companies-2025) | 2,000 large public companies; financial snapshot and industry. Latest 12 months available 25 Apr 2025. | Kaggle listing says CC0. | Established-public-company comparator only. No multi-year series or comprehensive startup coverage. |
| [Wikidata Query Service](https://query.wikidata.org/) | 1,275 exact-English-name candidate profile matches to Forbes names; 8,578 dated revenue/profit/assets claims for 417 companies. | Wikidata structured data CC0; community-maintained, sparse, possible name mismatches. | Supplemental profiles and claims; never merged with Forbes financials. Each record links to source. |

## Sources reviewed but not imported

| Source | Why it could help | Why it is not currently merged |
| --- | --- | --- |
| [Forbes Global 2000 2026 Kaggle copy](https://www.kaggle.com/datasets/ellimaaac/forbes-the-global-2000-companies-2026) | Newer 2,000 public-company snapshot. | Listing points to a separate permissions request; use remains excluded until its terms are clarified. |
| [Yigit Mete Ozcan accelerator portfolio aggregator](https://github.com/yigitmeteozcan/startups) | README reports 21,352 companies across seven portfolios with descriptions, locations, tags, cohorts, and source. | Repository declares MIT for its project but says to respect each accelerator provider's terms. That does not settle redistribution rights for each underlying portfolio record. No records copied. |
| [UK Companies House API](https://developer.company-information.service.gov.uk/) | Live UK registered-company information. | Requires API credentials; covers general registered entities and does not identify startups. Not a global startup directory. |
| [SEC EDGAR APIs](https://www.sec.gov/search-filings/edgar-application-programming-interfaces) | Public submissions and XBRL facts for U.S. filers. | Useful for public-company financial history, not a private/global startup directory. Browser CORS is not supported. Earlier automated retrieval from this environment was refused; no SEC facts are included. |
| [GLEIF Global LEI Index](https://www.gleif.org/en/about/open-data/) | CC0 global legal-entity reference data and ownership links. | LEIs do not mean “startup”; many entities have no LEI. Adding it to idea search would add legal entities without useful descriptions. |
| [OpenCorporates self-service API terms](https://opencorporates.com/legal-information/self-service-api-terms-of-service/) | Broad registry aggregation. | API access is limited and third-party distribution is restricted absent the applicable external-distribution license. No API key or license was obtained. |
| [LinkedIn Job Postings company profile dataset](https://www.kaggle.com/dsv/9200871) | Company descriptions, sector and size context for employers with postings. | Dataset page lists CC BY-SA 4.0 and scraper provenance. Employer coverage is biased and not a startup directory; not imported. |

## What “global” means here

The global sample contains reported funding events for a subset of funded startups. It is **not** a census of all startups or all countries, and a funding event does not establish that the company remains active. Recommendation context is often text from a funding-news article, not a reviewed company description. The app reports the sample size and offers source links so users can verify details.

No source found in this audit provides complete Indian and global startup profiles, funding, audited revenue/profit, and current operating status under one openly reusable license. Keep these kinds of records separate. A result's similarity to an idea does not establish direct competition, market size, originality, or commercial opportunity.

See [`data/SOURCES.md`](../data/SOURCES.md) for the in-project source catalog, verified counts, checksum, attribution, and reproduction command.
