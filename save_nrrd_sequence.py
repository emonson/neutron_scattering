import numpy as np
import SimpleITK as sitk

kbx = np.load('kbx.npy')
kby = np.load('kby.npy')
kbz = np.load('kbz.npy')
intensity = np.load("Nb5K_Im-3m (229)_S{PBZ}E_BoseNorm.npy")

# This saves as an "Image sequence", which is different from a "multi-volume"
# so it can be played back more conveniently than a multi-volume in Slicer
# 4th dimension gets saved as a vector of scalars in each pixel

# NOTE: image dimensions end up reversed from Numpy convention (zyx)
im_seq = sitk.GetImageFromArray(intensity[:,:,:,:60])
im_seq.SetSpacing((0.05, 0.025, 0.025))
im_seq.SetOrigin((-0.5, -0.5, -1.0))
print(im_seq)

writer = sitk.ImageFileWriter()
writer.SetFileName('./Nb5k/Ng5K_Im3m.seq.nrrd')
writer.Execute(im_seq) 