import numpy as np
import time
import process as process
import process_nw as processnw
import plot_me
import plot_me_3times

def run_simulation(process_func, alpha_0, etaprime, cases):
    # Initialize parameters
    tps = 1.0e3
    dt = 50  # time increment [yr]
    x_sh_test = 1.0
    gamma_eff = 1.1
    Mdot_stable = -999
    
    # Initialize arrays
    n_points = 41  # from tps=1000 to tps=3000 in steps of 50
    tps_arr = np.zeros(n_points)
    Mdisk = np.zeros(n_points)
    Ewind = np.zeros(n_points)
    
    start_time = time.time()
    
    for ii in range(n_points):
        # Call the appropriate process function
        pf = process_func(tps, x_sh_test, gamma_eff, alpha_0, etaprime, Mdot_stable)
        
        # Store results
        tps_arr[ii] = tps
        Mdisk[ii] = pf[6, -1]  # Assuming pf is a numpy array with shape (8, N)
        Ewind[ii] = pf[7, -1]
        
        print(f'ii = {ii+1}, tps = {tps}, Mdisk = {Mdisk[ii]}, Ew = {Ewind[ii]}')
        
        # Store in cases dictionary if provided
        if cases is not None:
            cases[f'pf{ii+1}'] = pf
        
        tps += dt
    
    elapsed_time = time.time() - start_time
    print(f'Elapsed time: {elapsed_time:.2f} seconds')
    
    return tps_arr, Mdisk, Ewind

# Main simulation
if __name__ == "__main__":
    # Parameters
    etaprime = 0.1
    Minfall = 6.1341e-5
    
    # Create dictionaries to store all cases
    results = {
        'post': {'eta1': {}, 'eta1nw': {}},
        'ordinary': {'eta1': {}, 'eta1nw': {}},
        'pre': {'eta1': {}, 'eta1nw': {}}
    }
    
    # Post cases (alpha_0 = 0.3)
    print("Running post cases (alpha=0.3)")
    results['post']['eta1']['tps'], results['post']['eta1']['Mdisk'], results['post']['eta1']['Ewind'] = \
        run_simulation(process.process, 0.5, 1.e-1, results['post']['eta1'])
    
    plot_mat_1 = results['post']['eta1']['pf1']
    
    results['post']['eta1nw']['tps'], results['post']['eta1nw']['Mdisk'], results['post']['eta1nw']['Ewind'] = \
        run_simulation(processnw.process, 0.5, etaprime, results['post']['eta1nw'])
    
    # Ordinary cases (alpha_0 = 0.5)
    print("\nRunning ordinary cases (alpha=0.5)")
    results['ordinary']['eta1']['tps'], results['ordinary']['eta1']['Mdisk'], results['ordinary']['eta1']['Ewind'] = \
        run_simulation(process.process, 0.5, 1.e-2, results['ordinary']['eta1'])
    
    plot_mat_2 = results['ordinary']['eta1']['pf1']
    
    results['ordinary']['eta1nw']['tps'], results['ordinary']['eta1nw']['Mdisk'], results['ordinary']['eta1nw']['Ewind'] = \
        run_simulation(processnw.process, 0.5, etaprime, results['ordinary']['eta1nw'])
    
    # Pre cases (alpha_0 = 0.8)
    print("\nRunning pre cases (alpha=0.8)")
    results['pre']['eta1']['tps'], results['pre']['eta1']['Mdisk'], results['pre']['eta1']['Ewind'] = \
        run_simulation(process.process, 0.5, 1.e-3, results['pre']['eta1'])
    
    plot_mat_3 = results['pre']['eta1']['pf1']

    #comment
    print("\nRunning pre cases (alpha=0.8)")
    results['pre']['eta1']['tps'], results['pre']['eta1']['Mdisk'], results['pre']['eta1']['Ewind'] = \
        run_simulation(process.process, 0.5, 1.e-4, results['pre']['eta1'])
    
    plot_mat_4 = results['pre']['eta1']['pf1']
    #comment

    results['pre']['eta1nw']['tps'], results['pre']['eta1nw']['Mdisk'], results['pre']['eta1nw']['Ewind'] = \
        run_simulation(processnw.process, 0.5, etaprime, results['pre']['eta1nw'])
    
    plot_me.plotme(plot_mat_1, plot_mat_2, plot_mat_3, plot_mat_4)

