# Plots the basis set primitives
# Requires numpy and matplotlib
import sys
from basclas import Basis

# These are the "Tableau 20" colors as RGB. Adapted from Randy Olson's blog
# http://www.randalolson.com/2014/06/28/how-to-make-beautiful-data-visualizations-in-python-with-matplotlib/
tableau20 = [(31, 119, 180), (255, 127, 14), (44, 160, 44), (214, 39, 40),
             (148, 103, 189), (140, 86, 75), (227, 119, 194), (127, 127, 127),
             (188, 189, 34), (23, 190, 207), (174, 199, 232), (255, 187, 120),
             (152, 223, 138), (255, 152, 150), (197, 176, 213), (196, 156, 148),
             (247, 182, 210), (199, 199, 199), (219, 219, 141), (158, 218, 229)]

def ViewComp(set):
    # Plots primitives for multiple sets by el.
    # Check for numpy and matplotlib, try to exit gracefully if not found
    import imp
    try:
        imp.find_module('numpy')
        foundnp = True
    except ImportError:
        foundnp = False
    try:
        imp.find_module('matplotlib')
        foundplot = True
    except ImportError:
        foundplot = False
    if not foundnp:
        print("Numpy is required for plotting exponents. Exiting")
        sys.exit()
    if not foundplot:
        print("Matplotlib is required for plotting exponents. Exiting")
        sys.exit()
    import numpy as np
    import matplotlib.pyplot as plt
    # Check that we have more than one set
    goodToGo = False
    thisCompare = []
    # Remember blank offset for the atomList of ticklabels
    atomList = []
    print("Using the first set as the template to determine available el.")
    for entry in set:
        if (entry.changeatom):
            goodToGo = True
            break
        # Use the first basis set as the template
        currentEl = entry.el
        thisCompare.append([float(i) for i in entry.exponents])
        firstRun = True
        for entry in set:
            if (entry.el == currentEl):
                atomList.append(entry.atom)
                if firstRun:
                    firstRun = False
                else:
                    thisCompare.append([float(i) for i in entry.exponents])
        # print(thisCompare) <- debug
        # Start plotting
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        # Convert to numpy array
        thisCompare = np.array(thisCompare)
        # Scale the Tableau RGB values to the [0, 1] range, which is the format matplotlib accepts.
        trimTableau=[]
        totEls = len(thisCompare)
        for i in range(totEls):
            r, g, b = tableau20[i]
            trimTableau.append((r / 255., g / 255., b / 255.))
        ax.set_xlabel('Atom')
        ax.set_ylabel('Exponent')
        ax.eventplot(thisCompare, colors=trimTableau, orientation='vertical', linelengths=0.75)
        ax.set_yscale('log')
        # Label with el
        ax.annotate(currentEl, xy=(0.95, 0.95), xycoords='axes fraction', size=15)
        plt.xticks(np.arange(len(atomList)))
        ax.set_xticklabels(atomList)
        plt.show()
        # All done, reset thisCompare
        thisCompare = []
        atomList = []
    if not goodToGo:
        print("Need more than one atom/set to be able to compare. Exiting.")
        sys.exit()

#---------------------------------------------------------------------------------------------------

def ViewPNG(set,viewfile,filename,save):
    # Currently does not handle multiple sets well, perhaps check for this and bomb?
    # Check for numpy and matplotlib, try to exit gracefully if not found
    import imp
    try:
        imp.find_module('numpy')
        foundnp = True
    except ImportError:
        foundnp = False
    try:
        imp.find_module('matplotlib')
        foundplot = True
    except ImportError:
        foundplot = False
    if not foundnp:
        print("Numpy is required for plotting exponents. Exiting.")
        sys.exit()
    if not foundplot:
        print("Matplotlib is required for plotting exponents. Exiting.")
        sys.exit()
    import numpy as np
    import matplotlib.pyplot as plt
    # Create python list of lists (all exponents)
    allExps = []
    # Grab angular momentum as labels
    labels = []
    for entry in set:
        workingExp = [float(i) for i in entry.exponents]
        allExps.append(workingExp)
        labels.append(entry.el.lower())
    # Convert to numpy array
    allExps = np.array(allExps, dtype=object)
    # Debug print
#    print(allExps, allExps.shape)
    # Start plotting
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    # Scale the Tableau RGB values to the [0, 1] range, which is the format matplotlib accepts.
    trimTableau=[]
    sets = len(labels)
    for i in range(sets):
        r, g, b = tableau20[i]
        trimTableau.append((r / 255., g / 255., b / 255.))
    ax.set_xlabel('Angular momentum')
    ax.set_ylabel('Exponent')
    ax.eventplot(allExps, colors=trimTableau, orientation='vertical', linelengths=0.75)
    # Switch to a log plot to make diffuse exponents more visible
    ax.set_yscale('log')
    # Creates a list of x_tick positions based on length of labels
    x_pos = [x for x in range(len(labels))]
    # Sets the position of the x_ticks based on that list
    ax.set_xticks(x_pos)
    # Labels the x_ticks with the angular momentum 
    ax.set_xticklabels(labels)
    if save:
        plt.savefig(viewfile)
        print('Plot written to PNG file', filename)
    else:
        plt.show()
