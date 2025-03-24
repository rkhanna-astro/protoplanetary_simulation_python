import numpy as np
import time

# Constants
AU_TO_M = 1.49597870691e11  # Astronomical unit to meters
SOLAR_MASS = 1.989e30       # Solar mass in kg
CONVERSION_FACTOR = 10 * (AU_TO_M**2) / SOLAR_MASS
J_CONVERSION_FACTOR = 1000 * 10 * (AU_TO_M**3) / SOLAR_MASS

def process_eta2_data(pf_dict, minr, initial_tps=1000, dt=50, max_tps=3000, case_label="eta2"):
    """Process time series data for eta2 cases (pre, standard, post, and no-wind versions)."""
    # Initialize results dictionary
    results = {
        'tps': [],
        f'Mdisk_pre_{case_label}': [], f'Mdisk_{case_label}': [], f'Mdisk_post_{case_label}': [],
        f'Ewind_pre_{case_label}': [], f'Ewind_{case_label}': [], f'Ewind_post_{case_label}': [],
        f'j_pre_{case_label}': [], f'j_{case_label}': [], f'j_post_{case_label}': [],
        f'M_tot_pre_{case_label}': [], f'M_tot_{case_label}': [], f'M_tot_post_{case_label}': [],
        f'J_tot_pre_{case_label}': [], f'J_tot_{case_label}': [], f'J_tot_post_{case_label}': [],
        f'MdMenv_pre_{case_label}': [], f'MdMenv_{case_label}': [], f'MdMenv_post_{case_label}': [],
        f'Menv_pre_{case_label}': [], f'Menv_{case_label}': [], f'Menv_post_{case_label}': []
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
        
        # Process each case (pre, standard, post)
        for case, pf_case in zip(['pre', '', 'post'], [pf_pre, pf, pf_post]):
            prefix = 'pre_' if case == 'pre' else 'post_' if case == 'post' else ''
            
            # Disk mass and wind energy
            results[f'Mdisk_{prefix}{case_label}'].append(pf_case[6][-1])
            results[f'Ewind_{prefix}{case_label}'].append(pf_case[7][-1])
            results[f'j_{prefix}{case_label}'].append(pf_case[1][-1] * pf_case[2][-1] * pf_case[3][-1])
            
            # Process radial profiles
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
            
            results[f'M_tot_{prefix}{case_label}'].append(M_tot)
            results[f'J_tot_{prefix}{case_label}'].append(J_tot)
            
            # Mass envelope calculations
            MdMenv = pf_case[10][-1]
            Menv = MdMenv / pf_case[6][-1]
            
            results[f'MdMenv_{prefix}{case_label}'].append(MdMenv)
            results[f'Menv_{prefix}{case_label}'].append(Menv)
        
        print(f'ii = {ii}, tps = {tps}, Mdisk = {results[f"Mdisk_post_{case_label}"][-1]}, Ew = {results[f"Ewind_post_{case_label}"][-1]}')
        
        ii += 1
        tps += dt
    
    return results

def main():
    # Load your pf data here - needs to be implemented based on your data storage
    # Example structure for wind case:
    # pf_dict_eta2 = {'pf1_pre': ..., 'pf1': ..., 'pf1_post': ..., 'pf2_pre': ...}
    # And for no-wind case:
    # pf_dict_eta2nw = {'pf1_pre': ..., 'pf1': ..., 'pf1_post': ..., 'pf2_pre': ...}
    
    pf_dict_eta2 = {}    # Replace with actual data loading for wind case
    pf_dict_eta2nw = {}  # Replace with actual data loading for no-wind case
    
    # Get minimum radius from one of the profiles
    minr = pf_dict_eta2['pf1'][1][0] if 'pf1' in pf_dict_eta2 else 0
    
    # Process with wind
    print("Processing eta2 with wind...")
    start_time = time.time()
    results_eta2 = process_eta2_data(pf_dict_eta2, minr, case_label="eta2")
    print(f"Completed in {time.time() - start_time:.2f} seconds")
    
    # Process no wind case
    print("\nProcessing eta2 no wind case...")
    start_time = time.time()
    results_eta2nw = process_eta2_data(pf_dict_eta2nw, minr, case_label="eta2nw")
    print(f"Completed in {time.time() - start_time:.2f} seconds")
    
    return results_eta2, results_eta2nw

if __name__ == "__main__":
    results_eta2, results_eta2nw = main()
