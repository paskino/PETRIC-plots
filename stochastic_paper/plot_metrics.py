#%%
import matplotlib.pyplot as plt
import pickle
import os
from warnings import warn

ROIS = [
"RMSE_whole_object",
"RMSE_background",
"AEM_VOI_sphere1",
"AEM_VOI_sphere3",
"AEM_VOI_sphere5",
]
algorithms = [ "SG", "SAG", "SAGA", "SVRG", "LSVRG", "SOS-SAGAfinal2"]
# algorithms = ['SAG', 'SAGA', 'SG', 'SVRG']
# algorithms = ['SOS-SAGAfinal2']
subsets = [21,42,63]
# subsets = [42]
dataset = ['mMR_NEMA_lowcounts']

#%%
data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'PETRIC-SOS', 'data_read')
# Open the file in read-binary mode
with open(os.path.join(data_dir, 'allresults_lowcounts3.pkl'), 'rb') as file:
    # Deserialize the dictionary from the file
    loaded_dict = pickle.load(file)

#%%
# plot one algorithm WRT number of subsets
linestyles = ['solid', 'dotted', 'dashed', 'solid', 'dotted', 'dashed']
linecolors = ['C0', 'C1', 'C2', 'C3', 'C4', 'C5']
# import pysnooper
# @pysnooper.snoop()
def _plot_it(data, algs: list, num_subsets, which, dataset="mMR_NEMA", linecolors=linecolors, 
             linestyles=linestyles, 
             yscale='linear', figsize=None, xlim=None, legend_loc=None, savefig=False,
            title:list=None, ylabel:str=None, show_legend:bool=True,
            additional_text:tuple=None):
    """
    legend_loc: 'upper left', 'upper right', 'lower left', 'lower right'
    """
    plt.figure(figsize=figsize)
    if not isinstance(num_subsets, list):
        num_subsets = [num_subsets]
    for alg_idx, alg in enumerate(algs):
        for ns_idx,ns in enumerate(num_subsets):
            idx = f"{alg}_{dataset}_{ns}"
            # print (f"processing {idx}")
            algdata = data[idx]
            tmp = algdata['iteration_num']
            if which == 'objective':
                x = [ el/num_subsets[ns_idx] for el in algdata['iteration_num']]
                y = algdata['objective']
                xlabel = 'epoch'
            else:
                # why this has one more than the data passes?
                
                if alg in ["SAG", "SAGA"]:
                    x = algdata['data_passes']
                    # the last one is the one at 80 epochs
                    y = algdata[which][:-1]
                    # print (f"{alg} {len(x)} {len(y)}")
                elif alg == "SOS-SAGAfinal2":
                    # we do 5 full gradients in SOS but the number of data passes is not accounted
                    # for correctly
                    x = [el + 5 for el in algdata['data_passes'] ]
                    x = [1,2,3,4,5] + x
                    y = algdata[which][:-1]
                    
                # x = [el for el in range(len(y))]
                xlabel = 'Data passes'

            # select only the values within xlim
            xx = x.copy()
            yy = y.copy()
            x = []
            y = []
            for i,el in enumerate(xx):
                if el <= xlim[1] and el >= xlim[0]:
                    x.append(el)
                    y.append(yy[i])
            
            # take from x (and y) the values within xlim
            if len(x) == len(y):
                ii = ns_idx + len(num_subsets) * alg_idx
                if title is None:
                    ttl = f"{alg} {ns} subsets"
                else:
                    ttl = title[ii]
                
                # print (f"{alg} ii {ii}, alg_idx {alg_idx} ns_idx {ns_idx}")
                fkwargs = {'linestyle': linestyles[ii] ,
                           'color': linecolors[ii]}
                        
                plt.plot(x,y, label=ttl, **fkwargs)
            else:
                warn(f"ERROR: {alg} {idx} {which}: len(x) != len(y) {len(x)}=!{len(y)} ")

    legend_size = 14
    if show_legend:
        if legend_loc is not None:
            plt.legend(loc=legend_loc, prop={'size': legend_size}, ncol=1)
        else:
            plt.legend(prop={'size': legend_size},ncol=1)
    plt.xlabel(xlabel)
    if xlim is not None:
        plt.xlim(xlim)
    if ylabel is None:
        ylabel = which
    plt.ylabel(ylabel)
    plt.yscale(yscale)
    # plt.title(which)
    if additional_text is not None:
        plt.text(*additional_text)

    # grids
    plt.grid(visible=True, which='both', axis='both', alpha=0.5, linewidth=0.5)
    if savefig:
        print("saving fig")
        gcf = plt.gcf()
        gcf.savefig(f"{which}_{num_subsets}.png", format='png')
    plt.show()
    
#%%
_linestyles = ['solid', 'dotted', 'dashed', 'dashdot']
_algos = algorithms
subsets = [1,21,42,63]

def get_linestyles(subsets, algos=_algos, linestyles=_linestyles):
    ls = []
    for algo in algos:
        for i,ds in enumerate(subsets):
            ls.append(linestyles[i])
    return ls

# linecolors = [f'C{i}' for i in [0,0,0,1,1,1,2,2,2,3,3,3,4,4,4,5,5,5]]
def get_linecolors(subsets, algos):
    lc = []
    for i,_ in enumerate(algos):
        for _ in subsets:
            lc.append(f'C{i}')
    return lc

# linestyles = get_linestyles(subsets)
# print (linestyles)
# print (get_linecolors(subsets, _algos))
#%%
import matplotlib
matplotlib.rcParams.update({'font.size': 20})
matplotlib.rcParams.update({'lines.linewidth': 3.0})
algos = [ "SAGA", "SOS-SAGAfinal2"]
_algos = algos
savefig = True
#"SG", "SAG", "SAGA", "SVRG", "LSVRG", 
_plot_it(loaded_dict, _algos , subsets, 
         which=ROIS[0], dataset="mMR_NEMA_lowcounts",
         linestyles=get_linestyles(subsets, algos),
         linecolors=get_linecolors(subsets, algos), 
         figsize=(9,7), yscale="log", xlim=(0,30),
         legend_loc='lower left', savefig=savefig,
        title=["SAGA-1 (N=1)", "SAGA-1 (N=21)", "SAGA-1 (N=42)", "SAGA-1 (N=63)",
              "SAGA-SOS (N=1)", "SAGA-SOS (N=21)", "SAGA-SOS (N=42)", "SAGA-SOS (N=63)"],
        ylabel="RMSE whole object",
        additional_text=(25,3e-1,"A"))

#%%
_plot_it(loaded_dict, _algos, subsets, 
         which=ROIS[2], dataset="mMR_NEMA_lowcounts",
         linestyles=get_linestyles(subsets, algos),
         linecolors=get_linecolors(subsets, algos),  figsize=(9,7), yscale="log", xlim=(0,30),
         legend_loc='lower left', savefig=savefig, 
        title=["SAGA-1 1 subsets", "SAGA-1 21 subsets", "SAGA-1 42 subsets", "SAGA-1 63 subsets",
              "SAGA-SOS 1 subsets", "SAGA-SOS 21 subsets", "SAGA-SOS 42 subsets", "SAGA-SOS 63 subsets"],
        ylabel="AEM sphere 1", show_legend=False,
        additional_text=(25,7e-1,"B"))
# %%
