import sys
import starfile
import numpy as np


from scipy.spatial.transform import Rotation as R



def get_coords(star_file):
    df2 = {}
    xyz_headings = [f'rlnCoordinate{axis}' for axis in "XYZ"]
    df = starfile.read(star_file)
    df =  df['optics'].merge(df['particles'])
    angpix = df['rlnImagePixelSize'].unique()
    tomo_list = df['rlnMicrographName'].unique().tolist()
    for tomo in tomo_list:
        a = df[df['rlnMicrographName'] == tomo]
        if len(a) > 20:
            xyz = a[xyz_headings].to_numpy()
            df2[tomo] = xyz
    return angpix, df2

def rotate_coords(arr, angle, axis):
    if axis == "X" or axis == "x":
        r = R.from_rotvec(angle * np.array([1,0,0]), degrees=True)
        xyz = r.apply(arr)
    if axis == "Y" or axis == "y":
        r = R.from_rotvec(angle * np.array([0,1,0]), degrees=True)
        xyz = r.apply(arr)
    if axis == "Z" or axis == "z":
        r = R.from_rotvec(angle * np.array([0,0,1]), degrees=True)
        xyz = r.apply(arr)
    return xyz

#---------------------------------------------------------------------------#
if len(sys.argv) < 2 or sys.argv[1] == '-h' or sys.argv[1] == '--help':
    print("WHAT IT DOES:\n")
    print("The script makes a rather naive assumption that the particles are \n")
    print("randomly distributed through the tomogram and that the minmax dims \n")
    print("are some kind of an indication of the overall thickness of the tomo. \n")
    print("It is recommended that all the good particles following 3D classification\n")
    print("(in case of multiple particle species) or 3D refinement be provided to the script\n")
    print("to estimate the thickness of the tomograms. The pretilt should be given in degrees. \n")
    print("TEMPLATE:\n")
    print("estimateTomoThickness.py <STARFILE> <PRETILT> \n")
    print("EXAMPLE:\n")
    print("estimateTomoThickness.py particles.star 10.6 \n")
else:
file_name = sys.argv[1]
pretilt = -(sys.argv[2])

apix, data = get_coords(file_name)
for key, value in data.items():
    xyzn = rotate_coords(value, pretilt, "Y")
    zdim = ((xyzn[:,2].max() - xyzn[:,2].min())*apix)/10
    print(f"The thickness of the current tomo {key} is {zdim}nm")
