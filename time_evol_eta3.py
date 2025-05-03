import numpy as np
import time
from typing import Dict, Tuple
import process as process
import process_nw as processnw
import plot_me_3times

def run_simulation(
    process_func, 
    alpha_0: float, 
    etaprime: float,
    gamma_eff: float,
    tps_start: float = 1.e3, 
    tps_end: float = 3.e3, 
    dt: float = 50
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Run a simulation with given parameters and return results."""
    tps_values = []
    mdisk_values = []
    ewind_values = []
    pf_storage = {}
    
    tps = tps_start
    ii = 1
    
    while tps <= tps_end:
        pf = process_func(tps, x_sh_test, gamma_eff, alpha_0, etaprime, Mdot_stable)
        
        pf_storage[f'pf{ii}'] = pf
        tps_values.append(tps)
        mdisk_values.append(pf[6, -1])  # Assuming pf is a numpy array
        ewind_values.append(pf[7, -1])
        
        print(f'ii = {ii}, tps = {tps}, Mdisk = {mdisk_values[-1]}, Ew = {ewind_values[-1]}')
        
        tps += dt
        ii += 1
    
    return np.array(tps_values), np.array(mdisk_values), np.array(ewind_values), pf_storage

# Constants
x_sh_test = 1.0
gamma_eff = 1.1
etaprime = 1.e-2
alpha = 0.5
Mdot_stable = -999
dt = 50  # time increment [yr]
Minfall = 6.1341e-5

# Define all simulation configurations
sim_configs = {
    'post_eta3': { 'gamma': 1.0,'func': process.process},
    'post_eta3nw': { 'gamma': 1.0, 'func': processnw.process},
    'eta3': { 'gamma': 1.05, 'func': process.process},
    'eta3nw': { 'gamma': 1.05, 'func': processnw.process},
    'pre_eta3': { 'gamma': 1.1, 'func': process.process},
    'pre_eta3nw': { 'gamma': 1.1, 'func': processnw.process}
}

# Run all simulations and store results
results = {}
for name, config in sim_configs.items():
    print(f"\nRunning {name} with gamma={config['gamma']}")
    start_time = time.time()
    
    tps_arr, mdisk, ewind, properties = run_simulation(
        process_func=config['func'],
        alpha_0=alpha,
        etaprime=etaprime,
        gamma_eff=config['gamma']
    )
    
    results[name] = {
        'tps': tps_arr,
        'Mdisk': mdisk,
        'Ewind': ewind,
        'time_elapsed': time.time() - start_time,
        'properties': properties
    }
    print(f"Completed {name} in {results[name]['time_elapsed']:.2f} seconds")

plot_mat_1 = results['post_eta3']['properties']['pf1']
plot_mat_2 = results['eta3']['properties']['pf1']
plot_mat_3 = results['pre_eta3']['properties']['pf1']

plot_me_3times.plotme3times(plot_mat_1, plot_mat_2, plot_mat_3)

# Access results like:
# post_eta3_tps = results['post_eta3']['tps']
# post_eta3_Mdisk = results['post_eta3']['Mdisk']
# etc.
