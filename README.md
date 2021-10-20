# Set of Joint Distributions Achieving Positive Zero-Outage Capacities

This repository contains supplementary material for the papers "On the Set of
Joint Rayleigh Fading Distributions Achieving Positive Zero-Outage Capacities"
(Karl-L. Besser, Pin-Hsun Lin, and Eduard Jorswieck, 2020 54th Asilomar
Conference on Signals, Systems, and Computers, Nov. 2020,
[doi:10.1109/IEEECONF51394.2020.9443271](https://doi.org/10.1109/IEEECONF51394.2020.9443271))
and "On Fading Channel Dependency Structures with a Positive Zero-Outage
Capacity" (Karl-L. Besser, Pin-Hsun Lin, and Eduard Jorswieck, IEEE
Transactions to Communications, vol. 69, no. 10, pp. 6561-6574, Oct. 2021,
[doi:10.1109/TCOMM.2021.3097755](https://doi.org/10.1109/TCOMM.2021.3097755),
[arXiv:2102.02541](https://arxiv.org/abs/2102.02541)).

The files specific to the conference version can be found in the `asilomar2020`
branch.


The idea is to give an interactive version of the calculations and presented
concepts to the reader. One can also change different parameters and explore
different behaviors on their own.

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gl/klb2%2Fzero-outage-joint-distributions/master)


## File List
The following files are provided in this repository:

* [Maximum Ratio
  Combining.ipynb](https://mybinder.org/v2/gl/klb2%2Fzero-outage-joint-distributions/master?filepath=Maximum%20Ratio%20Combining.ipynb):
  Jupyter notebook that contains the MRC examples.
* [Selection
  Combining.ipynb](https://mybinder.org/v2/gl/klb2%2Fzero-outage-joint-distributions/master?filepath=Selection%20Combining.ipynb):
  Jupyter notebook that contains the SC examples.
* [Example - Clayton
  Copula.ipynb](https://mybinder.org/v2/gl/klb2%2Fzero-outage-joint-distributions/master?filepath=Example%20%2D%20Clayton%20Copula.ipynb):
  Jupyter notebook that illustrates an example of a positive ZOC with an
  underlying Clayton copula.
* `rayleigh_fading.py`: Python module that contains the calculations of the ZOC
  for Rayleigh fading channels.
* `nakagami_fading.py`: Python module that contains the calculations of the ZOC
  for Nakagami-m fading channels.
* `maximum_ratio_combining.py`: Python module that contains the calculations of
  the MRC examples.
* `selection_combining.py`: Python module that contains the calculations of the
  SC examples.
* `boundary.py`: Python module that contains an illustration of the ZOC idea
  (boundary of the support).
* `copulas.py`: Python module that contains the copulas used to construct joint
  distributions with positive ZOCs.
* `utils.py`: Python module that contains some helper functions


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
jupyter notebook 'Maximum Ratio Combining.ipynb'
```

You can also recreate the figures from the paper by running
```bash
bash run.sh
```


## Acknowledgements
This research was supported in part by the Deutsche Forschungsgemeinschaft
(DFG) under grant JO 801/23-1.


## License and Referencing
This program is licensed under the GPLv3 license. If you in any way use this
code for research that results in publications, please cite our original
article listed above.

You can use the following BibTeX entry
```bibtex
@article{Besser2021zoc,
	author = {Besser, Karl-Ludwig and Lin, Pin-Hsun and Jorswieck, Eduard A.},
	title = {On Fading Channel Dependency Structures with a Positive Zero-Outage Capacity},
	journal = {{IEEE} Transactions on Communications},
	year = {2021},
	volume = {69},
	number = {10},
	month = {10},
	pages = {6561--6574},
	eprint = {2102.02541},
	archivePrefix = {arXiv},
	primaryClass = {cs.IT},
	doi = {10.1109/TCOMM.2021.3097755},
}
```
