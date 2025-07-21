import numpy as np
import time

# Constants
AU_TO_M = 1.49597870691e11  # Astronomical unit to meters
SOLAR_MASS = 1.989e30       # Solar mass in kg
CONVERSION_FACTOR = 10 * (AU_TO_M**2) / SOLAR_MASS
J_CONVERSION_FACTOR = 1000 * 10 * (AU_TO_M**3) / SOLAR_MASS

def process_time_series(pf_dict, minr, initial_tps=1000, dt=50, max_tps=3000):
    """Process time series data for pre, standard, and post cases."""
    # Initialize arrays
    results = {
        'tps': [],
        'Mdisk_pre': [], 'Mdisk': [], 'Mdisk_post': [],
        'Ewind_pre': [], 'Ewind': [], 'Ewind_post': [],
        'j_pre': [], 'j': [], 'j_post': [],
        'M_tot_pre': [], 'M_tot': [], 'M_tot_post': [],
        'J_tot_pre': [], 'J_tot': [], 'J_tot_post': [],
        'MdMenv_pre': [], 'MdMenv': [], 'MdMenv_post': [],
        'Menv_pre': [], 'Menv': [], 'Menv_post': []
    }
    
    tps = initial_tps
    ii = 1
    rmid = 5000  # Middle radius for calculations
    
    while tps <= max_tps:
        # Get the appropriate profiles for this time point
        pf_pre = pf_dict[f'pf{ii}_pre']
        pf = pf_dict[f'pf{ii}']
        pf_post = pf_dict[f'pf{ii}_post']
        
        # Store basic results
        results['tps'].append(tps)
        
        # Disk mass and wind energy
        for case, pf_case in zip(['pre', '', 'post'], [pf_pre, pf, pf_post]):
            prefix = 'pre_' if case == 'pre' else 'post_' if case == 'post' else ''
            results[f'Mdisk_{prefix}{case}'].append(pf_case[6][-1])
            results[f'Ewind_{prefix}{case}'].append(pf_case[7][-1])
            results[f'j_{prefix}{case}'].append(pf_case[1][-1] * pf_case[2][-1] * pf_case[3][-1])
        
        # Process radial profiles for each case
        for case, pf_case in zip(['pre', '', 'post'], [pf_pre, pf, pf_post]):
            prefix = 'pre_' if case == 'pre' else 'post_' if case == 'post' else ''
            
            # Get radial profiles within specified range
            rT = pf_case[1]
            ind0 = np.where((rT >= minr) & (rT <= rmid))[0]
            r = pf_case[1][ind0]
            v_phi = pf_case[2][ind0] * pf_case[3][ind0]
            sigma = pf_case[5][ind0]
            
            # Calculate dr (spacing between radial points)
            fresh_ind = np.arange(len(r))
            r_extended = np.append(r, r[-1] + (r[-1] - r[-2]))
            dr = r_extended[fresh_ind + 1] - r_extended[fresh_ind]
            
            # Calculate total mass and angular momentum
            M_tot = 2 * np.pi * np.sum(r * sigma * dr) * CONVERSION_FACTOR
            J_tot = 2 * np.pi * np.sum((r**2) * v_phi * sigma * dr) * J_CONVERSION_FACTOR
            
            results[f'M_tot_{prefix}{case}'].append(M_tot)
            results[f'J_tot_{prefix}{case}'].append(J_tot)
            
            # Mass envelope calculations
            MdMenv = pf_case[10][-1]
            Menv = MdMenv / pf_case[6][-1]
            
            results[f'MdMenv_{prefix}{case}'].append(MdMenv)
            results[f'Menv_{prefix}{case}'].append(Menv)
        
        print(f'ii = {ii}, tps = {tps}, Mdisk = {results["Mdisk_post"][-1]}, Ew = {results["Ewind_post"][-1]}')
        
        ii += 1
        tps += dt
    
    return results

# Main processing
def main():
    # Load your pf data here - this needs to be implemented based on how your data is stored
    # Example structure: pf_dict = {'pf1_pre': ..., 'pf1': ..., 'pf1_post': ..., 'pf2_pre': ...}
    pf_dict = {}  
    pf_dict_nw = {}  # No wind case
    
    # Get minimum radius from one of the profiles
    minr = pf_dict['pf1'][1][0] if 'pf1' in pf_dict else 0
    
    # Process with wind
    print("Processing with wind...")
    start_time = time.time()
    results_wind = process_time_series(pf_dict, minr)
    print(f"Completed in {time.time() - start_time:.2f} seconds")
    
    # Process no wind case
    print("\nProcessing no wind case...")
    start_time = time.time()
    results_no_wind = process_time_series(pf_dict_nw, minr)
    print(f"Completed in {time.time() - start_time:.2f} seconds")
    
    return results_wind, results_no_wind

if __name__ == "__main__":
    results_wind, results_no_wind = main()
