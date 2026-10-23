from pathlib import Path
import subprocess,sys,os
os.chdir(Path(__file__).parent)
subprocess.run([sys.executable,'-m','unittest','-v'],check=True)
subprocess.run([sys.executable,'-m','unittest','discover','-s','asset_management','-v'],check=True)
subprocess.run([sys.executable,'run_analysis.py'],check=True)
subprocess.run([sys.executable,'asset_management/run.py'],check=True)
subprocess.run([sys.executable,'financing_stress.py'],check=True)
subprocess.run([sys.executable,'investment_committee.py'],check=True)
subprocess.run([sys.executable,'embassy_case/verify_case.py'],check=True)
