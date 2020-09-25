# This script generates a points fairly evenly spaced on a sphere
# You paste this text into a Paraview Python Programmable Source window
# https://stackoverflow.com/questions/9600801/evenly-distributing-n-points-on-a-sphere
# https://stackoverflow.com/a/9601334
# https://web.archive.org/web/20120107030109/http://cgafaq.info/wiki/Evenly_distributed_points_on_sphere#Spirals

import math

R = 3.0
N = 1000
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

pdo = self.GetPolyDataOutput()
newPts = vtk.vtkPoints()
for i in range(0, N):
    xyz = node[i]
    newPts.InsertPoint(i, R*xyz[0], R*xyz[1], R*xyz[2])

pdo.SetPoints(newPts)
aPolyLine = vtk.vtkPolyLine()
aPolyLine.GetPointIds().SetNumberOfIds(N)
for i in range(N):
   aPolyLine.GetPointIds().SetId(i, i)

pdo.Allocate(1, 1)
pdo.InsertNextCell(aPolyLine.GetCellType(), aPolyLine.GetPointIds())
