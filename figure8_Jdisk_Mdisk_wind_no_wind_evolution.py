import numpy as np
import time
import process
import process_nw as processnw
import plot_me_3times
# import jspec_etavar_g
import jspec_c

# Constants and initial parameters
time_evolution = []
tps = 50
while tps <= 1000:
    time_evolution.append(tps)
    tps += 50

x_sh_test = 1.0
gamma_eff = 1.1
etaprime = 1.e-2
Mdot_stable = -999
dt = 50  # time increment [yr]
Minfall = 6.1341e-5  # 1.4086e-5 | 2.8509e-5 | 6.1341e-5
rmid = 5000

AU_TO_M = 1.49597870691e11  # Astronomical unit to meters
SOLAR_MASS = 1.989e30       # Solar mass in kg
CONVERSION_FACTOR = 10 * (AU_TO_M**2) / SOLAR_MASS
J_CONVERSION_FACTOR = 1000 * 10 * (AU_TO_M**3) / SOLAR_MASS

# Initialize storage dictionaries
results = {
    # 'post_eta2': {'tps': [], 'Mdisk': [], 'Ewind': [], 'alpha': 0.1, 'func': 'process'},
    # 'post_eta2nw': {'tps': [], 'Mdisk': [], 'Ewind': [], 'alpha': 0.2, 'func': 'process'},
    'eta2': {'tps': [], 'Mdisk': [], 'Ewind': [], 'alpha': 0.3, 'etaprime': 0.01, 'gamma': 1.1, 'lambda': 0.1, 'func': process.process},
    'eta2nw': {'tps': [], 'Mdisk': [], 'Ewind': [], 'alpha': 0.3, 'etaprime': 0.01, 'gamma': 1.1, 'lambda': 0.0, 'func': processnw.process},
    # 'pre_eta2': {'tps': [], 'Mdisk': [], 'Ewind': [], 'alpha': 0.3, 'etaprime': 0.001, 'gamma': 1.1, 'lambda': 0.1, 'func': 'process'},
    'eta3': {'tps': [], 'Mdisk': [], 'Ewind': [], 'alpha': 0.5, 'etaprime': 0.01, 'gamma': 1.1, 'lambda': 0.1, 'func': process.process},
    'eta3nw': {'tps': [], 'Mdisk': [], 'Ewind': [], 'alpha': 0.5, 'etaprime': 0.01, 'gamma': 1.1, 'lambda': 0.0, 'func': processnw.process},
    # 'pre_eta3': {'tps': [], 'Mdisk': [], 'Ewind': [], 'alpha': 0.5, 'etaprime': 0.001, 'gamma': 1.1, 'lambda': 0.1, 'func': 'process'},
    'eta4': {'tps': [], 'Mdisk': [], 'Ewind': [], 'alpha': 0.8, 'etaprime': 0.01, 'gamma': 1.1, 'lambda': 0.1, 'func': process.process},
    'eta4nw': {'tps': [], 'Mdisk': [], 'Ewind': [], 'alpha': 0.8, 'etaprime': 0.01, 'gamma': 1.1, 'lambda': 0.0, 'func': processnw.process},
    # 'pre_eta4': {'tps': [], 'Mdisk': [], 'Ewind': [], 'alpha': 0.8, 'etaprime': 0.001, 'gamma': 1.1, 'lambda': 0.1, 'func': 'process'},
}


def run_simulation(result_key):
    """Run simulation for a given configuration"""
    tps = 50
    ii = 1
    pf_dict = {}
    
    config = results[result_key]
    process_func = config['func']
    alpha_0 = config['alpha']
    etaprime = config['etaprime']
    gamma_eff = config['gamma']
    lambda0 = config['lambda']
    # process_func = globals()[config['func']]  # Get the function by name
    
    print(f"\nRunning simulation for {result_key} (alpha={alpha_0}, func={config['func']})")
    start_time = time.time()
    
    while tps <= 1000:
        # Store each pf result in a dictionary
        pf_dict[f'pf{ii}_{alpha_0}_{etaprime}'] = process_func(tps, x_sh_test, gamma_eff, alpha_0, etaprime, Mdot_stable)
        pf = pf_dict[f'pf{ii}_{alpha_0}_{etaprime}']
        
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
# J_tot_pre_eta1, M_tot_pre_eta1, J_tot_eta1, M_tot_eta1, J_tot_post_eta1, M_tot_post_eta1 = [], [], [], [], [], []
# J_tot_pre_eta2, M_tot_pre_eta2, J_tot_eta2, M_tot_eta2, J_tot_post_eta2, M_tot_post_eta2 = [], [], [], [], [], []
# J_tot_pre_eta3, M_tot_pre_eta3, J_tot_eta3, M_tot_eta3, J_tot_post_eta3, M_tot_post_eta3 = [], [], [], [], [], []

J_tot_pre_eta2, M_tot_pre_eta2, J_tot_eta2, M_tot_eta2, J_tot_post_eta2, M_tot_post_eta2 = [], [], [], [], [], []
J_tot_pre_eta2nw, M_tot_pre_eta2nw, J_tot_eta2nw, M_tot_eta2nw, J_tot_post_eta2nw, M_tot_post_eta2nw = [], [], [], [], [], []

for key in results.keys():
    dict[key] = run_simulation(key)
    alpha = results[key]['alpha']
    etaprime = results[key]['etaprime']

    for ii in range(1, 21):
        pf_case = dict[key][f'pf{ii}_{alpha}_{etaprime}']

        minr = pf_case[0][0]
        rT = pf_case[0]
        ind0 = np.where((rT >= minr) & (rT <= rmid))[0]

        r = pf_case[0][ind0]
        v_phi = pf_case[1][ind0] * pf_case[2][ind0]
        sigma = pf_case[4][ind0]
            
        # Calculate dr (spacing between radial points)
        fresh_ind = np.arange(len(r))
        r_extended = np.append(r, r[-1] + (r[-1] - r[-2]))
        dr = r_extended[fresh_ind + 1] - r_extended[fresh_ind]
        
        # Calculate total mass and angular momentum
        M_tot = 2 * np.pi * np.sum(r * sigma * dr)

        print("Time", ii)
        print("Radius", r)
        print("Sigma", sigma)
        print("dr", dr)

        M_tot = M_tot * CONVERSION_FACTOR
        J_tot = 2 * np.pi * np.sum((r**2) * v_phi * sigma * dr) * J_CONVERSION_FACTOR
        # print("dr", dr)

        if alpha == 0.3 and "nw" not in key:
            J_tot_pre_eta2.append(J_tot)
            M_tot_pre_eta2.append(M_tot)
        
        if alpha == 0.3 and "nw" in key:
            J_tot_pre_eta2nw.append(J_tot)
            M_tot_pre_eta2nw.append(M_tot)

            # if len(J_tot_pre_eta3) > 1:
            #     a = J_tot_pre_eta3[-1]/M_tot_pre_eta3[-1]
            #     b = J_tot_pre_eta3[-2]/M_tot_pre_eta3[-2]
            #     check_array.append(a/b)
        
        if alpha == 0.5 and "nw" not in key:
            J_tot_eta2.append(J_tot)
            M_tot_eta2.append(M_tot)
        
        if alpha == 0.5 and "nw" in key:
            J_tot_eta2nw.append(J_tot)
            M_tot_eta2nw.append(M_tot)
        
        if alpha == 0.8 and "nw" not in key:
            J_tot_post_eta2.append(J_tot)
            M_tot_post_eta2.append(M_tot)
        
        if alpha == 0.8 and "nw" in key:
            J_tot_post_eta2nw.append(J_tot)
            M_tot_post_eta2nw.append(M_tot)

jspec_c.jspec(time_evolution, time_evolution, np.array(J_tot_pre_eta2), np.array(M_tot_pre_eta2), np.array(J_tot_eta2), np.array(M_tot_eta2), 
              np.array(J_tot_post_eta2), np.array(M_tot_post_eta2), np.array(J_tot_pre_eta2nw), np.array(M_tot_pre_eta2nw), np.array(J_tot_eta2nw), np.array(M_tot_eta2nw), np.array(J_tot_post_eta2nw), np.array(M_tot_post_eta2nw))
    

# for key in results.keys():
#     results[key]['tps'] = np.array(results[key]['tps'])
#     results[key]['Mdisk'] = np.array(results[key]['Mdisk'])
#     results[key]['Ewind'] = np.array(results[key]['Ewind'])

# print(check_array)
# Access results like this:
# post_eta2_tps = results['post_eta2']['tps']
# post_eta2_Mdisk = results['post_eta2']['Mdisk']
# etc.