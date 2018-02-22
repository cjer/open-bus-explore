# open-bus-explore
Where I play with GTFS, some notebooks also published in https://cjer.github.io

## Setup
To run these notebooks you need Python 3.5+ with all the necessary packages, Jupyter Notebook (and an internet connection for some data fetches).

### Downloads and installs
1. Install Anaconda3 - this will give you all the basic scipy libraries (pandas, matplotlib, seaborn...) and Jupyter notebook. I'm using version 4.4, can't vouch for 5+. Get the right version [here](https://repo.continuum.io/archive/), make sure you're installing Anaconda**3** and not **2**
2. You might need to update some libraries (`conda update libname [-c conda-forge]`)
3. Install [partridge](https://github.com/remix/partridge)
4. (for notebook 3) Install [networkx](https://networkx.github.io/)
5. (for notebook 3) Install [peartree](https://github.com/kuanb/peartree)
*In the near-ish future, I'll try to publish a docker container and/or a spec-file for creating an environment more easily. A [binder](https://mybinder.org/) might pop-up at anytime too.*

### Run
After you have everything installed, run a local jupyter notebook (shortcut should be provided with the Anaconda installation), pointing it to the folder you cloned the repo to. And voila - you're on your own. 

## Notes
Note that the data is based on the time of download, so some parameters might need to be changed (e.g. the date for filtering the Partridge GTFS feed).


Please let me know if something's off or missing with anything.

