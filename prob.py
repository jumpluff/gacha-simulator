import numpy as np

class randPool:
    def __init__(self, pool, rng):
        self.pool = pool
        self.pity = pool.pity
        self.exponential = pool.exponential
        self.linear = pool.linear
        self.rng = rng

    @property
    def hasTargets(self):
        return len(self.pool.trial_targets) > 0
    
    @property
    def base_prob(self):
        return self.pool.prob
    
    def startTrial(self):
        self.pool.initForTrial()

    def getProb(self, rarity, pity_timers):
        if self.exponential:
            return self.exponentialProb(rarity, pity_timers) or self.base_prob[rarity]
        elif self.linear:
            return self.linearProb(rarity, pity_timers) or self.base_prob[rarity]
        return self.base_prob[rarity]
    
    def exponentialProb(self, rarity, pity_timers):
        pity_threshold = self.exponential[rarity]['pity_threshold']
        k = self.exponential[rarity]['k']
        prob = self.base_prob[rarity]
        start = self.pity[rarity] * pity_threshold
        timer = pity_timers[rarity]
        if timer > start:
            return prob + (1 - prob) * (1 - np.exp(-k * (timer - start)))
        
    def linearProb(self, rarity, pity_timers):
        pity_threshold = self.linear[rarity]['pity_threshold']
        m = self.linear[rarity]['m']
        start = self.pity[rarity] * pity_threshold
        timer = pity_timers[rarity]
        if timer > start:
            return self.base_prob[rarity] + m * (timer - start)
        
    def isOutfitAvailable(self, rarity):
        return len(self.pool.trial_clothes[rarity]) > 0
    
    def rand(self):
        return self.rng.random()
    
    def pull(self, rarity, results):
        pool = self.pool.trial_clothes[rarity]
        index = self.getPiece(rarity, pool)
        if not index is None:
            outfit = pool[index]
            removeFromList(pool, index)
            self.pool.updateClothesCount(outfit)
            self.checkAndReplenishOutfit(outfit, rarity, results)

    def getPiece(self, rarity, pool):
        pool_size = len(pool)
        if pool_size > 0:
            if self.pool.hasTidalGuidance(rarity):
                tidal_guidance_outfit = self.pool.tidalGuidanceOutfit(rarity)
                index = pool.index(tidal_guidance_outfit)
            else:
                index = self.rng.integers(pool_size)

            return index
    
    def checkAndReplenishOutfit(self, outfit, rarity, results):
        if self.pool.checkEmpty(outfit):
            self.pool.removeFromTidalGuidance(rarity)
            if not self.pool.no_duplicates:
                self.pool.addOutfit(outfit, True)
            results.completedOutfit(outfit)
            self.removeTarget(outfit)
    
    def removeTarget(self, outfit):
        targets = self.pool.trial_targets
        if outfit in targets:
            index = targets.index(outfit)
            removeFromList(targets, index)

class trialResults:
    def __init__(self):
        self.completed = {}
        self.pulls = 0
        self.pulled = {4: 0, 5: 0}

    def completedOutfit(self, outfit):
        if not outfit in self.completed:
            self.completed[outfit] = []
        self.completed[outfit].append(self.pulls)

def doTrials(trials, pool):
    pulls = []
    rng = np.random.default_rng()
    gacha = randPool(pool, rng)
    
    for _ in range(trials):
        result = simulateProbability(gacha)
        pulls.append(result)

    return pulls
 
def simulateProbability(gacha):   
    pity_timers = {4: 0, 5: 0}
    pity = gacha.pity

    results = trialResults()
    gacha.startTrial()

    while gacha.hasTargets:
        results.pulls += 1
        
        if gacha.isOutfitAvailable(5) and pity_timers[5] >= pity[5] - 1 and not pity[5] < 1:
            pullByRarity(pity_timers, gacha, results, 5)

        elif pity_timers[4] >= pity[4] - 1 and not pity[4] < 1:
            pullByRarity(pity_timers, gacha, results, '4+')

        else:
            pullRandom(pity_timers, gacha, results)

    return results

def pullByRarity(pity_timers, gacha, results, rarity):
    if rarity == '4+':
        rarity = pull4OrHigher(pity_timers, gacha)

    gacha.pull(rarity, results)
    
    pity_timers[rarity] = 0

    opposing_rarity = 4 if rarity == 5 else 5
    pity_timers[opposing_rarity] += 1

def pull4OrHigher(pity_timers, gacha):
    if gacha.isOutfitAvailable(5) and (gacha.rand() <= gacha.getProb(5, pity_timers) or not gacha.isOutfitAvailable(4)):
        return 5
    return 4

def pullRandom(pity_timers, gacha, results):
    rand = gacha.rand()
    prob_5 = gacha.getProb(5, pity_timers)
    if rand <= prob_5 and gacha.isOutfitAvailable(5):
        pullByRarity(pity_timers, gacha, results, 5)
    elif rand <= prob_5 + gacha.getProb(4, pity_timers) and gacha.isOutfitAvailable(4):
        pullByRarity(pity_timers, gacha, results, 4)
    else:
        pity_timers[4] += 1
        pity_timers[5] += 1

def removeFromList(to_remove, index):
    to_remove[index] = to_remove[-1]
    to_remove.pop()