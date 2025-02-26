import numpy as np 
import matplotlib.pyplot as plt
from math import ceil

def plotPulls(trials, pulls, results, pool):
    subplot_mode = True # change this to False if you want to see all the plots separately
    label_size = 7
    colors = ['#eb95c6', '#e26889', '#b4829e']
    figsize = (9, 9) # you might benefit from changing this depending on your screen
    plots = [
        lambda subplot: plotPullBins(subplot, trials, pulls, label_size, colors[0]),
        lambda subplot: plotPullsCumulative(subplot, pulls, label_size, colors[1]),
        lambda subplot: plotPullsNeeded(subplot, pulls, label_size, colors[2]),
        lambda subplot: plotCompletedTimes(subplot, results, pool.outfits, [colors[0], colors[1]])
    ]

    if subplot_mode:
        addPlotsSubplot(plots, figsize)
    else:
        addPlotsIndividual(plots)

    plt.show()

def addPlotsSubplot(plots, figsize):
    fig = plt.figure(figsize=figsize)
    subplots = fig.subplots(len(plots))
    for plot_num, plot in enumerate(plots):
        subplot = subplots[plot_num]
        plot(subplot)

    fig.tight_layout()

def addPlotsIndividual(plots):
    for plot in plots:
        fig = plt.figure()
        subplot = fig.subplots(1)
        plot(subplot)

def groupPulls(pulls, num_pulls, interval, cumulative=False):
    pulls_grouped = []
    for step in np.linspace(min(pulls), max(pulls), len(num_pulls)):
        upper_limit = step + interval - 1
        matching_pulls = [pull for pull in pulls if pull < step] if cumulative else [pull for pull in pulls if pull in range(int(step), int(upper_limit))]
        to_append = len(matching_pulls)/len(pulls) * 100 if cumulative else len(matching_pulls)
        pulls_grouped.append(to_append)

    return np.array(pulls_grouped)

def plotPullBins(subplot, trials, pulls, label_size, color):
    interval = getInterval(pulls)
    num_pulls = np.linspace(min(pulls), max(pulls), interval)
    pulls_grouped = groupPulls(pulls, num_pulls, interval)
    
    subplot.set_title(f'Average pulls needed (n={trials})')
    subplot.set_xlabel('Pulls')
    subplot.set_ylabel('Num. occurrences')
    subplot.tick_params(axis='x', labelsize=label_size)
    subplot.tick_params(axis='y', labelsize=label_size)
    subplot.plot(num_pulls, pulls_grouped, color=color)

def getInterval(input):
    q3, q1 = np.percentile(input, [75, 25])
    iqr = q3 - q1
    bin_width = 2 * iqr/(len(input) ** (1/3))
    bin_width = max(ceil(bin_width), 1)

    max_bins = 18 # chart size problem
    range = np.ptp(input)
    bins = range/bin_width
    if bins > max_bins:
        bin_width = range/max_bins

    return ceil(bin_width)

def plotPullsCumulative(subplot, pulls, label_size, color):
    interval = getInterval(pulls)
    num_pulls = np.linspace(min(pulls), max(pulls), interval)
    pulls_grouped = groupPulls(pulls, num_pulls, interval, True)

    subplot.set_title(f'Cumulative completion by number of pulls')
    subplot.set_xlabel('Pulls')
    subplot.set_ylabel('Percentage completed')
    subplot.set_xticks(np.arange(min(pulls), max(pulls), interval))
    subplot.tick_params(axis='x', labelsize=label_size)
    subplot.tick_params(axis='y', labelsize=label_size)
    subplot.plot(num_pulls, pulls_grouped, color=color)

def plotPullsNeeded(subplot, pulls, label_size, color):
    min_probability = 50
    max_probability = 100
    interval = 10
    range_probs = np.arange(min_probability, max_probability, interval)
    pulls_needed = [np.percentile(pulls, target) for target in range_probs]

    subplot.set_title('Pulls needed to attain probability')
    subplot.set_ylabel('Pulls needed')
    subplot.set_xlabel('Probability (%)')

    subplot.set_xticks(np.arange(min(range_probs), max(range_probs) + interval, interval))
    subplot.tick_params(axis='x', labelsize=label_size)
    subplot.tick_params(axis='y', labelsize=label_size)
    subplot.plot(range_probs, pulls_needed, color=color) 

def plotCompletedTimes(subplot, results, target_outfits, colors):
    events = getEvents(results, target_outfits)
    subplot.eventplot(events, colors=colors)
    subplot.set_title('Outfit completion times by star')
    subplot.tick_params(labelleft = False, left = False)
    subplot.legend(['4', '5'], loc='upper left')

def getEvents(results, outfits):
    events_4 = getEventsByRarity(results, outfits, 4)
    events_5 = getEventsByRarity(results, outfits, 5)
    return [events_4, events_5]

def getEventsByRarity(results, outfits, rarity):
    completed = [result.completed.get(outfit) for result in results for outfit in outfits if outfits[outfit]['rarity'] == rarity]
    if len(completed) > 0:
        completed_times = [time for time in completed if time is not None]
        return [time for completed_time in completed_times for time in completed_time]
    else:
        return []