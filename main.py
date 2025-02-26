from argparse import ArgumentParser

from file import readFile
from pool import clothesPool
from prob import doTrials
from calc import showCalculations
from plot import plotPulls

def runSimulation(**kwargs):
    outfits = getOutfits(**kwargs)
    trials, desired_probability = getTrials(kwargs.get('trials')), getDesired(kwargs.get('desired'))
    if outfits:
        pool = clothesPool(outfits)
        results = doTrials(trials, pool)
        pulls = getPulls(results)
        showCalculations(trials, pulls, outfits, pool, desired_probability)
        plotPulls(trials, pulls, results, pool)	

def getTrials(trials):
    if not trials:
        trials = 500
    trials = max(1, int(trials))
    return trials

def getDesired(desired):
    if not desired:
        desired = 75
    desired = int(desired)
    desired = min(max(1, desired), 99.99)
    return desired/100

def getOutfits(**kwargs):
    file = kwargs.get('file')
    with open(file, 'r') as f:
        return readFile(f)

def getPulls(results):
    return [trial.pulls for trial in results]

arguments_to_add = ['-trials', '-desired', '-file']
parser = ArgumentParser(prog='Infinity Nikki Gacha Simulator')
for argument in arguments_to_add:
    parser.add_argument(argument)
arguments = parser.parse_args()

runSimulation(**vars(arguments))