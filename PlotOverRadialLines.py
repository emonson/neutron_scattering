from paraview.simple import *
import vtk.util.numpy_support as ns
import pandas as pd
import math

# This script gets loaded as a Macro in Paraview, then you select the loaded
#   time-series Intensity volume data in the Pipeline Browser and run the Macro
# It probes the volume data Intensity field along lines starting at 0,0,0 and ending
#   distributed fairly evenly over the surface of the sphere, over all time points
# Output is a tidy-format CSV file with intensities, point coordinates,
#   and time, line, and point indices
# The goal is to create 1D curves that can be analyzed to detect peaks in intensity
#   which could result in point clouds over intensity peak surfaces

# Change the sphere radius such that the sphere will cover the whole volume.
# You can also set the line resolution which will change the resolution of the probed data
#   and the number of points covering the sphere

# Basic plot over line saving learned from this video:
#   Automate plot over line using python script in paraview
#   https://youtu.be/7lqYJxmp4_4

# Generate points on sphere
# This script generates a points fairly evenly spaced on a sphere
# https://stackoverflow.com/questions/9600801/evenly-distributing-n-points-on-a-sphere
# https://stackoverflow.com/a/9601334
# https://web.archive.org/web/20120107030109/http://cgafaq.info/wiki/Evenly_distributed_points_on_sphere#Spirals

# CSV file output, including path
output_filename = 'radial_n1000_r300.csv'
# Sphere radius
sphere_radius = 1.0
# Number of radial lines, ends distributed over the sphere
number_of_lines = 1000
# Line resolution
line_resolution = 300
# Volume data array name. For some reason I'm using all lowercase version in output data...
array_name = 'Intensity'


node = [None]*number_of_lines
dlong = math.pi*(3-math.sqrt(5))
dz = 2.0/number_of_lines
long = 0
z = 1 - dz/2
for k in range(number_of_lines):
    r = math.sqrt(1-z*z)
    node[k] = (math.cos(long)*r, math.sin(long)*r, z)
    z = z - dz
    long = long + dlong

# Get time steps in dataset
# https://discourse.paraview.org/t/go-to-specific-time-step-in-python-script/376
reader = GetActiveSource()
view = GetActiveView()
times = reader.TimestepValues

# plot over line
# Here set resolution of line over radius of the sphere
# Remember that if the radius is set large enough some points will be in blank space beyond the data
# which results in Nulls which will be taken out later.
line_source = Line( Resolution=line_resolution )
plotOverLine1 = PlotOverLine(Input=reader, Source=line_source)

# select fields
passArrays1 = PassArrays(Input=plotOverLine1)
passArrays1.PointDataArrays = [array_name]

df_big_list = []
# Time loop
for tt in times:
    view.ViewTime = tt
    Render()
    
    df_list = []
    
    # Loop over sphere end points
    for ii, xyz in enumerate(node):
        plotOverLine1.Source.Point1 = [0.0, 0.0, 0.0]
        plotOverLine1.Source.Point2 = [sphere_radius*xyz[0], sphere_radius*xyz[1], sphere_radius*xyz[2]]
        # Original method saved out one file per loop – just leaving for reference
        # writer = CreateWriter('/Users/emonson/Data/PointsOnSphere/data_pol_t{0}_p{1}.csv'.format(int(tt),ii))
        # writer.UpdatePipeline()
        passArrays1.UpdatePipeline()
        b = paraview.servermanager.Fetch(passArrays1)
        
        df = pd.DataFrame()
        df[array_name.lower()] = ns.vtk_to_numpy(b.GetPointData().GetArray(array_name))
        point_coords = ns.vtk_to_numpy(b.GetPoints().GetData())
        df['px'] = point_coords[:,0]
        df['py'] = point_coords[:,1]
        df['pz'] = point_coords[:,2]
        df['timestep'] = int(tt)
        df['lineindex'] = ii
        df.reset_index(inplace=True)
        df.rename(columns={'index':'pointindex'}, inplace=True)
        df.dropna(subset=[array_name.lower()], inplace=True)
        df_list.append(df)
    
    df_big_list.append(pd.concat(df_list))

df_all = pd.concat(df_big_list)
df_all.to_csv(output_filename, sep=',', index=False, encoding='utf-8')
