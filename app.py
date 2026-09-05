from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import json
from datetime import datetime, timezone

TX = [
 {"id":"TX-10482","amount":84500,"account":"ACC-1042","device":"DEV-77","ip":"10.24.8.91","location":"Mumbai, IN","velocity":6,"label":"suspicious"},
 {"id":"TX-10481","amount":1299,"account":"ACC-2091","device":"DEV-21","ip":"10.10.3.44","location":"Kochi, IN","velocity":1,"label":"normal"},
 {"id":"TX-10480","amount":22500,"account":"ACC-1042","device":"DEV-77","ip":"10.24.8.91","location":"Mumbai, IN","velocity":5,"label":"suspicious"},
 {"id":"TX-10479","amount":799,"account":"ACC-3018","device":"DEV-12","ip":"10.12.4.21","location":"Bengaluru, IN","velocity":1,"label":"normal"},
 {"id":"TX-10478","amount":68000,"account":"ACC-7788","device":"DEV-92","ip":"10.24.8.91","location":"Delhi, IN","velocity":4,"label":"suspicious"},
 {"id":"TX-10477","amount":3499,"account":"ACC-1190","device":"DEV-43","ip":"10.11.2.18","location":"Chennai, IN","velocity":2,"label":"normal"},
 {"id":"TX-10476","amount":15200,"account":"ACC-5521","device":"DEV-66","ip":"10.18.7.20","location":"Pune, IN","velocity":2,"label":"normal"},
 {"id":"TX-10475","amount":91500,"account":"ACC-8841","device":"DEV-77","ip":"10.24.8.91","location":"Hyderabad, IN","velocity":7,"label":"suspicious"},
 {"id":"TX-10474","amount":999,"account":"ACC-4220","device":"DEV-08","ip":"10.14.1.17","location":"Kolkata, IN","velocity":1,"label":"normal"},
 {"id":"TX-10473","amount":4200,"account":"ACC-6612","device":"DEV-51","ip":"10.16.2.10","location":"Mumbai, IN","velocity":2,"label":"normal"},
]
AUDIT=[]

def score(t):
    checks=[(t["amount"]>=50000,"Unusual transaction amount",25),
            (t["device"]=="DEV-77","Device linked to multiple accounts",20),
            (t["ip"]=="10.24.8.91","Shared IP across related activity",15),
            (t["velocity"]>=5,"High transaction velocity",20),
            (t["location"] in ("Delhi, IN","Hyderabad, IN"),"Location anomaly",10),
            (t["label"]=="suspicious","Suspicious behavioral pattern",10)]
    sig=[{"name":n,"points":p} for ok,n,p in checks if ok]
    s=min(100,sum(x["points"] for x in sig))
    sev="CRITICAL" if s>=80 else "HIGH" if s>=60 else "MEDIUM" if s>=30 else "LOW"
    return s,sev,sig

def related(t):
    return [x for x in TX if x["id"]!=t["id"] and (x["device"]==t["device"] or x["ip"]==t["ip"] or x["account"]==t["account"])]

def investigate(t):
    s,sev,sig=score(t); r=related(t)
    accounts=sorted({t["account"],*(x["account"] for x in r)})
    action="MANUAL_REVIEW" if s>=80 else "REVIEW" if s>=60 else "ALLOW"
    return {"transaction":t,"score":s,"severity":sev,"signals":sig,"related":r,"accounts":accounts,
            "devices":sorted({t["device"],*(x["device"] for x in r)}),
            "ips":sorted({t["ip"],*(x["ip"] for x in r)}),
            "summary":f"The transaction triggered {len(sig)} risk signals and is connected to {len(r)} related transaction(s). Shared infrastructure and behavioral anomalies indicate a pattern requiring {action.replace('_',' ').lower()}.",
            "recommendedAction":action}

class H(BaseHTTPRequestHandler):
    def js(self,o,status=200):
        b=json.dumps(o).encode(); self.send_response(status); self.send_header("Content-Type","application/json"); self.send_header("Content-Length",str(len(b))); self.end_headers(); self.wfile.write(b)
    def do_GET(self):
        p=urlparse(self.path); q=parse_qs(p.query)
        if p.path=="/": return self.page()
        if p.path=="/api/transactions":
            return self.js([{**t,"riskScore":score(t)[0],"severity":score(t)[1]} for t in TX])
        if p.path=="/api/summary":
            ss=[score(t)[0] for t in TX]; return self.js({"total":len(TX),"high":sum(x>=60 for x in ss),"medium":sum(30<=x<60 for x in ss),"avg":round(sum(ss)/len(ss),1)})
        if p.path=="/api/investigate":
            t=next((x for x in TX if x["id"]==q.get("id",[""])[0]),None); return self.js(investigate(t) if t else {"error":"not found"},200 if t else 404)
        if p.path=="/api/audit": return self.js(AUDIT)
        return self.js({"error":"not found"},404)
    def do_POST(self):
        if self.path=="/api/action":
            n=int(self.headers.get("Content-Length",0)); d=json.loads(self.rfile.read(n) or "{}")
            e={"time":datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),"transactionId":d.get("id"),"action":d.get("action"),"actor":"Risk Operator"}
            AUDIT.insert(0,e); return self.js({"ok":True,"event":e})
        return self.js({"error":"not found"},404)
    def log_message(self,*a): pass
    def page(self):
        b=HTML.encode(); self.send_response(200); self.send_header("Content-Type","text/html; charset=utf-8"); self.send_header("Content-Length",str(len(b))); self.end_headers(); self.wfile.write(b)

HTML = r"""<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>RazorShield AI</title>
<style>
*{box-sizing:border-box}body{margin:0;background:#071018;color:#e8f0f5;font:14px system-ui,-apple-system,sans-serif}.app{display:flex;min-height:100vh}.side{width:225px;background:#0b151e;border-right:1px solid #20303a;padding:26px 16px;position:fixed;inset:0 auto 0 0}.brand{font-size:20px;font-weight:800;margin:0 8px 35px}.brand span{color:#31d2a0}.nav{padding:12px;border-radius:9px;color:#8296a3;margin:5px 0}.active{background:#12232c;color:white}.main{margin-left:225px;width:calc(100% - 225px);padding:30px}.top{display:flex;justify-content:space-between;align-items:center;margin-bottom:24px}.eyebrow,.label{color:#7e929f;font-size:11px;text-transform:uppercase;letter-spacing:1.2px}.title{font-size:28px;font-weight:800;margin-top:4px}.live{padding:8px 12px;border-radius:18px;background:#0d2a25;color:#50dfb2;border:1px solid #205547}.cards{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-bottom:18px}.card,.panel{background:#0d1922;border:1px solid #1d2d37;border-radius:13px}.card{padding:18px}.num{font-size:28px;font-weight:800;margin-top:7px}.red{color:#ff6d72}.yellow{color:#ffc95b}.green{color:#52ddb0}.grid{display:grid;grid-template-columns:1.45fr 1fr;gap:18px}.head{padding:16px 18px;border-bottom:1px solid #1d2d37;display:flex;justify-content:space-between}.table{width:100%;border-collapse:collapse}.table th,.table td{padding:12px 14px;text-align:left;border-bottom:1px solid #182731}.table th{font-size:10px;color:#718592;text-transform:uppercase}.table tr:hover{background:#10202a;cursor:pointer}.badge{padding:5px 7px;border-radius:6px;font-size:10px;font-weight:800}.high,.critical{background:#39191c;color:#ff777c}.medium{background:#3a2b11;color:#ffd064}.low{background:#102d25;color:#59dfb1}.case{padding:19px}.score{font-size:46px;font-weight:850;margin-top:4px}.bar{height:7px;background:#1b2a33;border-radius:8px;margin:10px 0 18px;overflow:hidden}.bar i{display:block;height:100%;background:#ff626a}.sig{display:flex;justify-content:space-between;padding:10px 0;border-bottom:1px solid #182731}.pts{color:#ff8a8e;font-weight:800}.summary{margin-top:7px;padding:12px;border:1px solid #203540;background:#101f28;border-radius:9px;color:#b8c8d0;line-height:1.5}.btn{border:1px solid #2b424f;background:#14242e;color:#dce8ed;padding:8px 10px;border-radius:8px;margin:12px 5px 0 0}.primary{background:#22b98b;border-color:#22b98b;color:#03140f;font-weight:800}.graph{height:230px;position:relative;background:radial-gradient(circle,#10242e,#0b151e 68%)}.node{position:absolute;transform:translate(-50%,-50%);padding:8px 11px;border:1px solid #2d4a58;background:#13242e;border-radius:9px;font-size:10px}.core{background:#173e35;border-color:#2a9d7d;color:#70e4be}.line{position:absolute;height:1px;background:#38525e;transform-origin:0 0}.audit{padding:14px 18px}.event{padding:10px 0;border-bottom:1px solid #182731}.empty{text-align:center;padding:28px;color:#708591}@media(max-width:900px){.side{width:62px}.brand{font-size:0}.brand span{font-size:18px}.nav{font-size:0}.main{margin-left:62px;width:calc(100% - 62px);padding:18px}.cards{grid-template-columns:repeat(2,1fr)}.grid{grid-template-columns:1fr}}
</style></head><body><div class="app"><aside class="side"><div class="brand">Razor<span>Shield</span> AI</div><div class="nav active">◈ Risk Command Center</div><div class="nav">◉ Investigations</div><div class="nav">⌁ Risk Network</div><div class="nav">▣ Audit Trail</div><div style="position:absolute;bottom:20px;color:#607582;font-size:10px">MVP • SYNTHETIC DATA</div></aside>
<main class="main"><div class="top"><div><div class="eyebrow">Payment Risk Intelligence</div><div class="title">Risk Command Center</div></div><div class="live">● SYSTEM ONLINE</div></div>
<section class="cards"><div class="card"><div class="label">Transactions Analyzed</div><div class="num" id="total">—</div></div><div class="card"><div class="label">High-Risk Cases</div><div class="num red" id="high">—</div></div><div class="card"><div class="label">Medium-Risk</div><div class="num yellow" id="medium">—</div></div><div class="card"><div class="label">Average Risk Score</div><div class="num green" id="avg">—</div></div></section>
<div class="grid"><section class="panel"><div class="head"><b>Recent Transactions</b><span class="label">Click to investigate</span></div><table class="table"><thead><tr><th>ID</th><th>Amount</th><th>Account</th><th>Risk</th></tr></thead><tbody id="rows"></tbody></table></section>
<section class="panel"><div class="head"><b>AI Investigation</b><span id="state" class="label">No case</span></div><div id="case" class="empty">Select TX-10482 to begin.</div></section></div>
<div class="panel" style="margin-top:18px"><div class="head"><b>Risk Relationship Network</b><span class="label">Shared infrastructure</span></div><div id="graph" class="graph"><div class="empty">Investigation graph appears here.</div></div></div>
<div class="panel" style="margin-top:18px"><div class="head"><b>Audit Trail</b><span class="label">Session actions</span></div><div id="audit" class="audit"><div class="empty">No actions yet.</div></div></div>
</main></div>
<script>
const caseBox=document.getElementById("case"); const money=n=>"₹"+n.toLocaleString("en-IN");let selected="";
async function load(){let s=await fetch("/api/summary").then(r=>r.json());total.textContent=s.total;high.textContent=s.high;medium.textContent=s.medium;avg.textContent=s.avg+"/100";let t=await fetch("/api/transactions").then(r=>r.json());rows.innerHTML=t.map(x=>`<tr onclick="invest('${x.id}')"><td><b>${x.id}</b></td><td>${money(x.amount)}</td><td>${x.account}</td><td><span class="badge ${x.severity.toLowerCase()}">${x.riskScore} • ${x.severity}</span></td></tr>`).join("");auditLoad()}
async function invest(id){selected=id;state.textContent="INVESTIGATING";let d=await fetch("/api/investigate?id="+id).then(r=>r.json());state.textContent=d.severity+" • "+d.score+"/100";caseBox.innerHTML=`<div class="case"><div class="label">RISK SCORE</div><div class="score ${d.score>=60?"red":"green"}">${d.score}<span style="font-size:12px;color:#718592">/100</span></div><div class="bar"><i style="width:${d.score}%"></i></div><div class="label">Detected Signals</div>${d.signals.map(x=>`<div class="sig"><span>${x.name}</span><span class="pts">+${x.points}</span></div>`).join("")}<div class="label" style="margin-top:17px">AI Investigation</div><div class="summary">${d.summary}</div><div><button class="btn primary" onclick="act('MANUAL_REVIEW')">Manual Review</button><button class="btn" onclick="act('RESTRICT')">Restrict</button><button class="btn" onclick="act('ALLOW')">Allow</button></div></div>`;draw(d)}
function draw(d){let g=document.getElementById("graph");g.innerHTML="";let ns=[["ACCOUNT",d.transaction.account,50,22,1],["DEVICE",d.transaction.device,23,68,0],["TRANSACTION",d.transaction.id,50,72,1],["IP",d.transaction.ip,77,68,0]];d.accounts.filter(x=>x!==d.transaction.account).slice(0,2).forEach((x,i)=>ns.push(["RELATED",x,20+i*60,22,0]));ns.forEach(n=>{let e=document.createElement("div");e.className="node "+(n[4]?"core":"");e.style.left=n[2]+"%";e.style.top=n[3]+"%";e.innerHTML='<span class="label">'+n[0]+'</span><br><b>'+n[1]+"</b>";g.appendChild(e)});[[50,25,23,68],[50,25,77,68],[50,25,50,72]].forEach(a=>{let l=document.createElement("div");l.className="line";let dx=(a[2]-a[0])*g.clientWidth/100,dy=(a[3]-a[1])*g.clientHeight/100;l.style.left=a[0]+"%";l.style.top=a[1]+"%";l.style.width=Math.hypot(dx,dy)+"px";l.style.transform="rotate("+Math.atan2(dy,dx)+"rad)";g.appendChild(l)})}
async function act(a){await fetch("/api/action",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({id:selected,action:a})});auditLoad();alert("Action recorded: "+a.replace("_"," "))}
async function auditLoad(){let a=await fetch("/api/audit").then(r=>r.json());audit.innerHTML=a.length?a.map(e=>`<div class="event"><b>${e.action.replace("_"," ")}</b> • ${e.transactionId}<br><span class="label">${e.actor} · ${e.time}</span></div>`).join(""):'<div class="empty">No actions yet.</div>'}load();
</script></body></html>"""

if __name__=="__main__":
    print("RazorShield AI running at http://localhost:8000")
    HTTPServer(("127.0.0.1",8000),H).serve_forever()
