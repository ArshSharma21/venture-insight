# Venture Insight

Venture Insight is a local market research dashboard for exploring startup ideas, finding related companies, and comparing reported business and funding data. Its first release covers a broad global snapshot of large public companies and a separate historical dataset of Indian startup funding rounds.

## Start the local dashboard

Requires Python 3.9 or newer. The application uses only the Python standard library.

```bash
python3 app.py
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000). Stop the server with `Ctrl+C`.

## Features

- Search and filter 2,000 public companies by name, industry, and country.
- View a company profile with rank, location, industry, sales, profit/loss, assets, market value, and calculated profit margin.
- Explore a startup idea using transparent keyword-based sector classification and keyword similarity recommendations across the available records.
- Search 3,044 historical Indian startup funding records by company, investor, location, or sector.
- View an industry sales chart and major-company rankings.
- See source and period labels with data limitations throughout the interface.

## Sources and limits

The global company source is the [Forbes Global 2000 2025 Kaggle dataset](https://www.kaggle.com/datasets/ellimaaac/forbes-the-global-2000-companies-2025), listed as CC0. It contains a latest-12-month financial snapshot available as of 25 April 2025; it is not a current live feed or a multi-year trend. The India startup source is [Indian Startup Funding on Kaggle](https://www.kaggle.com/datasets/sudalairajkumar/indian-startup-funding), listed as CC0; its downloaded records span 2015–2020 and show fundraising events, not operating results. See [`data/README.md`](data/README.md) and [`docs/DATA_SOURCE_RESEARCH.md`](docs/DATA_SOURCE_RESEARCH.md) for provenance and limitations.

The 2026 Forbes Kaggle dataset was reviewed but is not included because its page specifies a separate license/permissions process. This repository keeps the redistributable 2025 source. The available sources do not provide complete descriptions or financial histories for every company, especially private startups. The interface labels fields absent from its sources as unavailable rather than filling them with guesses.

## Project pipeline

See [`docs/ROADMAP.md`](docs/ROADMAP.md) for the staged delivery plan and [`docs/PRODUCT_REQUIREMENTS.md`](docs/PRODUCT_REQUIREMENTS.md) for the product scope. Syllabus mapping is excluded at the user's direction.
