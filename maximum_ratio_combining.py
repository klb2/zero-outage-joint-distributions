"""Computations of the ZOC for dependent fading links and MRC at the receiver.

This module contains different functions to calculate the ZOC for dependent
fading channels, when maximum ratio combining (MRC) is employed at the
receiver.


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
from scipy import optimize
from scipy import integrate
from scipy import stats

from utils import export_results, pairwise

def _is_distribution(dist):
    if hasattr(dist, 'dist'):
        return isinstance(dist.dist, stats.rv_continuous)
    else:
        return isinstance(dist, stats.rv_continuous)

def max_zoc_outer_bound_mrc_homog(qf, n=2):
    if _is_distribution(qf):
        qf = qf.ppf
    return np.log2(1 + n*qf(1-1/n))

def max_zoc_outer_bound_joint_mix_mrc_homog(mean, n=2):
    if _is_distribution(mean):
        mean = mean.mean()
    return np.log2(1 + n*mean)

def max_zoc_inner_bound_mrc_homog(qf, n=2):
    if _is_distribution(qf):
        qf = qf.ppf
    x_star = qf((1-1./n)**(n-1))
    return np.log2(1 + n*x_star)


def _opt_x(x, t, rv_x, rv_y):
    return rv_y.pdf(rv_y.ppf(t-rv_x.cdf(x)))-rv_x.pdf(x)

def _xopt_numerical(t, rv_x, rv_y):
    if t == 1:
        _interval_bounds = np.logspace(-8, rv_x.ppf(1-1e-8), num=60)
    else:
        _interval_bounds = np.logspace(-5, rv_x.ppf(t), num=50)
    _interval_bounds_fw = np.concatenate(([0], _interval_bounds))
    _interval_bounds_bw = np.flip(np.concatenate(([max(_interval_bounds)],
                                  max(_interval_bounds)-_interval_bounds)))
    _interval_bounds_lin = np.linspace(0, max(_interval_bounds))
    xopts = []
    for _interval_bounds in [_interval_bounds_fw, _interval_bounds_bw, _interval_bounds_lin]:
        for _low, _up in pairwise(_interval_bounds):
            try:
                xopts.append(optimize.root_scalar(_opt_x, args=(t, rv_x, rv_y),
                                                bracket=[_low-np.finfo(float).eps, _up+np.finfo(float).eps]))
            except Exception as e:
                continue
    return xopts

def boundary_b(x, t, rv_x, rv_y):
    return rv_y.ppf(t-rv_x.cdf(x))

@np.vectorize
def zoc_copula_t_mrc_heterog(t, rv_x, rv_y):
    if t == 0:
        return 0.
    #elif t == 1:
    #    return 1.
    xopts = _xopt_numerical(t, rv_x, rv_y)
    if xopts:
        opt_s = min([xopt.root + boundary_b(xopt.root, t, rv_x, rv_y)
                     for xopt in xopts if xopt.converged])
    else:
        opt_s = np.inf
    #print(opt_s)
    #print(np.min([opt_s, rv_x.ppf(t), rv_y.ppf(t)]))
    return np.log2(1 + np.min([opt_s, rv_x.ppf(t), rv_y.ppf(t)]))




#### MAIN FUNCTIONS
def main(snr_db=10., m=5, plot=False, export=False):
    n = np.arange(2, 21, 1)
    snr = 10**(snr_db/10.)
    dist_exp = stats.expon(scale=snr)
    dist_naka = stats.gamma(a=m, scale=snr/m)
    print("Mode = {:.3f} < {:.3f} = median".format((m-1)/m*snr, dist_naka.median()))
    zoc_mrc_out_exp_w = max_zoc_outer_bound_mrc_homog(dist_exp.ppf, n)
    zoc_mrc_out_naka_w = max_zoc_outer_bound_mrc_homog(dist_naka.ppf, n)
    zoc_mrc_out_exp_jm = max_zoc_outer_bound_joint_mix_mrc_homog(dist_exp.mean(), n=n)
    zoc_mrc_out_naka_jm = max_zoc_outer_bound_joint_mix_mrc_homog(dist_naka.mean(), n=n)
    zoc_mrc_in_exp = max_zoc_inner_bound_mrc_homog(dist_exp.ppf, n)
    zoc_mrc_in_naka = max_zoc_inner_bound_mrc_homog(dist_naka.ppf, n)
    if export:
        export_results({"n": n, "zocExpOutW": zoc_mrc_out_exp_w,
                        "zocExpOutJM": zoc_mrc_out_exp_jm,
                        "zocExpIn": zoc_mrc_in_exp,
                        "zocNakaOutW": zoc_mrc_out_naka_w,
                        "zocNakaOutJM": zoc_mrc_out_naka_jm,
                        "zocNakaIn": zoc_mrc_in_naka},
                        "zoc-MRC-snr{}.dat".format(snr_db))
    if plot:
        fig, axs = plt.subplots()
        axs.plot(n, zoc_mrc_in_exp, 'r^-', label="Inner Bound -- Rayleigh Fading")
        axs.plot(n, zoc_mrc_out_exp_jm, 'ro-', label="Outer Bound (JM) -- Rayleigh Fading")
        axs.plot(n, zoc_mrc_out_exp_w, 'ro--', label="Outer Bound (W) -- Rayleigh Fading")
        axs.plot(n, zoc_mrc_in_naka, 'b^-', label="Inner Bound -- Nakagami-$m$ Fading")
        axs.plot(n, zoc_mrc_out_exp_jm, 'bo-', label="Outer Bound (JM) -- Nakagami-$m$ Fading")
        axs.plot(n, zoc_mrc_out_naka_w, 'bo--', label="Outer Bound (W) -- Nakagami-$m$ Fading")
        axs.set_xlabel("Number of Links $n$")
        axs.set_ylabel("Maximum Zero-Outage Capacity")
        axs.set_title("Bounds on the Maximum ZOC for Rayleigh Fading and Nakagami-$m$ Fading with MRC at the Receiver.\nSNR={:.3f} dB and $m={:d}$".format(snr_db, m))
        axs.legend()
        fig.tight_layout()
        fig.savefig("results-mrc-snr{}.png".format(snr_db), dpi=100)

if __name__ == "__main__":
    import argparse
    import matplotlib.pyplot as plt
    parser = argparse.ArgumentParser()
    parser.add_argument("--plot", action="store_true")
    parser.add_argument("--export", action="store_true")
    parser.add_argument("-s", "--snr_db", type=float, default=10)
    parser.add_argument("-m", type=int, default=5)
    args = vars(parser.parse_args())
    main(**args)
    plt.show()
    #rv2 = stats.lognorm(2)
    #print(max_zoc_sc_heterog([rv1.ppf, rv2.ppf]))
    #print(2**max_zoc_sc_heterog([stats.expon(scale=1).ppf,
    #                             stats.expon(scale=10**(-5/10)).ppf])-1)
