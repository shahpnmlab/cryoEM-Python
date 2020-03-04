#!/usr/local/bin/python

import argparse

parser=argparse.ArgumentParser()
parser.add_argument("--px", help="This is the pixsize of the tomogram",type=float)
parser.add_argument("--F", help="The desired freq you want to the tomogram filter to.",type=float)

args=parser.parse_args()

pixsize=args.px
nyq_freq=float(0.5)
freq=args.F
reso=float(pixsize * freq * nyq_freq**-1)

print(reso)
