# Bengaluru Investment & Asset Management

[Open the research dashboard](https://anjaney336.github.io/portfolio/research/bengaluru-real-estate-investment-lab/) · [Earlier component methodology](docs/PRE_CONSOLIDATION.md)

## Research question and scope
Consolidates the Bengaluru acquisition model, property operating review and financing stress. The monthly cohort model connects lease expiry and renewal assumptions to amortising debt and trailing coverage.

## Results
The synthetic 36-month lease case reaches 74% expected occupancy and 1.13× minimum trailing DSCR. The separate acquisition case still rejects the assumed INR100 crore entry price.

## Calculation conventions
Monthly expected rent sums occupied cohort area × rent. Renewal and reletting branches carry separate capex timing. Debt interest uses opening balance × annual rate / 12; trailing DSCR is 12-month NOI divided by 12-month debt service. Acquisition valuation remains a separately parameterised teaching case.

## Data and sources
Synthetic inputs in lease_engine.py and assumptions.json; source URLs and access dates in the result JSON. Public-filings case available in embassy_case/.

## Reproduce
Python 3.12. Install `requirements.txt`, then run `python reproduce.py`. Default tests/research run offline; historical runs need the local authorized cache. New entry point: `lease_engine.py`. Add `--prices /path/to/prices.csv` for historical strategy/derivative experiments.

## Verification
35 tests across the consolidated reproduction command. CI runs the same command. See ENGINEERING.md for boundaries and release checks. The dashboard displays bundled reports; change its view selector to compare analyses, and download CSV/JSON evidence.

## Limits
Synthetic leases and underwriting assumptions; no actual rent roll, lender agreement or technical inspection. Expected renewal cash flow is not a calibrated probability forecast. Native Excel verification remains pending.

## Lineage and authorship
Consolidates existing research modules; original repositories remain as history. This is AI-assisted portfolio research, not code represented as deployed at a financial institution.
