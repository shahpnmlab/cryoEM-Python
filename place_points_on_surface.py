import numpy as np
from numpy import pi, cos, sin, arccos, arange
import subprocess
import argparse

#Read input from the user
parser=argparse.ArgumentParser()
parser.add_argument("--i", help="IMOD mod file with centers of objects selected")
parser.add_argument("--r", help="The desired radius (px).",type=float)
parser.add_argument("--npts", help="Number of points you want to place on the sphere",type=int)
parser.add_argument("--rec", help="Name of tomogram for which points are being generated")
            
args=parser.parse_args()

#Convert IMOD mod file to a txt file, you need to have IMOD and its utils in
#$PATH
subprocess.run(['model2point', '-float', '-i', args.i, '-output', 'temp.txt'])#,stdout=subprocess.PIPE).stdout.decode('utf-8')
print("Converting your input mod file into a temporary text file")

#Do the magic
f=np.loadtxt("temp.txt")
origin_x=f[:,[0]]
origin_y=f[:,[1]]
origin_z=f[:,[2]]
r=args.r
num_pts = args.npts
if len(origin_x)==len(origin_y)==len(origin_z):
    indices = arange(0, num_pts, dtype=float)
    phi = arccos(1 - 2*indices/num_pts)
    theta = pi * (1 + 5**0.5) * indices
    x = cos(theta) * sin(phi) * r + origin_x
    y = sin(theta) * sin(phi) * r + origin_y
    z = cos(phi) * r + origin_z
    #x=np.array([x]).reshape(num_pts,1)
    x=np.array([x]).reshape(len(x)*num_pts,1)
    #y=np.array([y]).reshape(num_pts,1)
    y=np.array([y]).reshape(len(y)*num_pts,1)
    #z=np.array([z]).reshape(num_pts,1)
    z=np.array([z]).reshape(len(z)*num_pts,1)
    xy=np.hstack((x,y))
    xyz=np.hstack((xy,z))
    subprocess.run(['rm', 'temp.txt'])#, shell=True)
elif len(origin_x)!=len(origin_y)!=len(origin_z):
    print("Your input file is erroneous, have you checked if you length of X==Y++Z?")   

#Save txt as input for point2model
np.savetxt('temp.txt',xyz,delimiter=' ',fmt='%-5i')
print("Converting the points back into a mod file for you to use")
subprocess.run(['point2model', '-circle', '3', '-sphere', '5', '-scat', '-thick', '2', '-color', '80,191,255,', \
'-image', args.rec, 'temp.txt', args.rec[:-4]+"_sphere.mod"])
subprocess.run(['rm', 'temp.txt'])
print("Process has ended")
