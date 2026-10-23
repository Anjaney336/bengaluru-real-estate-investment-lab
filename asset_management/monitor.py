"""Publicly reproducible teaching fixtures. Monetary values are integer INR paise."""
import csv
import json
import sqlite3
from datetime import date
from pathlib import Path


def load(folder):
    db=sqlite3.connect(':memory:');db.execute('PRAGMA foreign_keys=ON')
    db.executescript('''
    CREATE TABLE assets(asset TEXT PRIMARY KEY,area INTEGER CHECK(area>0),debt_service INTEGER CHECK(debt_service>=0));
    CREATE TABLE leases(lease TEXT PRIMARY KEY,asset TEXT REFERENCES assets(asset),tenant TEXT,area INTEGER CHECK(area>0),rent INTEGER CHECK(rent>=0),start TEXT,end TEXT,CHECK(start<end));
    CREATE TABLE monthly(asset TEXT REFERENCES assets(asset),month TEXT,budget_area INTEGER CHECK(budget_area>=0),actual_area INTEGER CHECK(actual_area>=0),budget_rent INTEGER CHECK(budget_rent>=0),actual_rent INTEGER CHECK(actual_rent>=0),budget_cash INTEGER CHECK(budget_cash>=0),actual_cash INTEGER CHECK(actual_cash>=0),budget_opex INTEGER CHECK(budget_opex>=0),actual_opex INTEGER CHECK(actual_opex>=0),PRIMARY KEY(asset,month));
    ''')
    specs={'assets':(['asset','area','debt_service'],['area','debt_service']),
           'leases':(['lease','asset','tenant','area','rent','start','end'],['area','rent']),
           'monthly':(['asset','month','budget_area','actual_area','budget_rent','actual_rent','budget_cash','actual_cash','budget_opex','actual_opex'],['budget_area','actual_area','budget_rent','actual_rent','budget_cash','actual_cash','budget_opex','actual_opex'])}
    try:
        for table,(cols,ints) in specs.items():
            with (Path(folder)/(table+'.csv')).open(newline='') as f:
                reader=csv.DictReader(f)
                if reader.fieldnames!=cols:raise ValueError('Unexpected columns: '+table)
                for row in reader:
                    if any(not str(v).strip() for v in row.values()):raise ValueError('Missing value')
                    for k in ints:
                        if not row[k].isdigit():raise ValueError('Nonnegative integer required: '+k)
                        row[k]=int(row[k])
                    for k in ['start','end','month']:
                        if k in row:
                            d=date.fromisoformat(row[k])
                            if d.isoformat()!=row[k] or (k=='month' and d.day!=1):raise ValueError('ISO month/date required')
                    db.execute(f'INSERT INTO {table} VALUES('+','.join('?' for _ in cols)+')',[row[c] for c in cols])
        for asset,area in db.execute('SELECT asset,area FROM assets'):
            boundaries=[r[0] for r in db.execute('SELECT DISTINCT start FROM leases WHERE asset=?',(asset,))]
            for d in boundaries:
                occupied=db.execute('SELECT COALESCE(SUM(area),0) FROM leases WHERE asset=? AND start<=? AND end>?',(asset,d,d)).fetchone()[0]
                if occupied>area:raise ValueError('Overlapping leased area exceeds asset capacity')
            if db.execute('SELECT COUNT(*) FROM monthly WHERE asset=? AND (budget_area>? OR actual_area>?)',(asset,area,area)).fetchone()[0]:raise ValueError('Monthly occupied area exceeds capacity')
        for row in db.execute('SELECT budget_area,budget_rent,actual_area,actual_rent,budget_cash,actual_cash FROM monthly'):
            ba,br,aa,ar,bc,ac=row
            if bc>ba*br or ac>aa*ar:raise ValueError('Cash exceeds current rent; prior-period collections must be separated')
    except Exception:
        db.close();raise
    return db


def operating_bridge(row):
    ba,aa,br,ar,bc,ac,bo,ao=row
    occupancy=(aa-ba)*br
    rate=aa*(ar-br)
    collection=(ac-aa*ar)-(bc-ba*br)
    expense=bo-ao
    budget_noi,actual_noi=bc-bo,ac-ao
    residual=actual_noi-budget_noi-occupancy-rate-collection-expense
    assert residual==0
    return dict(budget_noi=budget_noi,actual_noi=actual_noi,occupancy_effect=occupancy,rate_effect=rate,collection_effect=collection,expense_effect=expense,residual=residual)


def report(db,asof,month):
    day=date.fromisoformat(asof);date.fromisoformat(month)
    result=[]
    for aid,capacity,service in db.execute('SELECT * FROM assets ORDER BY asset'):
        leases=db.execute('SELECT tenant,area,rent,end FROM leases WHERE asset=? AND start<=? AND end>? ORDER BY lease',(aid,asof,asof)).fetchall()
        area=sum(r[1] for r in leases);gross=sum(r[1]*r[2] for r in leases)
        tenant_rent={};expiry_rent=0;wale_numerator=0
        for tenant,la,rent,end in leases:
            weight=la*rent;days=(date.fromisoformat(end)-day).days;tenant_rent[tenant]=tenant_rent.get(tenant,0)+weight
            wale_numerator+=weight*days/365.25
            if days<=365:expiry_rent+=weight
        row=db.execute('SELECT budget_area,actual_area,budget_rent,actual_rent,budget_cash,actual_cash,budget_opex,actual_opex FROM monthly WHERE asset=? AND month=?',(aid,month)).fetchone()
        if row is None:raise ValueError(f'Missing month for {aid}')
        bridge=operating_bridge(row)
        dscr=None if service==0 else bridge['actual_noi']/service
        # Scenario: no forecast/advice; illustrative 10% cash rent reduction, 10% opex increase.
        downside_noi=row[5]*.9-row[7]*1.1
        result.append(dict(asset=aid,area_occupancy=area/capacity,rent_weighted_wale_years=None if not gross else wale_numerator/gross,
                           expiring_12m_rent_share=None if not gross else expiry_rent/gross,largest_tenant_share=None if not gross else max(tenant_rent.values())/gross,
                           tenant_hhi=None if not gross else sum((r/gross)**2 for r in tenant_rent.values()),monthly_noi_dscr=dscr,
                           downside_dscr=None if service==0 else downside_noi/service,contract_monthly_area_difference=row[1]-area,
                           **bridge))
    totals={k:sum(r[k] for r in result) for k in ['budget_noi','actual_noi','occupancy_effect','rate_effect','collection_effect','expense_effect','residual']}
    return dict(as_of=asof,operating_month=month,units='INR paise for money; ratios dimensionless',dataset='Synthetic demonstration; no actual property or employer records',assets=result,portfolio=totals)
