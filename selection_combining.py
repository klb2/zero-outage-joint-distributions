"""Computations of the maximum ZOC for dependent fading links and SC at the
receiver.

This module contains different functions to calculate the maximum ZOC for
dependent fading channels, when selection combining (SC) is employed at the
receiver.


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
from scipy import optimize

from utils import export_results


def max_zoc_sc_homog(qf, n=2):
    return np.log2(1 + qf(1-1/n))

def max_zoc_sc_heterog(qf_list):
    if len(qf_list) != 2:
        raise NotImplementedError("Right now, only n=2 is supported")
    p_star = _calc_p_star(*qf_list)
    print(p_star)
    return np.log2(1 + qf_list[0](p_star))

def _condition_p_star(p, qf1, qf2):
    return qf1(p) - qf2(1.-p)

def _calc_p_star(qf1, qf2):
    _p_star = optimize.root_scalar(_condition_p_star, args=(qf1, qf2),
                                   bracket=[0, 1])
    return _p_star.root


def main(m=5, snr_db=10., plot=False, export=False):
    key_naka = "zocNaka{:d}"
    n = np.arange(2, 21, 1)
    snr = 10**(snr_db/10.)
    dist1 = stats.expon(scale=snr)
    zoc_sc = max_zoc_sc_homog(dist1.ppf, n)
    results = {}
    for _m in m:
        dist2 = stats.gamma(a=_m, scale=snr/_m)
        zoc_sc_naka = max_zoc_sc_homog(dist2.ppf, n)
        results[key_naka.format(_m)] = zoc_sc_naka

    p = np.linspace(0, 1)
    _x = dist1.ppf(p)
    _y = dist2.ppf(1-p)
    _zoc = max_zoc_sc_heterog([dist1.ppf, dist2.ppf])
    _s_zoc = 2**_zoc - 1
    print(_s_zoc)
    print(_zoc)

    if export:
        results.update({"n": n, "zocExp": zoc_sc})
        export_results(results, "zoc-SC-snr{}-naka.dat".format(snr_db))
        export_results({"x": _x, "y": _y}, "zoc-sc-rayleigh-naka{}-snr{}.dat".format(m[-1], snr_db))
    if plot:
        fig, axs = plt.subplots()
        axs.plot(n, zoc_sc, 'o-', label="Rayleigh Fading")
        for _m in m:
            axs.plot(n, results[key_naka.format(_m)], 'o-',
                     label="Nakagami-m Fading -- m={:d}".format(_m))
        axs.set_xlabel("Number of Links $n$")
        axs.set_ylabel("Maximum Zero-Outage Capacity")
        axs.set_title("Bounds on the Maximum ZOC for Rayleigh Fading and Nakagami-$m$ Fading with SC at the Receiver.\nSNR={:.3f} dB and $m={}$".format(snr_db, m))
        axs.legend()
        fig.tight_layout()
        fig.savefig("results-sc-snr{}.png".format(snr_db), dpi=100)
        
        fig2, axs2 = plt.subplots()
        axs2.plot(_x, _y)
        axs2.plot([0, _s_zoc, _s_zoc], [_s_zoc, _s_zoc, 0], 'r--')
        axs2.set_xlabel("X")
        axs2.set_ylabel("Y")

if __name__ == "__main__":
    from scipy import stats
    import argparse
    import matplotlib.pyplot as plt
    parser = argparse.ArgumentParser()
    parser.add_argument("--plot", action="store_true")
    parser.add_argument("--export", action="store_true")
    parser.add_argument("-s", "--snr_db", type=float, default=10)
    parser.add_argument("-m", type=int, default=[5], nargs="+")
    args = vars(parser.parse_args())
    main(**args)
    plt.show()
