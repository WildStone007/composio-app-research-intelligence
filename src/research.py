import json, re, argparse, time
from pathlib import Path
from urllib.parse import urlparse
from ddgs import DDGS

ROOT = Path(__file__).resolve().parent.parent
DATA, OUT = ROOT / "data", ROOT / "output"
DATA.mkdir(exist_ok=True)
OUT.mkdir(exist_ok=True)

APPS = [
("Salesforce","CRM"),("HubSpot","CRM"),("Pipedrive","CRM"),("Attio","CRM"),("Twenty","CRM"),("Podio","CRM"),("Zoho CRM","CRM"),("Close","CRM"),("Copper","CRM"),("DealCloud","CRM"),
("Zendesk","Support"),("Intercom","Support"),("Freshdesk","Support"),("Front","Support"),("Pylon","Support"),("LiveAgent","Support"),("Plain","Support"),("Help Scout","Support"),("Gorgias","Support"),("Gladly","Support"),
("Slack","Communications"),("Twilio","Communications"),("Zoho Cliq","Communications"),("Lark","Communications"),("Pumble","Communications"),("Discord","Communications"),("Telegram","Communications"),("WhatsApp Business","Communications"),("Aircall","Communications"),("Vonage","Communications"),
("Google Ads","Marketing"),("Meta Ads","Marketing"),("LinkedIn Ads","Marketing"),("GoHighLevel","Marketing"),("Mailchimp","Marketing"),("Klaviyo","Marketing"),("systeme.io","Marketing"),("Pinterest","Marketing"),("Threads","Marketing"),("SendGrid","Marketing"),
("Shopify","Ecommerce"),("WooCommerce","Ecommerce"),("BigCommerce","Ecommerce"),("Salesforce Commerce Cloud","Ecommerce"),("Magento Adobe Commerce","Ecommerce"),("Squarespace","Ecommerce"),("Ecwid","Ecommerce"),("Gumroad","Ecommerce"),("Amazon Selling Partner API","Ecommerce"),("Fanbasis","Ecommerce"),
("DataForSEO","Data & SEO"),("SE Ranking","Data & SEO"),("Ahrefs","Data & SEO"),("MrScraper","Data & SEO"),("Apify","Data & SEO"),("Firecrawl","Data & SEO"),("Bright Data","Data & SEO"),("Sherlock","Data & SEO"),("Waterfall.io","Data & SEO"),("Clay","Data & SEO"),
("GitHub","Developer & Infra"),("Vercel","Developer & Infra"),("Netlify","Developer & Infra"),("Cloudflare","Developer & Infra"),("Supabase","Developer & Infra"),("Neo4j","Developer & Infra"),("Snowflake","Developer & Infra"),("MongoDB Atlas","Developer & Infra"),("Datadog","Developer & Infra"),("Sentry","Developer & Infra"),
("Notion","Productivity"),("Airtable","Productivity"),("Linear","Productivity"),("Jira","Productivity"),("Asana","Productivity"),("Monday.com","Productivity"),("ClickUp","Productivity"),("Coda","Productivity"),("Smartsheet","Productivity"),("Harvest","Productivity"),
("Stripe","Finance"),("Plaid","Finance"),("Binance","Finance"),("Paygent Connect","Finance"),("iPayX","Finance"),("QuickBooks","Finance"),("Xero","Finance"),("Brex","Finance"),("Ramp","Finance"),("PitchBook","Finance"),
("NotebookLM","AI, Research & Media-native"),
("Otter AI","AI, Research & Media-native"),
("Fathom","AI, Research & Media-native"),
("Consensus","AI, Research & Media-native"),
("Reducto","AI, Research & Media-native"),
("Devin","AI, Research & Media-native"),
("higgsfield","AI, Research & Media-native"),
("Mermaid CLI","AI, Research & Media-native"),
("YouTube Transcript","AI, Research & Media-native"),
("Grain","AI, Research & Media-native")
]

apps = [{"id":i+1,"app":a,"category":c} for i,(a,c) in enumerate(APPS)]
(DATA / "apps.json").write_text(json.dumps(apps,indent=2))

def discover(app):
    queries = [
        f"{app} official API developer documentation authentication",
        f"{app} API docs OAuth API key MCP"
    ]
    results = {}
    try:
        with DDGS() as ddgs:
            for query in queries:
                for r in ddgs.text(query,max_results=5):
                    url = r.get("href","")
                    if url:
                        results[url] = {
                            "title":r.get("title",""),
                            "url":url,
                            "snippet":r.get("body","")
                        }
    except Exception as e:
        return [], str(e)
    return list(results.values())[:10], None

def classify(item, evidence):
    text = " ".join(
        [item["app"]] +
        [x["title"]+" "+x["snippet"]+" "+x["url"] for x in evidence]
    ).lower()
    urls = [x["url"] for x in evidence]
    domains = list(dict.fromkeys(urlparse(u).netloc.replace("www.","") for u in urls))

    auth = []
    for name, pattern in [
        ("OAuth2",r"oauth ?2|oauth"),
        ("API key",r"api.?key|x-api-key"),
        ("Basic",r"basic authentication|http basic"),
        ("Bearer/token",r"bearer token|access token|personal access token")
    ]:
        if re.search(pattern,text):
            auth.append(name)

    api_type = "unknown"
    rest = bool(re.search(r"\brest api\b|restful|/api/v[0-9]",text))
    graphql = "graphql" in text
    if rest and graphql:
        api_type = "both"
    elif rest:
        api_type = "REST"
    elif graphql:
        api_type = "GraphQL"
    elif re.search(r"api documentation|developer api",text):
        api_type = "unknown"

    mcp = "unknown"
    if re.search(r"official.{0,35}mcp|mcp.{0,35}official",text):
        mcp = "possible_official_mention_needs_verification"
    elif "mcp" in text:
        mcp = "mention_found_needs_verification"
    else:
        mcp = "not_found_in_search"

    official_hints = [d for d in domains if any(
        x in d for x in [item["app"].lower().replace(" ",""),"developer","docs."]
    )]
    access = "unknown"
    if re.search(r"contact sales|partner program|request access",text):
        access = "possible_gated_needs_verification"
    elif re.search(r"free trial|free tier|sign up free",text):
        access = "possible_self_serve_needs_verification"

    return {
        "description":f"{item['app']} is listed in the {item['category']} category; product description requires documentation review.",
        "auth_methods":auth or ["unknown"],
        "access_model":access,
        "api_type":api_type,
        "api_breadth":"unknown",
        "mcp_status":mcp,
        "buildability":"needs_human_assessment",
        "main_blocker":"Authentication, API permissions, endpoint coverage and credential access need confirmation from official documentation.",
        "documentation_urls":urls,
        "search_domains":domains,
        "possible_official_domains":official_hints,
        "confidence":"low",
        "needs_human_review":True,
        "reasoning":"Rule-based keyword extraction from search results only. No claim is considered verified.",
        "evidence":evidence,
        "status":"researched" if evidence else "needs_review"
    }

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--limit",type=int,default=0)
    args=parser.parse_args()
    selected=apps[:args.limit] if args.limit else apps
    output=OUT/"research.json"
    existing={}
    if output.exists():
        try:
            existing={x["id"]:x for x in json.loads(output.read_text())}
        except Exception:
            pass
    results=[]
    print(f"Free research pipeline: {len(selected)} apps")
    for item in selected:
        if item["id"] in existing and existing[item["id"]].get("status")=="researched":
            results.append(existing[item["id"]])
            continue
        print(f"Researching {item['id']}/ {item['app']}...")
        evidence,error=discover(item["app"])
        result={**item,**classify(item,evidence)}
        if error:
            result["search_error"]=error
        results.append(result)
        output.write_text(json.dumps(results,indent=2,ensure_ascii=False))
        time.sleep(0.5)
    print("\nResearch run finished.")
    print("Processed:",len(results))
    print("With evidence:",sum(bool(x.get("evidence")) for x in results))
    print("Needs review:",sum(x.get("needs_human_review",True) for x in results))
    print("Saved:",output)

if __name__=="__main__":
    main()
