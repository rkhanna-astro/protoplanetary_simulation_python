import numpy as np
import time

# Constants and initial parameters
ii = 1
tps = 1.e3
x_sh_test = 1.0
gamma_eff = 1.1
etaprime = 1.e-1
Mdot_stable = -999
dt = 50  # time increment [yr]
xd = 1.0
Minfall = 6.1341e-5  # 1.4086e-5 | 2.8509e-5 | 6.1341e-5

# Initialize arrays
tpsArr_post_eta1 = np.zeros(1)
Mdisk_post_eta1 = np.zeros(1)
Ewind_post_eta1 = np.zeros(1)

alpha_0 = 0.3  # post

# First loop with process function
start_time = time.time()
while tps <= 3.e3:
    if ii == 1:
        pf1_post_eta1 = process(tps, x_sh_test, gamma_eff, alpha_0, etaprime, Mdot_stable)
        pf = pf1_post_eta1
    if ii == 2:
        pf2_post_eta1 = process(tps, x_sh_test, gamma_eff, alpha_0, etaprime, Mdot_stable)
        pf = pf2_post_eta1
    # ... (similar for ii=3 to ii=41)
    # Note: In Python, we could simplify this with a dictionary or list, but I'm keeping the structure similar to MATLAB
    
    tpsArr_post_eta1 = np.append(tpsArr_post_eta1, tps)
    Mdisk_post_eta1 = np.append(Mdisk_post_eta1, pf[6,-1])
    Ewind_post_eta1 = np.append(Ewind_post_eta1, pf[7,-1])
    print(f'ii = {ii} , tps = {tps} , Mdisk = {Mdisk_post_eta1[ii-1]} , Ew = {Ewind_post_eta1[ii-1]}')
    ii += 1
    tps += dt
print(f"Time elapsed: {time.time() - start_time} seconds")

# Second loop with processnw function
ii = 1
tps = 1.e3
tpsArr_post_eta1nw = np.zeros(1)
Mdisk_post_eta1nw = np.zeros(1)
Ewind_post_eta1nw = np.zeros(1)

while tps <= 3.e3:
    if ii == 1:
        pf1_post_eta1nw = processnw(tps, x_sh_test, gamma_eff, alpha_0, etaprime, Mdot_stable)
        pf = pf1_post_eta1nw
    if ii == 2:
        pf2_post_eta1nw = processnw(tps, x_sh_test, gamma_eff, alpha_0, etaprime, Mdot_stable)
        pf = pf2_post_eta1nw
    # ... (similar for ii=3 to ii=41)
    
    tpsArr_post_eta1nw = np.append(tpsArr_post_eta1nw, tps)
    Mdisk_post_eta1nw = np.append(Mdisk_post_eta1nw, pf[6,-1])
    Ewind_post_eta1nw = np.append(Ewind_post_eta1nw, pf[7,-1])
    print(f'ii = {ii} , tps = {tps} , Mdisk = {Mdisk_post_eta1nw[ii-1]} , Ew = {Ewind_post_eta1nw[ii-1]}')
    ii += 1
    tps += dt

# Third section with alpha_0 = 0.5 (ordinary)
ii = 1
tps = 1.e3
tpsArr_eta1 = np.zeros(1)
Mdisk_eta1 = np.zeros(1)
Ewind_eta1 = np.zeros(1)

alpha_0 = 0.5  # ordinary

start_time = time.time()
while tps <= 3.e3:
    if ii == 1:
        pf1_eta1 = process(tps, x_sh_test, gamma_eff, alpha_0, etaprime, Mdot_stable)
        pf = pf1_eta1
    # ... (similar structure as above)
    
    tpsArr_eta1 = np.append(tpsArr_eta1, tps)
    Mdisk_eta1 = np.append(Mdisk_eta1, pf[6,-1])
    Ewind_eta1 = np.append(Ewind_eta1, pf[7,-1])
    print(f'ii = {ii} , tps = {tps} , Mdisk = {Mdisk_eta1[ii-1]} , Ew = {Ewind_eta1[ii-1]}')
    ii += 1
    tps += dt
print(f"Time elapsed: {time.time() - start_time} seconds")

# Fourth section with processnw and alpha_0 = 0.5
ii = 1
tps = 1.e3
tpsArr_eta1nw = np.zeros(1)
Mdisk_eta1nw = np.zeros(1)
Ewind_eta1nw = np.zeros(1)

while tps <= 3.e3:
    if ii == 1:
        pf1_eta1nw = processnw(tps, x_sh_test, gamma_eff, alpha_0, etaprime, Mdot_stable)
        pf = pf1_eta1nw
    # ... (similar structure as above)
    
    tpsArr_eta1nw = np.append(tpsArr_eta1nw, tps)
    Mdisk_eta1nw = np.append(Mdisk_eta1nw, pf[6,-1])
    Ewind_eta1nw = np.append(Ewind_eta1nw, pf[7,-1])
    print(f'ii = {ii} , tps = {tps} , Mdisk = {Mdisk_eta1nw[ii-1]} , Ew = {Ewind_eta1nw[ii-1]}')
    ii += 1
    tps += dt

# Fifth section with alpha_0 = 0.8 (pre)
ii = 1
tps = 1.e3
tpsArr_pre_eta1 = np.zeros(1)
Mdisk_pre_eta1 = np.zeros(1)
Ewind_pre_eta1 = np.zeros(1)

alpha_0 = 0.8  # pre

start_time = time.time()
while tps <= 3.e3:
    if ii == 1:
        pf1_pre_eta1 = process(tps, x_sh_test, gamma_eff, alpha_0, etaprime, Mdot_stable)
        pf = pf1_pre_eta1
    # ... (similar structure as above)
    
    tpsArr_pre_eta1 = np.append(tpsArr_pre_eta1, tps)
    Mdisk_pre_eta1 = np.append(Mdisk_pre_eta1, pf[6,-1])
    Ewind_pre_eta1 = np.append(Ewind_pre_eta1, pf[7,-1])
    print(f'ii = {ii} , tps = {tps} , Mdisk = {Mdisk_pre_eta1[ii-1]} , Ew = {Ewind_pre_eta1[ii-1]}')
    ii += 1
    tps += dt
print(f"Time elapsed: {time.time() - start_time} seconds")

# Sixth section with processnw and alpha_0 = 0.8
ii = 1
tps = 1.e3
tpsArr_pre_eta1nw = np.zeros(1)
Mdisk_pre_eta1nw = np.zeros(1)
Ewind_pre_eta1nw = np.zeros(1)

while tps <= 3.e3:
    if ii == 1:
        pf1_pre_eta1nw = processnw(tps, x_sh_test, gamma_eff, alpha_0, etaprime, Mdot_stable)
        pf = pf1_pre_eta1nw
    # ... (similar structure as above)
    
    tpsArr_pre_eta1nw = np.append(tpsArr_pre_eta1nw, tps)
    Mdisk_pre_eta1nw = np.append(Mdisk_pre_eta1nw, pf[6,-1])
    Ewind_pre_eta1nw = np.append(Ewind_pre_eta1nw, pf[7,-1])
    print(f'ii = {ii} , tps = {tps} , Mdisk = {Mdisk_pre_eta1nw[ii-1]} , Ew = {Ewind_pre_eta1nw[ii-1]}')
    ii += 1
    tps += dt

