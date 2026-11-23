import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
data=json.loads((ROOT/"output/research.json").read_text())
verification=json.loads((ROOT/"output/verification.json").read_text()) if (ROOT/"output/verification.json").exists() else {}
payload=json.dumps(data,ensure_ascii=False).replace("</","<\\/")

html=r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Composio | App Research Intelligence</title>
<style>
:root{--bg:#080b12;--panel:#111722;--line:#263143;--muted:#91a0b5;--text:#edf2fa;--green:#63dfae;--blue:#81aaff;--orange:#ffbf75}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);font:14px/1.6 Inter,-apple-system,BlinkMacSystemFont,sans-serif}
main{max-width:1450px;margin:auto;padding:35px 5% 70px}
header{border-bottom:1px solid var(--line);padding-bottom:30px}
.eyebrow{color:var(--green);font-weight:700;letter-spacing:2px;font-size:11px}
h1{font-size:clamp(32px,5vw,54px);line-height:1.08;letter-spacing:-2px;margin:14px 0}
h2{font-size:22px;letter-spacing:-.5px;margin:35px 0 15px}
p{color:var(--muted)}.sub{font-size:16px;max-width:800px}
.tag{display:inline-block;border:1px solid var(--line);border-radius:20px;padding:4px 10px;color:var(--muted);font-size:11px}
.metrics{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:25px 0}
.card,.panel{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:18px}
.metric{font-size:34px;font-weight:750;letter-spacing:-1px}.muted{color:var(--muted)}
.green{color:var(--green)}.orange{color:var(--orange)}.blue{color:var(--blue)}
.grid{display:grid;grid-template-columns:repeat(2,1fr);gap:14px}
.barrow{display:grid;grid-template-columns:130px 1fr 35px;align-items:center;gap:10px;margin:12px 0}
.track{height:8px;background:#263143;border-radius:10px;overflow:hidden}.fill{height:100%;background:var(--green);border-radius:10px}
.insights{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}
.insight{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:16px}
.insight strong{display:block;margin-bottom:7px}
.controls{display:flex;gap:10px;flex-wrap:wrap;margin:15px 0}
input,select{background:var(--panel);color:var(--text);border:1px solid var(--line);border-radius:8px;padding:11px}
input{flex:1;min-width:220px}
.tablewrap{overflow:auto;border:1px solid var(--line);border-radius:12px}
table{width:100%;border-collapse:collapse;min-width:1050px}
th,td{text-align:left;padding:12px;border-bottom:1px solid var(--line);vertical-align:top}
th{background:#151e2b;color:var(--muted);font-size:11px;text-transform:uppercase;letter-spacing:.7px}
td{font-size:12px}a{color:var(--blue);text-decoration:none}a:hover{text-decoration:underline}
.pill{border:1px solid var(--line);border-radius:20px;padding:3px 8px;white-space:nowrap;font-size:11px}
.evidence a{display:block;margin-bottom:5px;max-width:250px;overflow-wrap:anywhere}
footer{margin-top:40px;border-top:1px solid var(--line);padding-top:20px;color:var(--muted)}
@media(max-width:750px){main{padding:22px 4%}.metrics{grid-template-columns:repeat(2,1fr)}.grid,.insights{grid-template-columns:1fr}.barrow{grid-template-columns:105px 1fr 25px}}
</style>
</head>
<body><main>
<header>
<div class="eyebrow">INTEGRATION INTELLIGENCE / RESEARCH CASE STUDY</div>
<h1>Can this app become an <span class="green">AI agent toolkit?</span></h1>
<p class="sub">A documentation-first research pipeline evaluating authentication, developer access, API surface, MCP availability and integration buildability across a 90-app research set.</p>
<span class="tag">AUTOMATED DISCOVERY</span> <span class="tag">EVIDENCE-LINKED</span> <span class="tag">HUMAN REVIEW REQUIRED</span>
</header>
<section class="metrics" id="metrics"></section>
<h2>The findings at a glance</h2>
<div class="insights" id="insights"></div>
<h2>Research coverage by category</h2>
<div class="panel"><div id="categories"></div></div>
<div class="grid">
<section><h2>Authentication signals</h2><div class="panel" id="auth"></div></section>
<section><h2>Access signals</h2><div class="panel" id="access"></div></section>
</div>
<h2>Application research explorer</h2>
<p>Search, filter and inspect individual application records and their discovery evidence.</p>
<div class="controls">
<input id="search" placeholder="Search apps, categories, auth...">
<select id="category"><option value="">All categories</option></select>
<select id="status"><option value="">All evidence statuses</option><option value="researched">Evidence found</option><option value="needs_review">No evidence</option><option value="error">Error</option></select>
</div>
<div class="tablewrap"><table>
<thead><tr><th>App</th><th>Category</th><th>Authentication signals</th><th>Access signals</th><th>API</th><th>MCP signal</th><th>Evidence</th><th>Review</th></tr></thead>
<tbody id="rows"></tbody></table></div>
<h2>Verification snapshot</h2>
<div class="metrics" id="verification"></div>
<h2>How the research agent works</h2>
<div class="grid">
<div class="panel"><strong>01 / Discovery</strong><p>DuckDuckGo search queries discover developer documentation, authentication references, API pages and MCP mentions.</p></div>
<div class="panel"><strong>02 / Extraction</strong><p>Python rules extract authentication and API-related keyword signals. No LLM API calls are required.</p></div>
<div class="panel"><strong>03 / Evidence capture</strong><p>Search titles, snippets, domains and URLs are stored with every application record.</p></div>
<div class="panel"><strong>04 / Human verification</strong><p>Official documentation and credential-access requirements must be checked before upgrading a signal to a verified finding.</p></div>
</div>
<h2>Verification and limitations</h2>
<div class="panel">
<strong class="orange">Discovery is not verification.</strong>
<p id="limitations"></p>
<p>The current pipeline does not fetch and parse every official documentation page, validate credential issuance, test API requests or establish MCP functionality. Search snippets can be stale, incomplete or community-authored. No accuracy percentage is claimed at this stage.</p>
</div>
<footer>Composio App Research Intelligence · Research prototype · Generated from local research.json · Findings are preliminary and require source-level validation.</footer>
</main>
<script>
const DATA=__DATA__;
const VERIFICATION=__VERIFY__;

const count=DATA.length;
const found=DATA.filter(x=>x.evidence?.length).length;
const empty=count-found;
const unique=arr=>[...new Set(arr)];
const metrics=[
["Applications",count,"Research records"],
["Evidence discovered",found,"Search-result evidence"],
["No evidence returned",empty,"Requires further discovery"],
["Human review",DATA.filter(x=>x.needs_human_review).length,"Conservative review policy"]
];
document.getElementById("metrics").innerHTML=metrics.map((x,i)=>`<div class="card"><div class="muted">${x[0]}</div><div class="metric ${i===1?'green':i===2?'orange':''}">${x[1]}</div><div class="muted">${x[2]}</div></div>`).join("");
document.getElementById("insights").innerHTML=[
["Evidence coverage",`${found} of ${count} apps returned at least one search result. This measures discovery only.`],
["Verification gap","All application records remain flagged for human review. Search snippets cannot establish API behavior or access eligibility."],
["Next priority","Validate official documentation, auth flows, API permissions and MCP ownership before assigning buildability."]
].map(x=>`<div class="insight"><strong>${x[0]}</strong><span class="muted">${x[1]}</span></div>`).join("");
const vs=VERIFICATION.url_reachability_summary||{};
document.getElementById("verification").innerHTML=[
["Sample size",VERIFICATION.sample_size||0,"Apps compared"],
["Auth signal overlap",`${VERIFICATION.auth_signal_overlaps||0}/${VERIFICATION.sample_size||0}`,"Not overall accuracy"],
["URLs reachable",`${vs.reachable||0}/${vs.total_urls||0}`,"HTTP checks"],
["Accuracy claim","Not claimed","Human content review pending"]
].map(x=>`<div class="card"><div class="muted">${x[0]}</div><div class="metric">${x[1]}</div><div class="muted">${x[2]}</div></div>`).join("");
function bars(el,values){
let max=Math.max(1,...values.map(x=>x[1]));
el.innerHTML=values.map(x=>`<div class="barrow"><span>${x[0]}</span><div class="track"><div class="fill" style="width:${x[1]/max*100}%"></div></div><b>${x[1]}</b></div>`).join("");
}
const cats=unique(DATA.map(x=>x.category)).map(c=>[c,DATA.filter(x=>x.category===c).length]);
bars(document.getElementById("categories"),cats);
let auth={};
DATA.forEach(x=>(x.auth_methods||["unknown"]).forEach(a=>auth[a]=(auth[a]||0)+1));
bars(document.getElementById("auth"),Object.entries(auth).sort((a,b)=>b[1]-a[1]));
let access={};
DATA.forEach(x=>access[x.access_model||"unknown"]=(access[x.access_model||"unknown"]||0)+1);
bars(document.getElementById("access"),Object.entries(access).sort((a,b)=>b[1]-a[1]));
const category=document.getElementById("category");
cats.forEach(x=>category.add(new Option(x[0],x[0])));
function render(){
let q=document.getElementById("search").value.toLowerCase();
let c=category.value,s=document.getElementById("status").value;
let filtered=DATA.filter(x=>(!c||x.category===c)&&(!s||x.status===s)&&JSON.stringify(x).toLowerCase().includes(q));
document.getElementById("rows").innerHTML=filtered.map(x=>`<tr>
<td><strong>${x.app}</strong></td><td>${x.category}</td>
<td>${(x.auth_methods||["unknown"]).join(", ")}</td>
<td>${x.access_model||"unknown"}</td><td>${x.api_type||"unknown"}</td>
<td>${x.mcp_status||"unknown"}</td>
<td class="evidence">${(x.documentation_urls||[]).slice(0,4).map(u=>`<a href="${u}" target="_blank" rel="noopener">${u}</a>`).join("")||"No links returned"}</td>
<td><span class="pill">${x.status==="researched"?"Evidence found":"Review required"}</span></td>
</tr>`).join("")||'<tr><td colspan="8">No matching applications.</td></tr>';
}
["search","category","status"].forEach(id=>document.getElementById(id).addEventListener(id==="search"?"input":"change",render));
render();
document.getElementById("limitations").textContent=`${found} applications returned search evidence; ${empty} returned none. All ${count} records are flagged for human review. The current dataset contains ${count} applications, not the requested 100.`;
</script></body></html>"""
html=html.replace("__DATA__",payload)
html=html.replace("__VERIFY__",json.dumps(verification,ensure_ascii=False))
target=ROOT/"output"/"index.html"
target.write_text(html,encoding="utf-8")
print("Dashboard created:",target)
print("Records:",len(data))
print("Size:",target.stat().st_size,"bytes")
