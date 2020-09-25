from vedo import *

data_dir = '/Users/emonson/Dropbox/People/OlivierDelaire/Data Visualization for INS/Nb_symmetrized_data/PeaksUgrid/'

print('loading files')
objs = load(data_dir+'ugrid_*.vtu')
print('point conversion')
pts_list = [Points(gd.points(), r=3) for gd in objs]
print('surface reconstructions')
reco_list = []
for ii,pts in enumerate(pts_list):
    print(ii,end=' ',flush=True)
    reco_list.append(recoSurface(pts, dims=70, radius=0.05).cutWithPlane())
print('\nvisualizing')

vp = show(reco_list[0], interactive=False, bg='bb')
vp.actors = reco_list

# Turn off all actors
for rr in reco_list[1:]:
    rr.off()

k = 0
def sliderfunc(widget, event):
    global k
    knew = int(widget.GetRepresentation().GetValue())
    if k==knew: return
    vp.actors[k].off()
    vp.actors[knew].on()
    k = knew

vp.addSlider2D(sliderfunc,0,len(objs)-1,value=0)
vp.show(interactive=True)
