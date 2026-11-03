# Venture Insight — Product Requirements

**Status:** captured from the user's project description; dataset and feature coverage depend on the sources selected.

## Product goal

Help someone investigate a startup idea by showing what similar businesses already exist, what those companies do, what evidence is available about their funding and financial performance, and what related areas merit further research.

The intended product is a searchable web dashboard for India and global markets, across industries. It must cover both startups and established large companies. The source data will determine actual coverage; the application must not imply that it contains every company or every industry where its sources are incomplete.

## User journey

1. The user enters a startup idea, product, or market keyword.
2. The application identifies likely industry terms and returns related companies from the available records.
3. The user opens a company profile with its business/industry description and available company facts.
4. The user compares related companies and views source-backed charts for available funding or financial metrics.
5. The user explores related companies, sectors, and market patterns as research suggestions, with the data and limitations visible.

## Company information to research

Use these familiar business and finance terms in labels and documentation:

- **Company overview:** name, business description/product, sector and sub-sector, geography, founding date, and source.
- **Large public-company profile:** rank/list membership, country, industry, sales, profit/loss, total assets, and market value where present in the chosen snapshot.
- **Funding history:** dated investment rounds, amount, currency, investment type, and named investors where available. Keep funding separate from operating performance.
- **Financial performance:** revenue/sales, gross profit, operating income, net income or loss, expenses, assets/liabilities, and reporting period/currency when a source provides them.
- **Business context:** company size, public/private status, market listing/ticker, and comparable companies where available.
- **Data quality:** source, last-updated/retrieved date, missing fields, unit/currency, and coverage caveats.

Do not infer a private company's revenue or profit from its fundraising. If a field is absent, display “Not available in this source.”

## Analytics and data science

- **Visualization:** funding by time, sector, location, and round; company revenue/profit trends where repeated reported periods exist; clear units and source dates.
- **Classification:** predict or assign a company/idea sector only where labeled examples and input features support an evaluated model. Show the predicted class as a model output, separate from source facts.
- **Recommendations:** retrieve similar companies using idea text and available sector/sub-sector/business-description features. Explain which shared terms or categories led to each match.
- **Market suggestions:** summarize observed clusters and funding patterns as research leads, not as claims that an idea will succeed or is guaranteed to be an opportunity.

## First local demonstration

- Search an idea such as “online grocery delivery” or a company name.
- Show matching companies and their business/industry fields.
- Open one company profile and distinguish observed fields from unavailable ones.
- Compare funding or financial history only when records support it.
- Show a chart with its source, period, currency, and known data coverage.
- Display related-company recommendations and a short explanation for each.

## Scope and limits

- Initial target scope: India and global markets; all industries.
- Include startup activity as well as established global public companies.
- A broad large-company snapshot can provide one-year financial fields, but that does not create a historical time series or a full business description.
- Actual searchable coverage will be limited to the selected datasets and must be described accurately.
- Public startup datasets often contain funding rounds rather than audited revenue/profit. Financial profiles require separate financial-statement sources and may cover listed companies only.
- No user account, idea storage, paid market feed, or external API key is required for the first local demo unless a source decision later requires one.
- Syllabus mapping is excluded at the user's direction.
