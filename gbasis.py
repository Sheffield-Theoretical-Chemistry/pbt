# Input and output filters for the GBASIS program of Dave Feller
# GBASIS was a CLI basis set library program, strongly related to the original Gaussian basis set order form
# (later replaced by the PNNL BSE). As such, the ability to read and write files in this format is still
# somewhat desirable (conversion of old files etc.).
#
# Currently implemented:
#
# Basic writing of GBASIS files.
#
# Known limitations:
#
# Currently the ability to read GBASIS files is missing. This would be incredibly useful to add.
#
import sys
import util
from basclas import Basis

def ParseGbasis(lines,set):
    # Reads in the GBASIS basis set format
    # Currently targetting the exact format output by WriteGbasis, rather than the slightly different
    # format used by Dave Feller.
    coeffs = []
    for count,line in enumerate(lines):
        # Remove the newlines and split into a list
        ParseObj = line.replace("\n", "").split()
# Debug statement - uncomment to print the line in list format
        print(ParseObj)
        # To add: Skip over any comments - these start with a !

        # On the first run through, the first line will define the element type
        if (count==0):
            atomType = None
            chunkedStart = ParseObj[0].split(":")
            if (str(chunkedStart[0]).lower() in util.periodicNames ):
                atomType = str(chunkedStart[0]).upper()
                print("Atom type is ", atomType)
            else:
                print("Unknown atom type, exiting.")
                sys.exit()


#---------------------------------------------------------------------------------------------------

def WriteGbasis(set,precis,outfile):
    comp = util.getPrim(set)
    contcomp = util.getContract(set)
    countchange = 0
    Els = util.getMaxEl(set)
    FirstRun = True
    for entry in set:
        if FirstRun:
            FirstRun = False
            if (entry.contraction):
                #Print the atom, basis name, compositions
                #Then, on the next line we need the maximum angular momentum within the set
                outfile.write('%s:BASNAME:(%s) -> [%s]\n%d\n' % (entry.atom.title(), comp[0], contcomp[0],  Els[0]))
            else:
                outfile.write('%s:BASNAME:(%s) -> [%s]\n%d\n' % (entry.atom.title(), comp[0], comp[0], Els[0]))

        #Check if we are moving to a different atom. If so, print a spacer and comment line
        if (entry.changeatom):
            countchange += 1
            if (entry.contraction):
                outfile.write('\n\n%s:BASNAME:(%s) -> [%s]\n%d\n' % (entry.atom.title(), comp[countchange], contcomp[countchange], Els[countchange]))
            else:
                outfile.write('\n\n%s:BASNAME:(%s) -> [%s]\n%d\n' % (entry.atom.title(), comp[countchange], comp[countchange], Els[countchange]))
            # Need to print the max el within the basis
        #Print a line in the format 'el n.prims n.contract'
        if (entry.contraction):
            outfile.write('%s %s %s\n' % (entry.el.upper(), len(entry.exponents), len(entry.contraction)))
        else:
            outfile.write('%s %s %s\n' % (entry.el.upper(), len(entry.exponents), len(entry.exponents)))
        # Output if the entry (primitives in this el) is contracted
        if (entry.contraction):
            for count,prim in enumerate(entry.exponents):
                outfile.write('{number:.{p}E}'.format(number=float(prim), p = precis-1))
                #Loop through contractions
                for pattern in entry.contraction:
                    # Catch incomplete contractions
                    if count >= len(pattern):
                        outfile.write(' {number:.{p}E}'.format(number=float(0.0), p = precis-1))
                    else:
                        outfile.write(' {number:.{p}E}'.format(number=float(pattern[count]), p = precis-1))
                # Print newline to finish each exponent
                outfile.write('\n')
        else:
            for count,prim in enumerate(entry.exponents):
                outfile.write('{number:.{p}E}'.format(number=float(prim), p = precis-1))
                for i in range(len(entry.exponents)):
                    if i == count:
                        outfile.write(' {number:.{p}E}'.format(number=float(1.0), p = precis-1))
                    else:
                        outfile.write(' {number:.{p}E}'.format(number=float(0.0), p = precis-1))
                outfile.write('\n')

    print("You may want to change 'BASNAME' to something more sensible.")
