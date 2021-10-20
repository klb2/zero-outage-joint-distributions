"""Copulas

This module contains different copula functions.


Copyright (C) 2021 Karl-Ludwig Besser

This program is used in the article:
Karl-Ludwig Besser, Pin-Hsun Lin, and Eduard Jorswieck, "On Fading Channel
Dependency Structures with a Positive Zero-Outage Capacity", IEEE Transactions
on Communications, vol. 69, no. 10, pp. 6561-6574, Oct 2021.

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
from scipy import stats

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

# Clayton Copula
def copula_clayton_dv(u, v, theta):
    """Derivative of C(u, v) wrt v. This corresponds to: Pr(U<u | V=v)"""
    return v**(-1-theta)*(u**(-theta)+v**(-theta)-1)**(-1-1/theta)

def inv_copula_clayton_dv(p, v, theta):
    if theta == -1:
        return 1.-v
    else:
        return (1-v**(-theta)+(v**(1+theta)*p)**(-theta/(1+theta)))**(-1/theta)

def clayton_samples(n, rv_x=stats.uniform, rv_y=stats.uniform, theta=.25, u=None):
    if theta == 0:
        _x = rv_x.rvs(size=n)
        _y = rv_y.rvs(size=n)
    else:
        if u is None:
            u = np.random.rand(n)
        u2 = np.random.rand(n)
        uk1 = inv_copula_clayton_dv(u2, u, theta)
        _y = rv_y.ppf(uk1)
        _x = rv_x.ppf(u)
    return (_x, _y)
