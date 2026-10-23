# Property Operating Monitor

SQL-backed asset-management demonstration using a transparent synthetic portfolio. AI-assisted implementation; review the equations and tests before discussing ownership in interviews.

## Reproduce from repository root
```
python -m unittest discover -s asset_management -v
python asset_management/run.py
```
Python 3.12 standard library only. Open index.html for the operating dashboard; inspect results/monitor.json and results/noi_bridge.csv for the calculation trail.

## Methodology
CSV data are validated and loaded into SQLite with primary/foreign keys. Four hypothetical 100,000-sqft assets, 20 lease records (16 current and 4 future) and 24 asset-month observations. Money is integer INR paise, rent is paise/sqft/month. Future leases are excluded; lease end dates are exclusive. Active lease area is checked at each lease commencement against physical capacity.

Area occupancy = active leased area / capacity. WALE = sum(monthly rent × remaining term in years) / sum(monthly rent), using 365.25 days/year. Concentration uses current contractual rent shares; HHI is the sum of squared tenant shares. Monthly DSCR = cash NOI / monthly debt service; zero debt returns null.

## Exact NOI attribution
Let A=occupied area, R=rent rate, C=cash collected, O=operating expense; b/a denote budget/actual.
- Occupancy effect = (Aa−Ab)Rb
- Rate effect = Aa(Ra−Rb)
- Collection effect = (Ca−AaRa)−(Cb−AbRb)
- Expense effect = Ob−Oa
- Actual NOI = budget NOI + all four effects.
The attribution order assigns the area/rate interaction to rate. All asset and portfolio bridges must reconcile to zero paise. September illustrative budget NOI is INR1.920 crore and actual NOI is INR1.872788 crore; these are simulated values, not employer outcomes.

## Data provenance
Named source: [public fixture generator](https://github.com/Anjaney336/bengaluru-office-underwriting/blob/main/asset_management/run.py). Generated/access date 2026-10-24; input SHA-256 hashes in monitor.json. No scraping or private data. All leases, rents, collections and debt service are explicit modelling assumptions.

## Checks and limitations
11 tests cover hand-calculated bridge, aggregate reconciliation, future/expired leases, zero debt, duplicate/orphan rows, overlapping lease capacity, invalid dates, overbilling and stress direction. Monthly occupied area is not silently forced to equal point-in-time lease occupancy: mismatches are flagged. Cash exceeding current gross billing is rejected; historical arrears need a separate field. Downside assumes cash rent −10%, opex +10%, unchanged debt. No lease-up forecast, valuation, balloon repayment, refinancing, tax or actual portfolio performance is inferred.
