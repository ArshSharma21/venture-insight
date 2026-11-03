const $ = (s) => document.querySelector(s);
const $$ = (s) => [...document.querySelectorAll(s)];
const fmtN = (n) => new Intl.NumberFormat('en-US', { maximumFractionDigits: 0 }).format(n || 0);
const moneyB = (n) => n == null ? 'Not available' : n >= 1000 ? `$${new Intl.NumberFormat('en-US', { maximumFractionDigits: 1 }).format(n / 1000)}T` : `$${new Intl.NumberFormat('en-US', { maximumFractionDigits: 1 }).format(n)}B`;
const billions = (n) => n >= 1000 ? `$${new Intl.NumberFormat('en-US', { maximumFractionDigits: 1 }).format(n / 1000)}T` : `$${new Intl.NumberFormat('en-US', { maximumFractionDigits: 1 }).format(n)}B`;
const cash = (n) => n == null ? 'Not disclosed' : `$${new Intl.NumberFormat('en-US', { maximumFractionDigits: 0 }).format(n)}`;
const esc = (s) => String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
async function get(url) { const r = await fetch(url); if (!r.ok) throw Error('Could not load this data.'); return r.json(); }

function pageFromHash() {
  const id = location.hash.slice(1) || 'overview';
  const target = document.getElementById(id);
  if (!target?.classList.contains('page')) return;
  $$('.page').forEach(p => p.classList.toggle('active-page', p === target));
  $$('.nav-link').forEach(a => a.classList.toggle('active', a.getAttribute('href') === `#${id}`));
  $('#crumb-current').textContent = ({ overview: 'Overview', 'idea-lab': 'Idea explorer', companies: 'Companies', funding: 'Startup funding' })[id] || 'Overview';
}
window.addEventListener('hashchange', pageFromHash);
pageFromHash();

function renderLeaders(rows) {
  $('#leader-list').innerHTML = rows.slice(0, 5).map((c, i) => `<div class="leader-row"><div class="rank-badge">${String(i + 1).padStart(2, '0')}</div><div><div class="leader-name">${esc(c.name)}</div><div class="leader-meta">${esc(c.industry)} · ${esc(c.location)}</div></div><div class="leader-sales">${moneyB(c.sales)}<small>reported sales</small></div></div>`).join('');
}
function renderSectors(rows) {
  const max = Math.max(...rows.map(x => x.sales));
  $('#sector-chart').innerHTML = rows.slice(0, 8).map(x => `<div class="bar-row"><span class="bar-name" title="${esc(x.industry)}">${esc(x.industry)}</span><div class="bar-track"><div class="bar-fill" style="width:${Math.max(2, x.sales / max * 100)}%"></div></div><span class="bar-val">$${fmtN(x.sales)}B</span></div>`).join('');
}
function openCompany(c) {
  const p = c.companyProfile;
  const profileFields = p ? [['Description', p.description], ['Founded', p.founded], ['Additional industry tags', p.industry], ['Headquarters', p.headquarters], ['Country', p.country], ['Employee count', p.employees], ['Ticker', p.ticker], ['Exchange', p.exchange]].filter(([, value]) => value) : [];
  const facts = (c.historicalFacts || []).slice().sort((a, b) => b.period.localeCompare(a.period)).slice(0, 12);
  const factsTable = facts.length ? `<h3 class="modal-section-title">Dated financial claims · supplemental</h3><div class="table-wrap"><table class="history-table"><thead><tr><th>METRIC</th><th>REPORTED VALUE</th><th>PERIOD</th></tr></thead><tbody>${facts.map(f => `<tr><td>${esc(f.metric)}</td><td>${esc(new Intl.NumberFormat('en-US', { maximumFractionDigits: 2 }).format(Number(f.amount)))} ${esc(f.unit)}</td><td>${esc(f.period)}</td></tr>`).join('')}</tbody></table></div><div class="modal-source">These are community-maintained claims, kept in reported currency and date. Values from different currencies or periods are not directly comparable. Check the source item before relying on a claim.</div>` : '';
  $('#modal-content').innerHTML = `<div class="eyebrow">PUBLIC COMPANY · GLOBAL 2000 RANK #${c.rank}</div><h2>${esc(c.name)}</h2><div class="modal-sub">${esc(c.industry)} · ${esc(c.location)}</div><div class="modal-grid">${[['Sales / revenue', moneyB(c.sales)], ['Profit / (loss)', moneyB(c.profit)], ['Profit margin', c.profitMargin == null ? 'Not available' : `${c.profitMargin}%`], ['Total assets', moneyB(c.assets)], ['Market value', moneyB(c.marketValue)], ['Source period', c.period]].map(([a, b]) => `<div class="modal-metric"><span>${a}</span><strong>${esc(b)}</strong></div>`).join('')}</div>${p ? `<h3 class="modal-section-title">Company profile · supplemental</h3><div class="modal-grid">${profileFields.map(([a, b]) => `<div class="modal-metric"><span>${esc(a)}</span><strong>${esc(b)}</strong></div>`).join('')}</div><div class="modal-source">Community-maintained profile matched by exact company name. Confirm identity and facts at <a href="${esc(p.sourceUrl)}" target="_blank" rel="noreferrer">Wikidata ${esc(p.wikidataId)}</a>. ${p.website ? `Website listed: <a href="${esc(p.website)}" target="_blank" rel="noreferrer">${esc(p.website)}</a>.` : ''} Employee facts may have different reporting dates.</div>` : '<div class="modal-source">No supplemental company profile matched in the current public profile source.</div>'}${factsTable}<div class="modal-source"><strong>Financial source:</strong> ${esc(c.source)}. USD billions, latest 12 months available as of 25 Apr 2025. This source does not contain multi-year financial statements or liabilities. Profit margin is calculated from reported profit ÷ reported sales.</div>`;
  $('#company-modal').classList.add('open');
  $('#company-modal').setAttribute('aria-hidden', 'false');
}
$('#modal-close').addEventListener('click', () => { $('#company-modal').classList.remove('open'); $('#company-modal').setAttribute('aria-hidden', 'true'); });
$('#company-modal').addEventListener('click', e => { if (e.target.id === 'company-modal') $('#modal-close').click(); });
document.addEventListener('keydown', e => { if (e.key === 'Escape') $('#modal-close').click(); });

let companyPage = 0, fundingPage = 0, searchTimer;
function renderPager(target, page, total, size, onChange) {
  const pages = Math.ceil(total / size);
  target.innerHTML = total ? `<span>Showing ${page * size + 1}–${Math.min(total, (page + 1) * size)} of ${fmtN(total)}</span><button ${page === 0 ? 'disabled' : ''} data-dir="-1">← Previous</button><button ${page >= pages - 1 ? 'disabled' : ''} data-dir="1">Next →</button>` : '';
  target.querySelectorAll('button').forEach(b => b.addEventListener('click', () => onChange(page + Number(b.dataset.dir))));
}
function renderCompanies(rows, total, page, size) {
  $('#company-count').textContent = `${fmtN(total)} companies`;
  $('#company-rows').innerHTML = rows.length ? rows.map(c => `<tr><td><a href="#" class="table-link company-open" data-name="${esc(c.name)}">${esc(c.name)}</a></td><td>${esc(c.industry)}</td><td>${esc(c.location)}</td><td>${moneyB(c.sales)}</td><td class="${(c.profit || 0) < 0 ? 'profit-negative' : 'profit-positive'}">${moneyB(c.profit)}</td><td>${c.profitMargin == null ? '—' : `${c.profitMargin}%`}</td><td>#${c.rank}</td></tr>`).join('') : '<tr><td colspan="7" class="empty">No companies match those filters.</td></tr>';
  renderPager($('#company-pager'), page, total, size, p => { companyPage = p; loadCompanies(); });
  $$('.company-open').forEach(a => a.addEventListener('click', async e => { e.preventDefault(); openCompany(await get(`/api/company?name=${encodeURIComponent(a.dataset.name)}`)); }));
}
async function loadCompanies() {
  const p = new URLSearchParams({ q: $('#company-search').value, industry: $('#industry-filter').value, country: $('#country-filter').value, page: companyPage });
  const d = await get(`/api/companies?${p}`);
  if (!$('#industry-filter').dataset.ready) {
    d.industries.forEach(v => $('#industry-filter').insertAdjacentHTML('beforeend', `<option>${esc(v)}</option>`));
    d.countries.forEach(v => $('#country-filter').insertAdjacentHTML('beforeend', `<option>${esc(v)}</option>`));
    $('#industry-filter').dataset.ready = '1';
  }
  renderCompanies(d.rows, d.total, d.page, d.pageSize);
}
['company-search', 'industry-filter', 'country-filter'].forEach(id => $('#' + id).addEventListener(id === 'company-search' ? 'input' : 'change', () => {
  clearTimeout(searchTimer); searchTimer = setTimeout(() => { companyPage = 0; loadCompanies(); }, 180);
}));

function renderFunding(rows, total, page, size) {
  $('#funding-count').textContent = `${fmtN(total)} records`;
  $('#funding-total').textContent = fmtN(total);
  $('#funding-rows').innerHTML = rows.length ? rows.map(r => `<tr><td>${esc(r.name || 'Unnamed startup')}</td><td>${esc(r.industry || 'Not specified')}${r.subIndustry ? `<div class="leader-meta">${esc(r.subIndustry)}</div>` : ''}</td><td>${esc(r.location || '—')}</td><td>${esc(r.date || '—')}</td><td>${esc(r.round || 'Not specified')}</td><td>${cash(r.amount)}</td><td>${esc(r.investors || 'Not disclosed')}</td></tr>`).join('') : '<tr><td colspan="7" class="empty">No funding records match those filters.</td></tr>';
  renderPager($('#funding-pager'), page, total, size, p => { fundingPage = p; loadFunding(); });
}
async function loadFunding() {
  const p = new URLSearchParams({ q: $('#funding-search').value, industry: $('#funding-industry').value, page: fundingPage });
  const d = await get(`/api/funding?${p}`);
  if (!$('#funding-industry').dataset.ready) {
    d.industries.forEach(v => $('#funding-industry').insertAdjacentHTML('beforeend', `<option>${esc(v)}</option>`));
    $('#funding-industry').dataset.ready = '1';
  }
  renderFunding(d.rows, d.total, d.page, d.pageSize);
}
['funding-search', 'funding-industry'].forEach(id => $('#' + id).addEventListener(id === 'funding-search' ? 'input' : 'change', () => {
  clearTimeout(searchTimer); searchTimer = setTimeout(() => { fundingPage = 0; loadFunding(); }, 180);
}));

$('#analyze-btn').addEventListener('click', async () => {
  const q = $('#idea-input').value.trim();
  if (!q) { $('#idea-input').focus(); return; }
  const btn = $('#analyze-btn'); btn.disabled = true; btn.textContent = 'Mapping the market…';
  try {
    const d = await get(`/api/idea?q=${encodeURIComponent(q)}`);
    const chips = d.classifications.length ? d.classifications.map(c => `<span class="class-chip">${esc(c.label)}<span>${Math.round(c.confidence * 100)}% signal</span></span>`).join('') : '<span class="class-chip">Explore across industries<span>no clear keyword signal</span></span>';
    const cards = d.matches.length ? d.matches.map(m => `<article class="match-card" ${m.recordType === 'public company' ? `data-company="${esc(m.name)}"` : ''}><div class="match-type">${esc(m.recordType)} · ${m.recordType === 'public company' ? 'Global 2000 rank #' + m.rank : esc(m.round || 'Funding record')}</div><h3>${esc(m.name || 'Unnamed company')}</h3><p>${esc(m.industry || 'Industry not specified')}${m.subIndustry ? ` · ${esc(m.subIndustry)}` : ''} · ${esc(m.location || 'Location not specified')}</p>${m.companyProfile?.description ? `<div class="match-detail">${esc(m.companyProfile.description)}</div>` : ''}<div class="match-detail">${m.recordType === 'public company' ? `Sales ${moneyB(m.sales)} · Profit / (loss) ${moneyB(m.profit)} · Margin ${m.profitMargin == null ? 'Not available' : `${m.profitMargin}%`} · Assets ${moneyB(m.assets)} · Market value ${moneyB(m.marketValue)}` : `Funding ${cash(m.amount)} · ${esc(m.date || 'Date not recorded')} · ${esc(m.investors || 'Investors not listed')} · ${esc(m.remarks || 'No remarks in source')}`}</div><div class="match-tags">${m.matchedTerms.map(t => `<span>text: ${esc(t)}</span>`).join('')}${m.sectorMatch ? '<span>sector match</span>' : ''}${m.matchScore > 0 ? `<span>${Math.round(m.matchScore * 100)}% text overlap</span>` : '<span>sector signal only · broad fit</span>'}${m.recordType === 'public company' ? '<span>click for full profile and source data</span>' : ''}</div></article>`).join('') : '<div class="empty">No keyword or sector signals matched the current source records. Try describing the product, customer, and problem, or search the company explorer.</div>';
    $('#idea-results').innerHTML = `<div class="result-head"><div><div class="eyebrow">YOUR MARKET MAP</div><h2>Companies and records to investigate</h2></div><span class="result-count">Top ${d.matches.length} dataset signals · not verified competitors</span></div><div class="classification-row">${chips || '<span class="class-chip">No clear sector signal <span>add product and customer details</span></span>'}</div><div class="match-grid">${cards}</div><div class="notice slim">${esc(d.modelNote)} Similarity uses the terms and sector fields shown on each record; it does not establish that a company sells the same product or competes directly. Public-company cards include all financial fields in the selected financial source and may include a separately labeled company profile. Current coverage combines the 2,000-company 2025 Global 2000 snapshot, 1,275 exact-name Wikidata profile candidates, and historical Indian startup funding records.</div>`;
    $$('.match-card[data-company]').forEach(el => el.addEventListener('click', async () => openCompany(await get(`/api/company?name=${encodeURIComponent(el.dataset.company)}`))));
  } catch (e) { $('#idea-results').innerHTML = `<div class="notice">${esc(e.message)}</div>`; }
  finally { btn.disabled = false; btn.innerHTML = 'Explore market <span>↗</span>'; }
});

async function init() {
  try {
    const d = await get('/api/overview');
    $('#stat-companies').textContent = fmtN(d.companyCount);
    $('#stat-countries').textContent = fmtN(d.globalCountries);
    $('#stat-industries').textContent = fmtN(d.industries);
    $('#stat-rounds').textContent = fmtN(d.startupRounds);
    $('#stat-sales').textContent = billions(d.totalSales);
    $('#funding-known').textContent = fmtN(d.fundingWithAmount);
    renderSectors(d.topSectors); renderLeaders(d.topCompanies); loadCompanies(); loadFunding();
  } catch (e) { document.querySelector('main').insertAdjacentHTML('beforeend', `<div class="notice">Unable to load the project data: ${esc(e.message)}</div>`); }
}
init();
