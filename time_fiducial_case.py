import numpy as np
import time
import process
import plot_me_3times
import menv

# Constants and initial parameters
tps = 1.e3
x_sh_test = 1.0
gamma_eff = 1.1
etaprime = 1.e-2
Mdot_stable = -999
dt = 50  # time increment [yr]
Minfall = 6.1341e-5  # 1.4086e-5 | 2.8509e-5 | 6.1341e-5

# Initialize storage dictionaries
# Change this results dictionary if you want to run other cases
results = {
    'fiducial': {'tps': [], 'Mdisk': [], 'Ewind': [], 'alpha': 0.5, 'etaprime': 0.01, 'gamma': 1.1, 'lambda': 0.1, 'func': 'process'},
    # 'eta2': {'tps': [], 'Mdisk': [], 'Ewind': [], 'alpha': 0.5, 'etaprime': 0.001, 'gamma': 1.1, 'lambda': 0.1, 'func': 'process'},
    # 'eta3': {'tps': [], 'Mdisk': [], 'Ewind': [], 'alpha': 0.5, 'etaprime': 0.0001, 'gamma': 1.1, 'lambda': 0.1, 'func': 'process'}
}

def run_simulation(result_key):
    """Run simulation for a given configuration"""
    tps = 1.e3
    ii = 1
    pf_dict = {}
    
    config = results[result_key]
    alpha_0 = config['alpha']
    etaprime = config['etaprime']
    gamma_eff = config['gamma']
    lambda0 = config['lambda']
    # process_func = globals()[config['func']]  # Get the function by name
    
    print(f"\nRunning simulation for {result_key} (alpha={alpha_0}, func={config['func']})")
    start_time = time.time()
    
    while tps <= 3.e3:
        # Store each pf result in a dictionary
        pf_dict[f'pf{ii}'] = process.process(tps, x_sh_test, gamma_eff, alpha_0, etaprime, Mdot_stable, lambda0)
        pf = pf_dict[f'pf{ii}']
        
        # Append results
        config['tps'].append(tps)
        config['Mdisk'].append(pf[6,-1])
        config['Ewind'].append(pf[7,-1])
        
        print(f'ii = {ii}, tps = {tps}, Mdisk = {config["Mdisk"][-1]}, Ew = {config["Ewind"][-1]}')
        
        ii += 1
        tps += dt
    
    print(f"Time elapsed: {time.time() - start_time:.2f} seconds")

    return pf_dict

# Run all simulations
dict = {}

for key in results.keys():
    dict[key] = run_simulation(key)

# Convert lists to numpy arrays for easier handling
for key in results.keys():
    results[key]['tps'] = np.array(results[key]['tps'])
    results[key]['Mdisk'] = np.array(results[key]['Mdisk'])
    results[key]['Ewind'] = np.array(results[key]['Ewind'])

# This is how we access the time = 1000 Year data
# It will be go from 1 (1000 Year) to 41 (3000 Year)
plot_mat_1 = dict['fiducial']['pf1']


# plot_mat_2 = dict['eta2nw']['pf1']
# plot_mat_3 = dict['pre_eta2']['pf1']
# plot_mat_4 = dict['pre_eta2nw']['pf1']

# In case you want to plot the cases
# plot_me_3times.plotme3times(plot_mat_1, plot_mat_2, plot_mat_3, plot_mat_4)
