# Input and output filters for the ACESII/CFour program
# Currently implemented:
# Write ACES format.
# This based on the GENBAS format specification found at:
# http://slater.chemie.uni-mainz.de/xaces2/aces2man/node17.html
#
# Known limitations:
# Currently only supports a single set in a file
# No working CFour install, so resulting files not verified
#
import sys
import util
from basclas import Basis

def WriteAces(set,precis,outfile):
    comp = util.getPrim(set)
    contcomp = util.getContract(set)

    # Currently only working for a single set in a file
    # so exit if multiple sets detected
    for entry in set:
        if entry.changeatom:
            print("Currently only a single set in a file is supported.")
            print("Exiting")
            sys.exit()

    # Print appropriate preamble
    outfile.write('\n{0}:BASNAME\n'.format(set[0].atom.upper()))
    outfile.write('Basis set from pbt: {0} -> {1}\n\n'.format(comp[0],contcomp[0]))
    # number of shells in the basis set
    nShells = int(util.getMaxEl(set)[0])+1
    outfile.write('{:3d}\n'.format(nShells))
    # angular momentum for each shell
    for entry in set:
        outfile.write('{:5d}'.format(util.numEl.get(entry.el.lower())))
    outfile.write('\n')
    # number of contracted basis functions for each shell
    for entry in set:
        if (entry.contraction):
            numexp = len(entry.contraction)
        else:
            numexp = len(entry.exponents)
        outfile.write('{:5d}'.format(numexp))
    outfile.write('\n')
    # number of primitives for each shell
    for entry in set:
        outfile.write('{:5d}'.format(len(entry.exponents)))
    outfile.write('\n\n')
    # end preamble

    # print primitives, then blank line, then contractions
    for entry in set:
        for count,prim in enumerate(entry.exponents):
            outfile.write('{:14.7f}'.format(float(prim)))
            # newline after 5 primitives
            if (((count + 1) % 5) == 0):
                outfile.write('\n')
        if ((len(entry.exponents) % 5) == 0):
            outfile.write('\n')
        else:
            outfile.write('\n\n')
        # move on to contraction coefficients
        if (entry.contraction):
            numcont = len(entry.contraction)
            for count,prim in enumerate(entry.exponents):
                for doublecount,pattern in enumerate(entry.contraction):
                    if (count > (len(pattern)-1)):
                        outfile.write('{: 10.7f} '.format(0.0))
                    else:
                        outfile.write('{: 10.7f} '.format(float(pattern[count])))
                    # newline after 7 coeffs for Fortran line lengths
                    if (((doublecount + 1) % 7) == 0) and (numcont != 7):
                        outfile.write('\n')
                outfile.write('\n')
            outfile.write('\n')
        else:
            # print some 'contraction coefficients' in uncontracted case
            numprims = len(entry.exponents)
            for count,prim in enumerate(entry.exponents):
                for doublecount,prim in enumerate(entry.exponents):
                    if (doublecount == count):
                        outfile.write('{: 10.7f} '.format(1.0))
                    else:
                        outfile.write('{: 10.7f} '.format(0.0))
                    # newline after 7 coeffs for Fortran line lengths
                    if (((doublecount + 1) % 7) == 0) and (numprims != 7):
                        outfile.write('\n')
                outfile.write('\n')
            outfile.write('\n')

    print("You may want to change 'BASNAME' to something more sensible.")
