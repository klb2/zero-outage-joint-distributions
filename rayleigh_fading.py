import numpy as np
from scipy import stats
from scipy import integrate


def zero_outage_capacity(t, lam_x, lam_y):
    _xstar = xopt(t, lam_x, lam_y)
    _opt_s = _xstar + boundary_b(_xstar, t, lam_x, lam_y)
    return np.log2(1+_opt_s)

def boundary_b(x, t, lam_x, lam_y):
    return -np.log(2-t-np.exp(-lam_x*x))/lam_y

def xopt(t, lam_x, lam_y):
    rv_x = stats.expon(scale=1/lam_x)
    inv_cdf_x = rv_x.ppf(t)
    _part2 = -np.log(((2-t)*lam_y)/(lam_x+lam_y))/lam_x
    _min = np.minimum(inv_cdf_x, _part2)
    return np.maximum(_min, 0)

def expected_zoc_uniform(t_min, t_max, lam_x, lam_y):
    integral = integrate.quad(zero_outage_capacity, t_min, t_max,
                              args=(lam_x, lam_y))
    expected_val = integral[0]/(t_max-t_min)
    return expected_val


###### PLOTS and EXPORTS ###########

def export_results(data, filename):
    import pandas as pd
    data = pd.DataFrame.from_dict(data)
    data.to_csv(filename, sep='\t', index=False)

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
    capac = zero_outage_capacity(t, LX, LY)
    if export:
        filename = "grid-zero-out-snr-t{}.dat".format(t)
        results = {"snrx": SNR_X_DB.ravel(), "snry": SNR_Y_DB.ravel(),
                   "capac": capac.ravel()}
        export_results(results, filename)

def main(snr_x_db, snr_y_db, alpha_x=1, alpha_y=1, plot=False, export=True):
    snr_x = 10**(snr_x_db/10.)
    snr_y = 10**(snr_y_db/10.)
    lam_x = 1./(snr_x*alpha_x)
    lam_y = 1./(snr_y*alpha_y)
    t = np.linspace(0, 1)
    zero_out = zero_outage_capacity(t, lam_x, lam_y)
    print(zero_out)
    expected = expected_zoc_uniform(0.8, 1, lam_x, lam_y)
    print(expected)
    if export:
        #filename = "zero-out-capac-rayleigh-lx{}-ly{}.dat".format(lam_x, lam_y)
        filename = "zero-out-capac-rayleigh-ax{}-ay{}-snrx{}-snry{}.dat".format(alpha_x, alpha_y, snr_x_db, snr_y_db)
        results = {"t": t, "capac": zero_out}
        export_results(results, filename)
    if plot:
        plt.plot(t, zero_out)
        plt.plot([0, 1], [np.log2(1 + 2*np.log(2))]*2)
        #plt.plot([0, 1], [np.log2(1 + np.log(2))]*2)
        plt.show()


if __name__ == "__main__":
    import argparse
    import matplotlib.pyplot as plt
    parser = argparse.ArgumentParser()
    parser.add_argument("--plot", action="store_true")
    parser.add_argument("--export", action="store_true")
    parser.add_argument("-x", "--snr_x_db", type=float, default=0)
    parser.add_argument("-y", "--snr_y_db", type=float, default=0)
    parser.add_argument("-ax", "--alpha_x", type=float, default=1)
    parser.add_argument("-ay", "--alpha_y", type=float, default=1)
    args = vars(parser.parse_args())
    main(**args)
    #zero_outage_snr_grid()
