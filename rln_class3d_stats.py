import glob
import os
import starfile
from termcolor import colored
from itertools import islice

relion_dir = os.getcwd()
class_3d_dir = os.path.join(relion_dir, "Class3D")
a = os.listdir(class_3d_dir)
a.sort()

for x in a:
    if "job" in x:
        print(colored(x,'cyan'))

job_name = input("Enter job folder name: ")
job_dir = os.path.join(class_3d_dir, job_name)
model_star_files = glob.glob(job_dir + "/*model.star")
data_star_file = job_dir+"/run_it000_data.star"

model_star_files.sort()


def line_numbers(fileIn):
    with open(fileIn, "r") as f_in:
        for num, lines in enumerate(f_in, 1):
            if "data_model_classes" in lines:
                begin_line = num
            if "data_model_class_1" in lines:
                end_line = num - 3
    return(begin_line, end_line)

def get_dist(fileIn):

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

df = starfile.read(data_star_file)
particle_number = df['particles']['rlnMicrographName'].shape[0]

for index, model_file in enumerate(model_star_files):
    print("\n")
    print(colored("ITERATION -------->",'red'), colored(index,'green'))
    line_start, line_end = line_numbers(model_file)
    data = get_dist(model_file)
    for k in range(len(data)):
        percentage = float(data[k][1])*100
        pcles_in_class = round(float(data[k][1])*particle_number)
        print("{} :========> {:.2f} % | ~{} particles".format(data[k][0], percentage,pcles_in_class))
