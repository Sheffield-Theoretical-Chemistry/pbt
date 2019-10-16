#!/usr/bin/env python3
# Python Basis Tool (pbt) is a collection of utilities for basis set development
# and for translating between different basis set formats.
#
# Current capabilities:
# Read Molpro external basis set format
# Write NWChem format, Molpro internal and external format, turbomole format
# Hooks are there for future plotting of Gaussian primitives
#
# Please check $program.py for more info and limitations.
#
import sys
import util
from basclas import Basis
import argparse

# Ensure set is a global object
set=[]
defaultOut=True

parser = argparse.ArgumentParser(description="Convert basis sets to different formats. Defaults to writing Molpro external (include file) format")
parser.add_argument("input", help="name of the input file (default of Molpro external format)")
parser.add_argument("-impe", "--input-molpro-ext", help="input in Molpro external format", action='store_true')
parser.add_argument("-itrb", "--input-turbo", help="input in TURBOMOLE format", action='store_true')
parser.add_argument("-ompe", "--output-molpro-ext", help="request output in Molpro external format", metavar="OUTPUT_FILE")
parser.add_argument("-ompi", "--output-molpro-int", help="request output in Molpro internal format", metavar="OUTPUT_FILE")
parser.add_argument("-onwc", "--output-nwchem", help="request output in NWChem format", metavar="OUTPUT_FILE")
parser.add_argument("-otrb", "--output-turbo", help="request output in TURBOMOLE format", metavar="OUTPUT_FILE")
parser.add_argument("-ogbs", "--output-gbasis", help="request output in GBASIS format", metavar="OUTPUT_FILE")
parser.add_argument("-ogau", "--output-gauss", help="request output in GAUSSIAN format", metavar="OUTPUT_FILE")
parser.add_argument("-p", "--precision", help="request SIGFIGS significant figures in output", metavar="SIGFIGS")
parser.add_argument("-v", "--view", help="filename for plotting the basis set primitives as PNG", metavar="PLOT_FILE")
args = parser.parse_args()

# Debug statement to check what we're getting from argparse
#print(args)

file = open(args.input, "r")
lines = file.readlines()
file.close()
if args.precision:
    precis=int(args.precision)
else:
    precis=6

#Logic for input
if args.input_molpro_ext:
    #Molpro external format input
    from molpro import ParseExt as mpe
    mpe(lines,set)
elif args.input_turbo:
    #TURBOMOLE format
    from turbo import ParseTurbo as rtrb
    rtrb(lines,set)
else:
    print("Defaulting to Molpro external format input.")
    from molpro import ParseExt as mpe
    mpe(lines,set)


#Logic for output
if args.output_molpro_ext:
    outfile = open(args.output_molpro_ext, 'w')
    print('Writing to file', args.output_molpro_ext)
    from molpro import WriteExt as mwe
    mwe(set,precis,outfile)
    defaultOut=False
if args.output_molpro_int:
    outfile = open(args.output_molpro_int, 'w')
    print('Writing to file', args.output_molpro_int)
    from molpro import WriteInt as mwi
    mwi(set,precis,outfile)
    defaultOut=False
if args.output_nwchem:
    outfile = open(args.output_nwchem, 'w')
    print('Writing to file', args.output_nwchem)
    from nwchem import WriteNWChem as wnwc
    wnwc(set,precis,outfile)
    defaultOut=False
if args.output_turbo:
    outfile = open(args.output_turbo, 'w')
    print('Writing to file', args.output_turbo)
    from turbo import WriteTurbo as wtrb
    wtrb(set,precis,outfile)
    defaultOut=False
if args.output_gbasis:
    outfile = open(args.output_gbasis, 'w')
    print('Writing to file', args.output_gbasis)
    from gbasis import WriteGbasis as wgbs
    wgbs(set,precis,outfile)
    defaultOut=False
if args.output_gauss:
    outfile = open(args.output_gauss, 'w')
    print('Writing to file', args.output_gauss)
    from gaussian import WriteGauss as wgau
    wgau(set,precis,outfile)
    defaultOut=False
if defaultOut:
    #Default to printing molpro external to sys.stdout
    outfile = sys.stdout
    from molpro import WriteExt as mwe
    mwe(set,precis,outfile)
if args.view:
    viewfile = open(args.view, 'w')
    from view import ViewPNG as vpng
    viewsave = True
    vpng(set,viewfile,args.view,viewsave)
    viewfile.close()

outfile.close()
