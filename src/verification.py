import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
records=json.loads((ROOT/"output/research.json").read_text())
by_name={x["app"].lower():x for x in records}

AUDIT=[
{
"app":"Google Ads",
"expected_auth":["OAuth2"],
"expected_api":"REST",
"finding":"OAuth 2.0 plus a developer access model undergoing transition.",
"source":"https://developers.google.com/google-ads/api/rest/auth",
"secondary":"https://developers.google.com/google-ads/api/docs/api-policy/developer-token"
},
{
"app":"Zendesk",
"expected_auth":["OAuth2","Basic","API token"],
"expected_api":"REST",
"finding":"OAuth is recommended; legacy API-token and Basic authentication have migration considerations.",
"source":"https://developer.zendesk.com/api-reference/introduction/security-and-auth/",
"secondary":"https://developer.zendesk.com/documentation/authentication/api-tokens-to-oauth/"
},
{
"app":"Shopify",
"expected_auth":["Access token"],
"expected_api":"REST and GraphQL",
"finding":"Scoped access tokens authenticate API requests. REST Admin API is legacy; GraphQL is the preferred direction.",
"source":"https://shopify.dev/docs/api/usage/authentication",
"secondary":"https://shopify.dev/docs/api/admin-graphql"
},
{
"app":"Apify",
"expected_auth":["API token"],
"expected_api":"REST",
"finding":"Public REST API with secret API-token authentication.",
"source":"https://docs.apify.com/integrations/api",
"secondary":"https://docs.apify.com/api/v2"
},
{
"app":"Notion",
"expected_auth":["API token","OAuth2"],
"expected_api":"REST",
"finding":"Internal connections use API tokens; external integrations can use OAuth. Workspace permissions affect access.",
"source":"https://www.notion.com/help/create-integrations-with-the-notion-api",
"secondary":"https://developers.notion.com/reference/intro"
},
{
"app":"Plaid",
"expected_auth":["Client ID","Secret","Access token"],
"expected_api":"REST",
"finding":"Client ID and secret identify the developer application; access tokens authorize access to linked Items.",
"source":"https://plaid.com/docs/quickstart/",
"secondary":"https://plaid.com/docs/api/"
}
]

def auth_hit(expected,actual):
    a=" ".join(actual).lower()
    aliases={
        "oauth2":["oauth"],
        "basic":["basic"],
        "api token":["api token","api key","bearer/token"],
        "access token":["bearer/token","access token"],
        "client id":["client id"],
        "secret":["secret"],
        "api key":["api key","api token"]
    }
    return any(term in a for e in expected for term in aliases.get(e.lower(),[e.lower()]))

report=[]
for item in AUDIT:
    found=by_name.get(item["app"].lower())
    actual=found or {}
    actual_auth=actual.get("auth_methods",[])
    report.append({
        **item,
        "agent_auth":actual_auth,
        "agent_api":actual.get("api_type","unknown"),
        "agent_status":actual.get("status","missing"),
        "agent_evidence_count":len(actual.get("evidence",[])),
        "auth_signal_overlap":auth_hit(item["expected_auth"],actual_auth),
        "human_source_review":"Reviewed against the listed official documentation",
        "limitations":"This is an authentication keyword-overlap check, not a full factual accuracy score."
    })

hits=sum(x["auth_signal_overlap"] for x in report)
result={
    "audit_type":"Manual official-source review plus automated signal comparison",
    "sample_size":len(report),
    "auth_signal_overlaps":hits,
    "auth_signal_non_overlaps":len(report)-hits,
    "overlap_rate":round(hits/len(report)*100,1),
    "accuracy_claimed":False,
    "records":report
}
(ROOT/"output"/"verification.json").write_text(json.dumps(result,indent=2))
(ROOT/"output"/"verification_report.md").write_text(
    "# Verification report\n\n"
    f"- Sample size: {len(report)}\n"
    f"- Authentication signal overlaps: {hits}\n"
    f"- Non-overlaps: {len(report)-hits}\n"
    f"- Signal overlap rate: {result['overlap_rate']}%\n"
    "- This is NOT an overall accuracy score.\n"
    "- Six records were cross-checked against official documentation.\n\n"
    + "\n".join(
        f"## {x['app']}\n"
        f"- Expected authentication: {', '.join(x['expected_auth'])}\n"
        f"- Agent authentication: {', '.join(x['agent_auth'])}\n"
        f"- Signal overlap: {'Yes' if x['auth_signal_overlap'] else 'No'}\n"
        f"- Finding: {x['finding']}\n"
        f"- Official source: {x['source']}\n"
        f"- Secondary source: {x['secondary']}\n"
        for x in report
    )
)
print(json.dumps({k:v for k,v in result.items() if k!="records"},indent=2))
print("\nCreated output/verification.json")
print("Created output/verification_report.md")
