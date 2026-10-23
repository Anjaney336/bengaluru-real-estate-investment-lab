from pathlib import Path
from dataclasses import replace
import csv,json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from model import Assumptions,underwrite
root=Path(__file__).parent;out=root/'results';a=Assumptions(**json.loads((root/'assumptions.json').read_text()));rows=[];grid=[]
for rate in [.06,.075,.09,.105,.12]:
 line=[]
 for ltv in [.3,.4,.5,.6,.7]:
  r=underwrite(replace(a,interest_rate=rate,ltv=ltv));line.append(r['minimum_dscr']);rows.append(dict(interest_rate=rate,ltv=ltv,minimum_dscr=r['minimum_dscr'],equity_npv=r['equity_npv'],coverage_pass=r['minimum_dscr']>=a.minimum_dscr))
 assert all(x>=y for x,y in zip(line,line[1:]));grid.append(line)
assert all(grid[i][j]>=grid[i+1][j] for i in range(4) for j in range(5))
with (out/'financing_stress.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
fig,ax=plt.subplots(figsize=(8,5));im=ax.imshow(grid,cmap='RdYlGn',vmin=.7,vmax=2.2)
for i in range(5):
 for j in range(5):ax.text(j,i,f'{grid[i][j]:.2f}x',ha='center',va='center')
ax.set(xticks=range(5),xticklabels=['30%','40%','50%','60%','70%'],yticks=range(5),yticklabels=['6%','7.5%','9%','10.5%','12%'],xlabel='Assumed acquisition LTV',ylabel='Assumed interest rate',title='Minimum NOI DSCR — illustrative debt stress, hurdle 1.25x');fig.colorbar(im,ax=ax);fig.tight_layout();fig.savefig(out/'financing_stress.svg')
print('25 financing scenarios; debt-rate and leverage monotonicity checks passed')
