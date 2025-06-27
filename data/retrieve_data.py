# import logging
# from collections import defaultdict
from pathlib import Path, PurePath

# import matplotlib.pyplot as plt
# import numpy as np
from tensorboard.backend.event_processing.event_accumulator import SCALARS, EventAccumulator
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

def valid(tensorboard_logfile: PurePath) -> bool:
    """False if invalid/empty logfile"""
    ea = EventAccumulator(str(tensorboard_logfile), size_guidance={SCALARS: 0})
    ea.Reload()
    return len({"RMSE_whole_object", "RMSE_background"}.intersection(ea.Tags()['scalars'])) == 2

# def get_data(path: PurePath):
#     """
#     Retrieve data from TensorBoard event files.
#     """
#     print (f"Processing path: {path}")
#     ea = EventAccumulator(str(tensorboard_logfile), size_guidance={SCALARS: 0})
#     ea.Reload()

#     try:
#         start_scalar = ea.Scalars("reset")[0]
#     except KeyError:
#         log.error("KeyError: reset: not using accurate relative time for %s", tensorboard_logfile.relative_to(LOGDIR))
#         start = 0.0
#     else:
#         assert start_scalar.value == 0
#         assert start_scalar.step == -1
#         start = start_scalar.wall_time

#     tag_names: set[str] = {tag for tag in ea.Tags()['scalars'] if any(tag.startswith(i) for i in TAGS)}
#     if (skip := TAG_BLACKLIST & tag_names):
#         log.warning("skipping tags: %s", skip)
#         tag_names -= skip
#     tags = {tag: scalars(ea, tag) for tag in tag_names}

#     metrics: np.ndarray = [tags.pop("RMSE_whole_object"), tags.pop("RMSE_background")]
#     thresholds = [
#         QualityMetrics.THRESHOLD["RMSE_whole_object"],
#         QualityMetrics.THRESHOLD["RMSE_background"],] + [QualityMetrics.THRESHOLD["AEM_VOI"]] * len(tags)
#     metrics.extend(tags.values())
#     metrics = np.array(metrics).T # [(value, time), step, (RMSE, RMSE, VOI, ...)]
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
    


for team, algos in algoteams.items():
    for algo in algos:
        for phantom in phantoms:
            path = base_path / team / algo / phantom
            if path.exists():
                for logfile in path.glob("events.out.tfevents.*"):
                    # get_data(logfile) for logfile in dataset.glob("events.out.tfevents.*") if valid(logfile)]
                    print (f"Processing logfile: {logfile}")
                    if valid(logfile):
                        print(f"Logfile {logfile} is valid.")
                    else:
                        print(f"Logfile {logfile} is invalid or empty.")
                
            else:
                print(f"Path {path} does not exist.")