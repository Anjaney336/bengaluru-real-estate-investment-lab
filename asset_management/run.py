from pathlib import Path
import csv,hashlib,html,json
from monitor import load,report

ROOT=Path(__file__).parent
def fixtures(folder):
    folder.mkdir(parents=True,exist_ok=True)
    assets=[];leases=[];monthly=[]
    for j in range(4):
        aid=f'Office-{j+1}';assets.append([aid,100000,300000000])
        # Four 20,000 sqft leases: 80% capacity. Two expiry buckets and a future lease.
        for k in range(4):leases.append([f'L{j}-{k}',aid,f'Tenant-{j}-{k//2}',20000,8000+100*j,'2025-01-01','2027-06-30' if k<2 else '2029-12-31'])
        leases.append([f'F{j}',aid,f'Future-{j}',20000,9000,'2027-01-01','2030-01-01'])
        for m in range(4,10):
            ba=80000;aa=80000-1000*((j+m)%4);br=8000;ar=8100+100*j;bg=ba*br;ag=aa*ar
            monthly.append([aid,f'2026-{m:02d}-01',ba,aa,br,ar,bg,ag-ag//50,160000000,165000000+j*1000000])
    for name,header,rows in [('assets',['asset','area','debt_service'],assets),('leases',['lease','asset','tenant','area','rent','start','end'],leases),('monthly',['asset','month','budget_area','actual_area','budget_rent','actual_rent','budget_cash','actual_cash','budget_opex','actual_opex'],monthly)]:
        with (folder/f'{name}.csv').open('w',newline='') as f:w=csv.writer(f);w.writerow(header);w.writerows(rows)

def main():
    folder=ROOT/'data';fixtures(folder);db=load(folder);r=report(db,'2026-09-30','2026-09-01');db.close()
    r['provenance']={'source':'Code-generated fixtures; asset_management/run.py','source_url':'https://github.com/Anjaney336/bengaluru-office-underwriting/tree/main/asset_management','generated_on':'2026-10-24','access_date':'2026-10-24','sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(folder.glob('*.csv'))}}
    out=ROOT/'results';out.mkdir(exist_ok=True);(out/'monitor.json').write_text(json.dumps(r,indent=2))
    with (out/'noi_bridge.csv').open('w',newline='') as f:
        keys=['asset','budget_noi','occupancy_effect','rate_effect','collection_effect','expense_effect','actual_noi','residual'];w=csv.DictWriter(f,fieldnames=keys,extrasaction='ignore');w.writeheader();w.writerows(r['assets'])
    rows=''.join('<tr>'+''.join(f'<td>{html.escape(str(x))}</td>' for x in [a['asset'],f"{a['area_occupancy']:.1%}",f"{a['rent_weighted_wale_years']:.2f}",f"{a['expiring_12m_rent_share']:.1%}",f"{a['largest_tenant_share']:.1%}",f"{a['actual_noi']/1e9:.3f}",f"{a['monthly_noi_dscr']:.2f}x",f"{a['downside_dscr']:.2f}x"] )+'</tr>' for a in r['assets'])
    page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Property Operating Monitor | Anjaney Malhotra</title><style>body{font:16px/1.7 system-ui;background:#f5f7fa;color:#183040;max-width:1100px;margin:40px auto;padding:20px}table{border-collapse:collapse;background:white;width:100%}td,th{padding:12px;text-align:left;border-bottom:1px solid #ddd}.scroll{overflow:auto}aside{padding:20px;background:#e7eef4}a{color:#1e5476}</style><h1>Property Operating Monitor</h1><p>SQL-backed lease exposure and monthly NOI attribution | Anjaney Malhotra</p><aside><strong>Synthetic teaching dataset.</strong> Four hypothetical assets, 20 lease records and 24 asset-month observations. This is not performance of a real property portfolio. All financial terms are modelling assumptions.</aside><h2>Operating review — September 2026</h2><div class="scroll"><table><tr><th>Asset</th><th>Area occupied</th><th>WALE years</th><th>Rent expires ≤365d</th><th>Largest tenant</th><th>NOI ₹cr</th><th>DSCR</th><th>Stress DSCR</th></tr>'''+rows+'''</table></div><h2>Management priorities</h2><p>The synthetic lease roll has half of current rent expiring within 365 days. Prioritise renewal discussions and compare retention terms against tenant-improvement and downtime costs. Monthly operating occupancy differs from the lease snapshot and is flagged for reconciliation, not silently overwritten.</p><p>Downside assumptions: cash rent −10%, operating expenses +10%, unchanged debt service. DSCR uses monthly NOI and excludes balloon payments. WALE is weighted by current monthly contractual rent and uses 365.25 days/year. No lease-up, tax, inflation or refinancing forecast is implied.</p><h2>Trace the result</h2><p>Actual NOI = budget NOI + occupancy effect + rate effect + collection effect + expense effect. Every asset and aggregate bridge reconciles to zero paise.</p><p><a href="results/monitor.json">Source hashes and full metrics</a> · <a href="results/noi_bridge.csv">NOI bridge CSV</a> · <a href="https://github.com/Anjaney336/bengaluru-office-underwriting/tree/main/asset_management">Code, tests and data definitions</a></p></html>'''
    (ROOT/'index.html').write_text(page,encoding='utf-8');print(json.dumps(r['portfolio']))
if __name__=='__main__':main()
