# Set of Joint Distributions Achieving Positive Zero-Outage Capacities

This repository contains supplementary material for the paper "On the Set of
Joint Rayleigh Fading Distributions Achieving Positive Zero-Outage Capacities"
(Karl-L. Besser, Pin-Hsun Lin, and Eduard Jorswieck, 2020 54th Asilomar
Conference on Signals, Systems, and Computers, 2020, [doi:XXX]()).

The idea is to give an interactive version of the calculations and presented
concepts to the reader. One can also change different parameters and explore
different behaviors on their own.

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gl/klb2%2Fzero-outage-joint-distributions/master)


## File List
The following files are provided in this repository:

* [Rayleigh
  Fading.ipynb](https://mybinder.org/v2/gl/klb2%2Fzero-outage-joint-distributions/master?filepath=Rayleigh%20Fading.ipynb):
  Jupyter notebook that contains plots about the results for Rayleigh fading.
* `rayleigh_fading.py`: Python module that contains the calculations of the ZOC
  for Rayleigh fading channels.
* `copulas.py`: Python module that contains the copulas used to construct joint
  distributions with positive ZOCs.


## Usage
### Running it online
The easiest way is to use services like [Binder](https://mybinder.org/) to run
the notebook online. Simply navigate to
[https://mybinder.org/v2/gl/klb2%2Fzero-outage-joint-distributions/master](https://mybinder.org/v2/gl/klb2%2Fzero-outage-joint-distributions/master)
to run the notebooks in your browser without setting everything up locally.

### Local Installation
If you want to run it locally on your machine, Python3 and Jupyter are needed.
The present code was developed and tested with the following versions:
- Python 3.8
- Jupyter 1.0
- numpy 1.18
- scipy 1.4

Make sure you have [Python3](https://www.python.org/downloads/) installed on
your computer.
You can then install the required packages (including Jupyter) by running
```bash
pip3 install -r requirements.txt
jupyter nbextension enable --py widgetsnbextension
```
This will install all the needed packages which are listed in the requirements 
file. The second line enables the interactive controls in the Jupyter
notebooks.

Finally, you can run the Jupyter notebooks with
```bash
jupyter notebook 'Rayleigh Fading.ipynb'
```


## Acknowledgements
This research was supported in part by the Deutsche Forschungsgemeinschaft
(DFG) under grant JO 801/23-1.


## License and Referencing
This program is licensed under the GPLv3 license. If you in any way use this
code for research that results in publications, please cite our original
article listed above.
