# coding: utf-8

# ## Find peaks
# Ran `PlotOverRadialLines.py` in Paraview on Nb5k image data time series
# Want to find the peaks of intensity over radial lines from center of data set 
#   so maybe can produce a surface on those manifolds

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks_cwt
# https://github.com/anaxilaus/peakdetect
import peakdetect
from uvw import UnstructuredGrid, DataArray
from uvw.unstructured import CellType

# TODO: parameterize input and output file names
df = pd.read_csv('radial_n1000_r300.csv.gz', sep=',', encoding='utf-8', compression='gzip')
print('Data Loaded...')

# #### Could have compiled list of lists for final DataFrame
# But if possible I always want to avoid relying on column order and would instead 
# rather access items by name to make sure there aren't any indexing mistakes.
# 
# *Takes about 65 sec on desktop...*

idx = pd.IndexSlice
peaks_dict = {'timestep':[],'lineindex':[],'pointindex':[],'peakindex':[],'intensity':[],'px':[], 'py':[], 'pz':[]}

timesteps = df['timestep'].unique().tolist()
lines = df['lineindex'].unique().tolist()

# Create multi-index to grab time steps
df_mi = df.set_index(keys=['timestep','lineindex','pointindex'])

# Skipping first time step
for ts in timesteps[1:]:
    print('Find peaks time', ts)
    # Much faster below for line selection if make a time subset to search in
    df_ts = df_mi.loc[(ts,),:]
    for ln in lines:
        df_subset = df_ts.loc[(ln,),:]
        x = df_subset['intensity'].values
        pos_neg_pks = peakdetect.peakdetect(x, lookahead=4, delta=0.05)

        # Result are returned as a list of pos,neg peaks, each with index,intensity
        pks = [pp[0] for pp in pos_neg_pks[0]]
        
        for pk_idx,pk in enumerate(pks):
            # indexing into df_subset loses index values...
            pt_dict = df_subset.loc[pk,:].to_dict()
            peaks_dict['timestep'].append(ts)
            peaks_dict['lineindex'].append(ln)
            peaks_dict['pointindex'].append(pk)
            peaks_dict['peakindex'].append(pk_idx)
            for k,v in pt_dict.items():
                peaks_dict[k].append(v)

df_peaks = pd.DataFrame(peaks_dict)

# ### Now need to turn this into a real VTK structure of points over time...
# Try Unstructured Grid from https://pypi.org/project/uvw/

# Index peak points by time for gathering intensities and coordinates
df_pts = df_peaks.set_index(keys='timestep')

for ts in df_pts.index.unique().tolist():
    print('UG time', ts)
    df_subset = df_pts.loc[ts,:]
    nodes = df_subset[['px','py','pz']].to_numpy()
    if nodes.ndim == 1:
        nodes = np.expand_dims(nodes,0)
    n_pts = nodes.shape[0]

    # vertex node connectivity needs to be like list of single element lists
    connectivity = {
        CellType.POLY_VERTEX: np.arange(n_pts).reshape(-1,1)
    }

    f = UnstructuredGrid('./Ugrid/ugrid_' + str(ts).zfill(2) + '.vtu', nodes, connectivity)
    
    for col in (set(df_pts.columns.tolist())-set(['px', 'py', 'pz'])):
        if n_pts == 1:
            data_array = np.array([df_subset[col]])
        else:
            data_array = df_subset[col].to_numpy()
        f.addPointData(DataArray(data_array, range(1), col))
    f.write()
