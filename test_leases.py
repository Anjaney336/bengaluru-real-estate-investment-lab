import unittest
from lease_engine import Lease, forecast, finance

class LeaseTests(unittest.TestCase):
    def test_contract_rent(self):
        self.assertEqual(forecast([Lease('a',100,10,12,1,0,20)],area=100,opex_psf=0)[0]['rent'],1000)
    def test_expiry_and_downtime(self):
        rows=forecast([Lease('a',100,10,1,0,2,20)],area=100)
        self.assertEqual([r['expected_occupancy'] for r in rows[:4]],[1,0,0,1])
    def test_ti_once_per_branch(self):
        rows=forecast([Lease('a',100,10,1,.6,2,20)],area=100)
        self.assertEqual(sum(r['leasing_capex'] for r in rows),50000)
    def test_zero_downtime(self):
        rows=forecast([Lease('a',100,10,1,.6,0,20)],area=100)
        self.assertEqual(rows[1]['leasing_capex'],50000)
    def test_area_guard(self):
        with self.assertRaises(ValueError):forecast([Lease('a',101,10,1,1,0,20)],area=100)
    def test_cash_bridge(self):
        for r in forecast([Lease('a',100,10,1,.6,2,20)],area=100):self.assertAlmostEqual(r['cash_after_leasing'],r['rent']-r['opex']-r['leasing_capex'])
    def test_monthly_debt_bridge(self):
        for r in finance(forecast([Lease('a',100,10,1,.6,2,20)],area=100)):
            self.assertAlmostEqual(r['closing_debt'],r['opening_debt']-r['principal'])
    def test_trailing_dscr_warmup(self):
        rows=finance(forecast([Lease('a',100,10,1,.6,2,20)],area=100))
        self.assertIsNone(rows[10]['trailing_12m_dscr']);self.assertIsNotNone(rows[11]['trailing_12m_dscr'])

if __name__=='__main__':unittest.main()
