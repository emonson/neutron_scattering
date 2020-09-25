from vedo import *

data_dir = '/Users/emonson/Dropbox/People/OlivierDelaire/Data Visualization for INS/Nb_symmetrized_data/PeaksUgrid/'

print('loading files')
objs = load(data_dir + 'ugrid_1*.vtu')
print('point conversion')
pts_list = [Points(gd.points(), r=3) for gd in objs]
print('surface reconstructions')
reco_list = [recoSurface(pts, dims=70, radius=0.05) for pts in pts_list]
print('visualizing')

vp = Plotter()
# vp = show(reco_list[0], interactive=False, bg='bb')
vp.actors = reco_list

# Turn off all actors
for oo in objs:
    oo.off()

k = 0
def sliderfunc(widget, event):
    global k
    knew = int(widget.GetRepresentation().GetValue())
    if k==knew: return
    if vp.cutterWidget:
        vp.cutterWidget.Off()
        vp.cutterWidget = None
    for aa in vp.actors:
        if aa == reco_list[knew]:
            aa.on()
        else:
            aa.off()
#     vp.actors[knew].on()
    vp.addCutterTool(reco_list[knew])
    k = knew

vp.addSlider2D(sliderfunc,k,len(objs)-1)
# vp.addCutterTool(reco_list[0])
# vp.show(reco_list[0], interactive=True)
print(vp.actors)
vp.show(interactive=True)