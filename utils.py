"""Helper functions

This module contains different helper functions, e.g., to export the results.


Copyright (C) 2021 Karl-Ludwig Besser

This program is used in the article:
Karl-Ludwig Besser and Eduard Jorswieck, "On Fading Channel Dependency
Structures with a Positive Zero-Outage Capacity", submitted to IEEE
Transactions in Communications.

License:
This program is licensed under the GPLv3 license. If you in any way use this
code for research that results in publications, please cite our original
article listed above.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.
See the GNU General Public License for more details.

Author: Karl-Ludwig Besser, Technische Universität Braunschweig
"""

from itertools import tee

import numpy as np
import pandas as pd

#https://docs.python.org/3/library/itertools.html#itertools-recipes
def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)

def export_results(data, filename):
    data = pd.DataFrame.from_dict(data)
    data.to_csv(filename, sep='\t', index=False)

def w_copula(a, b):
    return np.maximum(a + b - 1, 0)
