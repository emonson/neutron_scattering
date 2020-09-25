import numpy as np
from uvw import RectilinearGrid, DataArray

kbx = np.load('kbx.npy')
kby = np.load('kby.npy')
kbz = np.load('kbz.npy')
intensity = np.load("Nb5K_Im-3m (229)_S{PBZ}E_BoseNorm.npy")

for ii in range(intensity.shape[3]):
    filename = './Nb5k/Nb5K_Im3m_' + str(ii).zfill(2) + '.vtr'
    grid = RectilinearGrid(filename, (kbx,kby,kbz), compression=False)
    grid.addPointData(DataArray(intensity[:,:,:,ii], range(3), 'Intensity'))
    grid.write()
