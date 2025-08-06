# %%
import os
import numpy as np
import re

from cil.utilities.display import show2D

# %%
# Mediso NEMA low counts

# %%

fname = os.path.abspath(
    os.path.join(
    "/Users/edoardo.pasca/Documents/Papers/PETRIC/PETRIC-paper-data/NEMA", 
        f"reference_image.v")
)
# load as np array from the interfile
shape = (75, 155, 155)
crop = slice(40,120)

NEMA_reference = np.fromfile(fname, dtype=np.float32).reshape(shape)
show2D(NEMA_reference[25,35:115,37:117], 
    #    slice_list=(0,25), 
       num_cols=3,
       title = "NEMA reference",
       origin="upper-left", 
       cmap="cubehelix_r", fix_range=True)
# %%
# https://discord.com/channels/1242028164105109574/1248216263059177533/1401898950734381058

txt = """MaGeZ/ALG1/Mediso_NEMA_lowcounts/iter_0064.v
MaGeZ/ALG2/Mediso_NEMA_lowcounts/iter_0055.v
MaGeZ/ALG3/Mediso_NEMA_lowcounts/iter_0054.v
SOS/SAGA_final2/Mediso_NEMA_lowcounts/iter_0002.v
SOS/SVRG_final/Mediso_NEMA_lowcounts/iter_0003.v
Tomo-Unimib/LP_final/Mediso_NEMA_lowcounts/iter_0007.v
UCL-EWS/EWS_GD/Mediso_NEMA_lowcounts/iter_0008.v
UCL-EWS/EWS_SAGA/Mediso_NEMA_lowcounts/iter_0072.v
UCL-EWS/EWS_SGD/Mediso_NEMA_lowcounts/iter_0189.v"""
NEMA = {}
for line in txt.split("\n"):
    team, algo, phantom, string = line.split("/")
    # Match exactly 4 digits after "iter_"
    match = re.search(r'iter_(\d{4})', string)
    if match:
        number = match.group(1)  # Returns "0055"
        fname = os.path.abspath(
            os.path.join(
            "/Users/edoardo.pasca/Documents/Papers/PETRIC/PETRIC-paper-data/", 
            team, algo, phantom, 
                f"iter_{number}.v")
        )
        # load as np array from the interfile
        shape = (75, 155, 155)
        tmp = np.fromfile(fname, dtype=np.float32).reshape(shape)
        NEMA[f"{phantom}/{team}/{algo}"] = tmp.reshape(shape)

# %%

nemafig = show2D([v[25,35:115,37:117]  for k,v in NEMA.items()], 
    #    slice_list=(0,25), 
       num_cols=3,
       title = [k for k,v in NEMA.items()],
       origin="upper-left", 
       cmap="cubehelix_r", fix_range=True)
# %%
nemafig = show2D([(v - NEMA_reference)[25,35:115,37:117] for k,v in NEMA.items()], 
    #    slice_list=(0,25), 
       num_cols=3,
       title = [k for k,v in NEMA.items()],
       origin="upper-left", 
       cmap="seismic", fix_range=(-0.01, 0.01))
# %%
# load the NEMA VOIs

fname = os.path.abspath(
    os.path.join(
    "/Users/edoardo.pasca/Documents/Papers/PETRIC/PETRIC-paper-data/NEMA", 
        f"VOI_2.v")
)
# load as np array from the interfile
shape = (75, 155, 155)
crop = slice(40,120)

NEMA_VOI_2 = np.fromfile(fname, dtype=np.float32).reshape(shape)

#%%
show2D(NEMA_VOI_2[25,35:115,37:117], 
    #    slice_list=(0,25), 
       num_cols=3,
       title = "NEMA reference",
       origin="upper-left", 
       cmap="cubehelix_r", fix_range=True)
# %%
# calculate the statistics of the VOI

fig = plt.figure()
gs = fig.add_gridspec(3, 3)
# axs = gs.subplots(sharex='col', sharey='row')
axs = fig.subplots(3, 3)
for ax, k in zip(fig.get_axes(), NEMA.keys()):
    ax.hist(NEMA[k][NEMA_VOI_2 > 0], bins=20)

fig.show()
# %%
v = NEMA['Mediso_NEMA_lowcounts/MaGeZ/ALG1'][NEMA_VOI_2 > 0]
print(f"Mean: {np.mean(v):.3f}, Std: {np.std(v):.3f}, Max: {np.max(v):.3f}, Min: {np.min(v):.3f}")

# %%
import matplotlib.pyplot as plt
plt.hist(v, bins=20)
# %%
