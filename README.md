# Infinity Nikki Gacha Simulator

Hi! This is a Python program I wrote to simulate pulling for clothes in *Infinity Nikki* for statistical purposes/checking expected costs. It works for user-defined resonance banners (including presets I have included), as well as the Surprise-O-Matic. It supports speculative soft pity gradients (with exponential growth and linear functions) as well, because without soft pity for 5-star banners, [the advertised rates cannot be achieved](https://gist.github.com/jumpluff/a670af1dec36d444dd1fa4691c3b8223).

It is not the most robust thing, because I designed it primarily for my own use (sharing it is pretty embarrassing), but if you can't get it working or it seems broken in some way, please do let me know.

Warning: It has runtimes of about 2-3s for 10,000 trials of ~180 pulls each (so more is possible for e.g. Distant Sea and the Surprise-O-Matic). I'm not sure how to make it zippier :(

# Usage 

**Version**: I have only tested it in Python 3.13.1.

**Dependencies**: matplotlib (only tested with 3.10.0).

**Command**: With Python installed:

	py main.py -file=presets/5-star.json -trials=1000 -desired=80

`-trials`: optional; defaults to 500; 1000 recommended. Number of trials to perform

`-desired`: optional; defaults to 75. Specifies target percentage when computing number of pulls required to yield given probability of completing outfit(s)

`-file`: required; should specify the path of a .json file with the following structure:

> `4_star_pity`: integer value for the pity timer at which you roll a 4 or higher-rarity piece
> 
> `5_star_pity`: as above
> 
> `4_star_prob`: *base* (not consolidated) percentage for rolling a 4-star piece (do not divide by 100)
> 
> `5_star_prob`: as above
> 
> `no_duplicates`: optional; boolean. Disables rolling duplicates of completed outfits. The Surprise-O-Matic has duplicate protection for 4- and 5-stars, which this is for. Omit if in doubt
>
> `exponential`: optional; an object comprising objects as described below; only one of exponential/linear may be active
>
> `linear`: optional; an object comprising objects as described below
>
> `outfits`: an object comprising objects as described below

#### Exponential mode

`exponential` is an object consisting of `'4'` and `'5'` (as applicable), each with the following structure:

> `k`: integer or float above 0; growth factor
>
> `pity_threshold`: integer or float above/equal to 0 and less than 1; fraction of hard pity after which gradient should be activated

At pity timer > pity $\times$ the pity threshold, the simulator scales probability according to the following formula (for $p$ base probability, $h$ hard pity, $t$ timer, $l$ pity threshold):

$$p + (1 - p) \times (1 - e^{-k \times (t - h \times l)})$$

Feel free to make a pull request with something better.

#### Linear mode

`linear` is an object consisting of `'4'` and `'5'` (as applicable), each with the following structure:

> `m`: float > 0 and < 1; slope
>
> `pity_threshold`: integer or float above/equal to 0 and less than 1; fraction of hard pity after which linear mode should be activated

At pity timer > pity $\times$ the pity threshold, the simulator scales probability according to the following formula (for $p$ base probability, $h$ hard pity, $t$ timer, $l$ pity threshold):

$$p + m \times (t - h \times l)$$

#### Outfits

Outfits are objects with any name with the following structure:

> `rarity`: 4 or 5
>
> `pieces`: # of pieces in the outfit
> 
> `tidal_guidance`: optional; sets priority for rolling outfits in order (like in the Distant Sea banner), starting with the lowest value (e.g. 1). Can be a positive integer or a list of same
> 
> `copies`: optional; positive integer. Tracks target # of copies as desired outfits and will roll until all copies across all outfits are obtained. At least one outfit with `copies` >= 1 is required

A set of json files for the following types of banners are included in the ` presets` folder:
* 4-star
* 5-star
* Distant Sea
* Surprise-O-Matic
* 5-star using consolidated probability
* 5-star using an exponential pity formula (use your own values)
* 5-star using a linear pity formula (use your own values)

plot.py has a number of display variables that can be customised. Of note, `subplot_mode` shows all the graphs as subplots of one figure (so one window instead of four).