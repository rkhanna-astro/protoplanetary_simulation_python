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
results = {
    'post_eta2': {'tps': [], 'Mdisk': [], 'Ewind': [], 'alpha': 0.1, 'etaprime': 0.01, 'gamma': 1.1, 'lambda': 0.1, 'func': 'process'},
    'post_eta2nw': {'tps': [], 'Mdisk': [], 'Ewind': [], 'alpha': 0.2, 'etaprime': 0.01, 'gamma': 1.1, 'lambda': 0.1, 'func': 'process'},
    'eta2': {'tps': [], 'Mdisk': [], 'Ewind': [], 'alpha': 0.3, 'etaprime': 0.01, 'gamma': 1.1, 'lambda': 0.1, 'func': 'process'},
    'eta2nw': {'tps': [], 'Mdisk': [], 'Ewind': [], 'alpha': 0.5, 'etaprime': 0.01, 'gamma': 1.1, 'lambda': 0.1, 'func': 'process'},
    'pre_eta2': {'tps': [], 'Mdisk': [], 'Ewind': [], 'alpha': 0.8, 'etaprime': 0.01, 'gamma': 1.1, 'lambda': 0.1, 'func': 'process'},
    'pre_eta2nw': {'tps': [], 'Mdisk': [], 'Ewind': [], 'alpha': 1.0, 'etaprime': 0.01, 'gamma': 1.1, 'lambda': 0.1, 'func': 'process'}
}

def run_simulation(result_key):
    """Run simulation for a given configuration"""
    tps = 1.e2
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
Menv_a1eta2, MdMenv_a1eta2 = [], []
Menv_a2eta2, MdMenv_a2eta2 = [], []
Menv_a3eta2, MdMenv_a3eta2 = [], []
Menv_a4eta2, MdMenv_a4eta2 = [], []
Menv_a5eta2, MdMenv_a5eta2 = [], []
Menv_a6eta2, MdMenv_a6eta2 = [], []

turn = 1
for key in results.keys():
    dict[key] = run_simulation(key)

    for ii in range(1, 41):
        mdisk_menv = dict[key][f'pf{ii}'][9][-1]
        menvs = dict[key][f'pf{ii}'][14][-1]
        if turn == 1:
            Menv_a1eta2.append(menvs)
            MdMenv_a1eta2.append(mdisk_menv)
        
        if turn == 2:
            Menv_a2eta2.append(menvs)
            MdMenv_a2eta2.append(mdisk_menv)
        
        if turn == 3:
            Menv_a3eta2.append(menvs)
            MdMenv_a3eta2.append(mdisk_menv)
        
        if turn == 4:
            Menv_a4eta2.append(menvs)
            MdMenv_a4eta2.append(mdisk_menv)
        
        if turn == 5:
            Menv_a5eta2.append(menvs)
            MdMenv_a5eta2.append(mdisk_menv)

        if turn == 6:
            Menv_a6eta2.append(menvs)
            MdMenv_a6eta2.append(mdisk_menv)
    
    turn += 1

# print(Menv_a2eta2)
# print(MdMenv_a2eta2)

menv.menv(Menv_a1eta2, MdMenv_a1eta2, Menv_a2eta2, MdMenv_a2eta2, 
          Menv_a3eta2, MdMenv_a3eta2, Menv_a4eta2, MdMenv_a4eta2, 
          Menv_a5eta2, MdMenv_a5eta2, Menv_a6eta2, MdMenv_a6eta2)

# Convert lists to numpy arrays for easier handling
for key in results.keys():
    results[key]['tps'] = np.array(results[key]['tps'])
    results[key]['Mdisk'] = np.array(results[key]['Mdisk'])
    results[key]['Ewind'] = np.array(results[key]['Ewind'])

# Access results like this:
# post_eta2_tps = results['post_eta2']['tps']
# post_eta2_Mdisk = results['post_eta2']['Mdisk']
# etc.