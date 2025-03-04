from json import load

def readFile(file):
    values = load(file)
    required_keys = ['4_star_pity', '5_star_pity', '4_star_prob', '5_star_prob', 'outfits']
    if not all(key in values for key in required_keys):
        raise InvalidFile('Required key missing from file.')
    
    outfits = checkOutfits(values)

    return {
        'pity': getPity(values),
        'prob': getProb(values),
        'outfits': outfits,
        'pull_unit': getPullUnit(values),
        'pull_cost': getPullCost(values),
        'no_duplicates': getNoDuplicates(values),
        'exponential': getExponential(values, outfits),
        'linear': getLinear(values, outfits)
    }

def checkOutfits(values):
    outfits = values['outfits']
    required_outfit_keys = ['rarity', 'pieces']
    if any(key not in outfits[outfit] for outfit in outfits for key in required_outfit_keys):
        raise InvalidFile('Required key missing from at least one outfit.')
    target = [outfit for outfit in outfits if 'copies' in outfits[outfit]]
    if not len(target) >= 1:
        raise InvalidFile('At least one target (specified with \'copies\') is needed.')
    rarities = [outfits[outfit]['rarity'] for outfit in outfits]
    if not all(rarity in (4, 5) for rarity in rarities):
        raise InvalidFile('Rarities must only be 4 or 5.')
    for outfit in outfits:
        outfits[outfit]['name'] = outfit
    return outfits
    
def getPity(values):
    four_star_pity = checkPity(values['4_star_pity'])
    five_star_pity = checkPity(values['5_star_pity'])
    return {4: four_star_pity, 5: five_star_pity}

def checkPity(pity):
    pity = int(pity)
    return pity

def getProb(values):
    four_star_prob = checkProb(values['4_star_prob'])
    five_star_prob = checkProb(values['5_star_prob'])
    if four_star_prob == 0 and five_star_prob == 0:
        raise InvalidFile('At least one of 4- and 5-star probability must be over 0.')
    return {4: four_star_prob/100, 5: five_star_prob/100}

def checkProb(prob):
    prob = float(prob)
    return min(max(prob, 0), 99.99)

def getPullCost(values):
    pull_cost = values.get('pull_cost')
    if type(pull_cost) == int and not pull_cost is None:
        return pull_cost
    elif pull_cost is None:
        return 120
    raise InvalidFile('Pull cost must be an integer or omitted.')

def getPullUnit(values):
    pull_unit = values.get('pull_unit')
    if type(pull_unit) == str and not pull_unit is None:
        return pull_unit
    elif pull_unit is None:
        return 'Diamonds'
    raise InvalidFile('Pull unit must be a string or omitted.')

def getNoDuplicates(values):
    no_duplicates = values.get('no_duplicates')
    if no_duplicates and not type(no_duplicates) == bool:
        raise InvalidFile('No-duplicates flag must be a boolean.')
    return no_duplicates

def getExponential(values, outfits):
    exponential = values.get('exponential')
    if exponential and type(exponential) == dict:
        return {
            4: checkExponentialRarity(exponential.get('4'), outfits, 4),
            5: checkExponentialRarity(exponential.get('5'), outfits, 5)
        }
    elif exponential:
        raise InvalidFile('Exponential must be an object.')
    
def checkExponentialRarity(exponential, outfits, rarity):
    outfits_for_rarity = getOutfitsForRarity(outfits, rarity)
    if len(outfits_for_rarity) > 0 and not exponential:
        raise InvalidFile('Exponential must be specified for all probabilities outfits are listed for.')
    
    if exponential and not type(exponential) == dict:
        raise InvalidFile('Exponential subobjects must be objects.')
    elif exponential:
        k = exponential.get('k')
        pity_threshold = exponential.get('pity_threshold')
        if not ((type(k) == float or type(k) == int) and k >= 0):
            raise InvalidFile('Growth constant (k) must be an int or float > 0.')
        if not ((type(pity_threshold) == float or type(pity_threshold) == int) and pity_threshold >= 0 and pity_threshold < 1):
            raise InvalidFile('Pity threshold must be an int or float between 0 and 1.')
        if not (k and pity_threshold):
            raise InvalidFile('Exponentials must consist of a growth constant (k) and a pity threshold.')
        
        return {
            'k': k,
            'pity_threshold': pity_threshold
        }
    
def getLinear(values, outfits):
    linear = values.get('linear')
    if linear and not type(linear) == dict:
        raise InvalidFile('Linear must be an object.')
    elif linear:
        exponential = values.get('exponential')
        if exponential:
            raise InvalidFile('Linear and exponential mode cannot be used at the same time.')
        return {
            4: checkLinearRarity(linear.get('4'), outfits, 4),
            5: checkLinearRarity(linear.get('5'), outfits, 5)
        }

def checkLinearRarity(linear, outfits, rarity):
    outfits_for_rarity = getOutfitsForRarity(outfits, rarity)
    if len(outfits_for_rarity) > 0 and not linear:
        raise InvalidFile('Linear must be specified for all probabilities outfits are listed for.')
    
    m = linear.get('m')
    pity_threshold = linear.get('pity_threshold')
    if not (type(pity_threshold) == float or type(pity_threshold == int) and pity_threshold >= 0 and pity_threshold < 1):
        raise InvalidFile('Pity threshold must be an int or float between 0 and 1.')
    if not ((type(m) == int or type(m) == float) and m >= 0 and m < 1):
        raise InvalidFile('m must be an int or float between 0 and 1.')
    if not (m and pity_threshold):
        raise InvalidFile('Linear must consist of a slope (m) and a pity threshold.')
    
    return {
        'm': m,
        'pity_threshold': pity_threshold
    }
    
def getOutfitsForRarity(outfits, rarity):
    return [outfit for outfit in outfits if outfits[outfit]['rarity'] == rarity]
    
class InvalidFile(Exception):
    pass