import numpy as np
import argparse
import sys


parser=argparse.ArgumentParser(description='Convert AreTomo alignment stats into IMOD type xf files', add_help=True)

# Mandatory arguments
requiredNamed = parser.add_argument_group('required named arguments')
requiredNamed.add_argument("--i",help="Enter the AreTomo aln file here",required=True)
requiredNamed.add_argument("--oxf",help="Output filename (w/o the extension)",required=True)

# Optional Argument
parser.add_argument("--otlt",help="(OPTIONAL) Add this argument if you also want the refined angles in a seperate tlt file.",action="store_true")


# Print help if no options are provided
if len(sys.argv)==1:
    parser.print_help(sys.stderr)
    sys.exit(1)
args=parser.parse_args()

# Read file in
f=np.loadtxt(args.i,skiprows=2)

# Do the math
theta=np.radians(f[:,[1]])
c,s=np.cos(theta), np.sin(theta)

r11=np.array(c)
r12=np.array(-s)
r21=np.array(s)
r22=np.array(c)

# Assemble cols
a=np.hstack((r11,r12))
b=np.hstack((r21,r22))
ab=np.hstack((a,b))
c=f[:,[3,4]]

allcols=np.hstack((ab,c))

tlt=(f[:,[9]]).astype(float)

#Save output
np.savetxt(args.oxf+'.xf',allcols,fmt="%0.2f")
if args.otlt:
    np.savetxt(args.oxf+'.tlt',tlt,fmt="%0.2f")
