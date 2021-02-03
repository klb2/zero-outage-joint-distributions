"""Copulas

This module contains different copula functions.


Copyright (C) 2021 Karl-Ludwig Besser

This program is used in the article:
Karl-Ludwig Besser, Pin-Hsun Lin, and Eduard Jorswieck, "On Fading Channel
Dependency Structures with a Positive Zero-Outage Capacity", submitted to IEEE
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

import numpy as np

@np.vectorize
def zoc_copula1(a, b, t=.5):
    if np.abs(a-b)>t:
        c = np.minimum(a, b)
    elif np.abs(a+b-1) > 1-t:
        c = np.maximum(a+b-1, 0)
    else:
        c = (a+b)/2 - t/2
    return c

@np.vectorize
def zoc_copula2(a, b, t=.5):
    if a < t and b < t:
        c = np.maximum(a+b-t, 0)
    else:
        c = np.minimum(a, b)
    return c
