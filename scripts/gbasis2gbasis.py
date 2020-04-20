#!/usr/bin/env python3
# Python Basis Tool (pbt) script for reading in GBASIS format and writing to the same GBASIS format
#
# Please check gbasis.py for more info and limitations.
#
import sys
import util
from basclas import Basis

# Ensure set is a global object
set=[]
# Number of sig figs in the output
precis=8

if (len(sys.argv) < 2):
    print("Usage: gbasis2gbasis.py infile [outfile]")
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

import gbasis
# Parse the lines and return basis set information in set
gbasis.ParseGbasis(lines,set)
#Debug statement - return 'info' on all the entries in set - effectively dumps the basis to screen
#for entry in set:
#    print(entry.info())
#
gbasis.WriteGbasis(set,precis,outfile)
outfile.close()
