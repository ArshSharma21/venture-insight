# Data source catalog and audit

This catalog distinguishes the dataset's intended use, coverage, and limits. “Global” means a source reports records from multiple countries; it does not mean complete world coverage. Startup funding events, startup profiles, public-company data, and general legal-entity records are separate concepts.

| Source | Data in this project | Coverage / fields | License / access | Project treatment |
|---|---|---|---|---|
| [Fliar Research, Global Startup Funding Rounds 2019–2026](https://github.com/Busineessfree/global-startup-funding) | Pinned sample downloaded by `download_global_startup_funding.py` | Source release says Jan 2019–Jun 2026, 20,227 sample funding events; 11,836 distinct normalized profile paths in the raw file; the importer creates 11,853 profile records including fallback keys for records without a usable profile path; 137 countries and 69 sectors in the parsed sample. Company/domain, sector, country/city, founded year, round, amount status, investor, news excerpt, source/profile URLs. | CC BY-NC 4.0; attribution: Fliar Research / Fliar BI. Sample is 25% of source's 80,911 rounds, selected by a fixed company hash. Full data and monthly updates require the provider's API access. | Used for startup recommendation text and global event search. One recommendation record per profile path, using a domain/name fallback when the source profile path is missing. Amount is shown only when `amount_status=verified`; all event rows remain separate in funding search. Local CSV is fetched from a pinned source commit and SHA-256 checked; it is not committed to this GitHub repo. **Non-commercial use only under the stated dataset license.** |
| [Indian Startup Funding on Kaggle](https://www.kaggle.com/datasets/sudalairajkumar/indian-startup-funding) | `raw/startup_funding.csv` | 3,044 historical India event rows, 2015–2020; company, source sector/sub-sector, location, date, funding type/amount, investor, remarks. | Dataset page lists CC0; historical third-party collection. | Kept as a separate India source; never treated as current company performance. India-only entities not already represented in the global sample can add recommendation candidates. |
| [Forbes Global 2000 Companies 2025 on Kaggle](https://www.kaggle.com/datasets/ellimaaac/forbes-the-global-2000-companies-2025) | `raw/Forbes_2000_Companies_2025.csv` | 2,000 large listed companies; latest-12-month sales, profit, assets, market value and industry snapshot available to Forbes 25 Apr 2025. | Dataset page lists CC0. | Established public-company comparison only; not a startup directory or live financial feed. |
| [Wikidata Query Service](https://query.wikidata.org/) | Compressed profile and financial-claim snapshots in `data/` | Exact-name candidate matches against the 2,000 Forbes names; uneven profile fields and community-entered claims. | Wikidata structured data is CC0; query service is public and rate-limited. | Supplemental context only; exact-name entity matches need manual checking. Historical claims are kept separate from Forbes figures. |

## Download and verify the global sample

```bash
python3 data/download_global_startup_funding.py
```

The downloader pins upstream commit `225b3e0e84e5ed4a45b5311b20760930cfde9c72` and checks SHA-256 `1f1602f2a8266418899457527aec906ab32f8e19b97375c06f673492ee7e03f0`. The app starts without this optional file, but global startup recommendations require it. A fresh checkout should run the downloader before starting the dashboard.

## Source audit: reviewed, not merged into startup recommendations

- [yigitmeteozcan/startups](https://github.com/yigitmeteozcan/startups) reports more than 21,000 companies from seven accelerator portfolios and describes each record with a name, description, location, tags, cohort and source. Its repository says MIT for the project while also instructing users to respect each accelerator's terms. The data redistribution rights are therefore not treated as settled here; it is not copied into this project.
- [Companies House API](https://developer.company-information.service.gov.uk/) offers live UK company-register records but requires API credentials and includes general registered entities, not a startup-only population. It is not used as a global startup directory.
- [SEC EDGAR APIs](https://www.sec.gov/search-filings/edgar-application-programming-interfaces) provide US filer submissions and XBRL facts; filers are not a startup universe and coverage is not global/private-company coverage. SEC says the API does not support browser CORS. These sources are not presented as startup profiles.
- [GLEIF Global LEI Index](https://www.gleif.org/en/about/open-data/) is CC0 global legal-entity reference data, but LEIs are not a startup designation and only entities with LEIs appear. It is not used as a startup catalog.
- [OpenCorporates API terms](https://opencorporates.com/legal-information/self-service-api-terms-of-service/) include access limits and restrict sharing API data to third parties unless an external-distribution license and qualifying derivative terms apply. No API key/license was obtained, so it is not imported into this third-party-facing dashboard.

## Important limitations

This is a source-bounded research index, not a census of all startups. A company appearing in a funding sample means the source records a funding event, not that it is active today. A news excerpt may describe the funding announcement rather than the company's full product. Missing or failed amount checks are not converted into amounts. Similarity scores are text retrieval scores, not success probabilities, market-share estimates, or proof of direct competition. Users should open the source link and verify important details.
