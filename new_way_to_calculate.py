import numpy as np
import pandas as pd
import glob
import os
import jspec_c

# Constants
AU_TO_M = 1.49597870691e11  # Astronomical unit to meters
SOLAR_MASS = 1.989e30       # Solar mass in kg
CONVERSION_FACTOR = 10 * (AU_TO_M**2) / SOLAR_MASS
J_CONVERSION_FACTOR = 1000 * 10 * (AU_TO_M**3) / SOLAR_MASS

M_3, J_3 = [], []
M_5, J_5 = [], []
M_8, J_8 = [], []

M_3nw, J_3nw = [], []
M_5nw, J_5nw = [], []
M_8nw, J_8nw = [], []

# Function to compute M_tot and J_tot
def compute_totals(filepath):
    # Load data assuming 5-column format: r, v_phi, v_factor, _, sigma
    data = np.loadtxt(filepath, delimiter=",", skiprows=1)
    r = data[:, 0]  # Radius in AU
    v_phi = data[:, 1] * data[:, 2]  # Effective azimuthal velocity (km/s)
    sigma = data[:, 4]  # Surface density

    # Compute dr with edge padding method
    r_extended = np.append(r, r[-1] + (r[-1] - r[-2]))
    fresh_ind = np.arange(len(r))
    dr = r_extended[fresh_ind + 1] - r_extended[fresh_ind]

    # Total mass
    M_tot = 2 * np.pi * np.sum(r * sigma * dr) * CONVERSION_FACTOR

    # Total angular momentum
    J_tot = 2 * np.pi * np.sum((r**2) * v_phi * sigma * dr) * J_CONVERSION_FACTOR

    return M_tot, J_tot

# Optional: glob pattern to read multiple files
filepaths_3_w = sorted(glob.glob("output_alpha_0.3_eta_0.01_lambda_0.1_time_*.csv"))
filepaths_5_w = sorted(glob.glob("output_alpha_0.5_eta_0.01_lambda_0.1_time_*.csv"))
filepaths_8_w = sorted(glob.glob("output_alpha_0.8_eta_0.01_lambda_0.1_time_*.csv"))

filepaths_3_nw = sorted(glob.glob("output_alpha_0.3_eta_0.01_lambda_0.0_time_*.csv"))
filepaths_5_nw = sorted(glob.glob("output_alpha_0.5_eta_0.01_lambda_0.0_time_*.csv"))
filepaths_8_nw = sorted(glob.glob("output_alpha_0.8_eta_0.01_lambda_0.0_time_*.csv"))

for path in filepaths_3_w:
    m_3, j_3 = compute_totals(path)
    M_3.append(m_3)
    J_3.append(j_3)
    time = os.path.basename(path).split("_")[-1].split(".")[0]
    # print(f"Time: {time} | Ratio: {(J_3/M_3)*1000 }")

for path in filepaths_5_w:
    m_5, j_5 = compute_totals(path)
    M_5.append(m_5)
    J_5.append(j_5)
    time = os.path.basename(path).split("_")[-1].split(".")[0]
    # print(f"Time: {time} | Ratio: {(J_5/M_5)*1000 }")

for path in filepaths_8_w:
    m_8, j_8 = compute_totals(path)
    M_8.append(m_8)
    J_8.append(j_8)
    time = os.path.basename(path).split("_")[-1].split(".")[0]
    # print(f"Time: {time} | Ratio: {(J_8/M_8)*1000 }")

for path in filepaths_3_nw:
    m_3nw, j_3nw = compute_totals(path)
    M_3nw.append(m_3nw)
    J_3nw.append(j_3nw)
    time = os.path.basename(path).split("_")[-1].split(".")[0]
    # print(f"Time: {time} | Ratio: {(J_3/M_3)*1000 }")

for path in filepaths_5_nw:
    m_5nw, j_5nw = compute_totals(path)
    M_5nw.append(m_5nw)
    J_5nw.append(j_5nw)
    time = os.path.basename(path).split("_")[-1].split(".")[0]
    # print(f"Time: {time} | Ratio: {(J_5/M_5)*1000 }")

for path in filepaths_8_nw:
    m_8nw, j_8nw = compute_totals(path)
    M_8nw.append(m_8nw)
    J_8nw.append(j_8nw)
    time = os.path.basename(path).split("_")[-1].split(".")[0]
    # print(f"Time: {time} | Ratio: {(J_8/M_8)*1000 }")

time_evolution = []
tps = 1000
while tps <= 3000:
    time_evolution.append(tps)
    tps += 50


jspec_c.jspec(time_evolution, time_evolution, np.array(J_3), np.array(M_3), 
              np.array(J_5), np.array(M_5), np.array(J_8), np.array(M_8), 
              np.array(J_3nw), np.array(M_3nw), np.array(J_5nw), np.array(M_5nw), 
              np.array(J_8nw), np.array(M_8nw))
