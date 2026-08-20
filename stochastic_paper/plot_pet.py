# %%
import os
import numpy as np
import re
import glob

print (__file__, os.path.dirname(__file__))
#%%
data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'PETRIC-SOS', 'data_read')
os.chdir(os.path.dirname(__file__))
from cil.utilities.display import show2D
import matplotlib.pyplot as plt


crop = (71, slice(35, 115), slice(37, 117))
# crop = (71, None, None)

data = {}
for alg in ["SAGA", "SOS-SAGAfinal2"]:
    for ns in [21,42,63]:
        key = f"{alg}_{ns}"
        data[key] = np.load(f"{key}.npy")

reference = np.load("reference.npy")
whole_object = np.load("whole_object.npy")
spheres = {
    "sphere1": np.load("VOI_sphere1.npy"),
    "sphere5": np.load("VOI_sphere5.npy"),
    "sphere3": np.load("VOI_sphere3.npy"),
}

#%%
fig, axs = plt.subplots(2, 3, figsize=(12, 6.5))
# Remove all spacing between subplots
crop = (71, slice(30, 150), slice(37, 190))

for kv, ax in zip(data.items(), axs.flatten()):
    k, v = kv
    mask = whole_object.__getitem__(crop) > 0
    # img[~mask] = 0
    v = v.__getitem__(crop)
    v[~mask] = 0
    ref = reference.__getitem__(crop)
    ref[~mask] = 0
    img = ((v - ref)/ref)
    np.nan_to_num(img, nan=0, posinf=0, neginf=0)

    # img = v.__getitem__(crop)
    img = np.squeeze(img)
    # img = v-reference
    algo, ns = k.split("_")
    if algo == "SOS-SAGAfinal2":
        algo = "SAGA-SOS"
    elif algo == "SAGA":
        algo = "SAGA-1"
    title = f"{algo} (N={ns})"
    cmap = "seismic"
    # cmap = "gray"
    # vmin, vmax = (-2e-4, 2e-4)
    vmin, vmax = (-5e-2, 5e-2)
    sp = ax.imshow(img, cmap=cmap, 
                   vmin=vmin, vmax=vmax, 
                   label=title)
    ax.annotate(title, xy=(3, 12), textcoords='data', ha='left', 
                fontsize=15)
    ax.set_xticklabels([])
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_yticklabels([])

cax = plt.axes([0.8, 0.025, 0.02, 0.72])  # Adjust the position of the colorbar
from matplotlib.ticker import PercentFormatter
mf = PercentFormatter(xmax=1, decimals=0)
fig.colorbar(sp, orientation='vertical', 
             use_gridspec=True,
             cax=cax,
             format=mf)
# Remove tight_layout as it overrides GridSpec spacing
# fig.tight_layout()

# main_title = f"{dphantom} phantom on {scanner}"
# fig.suptitle(main_title, fontsize=16)
# Remove tight_layout and use subplots_adjust to control spacing precisely
plt.subplots_adjust(wspace=0.03, hspace=0.02, 
                    left=0.02, right=0.78, 
                    top=0.75, bottom=0.02)
# Ensure no spacing and tight layout
dfig = plt.gcf()
plt.show()
dfig.savefig(f"PET_whole_volume_diff.png")
# %%

