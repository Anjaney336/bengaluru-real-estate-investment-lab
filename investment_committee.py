"""Debt capacity and reverse underwriting. All inputs are labelled assumptions."""
from dataclasses import replace
from pathlib import Path
import csv,json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from model import Assumptions,underwrite,payment

def debt_capacity(a,dscr=1.25,ltv=.55,debt_yield=.09):
 if dscr<=0 or not 0<=ltv<1 or debt_yield<=0:raise ValueError('invalid limits')
 r=underwrite(a);nois=[x['noi'] for x in r['cash_flows']]
 factor=payment(1,a.interest_rate,a.amortization_years)
 limits={'DSCR':max(0,min(nois)/dscr/factor),'LTV':a.purchase_price*ltv,'Debt yield':max(0,min(nois)/debt_yield)}
 return {'limits':limits,'capacity':min(limits.values()),'binding':min(limits,key=limits.get)}

def max_price(a):
 lo,hi=1.,a.purchase_price*4
 def feasible(price):return underwrite(replace(a,purchase_price=price))['passes_screen']
 if not feasible(lo):return None
 if feasible(hi):raise ValueError('price root not bracketed')
 for _ in range(90):
  mid=(lo+hi)/2
  if feasible(mid):lo=mid
  else:hi=mid
 return lo

def run():
 a=Assumptions();out=Path(__file__).parent/'results';rows=[]
 for occ in [.7,.8,.9,.95]:
  for months in [0,3,6,9,12]:
   b=replace(a,occupancy=occ,downtime_months=months);c=debt_capacity(b)
   rows.append(dict(occupancy=occ,downtime_months=months,capacity_crore=c['capacity']/1e7,binding=c['binding'],maximum_price_crore=max_price(b)/1e7))
 with (out/'credit_capacity.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
 base=underwrite(a);elasticities={}
 for k in ['rent_psf_month','occupancy','exit_cap_rate','interest_rate']:
  value=getattr(a,k);up=underwrite(replace(a,**{k:value*1.01}))['equity_npv'];down=underwrite(replace(a,**{k:value*.99}))['equity_npv']
  elasticities[k]=(up-down)/2/1e7
 report={'case':'Synthetic Bengaluru office; not an actual deal','base_equity_npv_crore':base['equity_npv']/1e7,'base_minimum_dscr':base['minimum_dscr'],'debt_capacity':debt_capacity(a),'maximum_price_crore':max_price(a)/1e7,'npv_change_crore_per_1pct_relative_input_change':elasticities,'scenarios':len(rows),'assumed_debt_yield_floor':.09,'source':'model.py and assumptions.json','source_url':'https://github.com/Anjaney336/bengaluru-real-estate-investment-lab/blob/main/model.py','access_date':'2026-10-24'}
 (out/'committee_summary.json').write_text(json.dumps(report,indent=2))
 fig,ax=plt.subplots(figsize=(9,4.5))
 for occ in [.7,.8,.9,.95]:
  z=[r for r in rows if r['occupancy']==occ];ax.plot([r['downtime_months'] for r in z],[r['capacity_crore'] for r in z],marker='o',label=f'{occ:.0%} occupancy')
 ax.set(xlabel='Assumed rollover downtime (months)',ylabel='Maximum initial debt (INR crore)',title='Debt capacity: minimum of DSCR, LTV and debt-yield limits');ax.legend();fig.tight_layout();fig.savefig(out/'credit_capacity.svg');plt.close(fig)
 print(json.dumps(report,indent=2))
if __name__=='__main__':run()
