import numpy as np
import time
import process
import plot_me_3times

# Constants and initial parameters
tps = 1.e3
x_sh_test = 1.0
gamma_eff = 1.1
etaprime = 1.e-2
Mdot_stable = -999
dt = 50  # time increment [yr]
Minfall = 6.1341e-5  # 1.4086e-5 | 2.8509e-5 | 6.1341e-5

# Initialize storage dictionaries
results = {
    'post_eta2': {'tps': [], 'Mdisk': [], 'Ewind': [], 'alpha': 0.5, 'func': 'process'},
    'post_eta2nw': {'tps': [], 'Mdisk': [], 'Ewind': [], 'alpha': 0.5, 'func': 'processnw'},
    'eta2': {'tps': [], 'Mdisk': [], 'Ewind': [], 'alpha': 0.5, 'func': 'process'},
    'eta2nw': {'tps': [], 'Mdisk': [], 'Ewind': [], 'alpha': 0.5, 'func': 'processnw'},
    'pre_eta2': {'tps': [], 'Mdisk': [], 'Ewind': [], 'alpha': 0.5, 'func': 'process'},
    'pre_eta2nw': {'tps': [], 'Mdisk': [], 'Ewind': [], 'alpha': 0.5, 'func': 'processnw'}
}

def run_simulation(result_key):
    """Run simulation for a given configuration"""
    tps = 1.e3
    ii = 1
    pf_dict = {}
    
    config = results[result_key]
    alpha_0 = config['alpha']
    # process_func = globals()[config['func']]  # Get the function by name
    
    print(f"\nRunning simulation for {result_key} (alpha={alpha_0}, func={config['func']})")
    start_time = time.time()
    
    while tps <= 3.e3:
        # Store each pf result in a dictionary
        pf_dict[f'pf{ii}_{result_key}'] = process.process(tps, x_sh_test, gamma_eff, alpha_0, etaprime, Mdot_stable)
        pf = pf_dict[f'pf{ii}_{result_key}']
        
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
    if key == 'eta2':
        dict = run_simulation(key)


# Convert lists to numpy arrays for easier handling
for key in results.keys():
    results[key]['tps'] = np.array(results[key]['tps'])
    results[key]['Mdisk'] = np.array(results[key]['Mdisk'])
    results[key]['Ewind'] = np.array(results[key]['Ewind'])

plot_mat_1 = dict['pf1_eta2']
plot_mat_2 = dict['pf21_eta2']
plot_mat_3 = dict['pf41_eta2']

plot_me_3times.plotme3times(plot_mat_1, plot_mat_2, plot_mat_3)


# Access results like this:
# post_eta2_tps = results['post_eta2']['tps']
# post_eta2_Mdisk = results['post_eta2']['Mdisk']
# etc.