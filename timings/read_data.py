#%%
import json
import csv
import numpy as np
import pandas as pd

num_subsets = 14
repetitions = 10

with open(f"time_breakdown_num_subsets{num_subsets}_rep{repetitions}.json", "r") as f:
    time_breakdown = json.load(f)

#%%
keys = ["AcquisitionModelUsingParallelproj",
        "PoissonLogLikelihoodWithLinearModelForMeanAndProjData",
        "Submission"]

import numpy as np
#avg of AcquisitionModel
def get_avg(data, key:str, which:str):
    direct = []
    for k,v in data.items():
        if k.startswith(key):
            for subk, subv in v.items():
                if subk == which:
                    direct.append(subv)
    
    return direct
# %%

comb = [[keys[0],'direct'], [keys[0],'adjoint'],
        [keys[1],'gradient'], [keys[2],'run']]

for c in comb:
    res = get_avg(time_breakdown,
            c[0], c[1])
    res = np.array(res)
    np.mean(res, axis=0)
    print (f"{c[1]}: {np.mean(res, axis=0)}")
# %%

# collate all results
all_results = {}
all_num_subsets = [1,3,7,14,21,42,63]

repetitions = 10
for num_subsets in all_num_subsets:
    with open(f"time_breakdown_num_subsets{num_subsets}_rep{repetitions}.json", "r") as f:
        time_breakdown = json.load(f)
    
    comb = [[keys[0],'direct'], [keys[0],'adjoint'],
        [keys[1],'gradient'], [keys[2],'run']]

    tmp = {}
    for c in comb:
        res = get_avg(time_breakdown,
                c[0], c[1])
        res = np.array(res)
        tmp[c[1]] = np.hstack( (
            np.mean(res, axis=0)[0],
            np.std(res, axis=0)[0]
                   )
        )
        
        # print (f"{c[1]}: {np.mean(res, axis=0)} {np.std(res, axis=0)}")
    tmp = pd.DataFrame.from_dict(tmp, orient='index')
    tmp.columns = ['mean', 'std']
    all_results[num_subsets] = tmp
    # all_results.append(tmp)

# all_results = np.array(all_results)
# transpose so that rows are num_subsets and we only look at one of 
# direct/adjoint/gradient/run
# %% 
all_resultsT = {}
for c in comb:
    print (c[1])
    all_resultsT[c[1]] = {}
    for num_subsets in all_num_subsets:
        row = [ all_results[num_subsets]['mean'][c[1]], 
               all_results[num_subsets]['std'][c[1]]]
        df = pd.DataFrame(row).T
        df.columns = ['mean', 'std']
        all_resultsT[c[1]][num_subsets] = df


#%%
import matplotlib.pyplot as plt

# x = np.arange(len(all_num_subsets))  # the label locations
x = all_results[21].keys()

fig = plt.figure(figsize=(10,5))
plot_list = ['direct']#, 'adjoint', 'gradient']
for c in plot_list:
    x = np.array(list(all_resultsT[c].keys()))
    y = np.array(
        [ all_resultsT[c][k]['mean'] for k in all_resultsT[c].keys()]
    )
    dy = np.array(
        [ all_resultsT[c][k]['std'] for k in all_resultsT[c].keys()]
    )
    plt.errorbar(x, 
                 y.T[0], 
                 yerr=dy.T[0], 
                 label=c, color=f'C{plot_list.index(c)}')

    ty = [ all_resultsT[c][k]['mean'][0]/k for k in x ]
    plt.scatter(x, 
                ty, 
            label=f"{c} theoretical", color=f'C{plot_list.index(c)}')
# plt.errorbar(x, all_results.T[0][1], yerr=all_results.T[1][1], label='adjoint', color='C1')
# plt.scatter(x,[ all_results.T[0][1][0] / el for el in all_num_subsets], 
#          label='adjoint theoretical', color='C1')

# plt.errorbar(x, all_results.T[0][2], yerr=all_results.T[1][2], label='gradient', color='C2')
# plt.scatter(x,[ all_results.T[0][2][0] / el for el in all_num_subsets], 
#          label='gradient theoretical', color='C2')


# plt.xticks(ticks=[x for x in range(len(all_num_subsets))], 
#            labels=[ f"{el} subsets" for el in all_num_subsets ])
plt.ylabel("Time (s)")
plt.xlabel("Number of subsets")
plt.grid(axis='both')
plt.yscale('linear')
plt.legend()# %%

# %%
fig = plt.figure(figsize=(10,5))
plt.errorbar(x, all_results.T[0][3], yerr=all_results.T[1][3], label='iteration', marker='o')
plt.xticks(ticks=[x for x in range(len(all_num_subsets))], 
           labels=[ f"{el} subsets" for el in all_num_subsets ])
plt.ylabel("Time (s)")
plt.grid(axis='both')

plt.legend()# %%
# %%
