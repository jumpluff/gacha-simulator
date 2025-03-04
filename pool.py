from copy import copy

class clothesPool:
    def __init__(self, outfits):
        self.outfits = outfits['outfits']
        self.pity = outfits['pity']
        self.prob = outfits['prob']
        self.no_duplicates = outfits['no_duplicates']
        self.exponential = outfits['exponential']
        self.linear = outfits['linear']
        self.clothes = {}
        self.clothes_count = {}
        self.targets = []
        self.addPool()

    def addPool(self):
        self.clothes = {5: [], 4: []}
        self.tidal_guidance = {5: {}, 4: {}}
        for outfit in self.outfits:
            addOutfitToPool(self, outfit, self.outfits[outfit])
        self.tidal_guidance = sortTidalGuidance(self)

    def addOutfit(self, outfit_name, trial=False):
        outfit = self.outfits[outfit_name]
        outfit_pieces = outfit['pieces']
        clothes = self.clothes if not trial else self.trial_clothes
        clothes_count = self.clothes_count if not trial else self.trial_clothes_count
        clothes[outfit['rarity']] += [outfit_name] * outfit_pieces
        clothes_count[outfit_name] = outfit_pieces

    def initForTrial(self):
        self.trial_clothes = {5: list(self.clothes[5]), 4: list(self.clothes[4])}
        self.trial_clothes_count = copy(self.clothes_count)
        self.trial_tidal_guidance = {5: list(self.tidal_guidance[5]), 4: list(self.tidal_guidance[4])}
        self.trial_targets = list(self.targets)

    def updateClothesCount(self, outfit_name):
        self.trial_clothes_count[outfit_name] -= 1

    @property
    def target_pieces(self):
        return sum(getPiecesForOutfit(self, outfit) for outfit in self.targets)

    def hasTidalGuidance(self, rarity):
        return len(self.trial_tidal_guidance[rarity]) > 0

    def tidalGuidanceOutfit(self, rarity):
        return self.trial_tidal_guidance[rarity][0]
        
    def removeFromTidalGuidance(self, rarity):
        if self.hasTidalGuidance(rarity):
            tidal_guidance = self.trial_tidal_guidance[rarity]
            tidal_guidance[0] = tidal_guidance[-1]
            tidal_guidance.pop()

    def checkEmpty(self, outfit_name):
        return self.trial_clothes_count[outfit_name] <= 0

def addOutfitToPool(self, outfit_name, outfit):
    checkTarget(self, outfit, outfit_name) or 0
    checkTidalGuidance(self, outfit.get('tidal_guidance'), outfit_name)
    self.addOutfit(outfit_name)

def checkTarget(self, outfit, outfit_name):
    number_copies = outfit.get('copies')
    if number_copies:
        if not int(number_copies) and int(number_copies) > 0:
            raise ParseError('Number of copies must be a positive integer.')
        if self.no_duplicates and number_copies > 1:
            raise ParseError('Number of copies should not exceed 1 if no_duplicates is true.')
        self.targets += [outfit_name] * number_copies
        return number_copies

def checkTidalGuidance(self, tidal_guidance, outfit_name):
    if tidal_guidance and (isinstance(tidal_guidance, list) or isinstance(tidal_guidance, int)):
        if isinstance(tidal_guidance, list):
            for prio in tidal_guidance:
                checkTidalGuidance(self, prio, outfit_name)
        elif int(tidal_guidance) and int(tidal_guidance) >= 0:
            addOutfitToTidalGuidance(self, tidal_guidance, outfit_name)
        else:
            raise ParseError('Tidal Guidance must be an integer at value 0+, or a list of same.')
    
def addOutfitToTidalGuidance(self, prio, outfit_name):
    rarity = self.outfits[outfit_name]['rarity']
    tidal_guidance = self.tidal_guidance[rarity]
    tidal_guidance[prio] = outfit_name

def sortTidalGuidance(self):
    sorted_tidal_guidance = {}
    tidal_guidance = self.tidal_guidance
    for rarity in tidal_guidance:
        sorted_tidal_guidance[rarity] = [v for (k, v) in sorted(tidal_guidance[rarity].items(), key=lambda item: int(item[0]))]
    return sorted_tidal_guidance

def getPiecesForOutfit(self, outfit_name):
    outfit = self.outfits[outfit_name]
    return outfit['pieces']

class ParseError(Exception):
    pass