# Input and output filters for the NWChem program
# Currently implemented:
# Write NWChem format.
#
# Known limitations:
# No support for basis set contractions
#
import sys
import util
from basclas import Basis

def WriteNWChem(set,precis,outfile):
    outfile.write('BASIS "ao basis" PRINT\n')
    comp = util.getPrim(set)
    countchange = 0
    outfile.write('#BASIS SET: (%s)\n' % comp[0])
    for entry in set:
        if (entry.contraction):
            print("Writing contracted basis sets in NWChem format not yet supported")
            sys.exit()
        else:
            #Check if we are moving to a different atom. If so, print the required spacer
            if (entry.changeatom):
                countchange += 1
                outfile.write('#BASIS SET: (%s)\n' % comp[countchange])
            #Sort exponents, then step through them
            for exp in sorted(entry.exponents, key=float, reverse=True):
                outfile.write('%s\t%s\n' % (entry.atom.title(), entry.el.upper()))
                exponent = '{number:.{p}g}'.format(number=float(exp), p = precis)
                outfile.write(' %.*f\t%.*f\n' % (precis, float(exponent), precis, 1.0))
    outfile.write('END\n')
