import numpy as np
import time
from src import process
from helper import plot_me_3times

# Initial conditions and model parameters
tps = 1.e3
x_sh_test = 1.0
gamma_eff = 1.1
etaprime = 1.e-2
Mdot_stable = -999
dt = 50
max_tps = 3.e3
Minfall = 6.1341e-5  # Retained as a model parameter; not currently passed to process.

# Add or modify entries here to run additional parameter cases.
simulations = {
    "fiducial": {
        "time": [],
        "Mdisk": [],
        "Ewind": [],
        "alpha": 0.5,
        "etaprime": etaprime,
        "gamma": gamma_eff,
        "lambda": 0.1,
        "func": "process",
    },
    # 'eta2': {'tps': [], 'Mdisk': [], 'Ewind': [], 'alpha': 0.5, 'etaprime': 0.001, 'gamma': 1.1, 'lambda': 0.1, 'func': 'process'},
    # 'eta3': {'tps': [], 'Mdisk': [], 'Ewind': [], 'alpha': 0.5, 'etaprime': 0.0001, 'gamma': 1.1, 'lambda': 0.1, 'func': 'process'}
}

def run_simulation(result_key):
    """Run one parameter case and return its profiles at each time step."""
    ii = 1
    disk_props = {}
    curr_tps = tps

    config = simulations[result_key]
    config["time"] = []
    config["Mdisk"] = []
    config["Ewind"] = []

    alpha_0 = config["alpha"]
    case_etaprime = config["etaprime"]
    case_gamma_eff = config["gamma"]
    lambda0 = config["lambda"]

    print(
        f"\nRunning simulation for {result_key} "
        f"(alpha={alpha_0}, func={config['func']})"
    )
    start_time = time.perf_counter()

    while curr_tps <= max_tps:
        profile_key = f"pf{ii}"
        disk_props[profile_key] = process.process(
            curr_tps,
            x_sh_test,
            case_gamma_eff,
            alpha_0,
            case_etaprime,
            Mdot_stable,
            lambda0,
        )
        curr_disk_props = disk_props[profile_key]

        # The solver stores disk mass and wind energy in rows 6 and 7.
        config["time"].append(curr_tps)
        config["Mdisk"].append(curr_disk_props[6, -1])
        config["Ewind"].append(curr_disk_props[7, -1])

        print(
            f"ii = {ii}, time = {curr_tps}, "
            f"Mdisk = {config['Mdisk'][-1]}"
        )
        ii += 1
        curr_tps += dt

    print(f"Time elapsed: {time.perf_counter() - start_time:.2f} seconds")

    return disk_props


def main():
    """Run all configured cases and return their profiles."""
    model_output = {}

    for key in simulations:
        model_output[key] = run_simulation(key)
        for output_name in ("time", "Mdisk", "Ewind"):
            simulations[key][output_name] = np.asarray(
                simulations[key][output_name]
            )

    return model_output


if __name__ == "__main__":
    model_output = main()

    # The profile keys run from pf1 (1000 yr) through pf41 (3000 yr) [Increment by 50 years].
    plot_mat_1 = model_output["fiducial"]["pf1"]
    # plot_mat_2 = dict['eta2nw']['pf1']
    # plot_mat_3 = dict['pre_eta2']['pf1']
    # plot_mat_4 = dict['pre_eta2nw']['pf1']

    # In case you want to plot the cases
    # plot_me_3times.plotme3times(plot_mat_1, plot_mat_2, plot_mat_3, plot_mat_4)
