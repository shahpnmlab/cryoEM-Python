import glob
import os
from termcolor import colored
from itertools import islice
from tabulate import tabulate

relion_dir = os.getcwd()
refine_3d_dir = os.path.join(relion_dir, "Refine3D")

a = os.listdir(refine_3d_dir)
a.sort()

for x in a:
    if "job" in x:
        print(colored(x,'cyan'))


job_name = "job002"
job_dir = os.path.join(refine_3d_dir, job_name)
run_out = os.path.join(job_dir,"run.out")


model_star_files = glob.glob(job_dir +"/*_half1_model.star")
model_star_files.sort()

def flatten(t): return [item for sublist in t for item in sublist]

def line_numbers(fileIn):
    with open(fileIn, "r") as f_in:
        for num, lines in enumerate(f_in, 1):
            if "data_model_classes" in lines:
                begin_line = num
            if "data_model_class_1" in lines:
                end_line = num - 3
    return(begin_line, end_line)

def get_dist(fileIn,line_start,line_end):
    with open(fileIn, 'r') as f_in:
        lines = islice(f_in, line_start, line_end)
        data = [line.strip() for line in lines]
        data_header = []
        data_body = []
        for i in data:
            if i == 'loop_':
                continue
            if i.startswith('_rln'):
                data_header.append(i)
            else:
                data_body.append(i)
    data_body = list(filter(None, data_body))
    data = [x.split() for x in data_body]
    return(data)



with open(run_out, "r") as f_in:
    x = [line for line in f_in if 'Iteration' in line]
    y = [i.strip().split('=') for i in x]
    iteration = [i[-1] for i in y]

with open(run_out, "r") as f_in:
    x = [line for line in f_in if "Angular step=" in line]
    y = [i.strip().split(" ") for i in x]
    angular_step = [i[3] for i in y]
    local_searches = [i[7] for i in y]


accuracy_rotations =[]
accuracy_translations =[]
estimated_resolution = []

for model_star_file in model_star_files:

    begin_line,end_line = line_numbers(model_star_file)

    data = flatten(get_dist(model_star_file,begin_line,end_line))

    ar = data[2]
    at = data[3]
    er = data[4]
    accuracy_rotations.append(ar)
    accuracy_translations.append(at)
    estimated_resolution.append(er)

print(tabulate(
	{"Iteration": iteration, 
	"Resolution": estimated_resolution, 
	"AngularAccuracy": accuracy_rotations, 
	"AngularStep": angular_step, 
	"TranslationAccuracy(A)":accuracy_translations, 
	"LocalSearches": local_searches}, headers="keys"))

with open(run_out,"r") as f_in:
    for lines in f_in:
        if "Final resolution (without masking)" in lines:
            print("\n")
            print("Refinement has converged.\n")
            print(lines)
