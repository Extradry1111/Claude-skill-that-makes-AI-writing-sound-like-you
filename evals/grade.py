import json, re, subprocess, sys, os
W=os.path.dirname(os.path.abspath(__file__)); I=sys.argv[1] if len(sys.argv)>1 else W+"/iteration-1"; S="/home/user/new/unslop/scripts/unslop.py"
def run(*a):
    return json.loads(subprocess.run(["python3",S,*a,"--json"],capture_output=True,text=True).stdout)
subprocess.run(["python3",S,"voice",W+"/inputs/voice_sample_1.txt",W+"/inputs/voice_sample_2.txt","-o",W+"/voice.json","--json"],capture_output=True)
def A(text,passed,ev): return {"text":text,"passed":bool(passed),"evidence":ev}
evals={"boss-email":1,"linkedin-in-my-voice":2,"cover-letter-from-scratch":3,"roast-paragraph":4}
for name,eid in evals.items():
    asserts_meta=[]
    for cfg in ("with_skill","without_skill"):
        d=f"{I}/{name}/{cfg}"; f=d+"/outputs/final.txt"; t=open(f).read(); resp=open(d+"/outputs/response.md").read()
        ex=[]
        if name!="roast-paragraph":
            sc=run("scan",f)["score"]; wc=len(t.split())
            ex.append(A("Final text Slop Score <= 15 (HUMAN)",sc<=15,f"score {sc}"))
        if name=="boss-email":
            lk=run("lock",W+"/inputs/slop_email.txt",f)
            ex.append(A("$45,000 and October 14 survive the rewrite","45,000" in t and ("October 14" in t or "Oct 14" in t),"checked substrings"))
            ex.append(A("Fact Lock passes vs original (no lost/invented numbers)",not lk["missing"].get("numbers") and not lk["invented_numbers"],json.dumps({k:v for k,v in lk.items() if k!='checked'})))
            ex.append(A("Email ends with a concrete ask (contains a question to Sarah)","?" in t.split("Sarah",1)[-1],"question mark present" if "?" in t else "no question"))
            ex.append(A("Email body under 120 words",wc<120,f"{wc} words"))
        if name=="linkedin-in-my-voice":
            facts=["Northwind","Contoso","40,000","1.2M"]; miss=[x for x in facts if x not in t]
            ex.append(A("Keeps Northwind, Contoso, 40,000, 1.2M",not miss,f"missing {miss}"))
            ex.append(A("Keeps job title Head of Growth (any case)","head of growth" in t.lower(),""))
            vm=run("voicecheck",f,"--profile",W+"/voice.json")["match"]
            ex.append(A("Voice match >= 80% against the user's voiceprint",vm>=80,f"match {vm}%"))
            ex.append(A("No emoji, no staircase of one-line paragraphs",not re.search("[\U0001F300-\U0001FAFF]",t) and run("scan",f)["rhythm"]["one_line_paragraph_ratio"]<=0.6,""))
        if name=="cover-letter-from-scratch":
            ex.append(A("Length 180-320 words",180<=wc<=320,f"{wc} words"))
            bad=[p for p in ["passionate","I am writing to express","fast-paced","thrilled","excited to apply"] if p.lower() in t.lower()]
            ex.append(A("No cover-letter cliches (passionate, I am writing to express, fast-paced...)",not bad,f"found {bad}"))
            nums=set(re.findall(r"\d[\d,.]*%?",t))-{"6"}
            ex.append(A("No invented metrics (only numbers the user gave)",not nums,f"extra numbers {sorted(nums)}"))
            ex.append(A("Mentions UC Davis, Wells Fargo, Tableau, retention team",all(x.lower() in t.lower() for x in ["UC Davis","Wells Fargo","Tableau","retention"]),""))
        if name=="roast-paragraph":
            ex.append(A("Gives a clear verdict that it reads as AI",re.search(r"\b(yes|reads as AI|sounds AI|AI[- ]written|AI[- ]generated)",resp,re.I) is not None,""))
            quotes=[q for q in ["today's","pivotal","not just a tool","from healthcare","moreover","actionable insights","important to note","navigate"] if q in resp.lower()]
            ex.append(A("Quotes at least 5 specific tells from the paragraph",len(quotes)>=5,f"{len(quotes)}: {quotes}"))
            ex.append(A("Reports a measurable score",re.search(r"\b\d{1,3}\s*/\s*100|score",resp,re.I) is not None,""))
        p=sum(e["passed"] for e in ex)
        json.dump({"expectations":ex,"summary":{"passed":p,"failed":len(ex)-p,"total":len(ex),"pass_rate":round(p/len(ex),2)}},open(d+"/grading.json","w"),indent=2)
        asserts_meta=[e["text"] for e in ex]
        print(f"{name:28} {cfg:14} {p}/{len(ex)}", "|", "; ".join(("PASS " if e['passed'] else "FAIL ")+e['text'][:40]+" ("+e['evidence'][:40]+")" for e in ex if not e['passed']))
    json.dump({"eval_id":eid,"eval_name":name,"prompt":"","assertions":asserts_meta},open(f"{I}/{name}/eval_metadata.json","w"),indent=2)
