# Input and output filters for the Molpro program
# Currently implemented:
#
# Read Molpro external format.
# Read Molpro internal format.
# Converts even3 syntax to exponents, see: https://www.molpro.net/info/2012.1/doc/manual/node118.html
# Write Molpro external format.
# Write Molpro internal format (not well tested for contracted sets).
#
# Known limitations:
#
# No support for ECPs in any form
# No support for multiple el on a single line, e.g., spd,H,vtz type syntax
#
import sys
import util
from basclas import Basis

def ParseInt(lines,set):
    # Reads in Molpro internal (libmol) basis set format
    # This is a fixed format, hence some extra variables are used to keep track of numbers
    skipcount = 0
    numProcessed = 0
    skipline = False
    collectEls = False
    changeAtom = False
    coeffs=[]
    for count,line in enumerate(lines):
        if (count == 0):
            FirstRun = True
            atomtype = None
        # Remove the newlines and split into a list
        ParseObj = line.replace("\n", "").split()
# Debug statement - uncomment to print the line in list format
#        print(ParseObj)
        # Skip over any comments - these start with a star in libmol
        if (len(ParseObj[0]) != 0):
            if (str(ParseObj[0][0]) == '*'):
                skipcount += 1
                continue
        # Skip over the line if logic has detected it will be a comment
        if skipline:
            skipcount += 1
#            print("Skipping the line")
            skipline = False
            continue

        # Trap the currently unsupported case of ECPs
        if (len(ParseObj) > 1):
            if (len(ParseObj[1]) > 1):
                if ((len(ParseObj[1]) > 2) and (str(ParseObj[1][0:3]).lower() == 'ecp')):
                    print("ECPs not yet supported")
                    sys.exit()

        # Check if the line starts with an element
        if (str(ParseObj[0]).lower() in util.periodicNames ):
            # The next line will be a comment, so flag it to be skipped
            skipline = True
            if collectEls:
                # Time to process what we collected on the previous run
                ProcessInt(set,atomtype,orbAng,totalPrims,totalContrac,conPatterns,coeffs)
                if changeAtom:
                    set[numProcessed].changeatom = True
                    changeAtom = False 
                numProcessed += 1
                # Reset coeffs ready for the next run
                coeffs = []
            else:
                # Flag to start collecting values
                collectEls = True
            # First entry on the line is the atom type
            currentatom = str(ParseObj[0]).upper()
            if (currentatom != atomtype):
                # Looks like we have a new atomtype
                if not FirstRun:
                    changeAtom = True
                atomtype = ''.join(currentatom)
#                print("New atom type is ", atomtype)
            # Next entry is the orbital angular momentum
            orbAng = str(ParseObj[1]).lower()
            # There is then a series of basis set names / aliases, this is currently skipped by jumping to the colon character
            try:
                jumpPoint = ParseObj.index(':')
            except ValueError:
                print("Logic error when parsing line:")
                print(line, end="")
                print("Didn't find the colon character.")
                sys.exit()
            # Grab the total number of primitives
            totalPrims = int(ParseObj[jumpPoint+1])
            # Grab the total number post-contraction
            totalContrac = int(ParseObj[jumpPoint+2])
            # Remaining entries on the line are the contraction patterns
            conPatterns = []
            counter = jumpPoint+3
            while counter < len(ParseObj):
                conPatterns.append(ParseObj[counter])
                counter += 1
#            print(conPatterns)
        else:
            if collectEls:
                i = 0
                while i < len(ParseObj):
                    coeffs.append(ParseObj[i])
                    i += 1
        #No longer first run, as long as we haven't been counting blank lines
        if (len(ParseObj[0]) != 0):
            FirstRun = False

#Need to catch the case where we have the last entry in a file
    if collectEls:
        ProcessInt(set,atomtype,orbAng,totalPrims,totalContrac,conPatterns,coeffs)

#---------------------------------------------------------------------------------------------------

def ProcessInt(set,atomtype,orbAng,totalPrims,totalContrac,conPatterns,coeffs):
    # Process the information parsed and write it out to set
    # Keep track of where we are in this blob of coeffs
    coeffCounter = totalPrims - 1
    # Handle the contractions
    counter = 0
    fullContrac = []
    while counter < totalContrac:
        conLimits = conPatterns[counter].split(".")
        conLength = int(conLimits[1]) - int(conLimits[0]) + 1
        conRange = range(int(conLimits[0]), int(conLimits[1])+1)
        thisContrac = []
        i = 1
        while i < (totalPrims+1):
            if i in conRange:
                coeffCounter += 1
                thisContrac.append(coeffs[coeffCounter])
            else:
                thisContrac.append('0.0')
            i += 1
        # Debug statement, uncomment below to check the current contraction pattern
#        print(thisContrac)
        fullContrac.append(thisContrac)
        counter += 1
#    print(fullContrac)
    set.append(Basis(atomtype, orbAng, coeffs[:totalPrims], fullContrac))

#---------------------------------------------------------------------------------------------------

def ParseExt(lines,set):
    # Reads in Molpro external basis set format
    # Extract data from lines
    skipcount = 0
    # Variable for even-temp / other mathematical progressions of exponents
    eTemp = None
    for count,line in enumerate(lines):
        if (count == 0):
            FirstRun = True
            atomtype = None
        # Remove any white space and newlines, and split at comma
        ParseObj = line.replace(" ", "").replace("\n", "").split(',')
# Debug statement - uncomment to print the line in list format
#        print(ParseObj)
        # Jump over any terminating semi-colons (only at end of line, parses sets from KAP website)
        if (len(ParseObj[0]) != 0) and (ParseObj[-1][-1] == ';'):
            ParseObj[-1] = ParseObj[-1][0:-1]
        # Skip over any comments
        if (len(ParseObj[0]) != 0):
            if (str(ParseObj[0][0]) == '!'):
                skipcount += 1
                continue
        # Bomb if it looks like there is an incomplete (not blank) line
        if (len(ParseObj) < 3) and (len(ParseObj[0]) != 0):
            print("Error reading the line:")
            print(line, end="")
            print("Unable to parse. Exiting")
            sys.exit()

        # Trap a few cases that we don't (yet) support
        # Multiple el, e.g., spd,H,vtz type syntax, and ECPs
        if (len(ParseObj[0]) > 1):
            if ((len(ParseObj[0]) > 2) and (str(ParseObj[0][0:3]).lower() == 'ecp')):
                print("ECPs not yet supported")
            else:
                print("Angular momentum specification such as '", ParseObj[0], "' not yet supported")
            sys.exit()
        # Contraction coefficients, where line starts with c
        if (ParseObj[0].lower() == 'c'):
            skipcount += 1
            if not (set[-1].contraction):
                set[-1].contraction = []
            contractExps = ParseObj[1].split('.')
            thisContract = []
            # Is this a single (i.e., uncontracted) function?
            if (contractExps[0]  == contractExps[1]):
                for i in range(0, int(contractExps[0])-1):
                    # Fill the preceding contraction coefficients as zero
                    thisContract.append('0.0')
                thisContract.append(ParseObj[2])
            # If the contraction doesn't start with the first primitive
            elif (int(contractExps[0])!=1):
                for i in range(0, int(contractExps[0])-1):
                    # Fill the preceding contraction coefficients as zero
                    thisContract.append('0.0')
                thisContract.extend(ParseObj[2:])
            else:
                for i in ParseObj[2:]:
                    thisContract.append(i)
                if (len(thisContract) != int(contractExps[1])):
                    print("The type of contraction in:")
                    print(line, end="")
                    print("is not yet supported. Chat to a developer.")
                    sys.exit()
            # Substitute Fortran style double precision for Python scientific notation
            thisContract = [coeff.replace('D','E') for coeff in thisContract]
            set[-1].contraction.append(thisContract)

        else:
            # Read exponents
            # Skip blank lines
            if (len(ParseObj[0]) != 0):
                # Check for common typo, full stop used instead of comma.
                for exponent in ParseObj[2:]:
                    if (exponent.count(".") > 1):
                        print("Error detected in line:")
                        print(line, end="")
                        print("Too many full stops/periods.")
                        sys.exit()
            # Is this an even tempered basis?
                if (ParseObj[2].lower() == 'even3'):
                    # Parameter number check
                    noParams = len(ParseObj[2:])
                    if (noParams < 4) or (noParams > 5):
                        print("Error in even tempered line:")
                        print(line, end="")
                        sys.exit()
                    nPrim = int(ParseObj[3])
                    alpha = float(ParseObj[4])
                    beta = float(ParseObj[5])
                    if (noParams == 4):
                        gamma = 0.0
                    else:
                        gamma = float(ParseObj[6])
                    # Fill the list
                    eTemp = []
                    for prim in range(1, nPrim+1):
                        if (prim == 1):
                            eTemp.append(alpha)
                        else:
                            eTemp.append(eTemp[prim - 2]*beta*(1 + ((gamma*(prim**2))/((nPrim+1)**2))))
                    # Sort into tightest exponent first ordering
                    eTemp.sort(reverse=True)
                if (FirstRun):
                    if eTemp is not None:
                        set.append(Basis(ParseObj[1], ParseObj[0], eTemp))
                        eTemp = None
                    else:
                        set.append(Basis(ParseObj[1], ParseObj[0], ParseObj[2:]))
                    # Skip the following logic on the first run through
                else:
                    # Check if we already have this atom and angular momentum
                    SameType = False
                    for entry in set:
                        if (ParseObj[1].lower() == entry.atom.lower() and ParseObj[0].lower() == entry.el.lower()):
                            SameType = True
                            # Store the number of functions previously there, this will be useful if they are contracted
                            NPreExps = len(entry.exponents)
                            # Add the exponents to the existing list and prevent a duplicate addition
                            if eTemp is not None:
                                # Add even temp exponents to previous exponents of same el
                                entry.exponents.extend(eTemp)
                                eTemp = None
                            else:
                                entry.exponents.extend(ParseObj[2:])
                            # Increment the skipcount
                            skipcount += 1
                            if (entry.contraction):
                                # Add the necessary information to the contraction pattern
                                for i in range(NPreExps, len(entry.exponents)):
                                    thisContract = []
                                    for j in range(0, i):
                                        thisContract.append('0.0')
                                    thisContract.append('1.0')
                                    entry.contraction.append(thisContract)
                    if SameType is False:
                        if eTemp is not None:
                            set.append(Basis(ParseObj[1], ParseObj[0], eTemp))
                            eTemp = None
                        else:
                            set.append(Basis(ParseObj[1], ParseObj[0], ParseObj[2:]))
                # Check if the atom type has changed since previous line reads
                if (FirstRun):
                    # Set the atomtype on our first run through
                    atomtype = str(ParseObj[1]).upper()
                else:
                    currentatom = str(ParseObj[1]).upper()
                    if (currentatom != atomtype):
                        # Note where the change occurs
                        set[count - skipcount].changeatom = True
                        # Then update atomtype to reflect new atom
                        atomtype = ''.join(currentatom)
            else:
                # If it's a blank line increment the skip count
                skipcount += 1
        # No longer first run, as long as we haven't been reading blank lines
        if (len(ParseObj[0]) != 0):
            FirstRun = False
#---------------------------------------------------------------------------------------------------

def WriteExt(set,precis,outfile):
    comp = util.getPrim(set)
    contcomp = util.getContract(set)
    countchange = 0
    FirstRun = True
    for entry in set:
        if FirstRun:
            FirstRun = False
            if (entry.contraction):
                outfile.write('! Basis set from pbt: (%s) -> [%s]\n' % (comp[0], contcomp[0]))
            else:
                outfile.write('! Basis set from pbt: (%s)\n' % comp[0])
        #Check if we are moving to a different atom. If so, print a spacer and comment line
        if (entry.changeatom):
            countchange += 1
            if (entry.contraction):
                outfile.write('! Basis set from pbt: (%s) -> [%s]\n' % (comp[countchange], contcomp[countchange]))
            else:
                outfile.write('\n! Basis set from pbt: (%s)\n' % comp[countchange])
        # Make a string of the exponents, sorted in reverse numerical order and truncated at precis
        FormattedExp = []
        for exp in entry.exponents:
            FormattedExp.append('{number:.{p}E}'.format(number=float(exp), p = precis))
        if (entry.contraction):
            # Don't sort exponents in the contracted case as chaos will ensue.
            ExpString = ",".join(FormattedExp)
        else:
            ExpString = ",".join(sorted(FormattedExp, key=float, reverse=True) )
        outfile.write('%s,%s,%s\n' % (entry.el.lower(), entry.atom.title(), ExpString))
        # Do we have a contracted basis? - not yet well tested
        if (entry.contraction):
            # Loop through the contractions
            for pattern in entry.contraction:
                # Make a string of each set of contraction coefficients
                FormattedPattern = []
                FirstCoeff = False
                leadingZero = False
                numberOfZeros = 0
                nonZeroEntry = 0
                # Test if only one contraction coefficient is non-zero
                for count,coeff in enumerate(pattern):
                    if (float(coeff).is_integer and ((float(coeff) - 0.0) == 0.0)):
                        numberOfZeros += 1
                    else:
                        nonZeroEntry = count
#                print("Total number of zeros in contraction is ", numberOfZeros)
                if ((len(pattern) - numberOfZeros) == 1):
#                    print("Just a single non-zero contraction coeff")
                    leadingZero = True

                if leadingZero:
                    FormattedPattern.append('{number:.{p}E}'.format(number=float(pattern[nonZeroEntry]), p = precis))
#                    print("Non-zero entry is ", FormattedPattern)
                    CoeffString = ",".join(FormattedPattern)
                    outfile.write('c,%s.%s,%s\n' % (nonZeroEntry+1, nonZeroEntry+1, CoeffString))
                else:
                    for count,coeff in enumerate(pattern):
                        FormattedPattern.append('{number:.{p}E}'.format(number=float(coeff), p = precis))
                        if FirstCoeff is False:
                            FirstCoeff = True
                            StartCoeff = count + 1
                    CoeffString = ",".join(FormattedPattern)
                    outfile.write('c,%s.%s,%s\n' % (StartCoeff, len(pattern), CoeffString))

#---------------------------------------------------------------------------------------------------

def WriteInt(set,precis,outfile):
    comp = util.getPrim(set)
    contcomp = util.getContract(set)
    countchange = 0
    firstrun = True
    for entry in set:
        if (firstrun or entry.changeatom):
            if (firstrun):
                firstrun = False
            elif (entry.changeatom):
                countchange += 1
            # Print a comment line of element name and basis composition
            if (entry.contraction):
                outfile.write('*! %s\t\t%s\t->\t%s\n' % (util.getElemName(entry.atom).upper(), comp[countchange], contcomp[countchange]))
            else:
                outfile.write('*! %s\t\t%s\n' % (util.getElemName(entry.atom).upper(), comp[countchange]))
        # Assemble and print the specification for each el
        expCounter = []
        if (entry.contraction):
            # Loop through the contractions
            for pattern in entry.contraction:
                FirstCoeff = False
                for count,coeff in enumerate(pattern):
                    # Trap cases where leading contraction coeffs are zero
                    if (coeff != '0.0' and FirstCoeff is False):
                        FirstCoeff = True
                        StartCoeff = count + 1
                EndCoeff = len(pattern)
                expCounter.append('%s.%s' % (StartCoeff, EndCoeff))
        else:
            for i in range(1,(len(entry.exponents)+1)):
                expCounter.append('%s.%s' % (i, i))
        expCountString = " ".join(expCounter)
        if (entry.contraction):
            outfile.write('%s %s BASNAME : %s %s %s\n' % (entry.atom.upper(), entry.el.lower(), len(entry.exponents), len(entry.contraction), expCountString))
        else:
            outfile.write('%s %s BASNAME : %s %s %s\n' % (entry.atom.upper(), entry.el.lower(), len(entry.exponents), len(entry.exponents), expCountString))
        outfile.write('basis set from pbt\n')
        for count,exp in enumerate(entry.exponents):
            outfile.write('  %.8E' % (float(exp)))
            if (((count + 1) % 5) == 0):
                outfile.write('\n')
        # Add contraction coefficients
        if (entry.contraction):
            countTot = len(entry.exponents)
            # Loop through contractions
            for pattern in entry.contraction:
                for coeff in pattern:
                    # Skip the 0.0 entries
                    if (coeff != '0.0'):
                        # Alter spacing if coeff is negative
                        if (float(coeff) < 0):
                            outfile.write(' %.8E' % (float(coeff)))
                        else:
                            outfile.write('  %.8E' % (float(coeff)))
                        countTot += 1
                        # If the total number of exponents + contraction coefficients is divisible by 5, add a newline
                        if ((countTot % 5) == 0):
                            outfile.write('\n')
            # Work out if we need a new line before we move to new angular momentum.
            if ((countTot % 5) != 0):
                outfile.write('\n')
        else:
            for i in range(1,(len(entry.exponents)+1)):
                outfile.write('  %.8E' % (1.0))
                if (((len(entry.exponents) + i) % 5) == 0):
                    outfile.write('\n')
            if ((len(entry.exponents) * 2 % 5) != 0):
                outfile.write('\n')
    print("You may want to change 'BASNAME' to something more sensible.")
