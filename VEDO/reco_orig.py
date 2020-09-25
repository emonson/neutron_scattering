from vedo import *
import numpy as np

data_dir = '/Users/emonson/Dropbox/People/OlivierDelaire/Data Visualization for INS/Nb_symmetrized_data/PeaksUgrid/'

vp = Plotter()

orig_points = vp.load(data_dir+"ugrid_23.vtu")
pts0 = Points(orig_points.points(), r=3).legend("original points")
vp.add(pts0)

# reconstructed surface from point cloud
reco = recoSurface(pts0, dims=70, radius=0.05).legend("surf. reco")

vp.add(reco)
vp.addCutterTool(reco)
vp.show(axes=7, interactive=1)
