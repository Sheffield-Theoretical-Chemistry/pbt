# Input and output filters for the ACESII/CFour program
# Currently implemented:
# Write CFOUR format.
# This based on the GENBAS format specification found at:
# http://slater.chemie.uni-mainz.de/xaces2/aces2man/node17.html
#
# Read CFOUR format
#
# Known limitations:
# Currently only supports a single set in a file
# No working CFour install, so resulting files not verified
# No support for ECPs in any form
#
import sys
import util
from basclas import Basis

def WriteCfour(set,precis,outfile):
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

#---------------------------------------------------------------------------------------------------

def ParseCfour(lines,set):
    print('Reading CFOUR format basis sets is still a WIP. Please check carefully!')
    skipcount = 0
    totalEls = 0
    exponents = []
    contractCoeffs = []
    newEl = False
    ElCount = 0
    skipBlank = False
    newContract = False
    for count,line in enumerate(lines):
        # Replace any newlines and split data into a list
        ParseObj = line.replace("\n", "").split()
# Debug statement - uncomment to print the line in list format
        #print(ParseObj)
        # Grab the atom type from the first line
        if (count == 0):
            Atom = ParseObj[0].split(":")[0]
        elif (count == 3):
            totalEls = ParseObj[0]
        elif (count == 4):
            Els = ParseObj
        elif (count == 5):
            noContracted = ParseObj
        elif (count == 6):
            noPrimitives = ParseObj
        elif (count == 7):
            newEl = True
        # Read the information for an el block (exponents and contraction coeffs)
        if newEl and (count > 7):
            if (len(exponents) < int(noPrimitives[ElCount])):
                for exp in ParseObj:
                    exponents.append(exp)
            elif (len(exponents) == int(noPrimitives[ElCount])) and (len(ParseObj) == 0) and (skipBlank == False):
                skipBlank = True
                TotalContract = int(noContracted[ElCount]) * int(noPrimitives[ElCount])
                newContract = True
            elif skipBlank and (len(contractCoeffs) < TotalContract):
                if newContract:
                    sortContract = [[] for i in range(int(noContracted[ElCount]))]
                    newContract = False
                for i,coeff in enumerate(ParseObj):
                    sortContract[i].append(coeff)
                    contractCoeffs.append(coeff)
            elif (len(contractCoeffs) == TotalContract) and (len(ParseObj) == 0):
                # We should have all the exponents and contract coeffs for this El
                #print(sortContract)
                set.append(Basis(Atom, util.letterEl[Els[ElCount]], exponents, sortContract))
                exponents = []
                contractCoeffs = []
                ElCount += 1
                skipBlank = False
    # Catch the final el before exiting
    set.append(Basis(Atom, util.letterEl[Els[ElCount]], exponents, sortContract))

