"""Rayleigh Fading Example

This module contains different functions to calculate the example of Rayleigh
fading from the paper.


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
from scipy import stats
from scipy import integrate

from utils import export_results


def zoc_copula_t_mrc_heterog_rayleigh(t, lam_x, lam_y):
    _xstar = _xopt(t, lam_x, lam_y)
    _opt_s = _xstar + _boundary_b(_xstar, t, lam_x, lam_y)
    return np.log2(1+_opt_s)

def _boundary_b(x, t, lam_x, lam_y):
    return -np.log(2-t-np.exp(-lam_x*x))/lam_y

def _xopt(t, lam_x, lam_y):
    rv_x = stats.expon(scale=1/lam_x)
    inv_cdf_x = rv_x.ppf(t)
    _part2 = -np.log(((2-t)*lam_y)/(lam_x+lam_y))/lam_x
    _min = np.minimum(inv_cdf_x, _part2)
    return np.maximum(_min, 0)

#def expected_zoc_uniform(t_min, t_max, lam_x, lam_y):
#    integral = integrate.quad(zero_outage_capacity, t_min, t_max,
#                              args=(lam_x, lam_y))
#    expected_val = integral[0]/(t_max-t_min)
#    return expected_val


###### PLOTS and EXPORTS ###########

def export_loose_bound(snr_db):
    n = np.arange(2, 11)
    snr = 10**(snr_db/10.)
    lam = 1/snr
    capac_outer = outer_bound_symmetric(n, lam)
    capac_inner = inner_bound_symmetric(n, lam)
    results = {"n": n, "outer": capac_outer, "inner": capac_inner}
    filename = "rayleigh-max-zoc-loose-snr{}.dat".format(snr_db)
    export_results(results, filename)

def zero_outage_snr_grid(t=.5, alpha_x=1, alpha_y=1, export=True):
    snr_db = np.linspace(-10, 10, 50)
    SNR_X_DB, SNR_Y_DB = np.meshgrid(snr_db, snr_db)
    SNR_X = 10**(SNR_X_DB/10.)
    SNR_Y = 10**(SNR_Y_DB/10.)
    LX = 1/(SNR_X*alpha_x)
    LY = 1/(SNR_Y*alpha_y)
    capac = zoc_copula_t_mrc_heterog_rayleigh(t, LX, LY)
    if export:
        filename = "grid-zero-out-snr-t{}.dat".format(t)
        results = {"snrx": SNR_X_DB.ravel(), "snry": SNR_Y_DB.ravel(),
                   "capac": capac.ravel()}
        export_results(results, filename)
    return SNR_X_DB, SNR_Y_DB, capac

def main(snr_x_db, snr_y_db, alpha_x=1, alpha_y=1, plot=False, export=True):
    key_results = "zocX{}Y{}"
    snr_x_db = np.array(snr_x_db)
    snr_y_db = np.array(snr_y_db)
    snr_x = 10**(snr_x_db/10.)
    snr_y = 10**(snr_y_db/10.)
    lam_x = 1./(snr_x*alpha_x)
    lam_y = 1./(snr_y*alpha_y)
    t = np.linspace(0, 1)
    results = {}
    for _snr_x, _snr_y, _lam_x, _lam_y in zip(snr_x_db, snr_y_db, lam_x, lam_y):
        zero_out = zoc_copula_t_mrc_heterog_rayleigh(t, _lam_x, _lam_y)
        results[key_results.format(_snr_x, _snr_y)] = zero_out
    #expected = expected_zoc_uniform(0.8, 1, lam_x, lam_y)

    SNR_X_DB, SNR_Y_DB, CAPAC_GRID = zero_outage_snr_grid(t=.5, export=export)
    if export:
        #filename = "zero-out-capac-rayleigh-lx{}-ly{}.dat".format(lam_x, lam_y)
        #filename = "zero-out-capac-rayleigh-ax{}-ay{}-snrx{}-snry{}.dat".format(alpha_x, alpha_y, snr_x_db, snr_y_db)
        filename = "zoc-rayleigh-copula-t.dat"
        results.update({"t": t})
        export_results(results, filename)
    if plot:
        fig, axs = plt.subplots()
        for _snr_x, _snr_y in zip(snr_x_db, snr_y_db):
            zero_out = results[key_results.format(_snr_x, _snr_y)]
            axs.plot(t, zero_out, label="SNR_x={:.3f} - SNR_y={:.3f}".format(_snr_x, _snr_y))
        axs.legend()
        axs.set_xlabel("Copula Parameter t")
        axs.set_ylabel("Zero-Outage Capacity")
        axs.set_title("Zero-Outage Capacity for Rayleigh Fading and MRC")
        fig.tight_layout()
        fig.savefig("results-zoc-rayleigh-copula-t.png", dpi=100)
        fig2, axs2 = plt.subplots()
        axs2.pcolormesh(SNR_X_DB, SNR_Y_DB, CAPAC_GRID, vmin=0, alpha=.5, shading="auto")
        _contour = axs2.contour(SNR_X_DB, SNR_Y_DB, CAPAC_GRID, vmin=0)
        axs2.clabel(_contour, inline=1, fontsize=9)
        axs2.set_xlabel("SNR_x [dB]")
        axs2.set_ylabel("SNR_y [dB]")
        axs2.set_title("Zero-Outage Capacity for Rayleigh Fading and MRC\nt={:.3f}".format(.5))
        fig2.tight_layout()
        fig2.savefig("results-zoc-grid-rayleigh-copula-t{}.png".format(0.5), dpi=100)
        plt.show()


if __name__ == "__main__":
    import argparse
    import matplotlib.pyplot as plt
    parser = argparse.ArgumentParser()
    parser.add_argument("--plot", action="store_true")
    parser.add_argument("--export", action="store_true")
    parser.add_argument("-x", "--snr_x_db", type=float, default=[0, 5], nargs="+")
    parser.add_argument("-y", "--snr_y_db", type=float, default=[0, 5], nargs="+")
    parser.add_argument("-ax", "--alpha_x", type=float, default=1)
    parser.add_argument("-ay", "--alpha_y", type=float, default=1)
    args = vars(parser.parse_args())
    main(**args)
