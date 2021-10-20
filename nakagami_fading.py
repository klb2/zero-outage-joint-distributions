"""Nakagami-m Fading Example

This module contains different functions to calculate the example of Nakagami-m
fading from the paper.


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

from maximum_ratio_combining import (zoc_copula_t_mrc_heterog,
        max_zoc_inner_bound_mrc_homog, max_zoc_outer_bound_joint_mix_mrc_homog,
        max_zoc_outer_bound_mrc_homog)
from utils import export_results

def main_two_links(m=5, snr_x_db=10., snr_y_db=10., plot=False, export=False,
                   **kwargs):
    snr_x = 10**(snr_x_db/10.)
    snr_y = 10**(snr_y_db/10.)
    t = np.linspace(0, 1, 150)
    rv_x = stats.gamma(a=m, scale=snr_x/m)
    rv_y = stats.gamma(a=m, scale=snr_y/m)
    zoc_mrc = zoc_copula_t_mrc_heterog(t, rv_x, rv_y)
    if plot:
        plt.plot(t, zoc_mrc, 'o-')
    if export:
        export_results({"t": t, "capac": zoc_mrc},
                       "zoc-x_naka{0}-y_naka{0}-snrx{1}-snry{2}.dat".format(m, snr_x_db, snr_y_db))

def main_n_links(m=5, snr_x_db=0., plot=False, export=False, **kwargs):
    n = np.arange(2, 21)
    snr = 10**(snr_x_db/10.)
    rv = stats.gamma(a=m, scale=snr/m)
    zoc_inner = max_zoc_inner_bound_mrc_homog(rv.ppf, n)
    zoc_outer_w = max_zoc_outer_bound_mrc_homog(rv.ppf, n)
    zoc_outer_jm = max_zoc_outer_bound_joint_mix_mrc_homog(rv.mean(), n)
    if plot:
        fig, axs = plt.subplots()
        axs.plot(n, zoc_inner, label="Inner Bound")
        axs.plot(n, zoc_outer_jm, label="Outer Bound JM")
        axs.plot(n, zoc_outer_w, label="Outer Bound W")
        axs.legend()
    if export:
        export_results({"n": n, "zocInner": zoc_inner, "zocOuterW": zoc_outer_w,
                        "zocOuterJM": zoc_outer_jm},
                       "zoc-mrc-naka{}-snr{}.dat".format(m, snr_x_db))


if __name__ == "__main__":
    import argparse
    import matplotlib.pyplot as plt
    parser = argparse.ArgumentParser()
    parser.add_argument("--plot", action="store_true")
    parser.add_argument("--export", action="store_true")
    parser.add_argument("-x", "--snr_x_db", type=float, default=0)
    parser.add_argument("-y", "--snr_y_db", type=float, default=0)
    parser.add_argument("-m", type=int, default=5)
    parser.add_argument("--n-links", action="store_true")
    args = vars(parser.parse_args())
    n_links = args.pop("n_links")
    if n_links:
        main_n_links(**args)
    else:
        main_two_links(**args)
    plt.show()
