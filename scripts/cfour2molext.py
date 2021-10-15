#!/usr/bin/env python3
# Python Basis Tool (pbt) script for reading in CFOUR format and writing Molpro external format
#
# Please check $program.py for more info and limitations.
#
import sys
import util
from basclas import Basis

# Ensure set is a global object
set=[]
# Number of sig figs in the output
precis=6

if (len(sys.argv) < 2):
    print("Usage: cfour2molext.py infile [outfile]")
    print("The second of these is optional.")
    sys.exit()

scriptname = sys.argv[0]
filename = sys.argv[1]

if (len(sys.argv) > 2):
   outfile = open(sys.argv[2], 'w')
else:
   outfile = sys.stdout

file = open(filename, "r")
lines = file.readlines()
file.close()

import cfour
# Parse the lines and return basis set information in set
cfour.ParseCfour(lines,set)
#Debug statement - return 'info' on all the entries in set - effectively dumps the basis to screen
#for entry in set:
#    print(entry.info())
#
import molpro
molpro.WriteExt(set,precis,outfile)
outfile.close()
