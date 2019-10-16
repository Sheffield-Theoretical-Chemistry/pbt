# Input and output filters for the Turbomole program
# Currently implemented:
# Write uncontraced sets
# Write general contractions, but not well tested
#
# Known limitations:
# Reading contracted basis sets not supported
#
import sys
import util
from basclas import Basis

def ParseTurbo(lines,set):
    print('Reading Turbomole format basis sets is still a WIP. Please check carefully!')
    skipcount = 0
    inComment = False
    nSets = 0
    FirstRun = True
    SetChange = False
    Exponents = []
    for count,line in enumerate(lines):
        # Replace any newlines and split data into a list
        ParseObj = line.replace("\n", "").split()
# Debug statement - uncomment to print the line in list format
        print(ParseObj)
        if (ParseObj[0].lower() == '$basis') or (ParseObj[0].lower() == '$cbas'):
            # Skip over the start line
            skipcount += 1
            continue
        if (ParseObj[0][0] == '*') and not inComment:
            skipcount += 1
            inComment = True
            if (len(Exponents) > 0):
                # Change of atom type or basis set
                set.append(Basis(Atom, OrbAngular, Exponents))
                Exponents = []
            continue
        if (ParseObj[0][0] == '*') and inComment:
            skipcount += 1
            inComment = False
            continue
        if inComment and (ParseObj[0][0] == '#'):
            skipcount += 1
            continue
        if inComment and (ParseObj[0][0] != '#'):
            if (ParseObj[0].lower() == '$end'):
                continue
            else:
                # Tag this set as a change of atom
                Atom = ParseObj[0]
                NewAtom = True
                skipcount += 1
                continue
        # Is this a definition line, or the exponents?
        AllowedEl = ['s', 'p', 'd', 'f', 'g', 'h', 'i', 'k', 'l', 'm', 'n']
        if any(el in ParseObj[1] for el in AllowedEl):
                if NewAtom:
                    #This is the first run through for this atom
                    NewAtom = False
                    OrbAngular = ParseObj[1].lower()
                    Exponents = []
                    if FirstRun:
                        FirstRun = False
                    else:
                        SetChange = True
                else:
                    if ((ParseObj[1].lower()) != OrbAngular):
                        # Angular momentum has changed
                        set.append(Basis(Atom, OrbAngular, Exponents))
                        # Reset the angular momentum and Exponents
                        OrbAngular = ParseObj[1].lower()
                        Exponents = []
                        nSets += 1
                        # Do we need to tag this as a change in set or atom?
                        if SetChange:
                            SetChange = False
                            set[nSets].changeatom = True
                if (int(ParseObj[0]) != 1):
                    print("Contracted basis sets not yet supported, exiting.")
                    sys.exit()
                    # Loop over exponents by reading the next ParseObj[0] lines
                    # Check if we already have these exponents
                    # If yes, this appears to be an additional contraction of the same exponents
                    # If not, new exponents
        else:
            # Appears to be uncontracted exponents, is it an optimisation?
            if (len(ParseObj) == 2):
                Exponents.append(ParseObj[0])
            elif (len(ParseObj) == 3):
                Exponents.append(ParseObj[2])

#---------------------------------------------------------------------------------------------------

def WriteTurbo(set,precis,outfile):
    outfile.write('$basis\n*\n')
    comp = util.getPrim(set)
    contcomp = util.getContract(set)
    countchange = 0
    FirstRun = True

    def tabSpacing(exponent, precis):
        "Calculates a number of spaces to print as tabs aren't always supported in Turbomole"
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
                outfile.write('%s BASNAME\n# %s basis set from pbt (%s) / [%s]\n*\n' % (set[0].atom.lower(), set[0].atom.lower(), comp[0], contcomp[0]))
            else:
                outfile.write('%s BASNAME\n# %s basis set from pbt (%s)\n*\n' % (set[0].atom.lower(), set[0].atom.lower(), comp[0]))
        if (entry.changeatom):
            countchange +=1
            if (entry.contraction):
                outfile.write('*\n%s BASNAME\n# %s basis set from pbt (%s) / [%s]\n*\n' % (entry.atom.lower(), entry.atom.lower(), comp[countchange], contcomp[countchange]))
            else:
                outfile.write('*\n%s BASNAME\n# %s basis set from pbt (%s)\n*\n' % (entry.atom.lower(), entry.atom.lower(), comp[countchange]))
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
                    outfile.write('    1  %s\n' % entry.el.lower())
                    for count,coeff in enumerate(pattern):
                        if (coeff != '0.0'):
                            spaces = tabSpacing(entry.exponents[count], precis)
                            outfile.write('  %.*f%s%.*f\n' % (precis, float(entry.exponents[count]), spaces, precis, 1.0))
                else:
                # Looks like a contracted function
                    outfile.write('   %2i  %s\n' % (len(pattern), entry.el.lower()))
                    for count,coeff in enumerate(pattern):
                        spaces = tabSpacing(entry.exponents[count], precis)
                        # Adjust alignment in negative contraction coefficient case
                        if (float(coeff) < 0):
                            spaces = spaces[:-1]
                        outfile.write('  %.*f%s%.*f\n' % (precis, float(entry.exponents[count]), spaces, precis, float(coeff)))
        else:
            # If all of the functions in this el are uncontracted
            for exp in sorted(entry.exponents, key=float, reverse=True):
                outfile.write('    1  %s\n' % entry.el.lower())
                exponent = '{number:.{p}g}'.format(number=float(exp), p = precis)
                spaces = tabSpacing(exponent, precis)
                outfile.write('  %.*f%s%.*f\n' % (precis, float(exponent), spaces,  precis, 1.0))
    outfile.write('*\n$end\n')
    print("You may want to change 'BASNAME' to something more sensible.")
