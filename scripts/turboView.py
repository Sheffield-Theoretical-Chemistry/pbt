#!/usr/bin/env python3
# Python Basis Tool (pbt) script for reading in Turbomole format and visualising the exponents
#
# Please check turbo.py and view.py for more info and limitations.
# Requires numpy and matplotlib
#
import sys
import util
from basclas import Basis

# Ensure set is a global object
set=[]

if (len(sys.argv) < 2):
    print("Usage: turboView.py infile")
    sys.exit()

scriptname = sys.argv[0]
filename = sys.argv[1]

file = open(filename, "r")
lines = file.readlines()
file.close()

import turbo
# Parse the lines and return basis set information in set
turbo.ParseTurbo(lines,set)
import view
dummy=''
view.ViewPNG(set,dummy,dummy,False)

