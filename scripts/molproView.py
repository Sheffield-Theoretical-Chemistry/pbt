#!/usr/bin/env python3
# Python Basis Tool (pbt) script for reading in Molpro external format and visualising the exponents
#
# Please check molpro.py and view.py for more info and limitations.
# Requires numpy and matplotlib
#
import sys
import util
from basclas import Basis

# Ensure set is a global object
set=[]

if (len(sys.argv) < 2):
    print("Usage: molproView.py infile")
    sys.exit()

scriptname = sys.argv[0]
filename = sys.argv[1]

file = open(filename, "r")
lines = file.readlines()
file.close()

import molpro
# Parse the lines and return basis set information in set
molpro.ParseExt(lines,set)
import view
dummy=''
view.ViewPNG(set,dummy,dummy,False)

