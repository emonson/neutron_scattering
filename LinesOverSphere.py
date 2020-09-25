from paraview.simple import *

# Generate points on sphere
import math

R = 1.0
N = 50
node = [None]*N
dlong = math.pi*(3-math.sqrt(5))
dz = 2.0/N
long = 0
z = 1 - dz/2
for k in range(N):
    r = math.sqrt(1-z*z)
    node[k] = (math.cos(long)*r, math.sin(long)*r, z)
    z = z - dz
    long = long + dlong

# Get times
reader = GetActiveSource()
view = GetActiveView()
times = reader.TimestepValues

# a1 = GetActiveSource()
line_source = Line(Resolution=100)

# plot over line
plotOverLine1 = PlotOverLine(Input=reader, Source=line_source)

# select fields
passArrays1 = PassArrays(Input=plotOverLine1)
passArrays1.PointDataArrays = ['Intensity']

# Time loop
for tt in times:
    view.ViewTime = tt
    Render()
    
    # Loop over sphere end points
    for ii, xyz in enumerate(node):
        plotOverLine1.Source.Point1 = [0.0, 0.0, 0.0]
        plotOverLine1.Source.Point2 = [R*xyz[0], R*xyz[1], R*xyz[2]]
        writer = CreateWriter('/Users/emonson/Data/PointsOnSphere/data_pol_t{0}_p{1}.csv'.format(int(tt),ii))
        writer.UpdatePipeline()