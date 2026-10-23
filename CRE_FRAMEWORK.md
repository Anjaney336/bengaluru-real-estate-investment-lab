# Commercial real estate underwriting conventions

This guide maps CRE terminology to the implemented Bengaluru teaching case. It is not an appraisal, lease opinion or a claim of RICS/IVS compliance.

## DCF timing and terminal value — implemented
The acquisition model uses nominal INR, a five-year hold and end-of-year cash flows. Acquisition price, transaction costs and initial capex occur at t=0. Operating cash flows occur at t=1…5. This is annual periodic discounting, not mid-year discounting or date-based XNPV/XIRR.

Unlevered property cash flow = NOI − replacement reserve − tenant improvements/leasing costs.
PV = Σ(UCF_t/(1+r_u)^t) + net sale proceeds_5/(1+r_u)^5.
The assumed unlevered discount rate is 11%; the separate equity hurdle is 15%. Equity cash flows additionally deduct debt service and the outstanding loan at sale. Neither rate is a market-derived estimate.

Gross terminal value at year 5 = forward year-6 NOI / terminal capitalization rate.
The assumed terminal cap rate is 8%; net sale proceeds deduct 2% selling costs. Remaining year-5 debt is deducted only from equity sale proceeds. Year-6 NOI estimates resale value; it is not an additional operating cash receipt.

A cap rate converts a selected annual NOI into a value; a discount rate discounts a multi-period cash-flow stream. Going-in cap rate (year-1 NOI/purchase price) and terminal cap rate need not be equal. Compare cap rates on consistent NOI, occupancy, tenure, lease quality and valuation dates.

## Lease economics — implemented convention and diligence distinction
The code deducts an aggregate landlord operating-expense allowance with no separate tenant recovery schedule: a simplified gross-style cash-flow convention, not a verified gross lease.
- Gross: quoted rent generally embeds landlord-paid operating expenses, subject to the contract.
- Triple Net / NNN: base rent plus tenant responsibility for property taxes, insurance and maintenance/operating costs as specified in the lease. It does not automatically remove all owner capex or vacancy costs.
- Modified gross: costs are shared using negotiated inclusions, expense stops or other recovery provisions.

For a Bengaluru lease abstract, reconcile base rent, CAM recoveries, taxes/insurance, deposits, escalation, lock-in/break rights, rent-free periods, fit-out contributions and repair obligations. Classify the actual cash flows from the signed lease rather than assuming US lease labels apply unchanged. Current code does not model CAM recovery, expense stops, rent-free periods or deposits; adding the terminology does not imply these features are implemented.

Normalize lease comparables by area basis, INR/sqft/month versus annual units, net versus gross quote, incentives, escalation and transaction date. Net effective rent should reflect incentives and landlord leasing expenditure under a stated calculation convention. Do not compare headline rents alone.

## NOI and lease rollover — implemented
NOI in this case = effective rental revenue − property operating expenses, before debt service, reserves and leasing capex. This convention is stated explicitly because reporting definitions differ. The annual model applies occupancy and a rollover vacancy deduction; leasing capex includes tenant improvements (TI) and leasing fees (LC). NOI DSCR and post-capex cash coverage are both available and must not be conflated.

The separate monthly cohort model tracks expected lease expiries, renewal/reletting downtime and capex; it is not the same parameter set as the annual DCF. No observed tenant credit or lease probability is claimed.

## Market underwriting — diligence inputs, not calibrated forecasts
Net absorption = ending occupied area − beginning occupied area over a defined period and consistent market universe. It differs from gross leasing activity, which can include renewals and relocations. Inventory changes and supply delivery must be reconciled. Vacancy rate uses vacant area/inventory; availability can also include occupied space marketed for future lease.

Collect dated Bengaluru micro-market net absorption, new completions, vacancy, competing pipeline, pre-leasing and comparable achieved rents from consistent public reports. Use these inputs to challenge lease-up, downtime, occupancy and rental-growth assumptions. The current 90% occupancy and 5% annual rent growth are assumptions; no Bengaluru net-absorption series has been loaded or used to calibrate them.

## Brokerage and valuation review sequence
1. Lease abstract and rent-roll reconciliation: areas, contractual rent, recoveries, expiries and incentives.
2. Market comparison: comparable assets, quote basis, achieved rent, vacancy, absorption and supply.
3. Income bridge: potential rent → occupancy/downtime deductions → effective revenue → NOI → reserves/TI/LC → unlevered cash flow.
4. Value and finance: year-6 NOI/exit cap, annual DCF, debt capacity and equity returns.
5. Investment decision: stress rent, occupancy, cap rate and funding; state the price supported by assumptions and the evidence still required.

## Evidence and references
Implementation: model.py (npv, underwrite), assumptions.json, lease_engine.py and results/annual_cash_flows.csv.
Terminology references accessed 24 October 2026:
- JLL commercial real-estate glossary: https://www.jll.com/en-ca/real-estate-terms-definitions
- NAIOP office/industrial definitions: https://www.naiop.org/globalassets/research-and-publications/report/terms-and-definitions-/researchreportnaiop-terms-and-definitions-2012.pdf
These are general terminology references, not Bengaluru rent, lease or cap-rate evidence.
