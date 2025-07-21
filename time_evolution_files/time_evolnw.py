import numpy as np
from typing import Tuple
import process_nw as processnw

def run_simulation_nw(
    process_func,
    xd: float,
    Minfall: float,
    tps_start: float = 0,
    tps_end: float = 3.e3,
    dt: float = 50
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Run simulation without wind using processnw function
    
    Args:
        process_func: The processing function to use (processnw)
        xd: x_sh_test value
        Minfall: Minfall parameter
        tps_start: Starting time (years)
        tps_end: Ending time (years)
        dt: Time increment (years)
        
    Returns:
        Tuple of (time_points, disk_masses, wind_energies)
    """
    tps_values = []
    mdisk_values = []
    ewind_values = []
    
    tps = tps_start
    ii = 1
    
    while tps <= tps_end:
        pf = process_func(tps, xd, Minfall)
        
        tps_values.append(tps)
        mdisk_values.append(pf[6, -1])  # Assuming pf is a 2D numpy array
        ewind_values.append(pf[7, -1])
        
        print(f'ii = {ii}, tps = {tps}, Mdisk = {mdisk_values[-1]}, Ew = {ewind_values[-1]}')
        
        tps += dt
        ii += 1
    
    return np.array(tps_values), np.array(mdisk_values), np.array(ewind_values)

# Constants
xd = 1.0
Minfall = 1.8341e-5  # 9.0624e-6 | 1.8341e-5 | 3.9463e-5
dt = 50  # time increment [yr]

# Run the simulation
print("Running no-wind simulation...")
tpsArr_nw, Mdisk_nw, Ewind_nw = run_simulation_nw(
    process_func=processnw.process,
    xd=xd,
    Minfall=Minfall
)

# Results are now available in:
# tpsArr_nw - time points
# Mdisk_nw - disk masses at each time point
# Ewind_nw - wind energies at each time point
