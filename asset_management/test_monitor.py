from pathlib import Path
import tempfile,unittest,sqlite3
from monitor import load,report,operating_bridge
from run import fixtures

class MonitorTests(unittest.TestCase):
    def setUp(self):self.temp=tempfile.TemporaryDirectory();self.folder=Path(self.temp.name);fixtures(self.folder)
    def tearDown(self):self.temp.cleanup()
    def test_hand_calculated_noi_bridge(self):
        r=operating_bridge((100,90,10,12,1000,1000,100,150))
        self.assertEqual([r[k] for k in ['occupancy_effect','rate_effect','collection_effect','expense_effect','actual_noi','residual']],[-100,180,-80,-50,850,0])
    def test_sql_counts_and_portfolio_reconciliation(self):
        db=load(self.folder);r=report(db,'2026-09-30','2026-09-01')
        self.assertEqual(db.execute('SELECT COUNT(*) FROM leases').fetchone()[0],20)
        p=r['portfolio'];self.assertEqual(p['actual_noi']-p['budget_noi'],sum(p[x] for x in ['occupancy_effect','rate_effect','collection_effect','expense_effect']));db.close()
    def test_future_leases_excluded(self):
        db=load(self.folder);a=report(db,'2026-09-30','2026-09-01')['assets'][0]
        self.assertEqual(a['area_occupancy'],.8);self.assertEqual(a['largest_tenant_share'],.5);self.assertEqual(a['expiring_12m_rent_share'],.5);self.assertEqual(a['tenant_hhi'],.5);db.close()
    def test_end_date_exclusive(self):
        db=load(self.folder);a=report(db,'2027-06-30','2026-09-01')['assets'][0];self.assertEqual(a['area_occupancy'],.6);db.close()
    def test_empty_portfolio_and_zero_debt(self):
        db=load(self.folder);db.execute('DELETE FROM leases');db.execute('UPDATE assets SET debt_service=0');a=report(db,'2026-09-30','2026-09-01')['assets'][0]
        self.assertIsNone(a['rent_weighted_wale_years']);self.assertIsNone(a['monthly_noi_dscr']);self.assertEqual(a['area_occupancy'],0);db.close()
    def test_duplicate_asset_month_rejected(self):
        p=self.folder/'monthly.csv';s=p.read_text();p.write_text(s+s.splitlines()[1]+'\n')
        with self.assertRaises(sqlite3.IntegrityError):load(self.folder)
    def test_orphan_lease_rejected(self):
        p=self.folder/'leases.csv';p.write_text(p.read_text().replace('Office-1','Unknown'))
        with self.assertRaises(sqlite3.IntegrityError):load(self.folder)
    def test_overlapping_area_rejected(self):
        p=self.folder/'leases.csv';p.write_text(p.read_text().replace('20000','40000'))
        with self.assertRaises(ValueError):load(self.folder)
    def test_cash_overbilling_rejected(self):
        p=self.folder/'monthly.csv';rows=p.read_text().splitlines();r=rows[1].split(',');r[7]='999999999999';rows[1]=','.join(r);p.write_text('\n'.join(rows)+'\n')
        with self.assertRaises(ValueError):load(self.folder)
    def test_invalid_date_and_missing_month(self):
        p=self.folder/'leases.csv';old=p.read_text();p.write_text(old.replace('2025-01-01','2025-02-30'))
        with self.assertRaises(ValueError):load(self.folder)
        p.write_text(old);db=load(self.folder)
        with self.assertRaises(ValueError):report(db,'2026-09-30','2026-01-01')
        db.close()
    def test_stress_direction_and_snapshot_mismatch(self):
        db=load(self.folder);r=report(db,'2026-09-30','2026-09-01');self.assertTrue(any(a['contract_monthly_area_difference']!=0 for a in r['assets']))
        self.assertTrue(all(a['downside_dscr']<a['monthly_noi_dscr'] for a in r['assets']));db.close()

if __name__=='__main__':unittest.main()
