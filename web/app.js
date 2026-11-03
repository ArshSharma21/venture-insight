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

function renderFunding(rows, total, page, size, scope, indiaRounds, globalRounds, withAmount) {
  $('#funding-count').textContent = `${fmtN(total)} records`;
  $('#funding-total').textContent = fmtN(total);
  $('#funding-known').textContent = fmtN(withAmount);
  $('#funding-period').textContent = scope === 'india' ? '2015–2020' : scope === 'global' ? '2019–Jun 2026' : '2015–Jun 2026';
  $('#funding-coverage').textContent = scope === 'india' ? 'India' : scope === 'global' ? `${fmtN(globalRounds)} sample rounds` : `India + ${fmtN(globalRounds)} global sample rounds`;
  $('#funding-rows').innerHTML = rows.length ? rows.map(r => `<tr><td>${esc(r.name || 'Unnamed startup')}</td><td>${esc(r.industry || 'Not specified')}${r.subIndustry ? `<div class="leader-meta">${esc(r.subIndustry)}</div>` : ''}</td><td>${esc(r.location || '—')}</td><td>${esc(r.date || '—')}</td><td>${esc(r.round || 'Not specified')}</td><td>${cash(r.amount)}${r.amountStatus && r.market === 'Global' ? `<div class="leader-meta">${esc(r.amountStatus)}</div>` : ''}</td><td>${esc(r.investors || 'Not disclosed')}</td><td>${r.sourceUrl?.startsWith('https://') ? `<a href="${esc(r.sourceUrl)}" target="_blank" rel="noreferrer">${esc(r.market)} source ↗</a>` : esc(r.source || 'Source not recorded')}<small>${esc(r.newsSource || r.source || '')}</small></td></tr>`).join('') : '<tr><td colspan="8" class="empty">No funding records match those filters.</td></tr>';
  renderPager($('#funding-pager'), page, total, size, p => { fundingPage = p; loadFunding(); });
}
async function loadFunding() {
  const p = new URLSearchParams({ q: $('#funding-search').value, industry: $('#funding-industry').value, scope: $('#funding-scope').value, page: fundingPage });
  const d = await get(`/api/funding?${p}`);
  if (!$('#funding-industry').dataset.ready) {
    d.industries.forEach(v => $('#funding-industry').insertAdjacentHTML('beforeend', `<option>${esc(v)}</option>`));
    $('#funding-industry').dataset.ready = '1';
  }
  renderFunding(d.rows, d.total, d.page, d.pageSize, d.scope, d.indiaRounds, d.globalRounds, d.withAmount);
}
['funding-search', 'funding-industry', 'funding-scope'].forEach(id => $('#' + id).addEventListener(id === 'funding-search' ? 'input' : 'change', () => {
  clearTimeout(searchTimer); searchTimer = setTimeout(() => { fundingPage = 0; loadFunding(); }, 180);
}));

$('#analyze-btn').addEventListener('click', async () => {
  const q = $('#idea-input').value.trim();
  if (!q) { $('#idea-input').focus(); return; }
  const btn = $('#analyze-btn'); btn.disabled = true; btn.textContent = 'Mapping the market…';
  try {
    const method = $('#classifier-method').value;
    const d = await get(`/api/idea?q=${encodeURIComponent(q)}&method=${method}`);
    const renderChips = items => items.length ? items.map(c => `<span class="class-chip">${esc(c.label)}<span>${c.score != null ? `score ${Number(c.score).toFixed(2)} · ${esc(c.scoreType || 'model score')}` : `${Math.round((c.signal || 0) * 100)}% rule signal`}</span></span>`).join('') : '<span class="class-chip">No signal<span>this method returned no sector matches</span></span>';
    const chips = renderChips(d.classifications);
    const comparingRules = d.method === 'ml';
    const comparison = renderChips(comparingRules ? d.ruleBaseline : d.mlComparison);
    const sourceLink = m => m.sourceUrl && m.sourceUrl.startsWith('https://') ? `<a href="${esc(m.sourceUrl)}" target="_blank" rel="noreferrer">Open source ↗</a>` : esc(m.source || 'Source not recorded');
    const scoreCell = m => `<td class="recommendation-percent"><strong>${Number(m.matchPercent ?? m.matchScore * 100).toFixed(1)}%</strong><div class="similarity-track"><i style="width:${Math.max(0, Math.min(100, m.matchPercent ?? m.matchScore * 100))}%"></i></div><small>text similarity</small></td>`;
    const startupRows = d.startupMatches.map(m => `<tr><td><strong>${esc(m.name)}</strong><small>${esc(m.recordType === 'global startup' ? 'Global startup' : 'India startup')}</small>${m.contextSnippet ? `<p class="recommendation-context">${esc(m.contextSnippet.slice(0, 200))}${m.contextSnippet.length > 200 ? '…' : ''}</p>` : ''}</td>${scoreCell(m)}<td>${esc(m.industry || 'Sector not recorded')}<small>${esc(m.location || 'Location not recorded')}${m.foundedYear ? ` · Founded ${m.foundedYear}` : ''}</small></td><td>${esc(m.round || 'Round not recorded')}<small>${esc(m.date || 'Date not recorded')}${m.amount != null ? ` · ${cash(m.amount)}` : m.recordType === 'global startup' ? ' · Amount not verified' : ' · Not disclosed'}${m.roundCount ? ` · ${m.roundCount} source rounds` : ''}</small></td><td>${sourceLink(m)}<small>${esc(m.newsSource ? `News source: ${m.newsSource}` : m.source || '')}</small></td></tr>`).join('');
    const startupTable = startupRows ? `<div class="table-wrap recommendation-wrap"><table class="recommendation-table"><thead><tr><th>RECOMMENDED STARTUP</th><th>MATCH TO YOUR DESCRIPTION</th><th>SECTOR / MARKET</th><th>LATEST FUNDING SIGNAL</th><th>SOURCE</th></tr></thead><tbody>${startupRows}</tbody></table></div>` : '<div class="empty">No startup text matched this description in the downloaded source snapshot. Try adding a product, customer, or problem detail.</div>';
    const companyRows = d.companyMatches.map(m => `<tr class="company-recommendation" data-company="${esc(m.name)}"><td><strong>${esc(m.name)}</strong><small>Established public company · Global 2000</small>${m.companyProfile?.description ? `<p class="recommendation-context">${esc(m.companyProfile.description)}</p>` : ''}</td>${scoreCell(m)}<td>${esc(m.industry)}<small>${esc(m.location)}</small></td><td>Sales ${moneyB(m.sales)}<small>Profit / (loss) ${moneyB(m.profit)} · USD billions</small></td><td>${sourceLink(m)}<small>click row for full profile</small></td></tr>`).join('');
    const companyTable = companyRows ? `<div class="table-wrap recommendation-wrap"><table class="recommendation-table"><thead><tr><th>PUBLIC COMPANY COMPARATOR</th><th>MATCH TO YOUR DESCRIPTION</th><th>INDUSTRY / HQ</th><th>FINANCIAL SNAPSHOT</th><th>SOURCE</th></tr></thead><tbody>${companyRows}</tbody></table></div>` : '<div class="empty">No public-company text match was found in the current dataset.</div>';
    const catalog = d.catalog || {};
    const classifierLabel = d.catalog?.globalStartupProfiles ? `${fmtN(catalog.startupProfiles)} startup profiles searched, including ${fmtN(catalog.globalStartupProfiles)} profiles from the global funding sample` : 'Global startup sample not downloaded; only available local profiles can be searched';
    $('#idea-results').innerHTML = `<div class="result-head"><div><div class="eyebrow">YOUR MARKET MAP · ${esc(d.classifierName)}</div><h2>Startup recommendations</h2></div><span class="result-count">${d.startupMatches.length} results · ${esc(classifierLabel)}</span></div><h3 class="recommendation-heading">Startup recommendations · ranked by description similarity</h3>${startupTable}<h3 class="recommendation-heading">Established public-company comparators</h3>${companyTable}<div class="classifier-results"><div class="eyebrow">${d.method === 'ml' ? 'SUPERVISED CLASSIFIER OUTPUT' : 'SELECTED CLASSIFIER OUTPUT'}</div><div class="classification-row">${chips}</div><div class="eyebrow">${comparingRules ? 'KEYWORD RULE BASELINE · COMPARISON' : 'SUPERVISED CLASSIFIER · COMPARISON'}</div><div class="classification-row">${comparison}</div></div><div class="notice slim">${esc(d.modelNote)} Each match percentage is TF-IDF cosine text similarity scaled from 0–100, not a probability that the startup matches, succeeds, or competes directly. Global company descriptions are represented by funding-news excerpts where available. Funding amounts appear only when the source marks them verified; open the linked source to inspect context.</div>`;
    $$('.company-recommendation[data-company]').forEach(el => el.addEventListener('click', async () => openCompany(await get(`/api/company?name=${encodeURIComponent(el.dataset.company)}`))));
  } catch (e) { $('#idea-results').innerHTML = `<div class="notice">${esc(e.message)}</div>`; }
  finally { btn.disabled = false; btn.innerHTML = 'Explore market <span>↗</span>'; }
});

async function init() {
  try {
    const d = await get('/api/overview');
    $('#stat-companies').textContent = fmtN(d.companyCount);
    $('#stat-countries').textContent = fmtN(d.globalCountries);
    $('#stat-industries').textContent = fmtN(d.industries);
    $('#stat-rounds').textContent = fmtN(d.globalStartupProfiles);
    $('#stat-sales').textContent = billions(d.totalSales);
    $('#funding-known').textContent = fmtN(d.fundingWithAmount);
    renderSectors(d.topSectors); renderLeaders(d.topCompanies); loadCompanies(); loadFunding();
    loadModelComparison();
  } catch (e) { document.querySelector('main').insertAdjacentHTML('beforeend', `<div class="notice">Unable to load the project data: ${esc(e.message)}</div>`); }
}

async function loadModelComparison() {
  try {
    const { metrics, activeModel, mlAvailable } = await get('/api/model');
    const rows = metrics.algorithms || [];
    const panel = $('#model-comparison');
    if (!panel) return;
    if (!mlAvailable || !rows.length) {
      panel.innerHTML = `<div class="notice">ML classifier is not trained yet. ${esc(metrics.message || 'Run the documented training command to enable it.')}</div>`;
      $('#classifier-method').options[0].text = 'ML unavailable — using rules';
      return;
    }
    const score = x => x == null ? '—' : `${(x * 100).toFixed(1)}%`;
    const sourceSummary = Object.entries(metrics.corpus.sourceCounts || {}).map(([name, count]) => `${fmtN(count)} ${name}`).join(' · ');
    panel.innerHTML = `<div class="panel-head"><div><h3>Classifier comparison</h3><p>Final test: ${metrics.holdout.records} records · winner selected on validation macro-F1</p></div><span class="result-count">Active: ${esc(activeModel)}</span></div><div class="model-rows">${rows.map(row => `<div class="model-row"><strong>${esc(row.name)}</strong><span>Accuracy ${score(row.accuracy)}</span><span>Macro-F1 ${score(row.macroF1)}</span><div class="bar-track"><div class="bar-fill" style="width:${Math.max(0, Math.min(100, (row.macroF1 || row.accuracy || 0) * 100))}%"></div></div></div>`).join('')}</div><p class="model-caveat">${esc(metrics.caveat || '')} Corpus: ${fmtN(metrics.corpus.records)} weak-labeled records. Sources: ${esc(sourceSummary)}.</p>`;
  } catch (e) { $('#model-comparison').innerHTML = `<div class="notice">Could not load classifier metrics: ${esc(e.message)}</div>`; }
}
init();
