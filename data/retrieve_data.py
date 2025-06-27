# import logging
# from collections import defaultdict
from pathlib import Path, PurePath

# import matplotlib.pyplot as plt
# import numpy as np
# from tensorboard.backend.event_processing.event_accumulator import SCALARS, EventAccumulator
# from tqdm import tqdm
import os


teams = ['MaGeZ',  'SOS',  'Tomo-Unimib',  'UCL-EWS']
phantoms = ['Mediso_NEMA_lowcounts', 'Vision600_Hoffman']

algoteams = {
    'MaGeZ': ['ALG1', 'ALG2', 'ALG3'],
    'SOS': ['SAGA_final2', 'SVRG_final'],
    'Tomo-Unimib': ['LP_final'],
    'UCL-EWS': ['EWS_GD', 'EWS_SAGA', 'EWS_SGD']
}

base_path = Path('/opt/runner/logs')

def get_data(path: PurePath):
    """
    Retrieve data from TensorBoard event files.
    """
    # event_acc = EventAccumulator(path, size_guidance={SCALARS: 0})
    # event_acc.Reload()

    # # Get scalar tags
    # tags = event_acc.Tags()[SCALARS]
    
    # # Initialize a dictionary to hold the data
    # data = {}
    
    # for tag in tags:
    #     events = event_acc.Scalars(tag)
    #     steps = [event.step for event in events]
    #     values = [event.value for event in events]
    #     data[tag] = (steps, values)
    print (f"Processing path: {path}")


for team, algos in algoteams.items():
    for algo in algos:
        for phantom in phantoms:
            path = base_path / team / algo / phantom
            if path.exists():
                get_data(path)
            else:
                print(f"Path {path} does not exist.")