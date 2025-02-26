import numpy as np
from math import ceil

def showCalculations(trials, pulls, outfits, pool, desired_probability):
    pull_cost = outfits['pull_cost']
    pull_unit = outfits['pull_unit']
    pieces = pool.target_pieces
    
    q1, q2, q3 = np.percentile(pulls, [25, 50, 75])
    iqr = q3 - q1
    mean = np.mean(pulls)
    needed = np.percentile(pulls, [desired_probability * 100])[0]
    needed_cost = '{:,}'.format(ceil(needed) * pull_cost)    
    average_cost = '{:,}'.format(ceil(mean) * pull_cost)
    trials = '{:,}'.format(trials)

    print(f'{needed} pulls needed to attain at least a {desired_probability * 100}% chance of getting all {pieces} pieces over {trials} trials, costing {needed_cost} {pull_unit}.')
    print(f'The interquartile range was {iqr} pulls (Q1: {q1} pulls, Q3: {q3} pulls).')
    print(f'The minimum was {min(pulls)} pulls, and the maximum was {max(pulls)}.')
    print(f'Mean {mean} and median {q2} pulls to complete, costing {average_cost} {pull_unit}.')