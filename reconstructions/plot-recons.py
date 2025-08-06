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
                "crop": (25, slice(35, 115), slice(37, 117)),
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
                "diff_range": (-0.01, 0.01),
                "VOI" : [
                    {"fname": "VOI_2.v"},
                    {"fname": "VOI_3.v"},
                    {"fname": "VOI_4.v"},
                ]},

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
                "diff_range": (-0.1, 0.1),
                "VOI" : [
                    {"fname": "VOI_GM.v"},
                    {"fname": "VOI_ventricles.v"},
                    {"fname": "VOI_WM.v"},
                ]
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
    
    voi_data = {}
    for voi in phantoms[phantom_name]['VOI']:
        fname = os.path.join(phantoms[phantom_name]['dirname'], voi['fname'])
        tmp = np.fromfile(fname, dtype=np.float32).reshape(shape)
        voi_data[voi['fname'].strip(".v")] = tmp.reshape(shape)
    
    return ret, reference, voi_data

# %%
# Mediso NEMA low counts
# dphantom = "NEMA"
dphantom = "Hoffman"

algos, reference , VOIs = get_phantom_data(dphantom, phantoms)
# NEMA_reference = np.fromfile(fname, dtype=np.float32).reshape(shape)
show2D(reference.__getitem__(phantoms[dphantom]['crop']), 
    #    slice_list=(0,25), 
       num_cols=3,
       title = "reference",
       origin="upper-left", 
       cmap="cubehelix_r", fix_range=True)


# %%

nemafig = show2D([v.__getitem__(phantoms[dphantom]['crop']) for k,v in algos.items()], 
    #    slice_list=(0,25), 
       num_cols=3,
       title = [k for k,v in algos.items()],
       origin="upper-left", 
       cmap="cubehelix_r", fix_range=True)
# %%
nemafig = show2D([(v - reference).__getitem__(phantoms[dphantom]['crop']) for k,v in algos.items()], 
    #    slice_list=(0,25), 
       num_cols=3,
       title = [k for k,v in algos.items()],
       origin="upper-left", 
       cmap="seismic", fix_range=phantoms[dphantom]['diff_range'])

# %%
# calculate the statistics of the VOI

fig, axs = plt.subplots(3, 3)
for kk,voi in VOIs.items():
    for ax, k in zip(fig.get_axes(), algos.keys()):
        ax.hist(algos[k][voi > 0], bins=20, label=kk, alpha=1, histtype='step')
ax.legend(prop={'size': 10})
fig.suptitle(f"{dphantom}")
fig.show()
# %%
