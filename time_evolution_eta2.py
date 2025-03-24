import numpy as np
import time
from typing import Dict, List

# Constants
AU_TO_M = 1.49597870691e11  # Astronomical unit to meters
SOLAR_MASS = 1.989e30       # Solar mass in kg
CONVERSION_FACTOR = 10 * (AU_TO_M**2) / SOLAR_MASS
J_CONVERSION_FACTOR = 1000 * 10 * (AU_TO_M**3) / SOLAR_MASS

class DiskAnalysis:
    def __init__(self, case_name: str):
        self.case_name = case_name
        self.results = {
            'tps': [],
            'Mdisk_pre': [], 'Mdisk': [], 'Mdisk_post': [],
            'Ewind_pre': [], 'Ewind': [], 'Ewind_post': [],
            'j_pre': [], 'j': [], 'j_post': [],
            'M_tot_pre': [], 'M_tot': [], 'M_tot_post': [],
            'J_tot_pre': [], 'J_tot': [], 'J_tot_post': [],
            'MdMenv_pre': [], 'MdMenv': [], 'MdMenv_post': [],
            'Menv_pre': [], 'Menv': [], 'Menv_post': []
        }
        
    def process_time_series(self, pf_dict: Dict, minr: float, 
                          initial_tps: int = 1000, dt: int = 50, max_tps: int = 3000):
        """Process time series data for pre, standard, and post cases."""
        tps = initial_tps
        ii = 1
        rmid = 5000  # Middle radius for calculations
        
        while tps <= max_tps:
            try:
                # Get the appropriate profiles for this time point
                pf_pre = pf_dict[f'pf{ii}_pre']
                pf = pf_dict[f'pf{ii}']
                pf_post = pf_dict[f'pf{ii}_post']
                
                # Store time point
                self.results['tps'].append(tps)
                
                # Process each case (pre, standard, post)
                for case, pf_case in zip(['pre', '', 'post'], [pf_pre, pf, pf_post]):
                    self._process_single_case(case, pf_case, minr, rmid)
                
                print(f'ii = {ii}, tps = {tps}, Mdisk = {self.results["Mdisk_post"][-1]:.4e}, '
                      f'Ew = {self.results["Ewind_post"][-1]:.4e}')
                
                ii += 1
                tps += dt
                
            except KeyError:
                print(f"Warning: Missing data for ii={ii}, stopping processing")
                break
        
        return self.results
    
    def _process_single_case(self, case: str, pf_case: np.ndarray, minr: float, rmid: float):
        """Process data for a single case (pre, standard, or post)."""
        prefix = 'pre_' if case == 'pre' else 'post_' if case == 'post' else ''
        
        # Disk mass and wind energy
        self.results[f'Mdisk_{prefix}{self.case_name}'].append(pf_case[6][-1])
        self.results[f'Ewind_{prefix}{self.case_name}'].append(pf_case[7][-1])
        self.results[f'j_{prefix}{self.case_name}'].append(pf_case[1][-1] * pf_case[2][-1] * pf_case[3][-1])
        
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
        
        self.results[f'M_tot_{prefix}{self.case_name}'].append(M_tot)
        self.results[f'J_tot_{prefix}{self.case_name}'].append(J_tot)
        
        # Mass envelope calculations
        MdMenv = pf_case[10][-1]
        Menv = MdMenv / pf_case[6][-1]
        
        self.results[f'MdMenv_{prefix}{self.case_name}'].append(MdMenv)
        self.results[f'Menv_{prefix}{self.case_name}'].append(Menv)

def main():
    # Load your data - replace with actual data loading
    pf_dict_eta2 = {}    # Should contain pf1_pre, pf1, pf1_post, pf2_pre, etc.
    pf_dict_eta2nw = {}  # No-wind version
    
    # Get minimum radius from one of the profiles
    minr = pf_dict_eta2['pf1'][1][0] if 'pf1' in pf_dict_eta2 else 0
    
    # Process with wind
    print("Processing eta2 with wind...")
    start_time = time.time()
    eta2_analysis = DiskAnalysis("eta2")
    results_eta2 = eta2_analysis.process_time_series(pf_dict_eta2, minr)
    print(f"Completed in {time.time() - start_time:.2f} seconds")
    
    # Process no wind case
    print("\nProcessing eta2 no wind case...")
    start_time = time.time()
    eta2nw_analysis = DiskAnalysis("eta2nw")
    results_eta2nw = eta2nw_analysis.process_time_series(pf_dict_eta2nw, minr)
    print(f"Completed in {time.time() - start_time:.2f} seconds")
    
    return results_eta2, results_eta2nw

if __name__ == "__main__":
    results_eta2, results_eta2nw = main()
