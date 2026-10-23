"""Monthly expected-cash lease model; assumptions, not a tenant forecast."""
from dataclasses import dataclass, asdict
from pathlib import Path
import csv
import json
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from model import payment


@dataclass(frozen=True)
class Lease:
    name: str
    area: float
    rent: float
    expiry: int
    renewal_probability: float
    downtime: int
    renewal_rent: float
    ti_psf: float = 500
    escalation: float = .05

    def validate(self):
        values = [self.area, self.rent, self.renewal_probability, self.renewal_rent, self.ti_psf, self.escalation]
        if not all(math.isfinite(v) for v in values):
            raise ValueError('finite lease inputs required')
        if min(self.area, self.rent, self.renewal_rent) <= 0 or self.ti_psf < 0 or self.escalation <= -1:
            raise ValueError('invalid lease economics')
        if type(self.expiry) is not int or type(self.downtime) is not int or min(self.expiry, self.downtime) < 0:
            raise ValueError('nonnegative integer months required')
        if not 0 <= self.renewal_probability <= 1:
            raise ValueError('renewal probability outside [0,1]')


def forecast(leases, area=100000, months=36, opex_psf=15):
    if area <= 0 or months < 1 or opex_psf < 0 or len({l.name for l in leases}) != len(leases):
        raise ValueError('invalid asset or duplicate tenant')
    for lease in leases:
        lease.validate()
    if sum(l.area for l in leases) > area:
        raise ValueError('leases exceed physical capacity')
    rows = []
    for month in range(1, months+1):
        rent = occupied = ti = 0.
        for lease in leases:
            if month <= lease.expiry:
                fraction = 1.
                rate = lease.rent * (1+lease.escalation)**((month-1)//12)
            else:
                fraction = lease.renewal_probability if month <= lease.expiry+lease.downtime else 1.
                rate = lease.renewal_rent * (1+lease.escalation)**((month-lease.expiry-1)//12)
                if month == lease.expiry+1:
                    ti += lease.area*lease.renewal_probability*lease.ti_psf
                if month == lease.expiry+lease.downtime+1:
                    ti += lease.area*(1-lease.renewal_probability)*lease.ti_psf
            rent += lease.area*fraction*rate
            occupied += lease.area*fraction
        expense = area*opex_psf*1.03**((month-1)//12)
        rows.append(dict(month=month,expected_occupancy=occupied/area,rent=rent,opex=expense,noi=rent-expense,leasing_capex=ti,cash_after_leasing=rent-expense-ti))
    return rows


def finance(rows, principal=550_000_000, annual_rate=.09, amortization_months=180):
    if principal<0 or annual_rate<0 or amortization_months<1:
        raise ValueError('invalid debt terms')
    balance=principal
    installment=payment(principal,annual_rate/12,amortization_months)
    output=[]
    for row in rows:
        interest=balance*annual_rate/12
        repaid=min(balance,max(0,installment-interest))
        service=interest+repaid
        opening=balance;balance-=repaid
        output.append({**row,'opening_debt':opening,'interest':interest,'principal':repaid,'debt_service':service,'closing_debt':balance,'equity_operating_cash':row['cash_after_leasing']-service})
    for i,row in enumerate(output):
        window=output[max(0,i-11):i+1];service=sum(r['debt_service'] for r in window)
        row['trailing_12m_dscr']=sum(r['noi'] for r in window)/service if i>=11 and service else None
    return output


def main():
    leases = [Lease('A',40000,92,12,.75,6,98),Lease('B',30000,88,24,.6,9,95),Lease('C',20000,90,30,.8,3,96)]
    rows = finance(forecast(leases))
    out = Path(__file__).parent/'results'
    with (out/'monthly_leases.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=rows[0]);writer.writeheader();writer.writerows(rows)
    summary={'source':'Synthetic lease cohorts specified in lease_engine.py','source_url':'https://github.com/Anjaney336/bengaluru-real-estate-investment-lab/blob/main/lease_engine.py','access_date':'2026-10-24','assumptions':[asdict(l) for l in leases],'minimum_expected_occupancy':min(r['expected_occupancy'] for r in rows),'total_leasing_capex':sum(r['leasing_capex'] for r in rows),'months':len(rows),'limitation':'Probability-weighted expected rent, not simulated tenant outcomes. Reletting after downtime assumed certain. No lease renewal correlation, credit loss, rent-free incentives or tax.'}
    summary['minimum_trailing_12m_dscr']=min(r['trailing_12m_dscr'] for r in rows if r['trailing_12m_dscr'] is not None)
    summary['closing_debt']=rows[-1]['closing_debt']
    summary['financing_assumptions']={'principal':550_000_000,'annual_rate':.09,'amortization_months':180}
    (out/'lease_summary.json').write_text(json.dumps(summary,indent=2))
    fig,axes=plt.subplots(2,1,figsize=(10,6),sharex=True)
    axes[0].plot([r['month'] for r in rows],[r['expected_occupancy'] for r in rows]);axes[0].set(ylabel='Expected occupied fraction',title='Lease expiry and renewal assumptions — monthly asset review')
    axes[1].plot([r['month'] for r in rows],[r['noi']/1e6 for r in rows],label='NOI');axes[1].plot([r['month'] for r in rows],[r['cash_after_leasing']/1e6 for r in rows],label='After leasing capex');axes[1].set(xlabel='Month',ylabel='INR million');axes[1].legend();fig.tight_layout();fig.savefig(out/'monthly_leases.svg');plt.close(fig)
    print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
