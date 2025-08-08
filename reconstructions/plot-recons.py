# %%
import os
import numpy as np
import re

from cil.utilities.display import show2D
import matplotlib.pyplot as plt
# %%
# phantoms
# https://discord.com/channels/1242028164105109574/1248216263059177533/1401898950734381058


phantoms = {"NEMA": {
                "shape": (75, 155, 155),
                "crop": (21, slice(35, 115), slice(37, 117)),
                "reference": "reference_image.v",
                "dirname": "/Users/edoardo.pasca/Documents/Papers/PETRIC/PETRIC-paper-data/NEMA",
                "algos":  """MaGeZ/ALG1/Mediso_NEMA_lowcounts/iter_0064.v
MaGeZ/ALG2/Mediso_NEMA_lowcounts/iter_0055.v
MaGeZ/ALG3/Mediso_NEMA_lowcounts/iter_0054.v
SOS/SAGA_final2/Mediso_NEMA_lowcounts/iter_0002.v
SOS/SVRG_final/Mediso_NEMA_lowcounts/iter_0003.v
Tomo-Unimib/LP_final/Mediso_NEMA_lowcounts/iter_0007.v
UCL-EWS/EWS_GD/Mediso_NEMA_lowcounts/iter_0008.v
UCL-EWS/EWS_SAGA/Mediso_NEMA_lowcounts/iter_0072.v
UCL-EWS/EWS_SGD/Mediso_NEMA_lowcounts/iter_0189.v""",
                "diff_range": (-0.012, 0.012),
                "diff_scale_max": 0.1,
                # "diff_range": [(-0.005, 0.005),(-0.005, 0.005),(-0.005, 0.005),
                #                (-0.05, 0.05),(-0.05, 0.05),(-0.15,0.15),
                #                (-0.025, 0.025),(-0.025, 0.025),(-0.025, 0.025)],
                "VOI" : [
                    {"fname": "VOI_2.v"},
                    {"fname": "VOI_3.v"},
                    {"fname": "VOI_4.v"},
                ],
                "OSEM": "OSEM_image.v",
                },

            "Hoffman": {
                "shape": (159, 169, 169),
                "crop": (79, slice(30, 140), slice(30, 140)),
                "reference": "reference_image.v",
                "dirname": "/Users/edoardo.pasca/Documents/Papers/PETRIC/PETRIC-paper-data/Hoffman",
                "algos": """MaGeZ/ALG1/Vision600_Hoffman/iter_0450.v
MaGeZ/ALG2/Vision600_Hoffman/iter_0450.v
MaGeZ/ALG3/Vision600_Hoffman/iter_0520.v
SOS/SAGA_final2/Vision600_Hoffman/iter_0149.v
SOS/SVRG_final/Vision600_Hoffman/iter_0099.v
Tomo-Unimib/LP_final/Vision600_Hoffman/iter_0033.v
UCL-EWS/EWS_GD/Vision600_Hoffman/iter_0177.v
UCL-EWS/EWS_SAGA/Vision600_Hoffman/iter_0337.v
UCL-EWS/EWS_SGD/Vision600_Hoffman/iter_0453.v""",
                "diff_range": (-0.05, 0.05),
                "diff_scale_max": 0.1,
                "VOI" : [
                    {"fname": "VOI_GM.v"},
                    {"fname": "VOI_ventricles.v"},
                    {"fname": "VOI_WM.v"},
                ],
                "OSEM": "OSEM_image.v",
                },
}

def get_phantom_data(phantom_name, phantoms):
    ret = {}
    for line in phantoms[phantom_name]['algos'].split("\n"):
        team, algo, phantom, string = line.split("/")
        # Match exactly 4 digits after "iter_"
        match = re.search(r'iter_(\d{4})', string)
        if match:
            number = match.group(1)  # Returns "0055"
            fname = os.path.abspath(
                os.path.join(
                phantoms[phantom_name]['dirname'], "..", 
                team, algo, phantom, 
                    f"iter_{number}.v")
            )
            # load as np array from the interfile
            shape = phantoms[phantom_name]['shape']
            tmp = np.fromfile(fname, dtype=np.float32).reshape(shape)
            ret[f"{team}/{algo}/{phantom}"] = tmp.reshape(shape)

    fname = os.path.join(phantoms[phantom_name]['dirname'], phantoms[phantom_name]['reference'])
    reference = np.fromfile(fname, dtype=np.float32).reshape(shape)
    fname = os.path.join(phantoms[phantom_name]['dirname'], phantoms[phantom_name]['OSEM'])
    osem = np.fromfile(fname, dtype=np.float32).reshape(shape)
    
    voi_data = {}
    for voi in phantoms[phantom_name]['VOI']:
        fname = os.path.join(phantoms[phantom_name]['dirname'], voi['fname'])
        tmp = np.fromfile(fname, dtype=np.float32).reshape(shape)
        voi_data[voi['fname'].strip(".v")] = tmp.reshape(shape)
    
    return ret, reference, voi_data, osem

# %%
# Mediso NEMA low counts
# dphantom = "NEMA"
dphantom = "Hoffman"

algos, reference , VOIs, osem = get_phantom_data(dphantom, phantoms)
# NEMA_reference = np.fromfile(fname, dtype=np.float32).reshape(shape)
fig = show2D([el.__getitem__(phantoms[dphantom]['crop']) for el in [reference, osem]], 
    #    slice_list=(0,25), 
       num_cols=3,
       title = ["reference","OSEM"],
       origin="upper-left", 
       cmap="afmhot_r", fix_range=True)
fig.save(f"{dphantom}_reference_osem.png")


fig, axs = plt.subplots(1, 3)
labels = ["reference", "OSEM"]
for ax, (kk, voi) in zip (fig.get_axes(), VOIs.items()):
    for i,v in enumerate([reference, osem]):
        ax.hist(v[voi > 0], bins=20, label=labels[i], alpha=1, histtype='step')
        ax.set_title(kk)
ax.legend(prop={'size': 10})
fig.suptitle(f"{dphantom}")
fig.show()
fig.savefig(f"{dphantom}_VOI_hist_reference_osem.png")

# find range for the difference images as 10% of the max value in the reference image
max_value = np.max(reference)
diff_range = (-phantoms[dphantom]['diff_scale_max'] * max_value, 
               phantoms[dphantom]['diff_scale_max'] * max_value)
# %%

nemafig = show2D([v.__getitem__(phantoms[dphantom]['crop']) for k,v in algos.items()], 
    #    slice_list=(0,25), 
       num_cols=3,
       title = [k for k,v in algos.items()],
       origin="upper-left", 
       cmap="cubehelix_r", fix_range=True)

nemafig.save(f"{dphantom}.png")
# %%
no_xticks = []
no_yticks = []
for k,v in algos.items():
    team, algo, scanner = k.split("/")
    if (team, algo) == ("MaGeZ", "ALG1") or \
        (team, algo) == ("SOS", "SAGA_final2") or \
        (team, algo) == ("UCL-EWS", "EWS_GD"):
        no_yticks.append(False)
    else:
        no_yticks.append(True)
for k,v in algos.items():
    team, algo, scanner = k.split("/")
    if team == "UCL-EWS":
        no_xticks.append(False)
    else:
        no_xticks.append(True)

nemafig = show2D([(v - reference).__getitem__(phantoms[dphantom]['crop']) for k,v in algos.items()], 
    #    slice_list=(0,25), 
       num_cols=3,
       title = [k for k,v in algos.items()],
       origin="upper-left", 
       cmap="seismic", fix_range=diff_range,
       no_xticks=no_xticks, no_yticks=no_yticks, no_colorbar=True,
       facecolor='w')
nemafig.save(f"{dphantom}_diff.png")


#%%
from matplotlib.gridspec import GridSpec

fig, axs = plt.subplots(3, 3, figsize=(10, 10))
# Remove all spacing between subplots

for kv, ax in zip(algos.items(), axs.flatten()):
    k, v = kv
    img = (v - reference).__getitem__(phantoms[dphantom]['crop'])
    team, algo, scanner = k.split("/")
    title = f"{team} {algo}"
    cmap = "seismic"
    vmin, vmax = diff_range
    sp = ax.imshow(img, cmap=cmap, vmin=vmin, vmax=vmax, label=title)
    ax.annotate(title, xy=(3, 5), textcoords='data', ha='left', fontsize=10)
    ax.set_xticklabels([])
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_yticklabels([])

cax = plt.axes([0.915, 0.02, 0.02, 0.907])  # Adjust the position of the colorbar
fig.colorbar(sp, orientation='vertical', 
             use_gridspec=True,
             cax=cax)
# Remove tight_layout as it overrides GridSpec spacing
# fig.tight_layout()

main_title = f"{dphantom} phantom on {scanner}"
fig.suptitle(main_title, fontsize=16)
# Remove tight_layout and use subplots_adjust to control spacing precisely
plt.subplots_adjust(wspace=0.03, hspace=0.02, 
                    left=0.02, right=0.91, 
                    top=0.93, bottom=0.02)
# Ensure no spacing and tight layout
dfig = plt.gcf()
plt.show()
dfig.savefig(f"{dphantom}_diff.png")
# %%
# calculate the statistics of the VOI

fig, axs = plt.subplots(3, 3)
for kk,voi in VOIs.items():
    for ax, k in zip(fig.get_axes(), algos.keys()):
        ax.hist(algos[k][voi > 0], bins=20, label=kk, alpha=1, histtype='step')
ax.legend(prop={'size': 10})
fig.suptitle(f"{dphantom}")
fig.show()

fig.savefig(f"{dphantom}_VOI_hist.png")
# %%
# evaluate the total variation of the reconstructions as proxy of smoothness


from cil.optimisation.functions import TotalVariation
from cil.framework import ImageGeometry, ImageData

ig = ImageGeometry(voxel_num_x=phantoms[dphantom]['shape'][2],
                   voxel_num_y=phantoms[dphantom]['shape'][1],
                   voxel_num_z=phantoms[dphantom]['shape'][0])

TV = {}
for k,v in algos.items():
    a = ig.allocate(None)
    a.fill(v)
    # a = ImageData(v, geometry=ig)
    TV[k] = TotalVariation(max_iteration=1000)(a)

print (f"TV for {dphantom} phantom: {TV}")
# %%
x = np.arange(0, 10, 0.1)
y = np.sin(x)
fig = plt.figure()
gs = fig.add_gridspec(3, 3, hspace=0, wspace=0)
(ax1, ax2) , (ax3, ax4) = gs.subplots(sharex='col', sharey='row')
fig.suptitle('Sharing x per column, y per row')
ax1.plot(x, y)
ax2.plot(x, y**2, 'tab:orange')
ax3.plot(x + 1, -y, 'tab:green')
ax4.plot(x + 2, -y**2, 'tab:red')

ax3.plot(x + 1, -y, 'tab:green')
ax4.plot(x + 2, -y**2, 'tab:red')

ax12.plot(x + 1, -y, 'tab:green')
ax23.plot(x + 2, -y**2, 'tab:red')

for ax in fig.get_axes():
    ax.label_outer()
# %%
