import unittest
from dataclasses import replace
from model import Assumptions,underwrite
from investment_committee import debt_capacity,max_price
class CommitteeTests(unittest.TestCase):
 def test_capacity_satisfies_all_limits(self):
  x=debt_capacity(Assumptions());self.assertTrue(all(x['capacity']<=v for v in x['limits'].values()))
 def test_tighter_dscr_reduces_capacity(self):
  a=Assumptions();self.assertLessEqual(debt_capacity(a,dscr=1.6)['capacity'],debt_capacity(a)['capacity'])
 def test_downtime_reduces_capacity(self):
  a=Assumptions();self.assertLessEqual(debt_capacity(replace(a,downtime_months=12))['capacity'],debt_capacity(a)['capacity'])
 def test_price_threshold(self):
  a=Assumptions();p=max_price(a);self.assertTrue(underwrite(replace(a,purchase_price=p*.999))['passes_screen']);self.assertFalse(underwrite(replace(a,purchase_price=p*1.001))['passes_screen'])
 def test_zero_rate(self):self.assertGreater(debt_capacity(replace(Assumptions(),interest_rate=0))['capacity'],0)
 def test_invalid_limits(self):
  with self.assertRaises(ValueError):debt_capacity(Assumptions(),dscr=0)
if __name__=='__main__':unittest.main()
