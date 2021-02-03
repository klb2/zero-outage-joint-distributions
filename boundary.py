"""Illustration of the ZOC for dependent fading channels.

This module contains a illustration of the ZOC for dependent fading channels.
It shows the boundary of the support and the different areas relevant for SC
and MRC.


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

import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

from utils import export_results
from rayleigh_fading import _boundary_b, zoc_copula_t_mrc_heterog_rayleigh
from selection_combining import max_zoc_sc_heterog

def main(snr_x_db, snr_y_db, plot=False, export=False):
    snr_x = 10**(snr_x_db/10.)
    snr_y = 10**(snr_y_db/10.)
    lam_x = 1./(snr_x)
    lam_y = 1./snr_y
    rv_x = stats.expon(scale=snr_x)
    rv_y = stats.expon(scale=snr_y)
    x = np.linspace(0, 3, 100)
    b = _boundary_b(x, 1, lam_x, lam_y)
    mrc = zoc_copula_t_mrc_heterog_rayleigh(1, lam_x, lam_y)
    s_mrc = 2**mrc - 1
    sc = max_zoc_sc_heterog([rv_x.ppf, rv_y.ppf])
    s_sc = 2**sc - 1
    print("s_mrc: {:.3f}".format(s_mrc))
    print("s_sc: {:.3f}".format(s_sc))
    if export:
        export_results({"x": x, "boundary": b}, "boundary-example.dat")
    if plot:
        fig, axs = plt.subplots()
        axs.fill_between(x, b, label="Boundary B", alpha=.5)#, ec=(1, 0, 0, 1))
        axs.fill_between([0, s_mrc], [s_mrc, 0], label="S MRC", alpha=.5)
        axs.fill_between([0, s_sc, s_sc], [s_sc, s_sc, 0], label="S SC", alpha=.5)
        axs.set_xlabel("x")
        axs.set_ylabel("y")
        axs.legend()
        fig.tight_layout()


if __name__ == "__main__":
    import argparse
    import matplotlib.pyplot as plt
    parser = argparse.ArgumentParser()
    parser.add_argument("--plot", action="store_true")
    parser.add_argument("--export", action="store_true")
    parser.add_argument("-x", "--snr_x_db", type=float, default=8.)
    parser.add_argument("-y", "--snr_y_db", type=float, default=0.)
    args = vars(parser.parse_args())
    main(**args)
    plt.show()
