#Some utilities that might be used in various places
periodicNames = {'h': 'hydrogen', 'he': 'helium', 'li': 'lithium', 'be': 'beryllium', 'b': 'boron', 'c': 'carbon', 'n': 'nitrogen', 'o': 'oxygen', 'f': 'fluorine', 'ne': 'neon', 'na': 'sodium', 'mg': 'magnesium', 'al': 'aluminium', 'si': 'silicon', 'p': 'phosphorus', 's': 'sulfur', 'cl': 'chlorine', 'ar': 'argon', 'k': 'potassium', 'ca': 'calcium', 'sc': 'scandium', 'ti': 'titanium', 'v': 'vanadium', 'cr': 'chromium', 'mn': 'manganese', 'fe': 'iron', 'co': 'cobalt', 'ni': 'nickel', 'cu': 'copper', 'zn': 'zinc', 'ga': 'gallium', 'ge': 'germanium', 'as': 'arsenic', 'se': 'selenium', 'br': 'bromine', 'kr': 'krypton', 'rb': 'rubidium', 'sr': 'strontium', 'y': 'yttrium', 'zr': 'zirconium', 'nb': 'niobium', 'mo': 'molybdenum', 'tc': 'technetium', 'ru': 'ruthenium', 'rh': 'rhodium', 'pd': 'palladium', 'ag': 'silver', 'cd': 'cadmium', 'in': 'indium', 'sn': 'tin', 'sb': 'antimony', 'te': 'tellurium', 'i': 'iodine', 'xe': 'xenon', 'cs': 'caesium', 'ba': 'barium', 'la': 'lanthanum', 'ce': 'cerium', 'pr': 'praseodymium', 'nd': 'neodymium', 'pm': 'promethium', 'sm': 'samarium', 'eu': 'europium', 'gd': 'gadolinium', 'tb': 'terbium', 'dy': 'dysprosium', 'ho': 'holmium', 'er': 'erbium', 'tm': 'thulium', 'yb': 'ytterbium', 'lu': 'lutetium', 'hf': 'hafnium', 'ta': 'tantalum', 'w': 'tungsten', 're': 'rhenium', 'os': 'osmium', 'ir': 'iridium', 'pt': 'platinum', 'au': 'gold', 'hg': 'mercury', 'tl': 'thallium', 'pb': 'lead', 'bi': 'bismuth', 'po': 'polonium', 'at': 'astatine', 'rn': 'radon', 'fr': 'francium', 'ra': 'radium', 'ac': 'actinium', 'th': 'thorium', 'pa': 'protactinium', 'u': 'uranium', 'np': 'neptunium', 'pu': 'plutonium', 'am': 'americium', 'cm': 'curium', 'bk': 'berkelium', 'cf': 'californium', 'es': 'einsteinium', 'fm': 'fermium', 'md': 'mendelevium', 'no': 'nobelium', 'lr': 'lawrencium', 'rf': 'rutherfordium', 'db': 'dubnium', 'sg': 'seaborgium', 'bh': 'bohrium', 'hs': 'hassium', 'mt': 'meitnerium', 'ds': 'darmstadtium', 'rg': 'roentgenium', 'cn': 'copernicium', 'uut': 'ununtrium', 'fl': 'flerovium', 'uup': 'ununpentium', 'lv': 'livermorium', 'uus': 'ununseptium', 'uuo': 'ununoctium'}

atomicNumber = {'1': 'h', '2': 'he', '3': 'li', '4': 'be', '5': 'b', '6': 'c', '7': 'n', '8': 'o', '9': 'f', '10': 'ne', '11': 'na', '12': 'mg', '13': 'al', '14': 'si', '15': 'p', '16': 's', '17': 'cl', '18': 'ar', '19': 'k', '20': 'ca', '21': 'sc', '22': 'ti', '23': 'v', '24': 'cr', '25': 'mn', '26': 'fe', '27': 'co', '28': 'ni', '29': 'cu', '30': 'zn', '31': 'ga', '32': 'ge', '33': 'as', '34': 'se', '35': 'br', '36': 'kr', '37': 'rb', '38': 'sr', '39': 'y', '40': 'zr', '41': 'nb', '42': 'mo', '43': 'tc', '44': 'ru', '45': 'rh', '46': 'pd', '47': 'ag', '48': 'cd', '49': 'in', '50': 'sn', '51': 'sb', '52': 'te', '53': 'i', '54': 'xe', '55': 'cs', '56': 'ba', '57': 'la', '58': 'ce', '59': 'pr', '60': 'nd', '61': 'pm', '62': 'sm', '63': 'eu', '64': 'gd', '65': 'tb', '66': 'dy', '67': 'ho', '68': 'er', '69': 'tm', '70': 'yb', '71': 'lu', '72': 'hf', '73': 'ta', '74': 'w', '75': 're', '76': 'os', '77': 'ir', '78': 'pt', '79': 'au', '80': 'hg', '81': 'tl', '82': 'pb', '83': 'bi', '84': 'po', '85': 'at', '86': 'rn', '87': 'fr', '88': 'ra', '89': 'ac', '90': 'th', '91': 'pa', '92': 'u', '93': 'np', '94': 'pu', '95': 'am', '96': 'cm', '97': 'bk', '98': 'cf', '99': 'es', '100': 'fm', '101': 'md', '102': 'no', '103': 'lr', '104': 'rf', '105': 'db', '106': 'sg', '107': 'bh', '108': 'hs', '109': 'mt', '110': 'ds', '111': 'rg', '112': 'cn', '113': 'nh', '114': 'fl', '115': 'mc', '116': 'lv', '117': 'ts', '118': 'og'}

# Dictionary of numerical values for orbital angular momentum. j is skipped as it is special (not sure if this
# is done in Gaussian?). Assumed an alphabetical progression after that, skipping a second occurance of s/p.
numEl = {'s': 0, 'p': 1, 'd': 2, 'f': 3, 'g': 4, 'h': 5, 'i': 6, 'k': 7, 'l': 8, 'm': 9, 'n': 10, 'o': 11,
'q': 12, 'r': 13}

def getMaxEl(set):
#Determines the maximum angular momentum within a set, returning a list of numerical values
    maxEl = []
    El = 0
    for entry in set:
        if (entry.changeatom):
            maxEl.append(El)
            El = 0
        if numEl.get(entry.el.lower()) > El:
            El = numEl.get(entry.el.lower())
    maxEl.append(El)
    return maxEl

def getPrim(set):
#Calculates the number and type of the primitives in set, returns composition as the list lcomp
    lcomp = []
    comp = ""
    for entry in set:
        if (entry.changeatom):
            lcomp.append(comp)
            comp = ""
        numexp = len(entry.exponents)
        comp += str(numexp)
        comp += entry.el.lower()
    #Make sure we add the last composition to the list
    lcomp.append(comp)
    return lcomp

def getContract(set):
#Extracts the number and type of contracted functions in set, returning compositions as a list lcontcomp
#Assumes that Basis.contraction will have one list for each contracted function
    lcontcomp = []
    contcomp = ""
    for entry in set:
        if (entry.changeatom):
            lcontcomp.append(contcomp)
            contcomp = ""
        if (entry.contraction):
            numexp = len(entry.contraction)
        # If we have uncontracted exponents in addition to contracted
        else:
            numexp = len(entry.exponents)
        contcomp += str(numexp)
        contcomp += entry.el.lower()
    lcontcomp.append(contcomp)
    return lcontcomp

def getElemName(element):
#Converts a chemical symbol into the name of the element, returning the name
    if (element.lower() not in periodicNames):
        print('Element ', element.title(), ' not recognised')
        name = 'Unknown'
    else:
        name = periodicNames.get(element.lower())
    return name
