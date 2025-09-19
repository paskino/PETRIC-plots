#%%
import json
import csv
import numpy as np
import pandas as pd

num_subsets = 14
repetitions = 30

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

# collate all results
all_results = {}
all_num_subsets = [3,7,14,21,42,63]

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
    # tmp = pd.DataFrame.from_dict(tmp, orient='index')
    # tmp.columns = ['mean', 'std']
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
    rows = []
    for num_subsets in all_num_subsets:
        row = [ all_results[num_subsets][c[1]][0],
                all_results[num_subsets][c[1]][1]]
        
        rows.append(row)

        all_resultsT[c[1]] = np.array(rows).T
        # df = pd.DataFrame(row).T
        # df.columns = ['mean', 'std']
        # all_resultsT[c[1]][num_subsets] = df


#%%
import matplotlib.pyplot as plt

# x = np.arange(len(all_num_subsets))  # the label locations
x = all_results[21].keys()

fig = plt.figure(figsize=(10,5))
plot_list = ['direct', 'adjoint', 'gradient', 'run']
plot_fit = False
# plot_list = ['adjoint']
linear = True
for c in plot_list:
    if linear:
        x = [ 1/el for el in all_num_subsets[::-1] ]
        plt.xlabel("1/Number of subsets")
        
        plt.xticks(ticks=x, 
                   labels=[ f"{el}" for el in all_num_subsets[::-1] ],
                   rotation=-45)
    else:
        x = np.arange(len(all_num_subsets))  # the label locations

        plt.xticks(ticks=x, 
                   labels=[ f"{el}" for el in all_num_subsets ])
    y = all_resultsT[c][0][::-1] 
    dy = all_resultsT[c][1][::-1]
    ty = all_resultsT[c][0][0] / np.array(all_num_subsets)[::-1]
    m,q = np.polyfit(x, y, 1)
    plt.errorbar(x, 
                 y, 
                 yerr=dy, 
                 label=f"{c} {m:.2f} {q:.2f}", color=f'C{plot_list.index(c)}')
    if plot_fit and linear and c in ['direct', 'adjoint', 'gradient']:
        plt.plot(x, 
                m*np.array(x)+q, 
                linestyle='--', color=f'C{plot_list.index(c)}')
    
    # plt.scatter(x, 
    #             ty, 
    #         label=f"{c} theoretical", color=f'C{plot_list.index(c)}')

plt.ylabel("Time (s)")
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
