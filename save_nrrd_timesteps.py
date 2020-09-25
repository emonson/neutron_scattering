import numpy as np
import nrrd

kbx = np.load('kbx.npy')
kby = np.load('kby.npy')
kbz = np.load('kbz.npy')
intensity = np.load("Nb5K_Im-3m (229)_S{PBZ}E_BoseNorm.npy")

# spacings = (kbx[1]-kbx[0], kby[1]-kby[0], kbz[1]-kbz[0])
# origin = (kbx[0],kby[0],kbz[0])
# header_dict = {'spacings':spacings, 'space origin':origin}
# print(header_dict)

# 'space origin' seems to be screwing it up...
# https://pynrrd.readthedocs.io/en/latest/user-guide.html#supported-fields
header_dict = {'spacings':(0.025, 0.025, 0.05)}

# for ii in range(intensity.shape[3]):
for ii in range(60):
    filename = './Nb5k/NRRD/Nb5K_Im3m_' + str(ii).zfill(2) + '.nrrd'
    nrrd.write(filename, intensity[:,:,:,ii], index_order='F', header=header_dict)