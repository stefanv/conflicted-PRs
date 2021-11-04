import matplotlib
import matplotlib.pyplot as plt

import json
import glob
import sys
from dateutil.parser import isoparse

json_files = glob.glob('data/*.json')

f, ax = plt.subplots(1, len(json_files), sharey=True, figsize=(20, 8))

font = {'size'   : 12}
matplotlib.rc('font', **font)

for i, fn in enumerate(json_files):
    data = json.load(open(fn, 'r'))

    prs_unknown = [p for p in data if p['mergeable'] == 'UNKNOWN']
    if len(prs_unknown) != 0:
        print('Found PRs with unknown merge status.  Please redownload data.')
        sys.exit(-1)

    prs_conflicting = [isoparse(p['createdAt']) for p in data if p['mergeable'] == 'CONFLICTING']
    prs_other = [isoparse(p['createdAt']) for p in data if p['mergeable'] == 'MERGEABLE']
    ax[i].hist(
        [prs_conflicting, prs_other],
        bins='auto',
        histtype='bar',
        label=('conflicting', 'other'),
        color=('red', 'blue')
    )
    ax[i].set_title('/'.join(fn.replace('.json', '').split('__')))
    ax[i].set_xlabel('PR number')
    ax[i].legend()
    if i == 0:
        ax[i].set_ylabel('Number of conflicting PRs')

plt.tight_layout()
plt.savefig('pr-hist.png', dpi=300, )
plt.show()
