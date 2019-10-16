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
                outfile.write('%.6E' % (float(prim)))
                #Loop through contractions
                for pattern in entry.contraction:
                    # Catch incomplete contractions
                    if count >= len(pattern):
                        outfile.write(' %.6E' %(0.0))
                    else:
                        outfile.write(' %.6E' % (float(pattern[count])))
                # Print newline to finish each exponent
                outfile.write('\n')
        else:
            for count,prim in enumerate(entry.exponents):
                outfile.write('%.6E' % (float(prim)))
                for i in range(len(entry.exponents)):
                    if i == count:
                        outfile.write(' %.6E' %(1.0))
                    else:
                        outfile.write(' %.6E' %(0.0))
                outfile.write('\n')

    print("You may want to change 'BASNAME' to something more sensible.")
