import json
import requests
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

ROOT=Path(__file__).resolve().parent.parent
path=ROOT/"output/verification.json"
report=json.loads(path.read_text())

def check(record):
    results=[]
    for url in [record["source"],record["secondary"]]:
        try:
            r=requests.get(url,timeout=12,headers={"User-Agent":"Mozilla/5.0"})
            results.append({
                "url":url,
                "http_status":r.status_code,
                "reachable":r.status_code < 400,
                "title_present":"<title" in r.text.lower()
            })
        except Exception as e:
            results.append({"url":url,"reachable":False,"error":str(e)})
    return {"app":record["app"],"sources":results}

with ThreadPoolExecutor(max_workers=6) as pool:
    checked=list(pool.map(check,report["records"]))

report["url_reachability_check"]=checked
report["url_reachability_summary"]={
    "total_urls":sum(len(x["sources"]) for x in checked),
    "reachable":sum(s.get("reachable",False) for x in checked for s in x["sources"]),
    "failed":sum(not s.get("reachable",False) for x in checked for s in x["sources"])
}
report["human_source_review"]="Official documentation URLs selected for checking; HTTP reachability checked automatically. Manual content verification remains outstanding."
report["accuracy_claimed"]=False

path.write_text(json.dumps(report,indent=2))
print(json.dumps(report["url_reachability_summary"],indent=2))
print("Updated verification.json")
