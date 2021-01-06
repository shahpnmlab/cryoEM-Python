#!/Library/Frameworks/Python.framework/Versions/3.7/bin/python3
import shutil
import glob
import os
import argparse

import numpy as np
import pandas as pd
from pandas.core.common import flatten

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
work_folder=os.getcwd()+'/mdocs'
fileIn=[x for x in glob.glob(work_folder+'/*.mdoc')]
src_frame_dir_name="frames"
frame_range=[[38], [4, 32], [5, 28]]
src_frame_dir=os.getcwd() + '/' + src_frame_dir_name
dest_frame_dir_name=os.getcwd()+'/selectedFrames'

tmp_list=[]
for i in range(len(fileIn)):
    frame_name=getFrames(fileIn[i])
    frame_angle=getAngle(fileIn[i])
    start=frame_range[i][0]+1
    end=frame_range[i][1]+1
    df = pd.DataFrame(list(zip(frame_name, frame_angle)),columns=['Name','StageAngle'])
    df=df.apply(pd.to_numeric,errors='ignore')
    df=df.sort_values(by=['StageAngle'])
    sorted_frame_list=df['Name'].to_list()
    tmp_list.append(sorted_frame_list[start:end])
    
selected_frame_list = list(flatten(tmp_list))

src=[src_frame_dir+'/'+x for x in selected_frame_list]
dest=[dest_frame_dir_name+'/'+x for x in selected_frame_list]

if not os.path.isdir(dest_frame_dir_name):
    os.mkdir(dest_frame_dir_name)

for i,j in zip(src, dest):
    print("Linking",i,"to",j)
    os.symlink(i,j,target_is_directory='True')
    
print("FINISHED SELCTING AND LINKING SUBSET FRAMES!")
