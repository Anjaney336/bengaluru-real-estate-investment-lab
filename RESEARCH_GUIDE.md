# Bengaluru Investment & Asset Management — calculation and decision guide

What entry price and financing can the property cash flows support?

## Underwrite the acquisition

Forecast rent, vacancy, operating expenses and capital expenditure before financing. Discount equity cash flows at the assumed required return; keep exit value and sale costs explicit.

## Size the loan

Debt capacity is the minimum of DSCR, LTV and debt-yield limits. The base case is DSCR-constrained at INR45.94 crore. At the assumed INR100 crore price, equity NPV is about −INR11.00 crore and minimum DSCR is 1.04x.

## Make the investment decision

The model supports a maximum price of about INR83.53 crore under its stated assumptions. Reject or reprice the INR100 crore case; validate market rents and physical capex before treating this as a real deal.

## Manage lease events

The separate monthly case links expiry, renewal probability, vacancy and leasing capex to amortising debt. A 1.13x minimum trailing DSCR is specific to that case, not the acquisition model.

## Calculation

NOI = rental income − operating expenses; debt service = interest + principal; DSCR = NOI / debt service; equity cash = NOI − leasing capex − debt service.

## Graph interpretation

### Lease and debt review

Occupancy falls during assumed downtime; leasing capex makes cash flow more volatile than NOI. Read the upper panel as expected occupied area, not a realised tenant forecast. The lower panel is INR million before debt service.

### Credit capacity

Read debt capacity against the coverage, collateral and debt-yield constraints. A loan sized to LTV alone can still fail DSCR. The committee summary identifies which constraint binds.

### Financing sensitivity

Each cell is minimum NOI DSCR under assumed interest rate and acquisition LTV. Cells below the illustrative 1.25x hurdle show financing combinations that fail the coverage screen; they are not lender quotes.

## Review evidence

lease_engine.py · model.py · results/committee_summary.json · results/monthly_leases.csv

Demonstrates: Acquisition pricing, debt sizing, asset-management cash flow and investment judgement.

All values are existing recorded outputs. No new performance experiment was run for this presentation update. Refer to the README and result JSON for data sources, access dates, units and limitations.
