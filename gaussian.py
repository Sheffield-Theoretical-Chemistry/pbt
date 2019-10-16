# Input and output filters for the Gaussian program
# Currently implemented:
# Write uncontraced sets
# Write general contractions, but not well tested
#
# Known limitations:
# Reading basis sets not supported
#
import sys
import util
from basclas import Basis

def WriteGauss(set,precis,outfile):
    outfile.write('****\n')
    comp = util.getPrim(set)
    contcomp = util.getContract(set)
    countchange = 0
    FirstRun = True

    def tabSpacing(exponent, precis):
        "Calculates a number of spaces to print as tabs aren't always supported"
        # A guess at some value for the spacing
        contractPos = 15
        SomeSpaces = str()
        expLen = len("%.*f" % (precis, float(exponent)))
        # Quick check than contractPos isn't too short
        if (contractPos <= (expLen + 3)):
            contractPos = expLen + 3
        numSpace = contractPos - expLen
        for x in range(0, numSpace):
            SomeSpaces += ' ';
        return SomeSpaces

    for entry in set:
        # Print comment lines for each basis
        if FirstRun:
            FirstRun = False
            if (entry.contraction):
                outfile.write('%s 0\n' % (set[0].atom.lower()))
            else:
                outfile.write('%s 0\n' % (set[0].atom.lower()))
        if (entry.changeatom):
            countchange +=1
            outfile.write('****\n%s 0\n' % (entry.atom.lower()))
        # Split in logic depending if basis is contracted or not
        if (entry.contraction):
            # Loop through contractions
            for pattern in entry.contraction:
                # Trap cases where the leading contraction coefficients are zero - i.e., uncontracted part
                FirstCoeff = True
                Uncontracted = False
                for count,coeff in enumerate(pattern):
                    if (coeff == '0.0') and (FirstCoeff):
                        FirstCoeff = False
                        Uncontracted = True
                if (Uncontracted):
                    # Format for shell definition: 'el' 'num of primitives' 'shell scale factor'
                    outfile.write('%s    1 1.00\n' % entry.el.upper())
                    for count,coeff in enumerate(pattern):
                        if (coeff != '0.0'):
                            spaces = tabSpacing(entry.exponents[count], precis)
                            outfile.write('  %.*f%s%.*f\n' % (precis, float(entry.exponents[count]), spaces, precis, 1.0))
                else:
                # Looks like a contracted function
                    outfile.write('%s   %2i 1.00\n' % (entry.el.upper(), len(pattern)))
                    for count,coeff in enumerate(pattern):
                        spaces = tabSpacing(entry.exponents[count], precis)
                        # Adjust alignment in negative contraction coefficient case
                        if (float(coeff) < 0):
                            spaces = spaces[:-1]
                        outfile.write('  %.*f%s%.*f\n' % (precis, float(entry.exponents[count]), spaces, precis, float(coeff)))
        else:
            # If all of the functions in this el are uncontracted
            for exp in sorted(entry.exponents, key=float, reverse=True):
                outfile.write('%s    1 1.00\n' % entry.el.upper())
                exponent = '{number:.{p}g}'.format(number=float(exp), p = precis)
                spaces = tabSpacing(exponent, precis)
                outfile.write('  %.*f%s%.*f\n' % (precis, float(exponent), spaces,  precis, 1.0))
    outfile.write('****\n')
