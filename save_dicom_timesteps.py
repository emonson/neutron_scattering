import numpy as np
import SimpleITK as sitk

kbx = np.load('kbx.npy')
kby = np.load('kby.npy')
kbz = np.load('kbz.npy')
intensity = np.load("Nb5K_Im-3m (229)_S{PBZ}E_BoseNorm.npy")

# NOTE: This isn't going to set the spacing of the images properly yet...
for ii in range(intensity.shape[3]):
    filename = './Nb5k/DICOM/Nb5K_Im3m_' + str(ii).zfill(2) + '.dcm'
    img = sitk.GetImageFromArray((65536*intensity[:,:,:,ii]).astype(np.uint16))
    sitk.WriteImage(img,filename)