#!/Library/Frameworks/Python.framework/Versions/3.7/bin/python3
import shutil
import argparse
import os

import numpy as np
import pandas as pd

"""
fileIn = sys.argv[1]
"""


def readMdoc(fileIn):
    fn = open(fileIn,"r")
    return(fn)

def getFrames(fileIn):
    with open(fileIn,"r") as fn:
        x = [line for line in fn if 'SubFramePath' in line]
        y = [i.strip().split("\\") for i in x]
        z = [i[-1] for i in y]
    return(z)

def getDateTime(fileIn):
    with open(fileIn,"r") as fn:
        x = [line for line in fn if 'DateTime' in line]
        y = [i.strip().split() for i in x]
        date = [y[i][2] for i in range(len(y))]
        time = [y[i][3] for i in range(len(y))]
    return(date,time)
    
def getAngle(fileIn):
    with open(fileIn,"r") as fn:
        x = [line for line in fn if 'TiltAngle' in line]
        y = [i.strip().split() for i in x]
        z = [float(i[-1]) for i in y]
    return(z)

# User Inputs
parser = argparse.ArgumentParser()
parser.add_argument("--i", type = str, help = "mdoc file name")
parser.add_argument("--frame_dir", type = str, help = "name of directory containg the frames")
parser.add_argument("--start", type = int, help = "TS start number")
parser.add_argument("--end", type = int, help = "TS end number")

args = parser.parse_args()

fileIn=args.i
src_frame_dir_name=args.frame_dir
start=args.start
end=args.end

# Get Data
frame_name = getFrames(fileIn)
frame_date,frame_time = getDateTime(fileIn)
frame_angle= getAngle(fileIn)

# Convert to Data Frame
df = pd.DataFrame(list(zip(frame_name, frame_angle, frame_date,frame_time)), 
               columns =['Name', 'StageAngle','Date','Time']) 
df = df.apply(pd.to_numeric, errors='ignore')

# Sort data based on tilt angle which is lowest to highest be default
df=df.sort_values(by=['StageAngle'])

# get 
sorted_frame_list=df['Name'].to_list()

selected_frame_list=sorted_frame_list[start+1:end+1]

src_frame_dir=os.getcwd() + '/' + src_frame_dir_name
dest_frame_dir_name=os.getcwd()+'/selectedFrames'

if not os.path.isdir(dest_frame_dir_name):
    os.mkdir(dest_frame_dir_name)

for i in selected_frame_list:
    print("Copying",src_frame_dir+'/'+i,"to",dest_frame_dir_name)
    shutil.copy(src_frame_dir+'/'+i,dest_frame_dir_name)
    
