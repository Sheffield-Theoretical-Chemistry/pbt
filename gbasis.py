# Input and output filters for the GBASIS program of Dave Feller
# GBASIS was a CLI basis set library program, strongly related to the original Gaussian basis set order form
# (later replaced by the PNNL BSE). As such, the ability to read and write files in this format is still
# somewhat desirable (conversion of old files etc.).
#
# Currently implemented:
#
# Basic writing of GBASIS files.
# Basic reading of a GBASIS file, in both PBT and Feller formats.
#
# Known limitations:
#
# Reading of GBASIS files only works for a single atom and single basis set. This isn't trapped.
# When reading, blank lines may break parser.
#
import sys
import util
from basclas import Basis

def ParseGbasis(lines,set):
    # Reads in the GBASIS basis set format
    # Currently targetting the exact format output by WriteGbasis, rather than the slightly different
    # format used by Dave Feller.
    coeffs = []
    skipcount = 0
    Feller = False
    skipline = False
    skipdouble = False
    fellerFirst = True

    for count,line in enumerate(lines):
        # Remove the newlines and split into a list
        ParseObj = line.replace("\n", "").split()
# Debug statement - uncomment to print the line in list format
        print(ParseObj)
        # To add: Skip over any comments - these start with a !
        if (len(ParseObj[0]) != 0):
            if (str(ParseObj[0][0]) == '!'):
                skipcount += 1
                continue
        # Skip over the line if logic has detected that
        if skipline:
            skipcount += 1
#            print("Skipping the line")
            if skipdouble:
                skipdouble = False
            else:
                skipline = False
            continue

        # Detect if this uses Feller's format
        if (str(ParseObj[0][:2]).upper() == 'Z='):
            Feller = True
            FirstRun = True
#            print("Detected Feller version of GBASIS format")

        if Feller and fellerFirst:
            if ((count - skipcount) ==0):
                # Determine atom type
                #            print("Atomic number is ", ParseObj[0][2:])
                if (str(ParseObj[0][2:]) in util.atomicNumber):
                    atomType = util.atomicNumber[str(ParseObj[0][2:])]
#                    print("Atom type is ", atomType)
                else:
                    print("Unknown atom type, exiting.")
                    sys.exit()
            #Next two lines will be effectively comments
            skipline = True
            skipdouble = True
            fellerFirst = False
            continue

        elif (Feller and str(ParseObj[0][:2]).lower()=='z='):
            # New atom or basis definition
            print("Detected change of atom")
            # Process the data collected on previous run
            sortedCoeffs = []
            i = 0
            while i < totalContrac:
                j = 0
                tmpCoeffs = []
                while j < totalCoeffs:
                    tmpCoeffs.append(coeffs[i+j])
                    j += totalContrac
                sortedCoeffs.append(tmpCoeffs)
                i += 1
            set.append(Basis(atomType, orbAng, exponents, sortedCoeffs))
            if (str(ParseObj[0][2:]) in util.atomicNumber):
                atomType = util.atomicNumber[str(ParseObj[0][2:])]
                print("Atom type is ", atomType)
            else:
                print("Unknown atom type, exiting.")
                sys.exit()
            skipline = True
            skipdouble = True
            continue

        else:
            # On the first run through, the first line will define the element type
            if ((count - skipcount) ==0):
                FirstRun = True
                exponents = []
                coeffs = []
                atomType = None
                chunkedStart = ParseObj[0].split(":")
                if (str(chunkedStart[0]).lower() in util.periodicNames ):
                    atomType = str(chunkedStart[0]).upper()
#                    print("Atom type is ", atomType)
                else:
                    print("Unknown atom type, exiting.")
                    sys.exit()
            if ((count-skipcount)==1):
                maxEl = ParseObj[0]

        # Check if we have an El definition line
        if (str(ParseObj[0]).lower() in util.numEl ):

            if FirstRun:
                FirstRun = False
            else:
                #Process the previous angular momentum
                sortedCoeffs = []
                i = 0
                while i < totalContrac:
                    j = 0
                    tmpCoeffs = []
                    while j < totalCoeffs:
                        tmpCoeffs.append(coeffs[i+j])
                        j += totalContrac
                    sortedCoeffs.append(tmpCoeffs)
                    i += 1
                # Pass the info to the internal set
                set.append(Basis(atomType, orbAng, exponents, sortedCoeffs))

            orbAng = str(ParseObj[0].lower())
            totalPrims = int(ParseObj[1])
            totalContrac = int(ParseObj[2])
            totalCoeffs = totalPrims * totalContrac

            exponents = []
            coeffs = []

        elif (Feller and str(ParseObj[0][:6]).lower()=='numexp'):
            if FirstRun:
                FirstRun = False
            else:
                #Process the previous angular momentum
                sortedCoeffs = []
                i = 0
                while i < totalContrac:
                    j = 0
                    tmpCoeffs = []
                    while j < totalCoeffs:
                        tmpCoeffs.append(coeffs[i+j])
                        j += totalContrac
                    sortedCoeffs.append(tmpCoeffs)
                    i += 1
                # Pass the info to the internal set
                set.append(Basis(atomType, orbAng, exponents, sortedCoeffs))

            totalPrims = int(ParseObj[0][7:])
            totalContrac = len(ParseObj) - 1
            orbAng = str(ParseObj[1][-1:].lower())
            totalCoeffs = totalPrims * totalContrac

            exponents = []
            coeffs = []

        else:
            # Collect the exponents and contraction coeffs
            exponents.append(ParseObj[0])
            i = 0
            while i < (len(ParseObj)-1):
                coeffs.append(ParseObj[i+1])
                i += 1


#Need to trap the last entry
    sortedCoeffs = []
    i = 0
    while i < totalContrac:
        j = 0
        tmpCoeffs = []
        while j < totalCoeffs:
            tmpCoeffs.append(coeffs[i+j])
            j += totalContrac
        sortedCoeffs.append(tmpCoeffs)
        i += 1
    set.append(Basis(atomType, orbAng, exponents, sortedCoeffs))



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
