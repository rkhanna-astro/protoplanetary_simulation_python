import numpy as np
import time
import process
import plot_me_3times
import new_figure
import menv
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.ticker import ScalarFormatter
import matplotlib.ticker as ticker
from scipy.signal import savgol_filter


# Constants and initial parameters
tps = 1.e3
x_sh_test = 1.0
gamma_eff = 1.1
etaprime = 1.e-2
Mdot_stable = -999
dt = 50  # time increment [yr]
Minfall = 6.1341e-5  # 1.4086e-5 | 2.8509e-5 | 6.1341e-5

mdisk1 = []
mps_acc1 = []
mdisk_acc1 = []
qtoomre1 = []
toom1 = []

mdisk2 = []
mps_acc2 = []
mdisk_acc2 = []
qtoomre2 = []
toom2 = []

mdisk3 = []
mps_acc3 = []
mdisk_acc3 = []
qtoomre3 = []
toom3 = []

mdisk4 = []
mps_acc4 = []
mdisk_acc4 = []
qtoomre4 = []
toom4 = []



Lstyle0 = '-'
Lstyle1 = '--'
Lstyle2 = '-.'
Lstyle3 = ':'

Lwidth0 = 0.8
Lwidth1 = 0.8
Lwidth2 = 0.8
Lwidth3 = 0.8

Lcolor0 = np.array([0, 0.4157, 1])       # blue
Lcolor1 = np.array([0.3, 0.9333, 0])     # green
Lcolor2 = np.array([1, 0.3333, 0])       # red
Lcolor3 = 'magenta'

# Initialize storage dictionaries
results = {
    # 'post_eta2': {'tps': [], 'Mdisk': [], 'Ewind': [], 'alpha': 0.1, 'func': 'process'},
    # 'post_eta2nw': {'tps': [], 'Mdisk': [], 'Ewind': [], 'alpha': 0.2, 'func': 'process'},
    'alpha1': {'tps': [], 'Mdisk': [], 'Ewind': [], 'alpha': 0.5, 'etaprime': 0.001, 'gamma': 1.1, 'lambda': 0.1, 'func': 'process'},
    'alpha2': {'tps': [], 'Mdisk': [], 'Ewind': [], 'alpha': 0.5, 'etaprime': 0.01, 'gamma': 1.1, 'lambda': 0.1, 'func': 'process'},
    'alpha3': {'tps': [], 'Mdisk': [], 'Ewind': [], 'alpha': 0.5, 'etaprime': 0.01, 'gamma': 1.1, 'lambda': 0.2, 'func': 'process'},
    'alpha4': {'tps': [], 'Mdisk': [], 'Ewind': [], 'alpha': 0.5, 'etaprime': 0.1, 'gamma': 1.1, 'lambda': 0.5, 'func': 'process'},
    # 'alpha2': {'tps': [], 'Mdisk': [], 'Ewind': [], 'alpha': 0.5, 'etaprime': 0.1, 'gamma': 1.1, 'lambda': 0.4, 'func': 'process'},
    # 'alpha3': {'tps': [], 'Mdisk': [], 'Ewind': [], 'alpha': 0.5, 'etaprime': 0.1, 'gamma': 1.1, 'lambda': 0.6, 'func': 'process'},
    # 'alpha4': {'tps': [], 'Mdisk': [], 'Ewind': [], 'alpha': 0.5, 'etaprime': 0.1, 'gamma': 1.1, 'lambda': 0.8, 'func': 'process'},
    # 'pre_eta2nw': {'tps': [], 'Mdisk': [], 'Ewind': [], 'alpha': 0.5, 'etaprime': 0.0001, 'gamma': 1.1, 'lambda': 0.1, 'func': 'process'}
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
    
    while tps <= 2.e3:
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
time_series = {}

for key in results.keys():
    dict[key] = run_simulation(key)

plot_mat_1 = dict['alpha1']['pf19']
plot_mat_2 = dict['alpha2']['pf19']
plot_mat_3 = dict['alpha3']['pf19']
plot_mat_4 = dict['alpha4']['pf19']

# aplha_str_1 = r'$\alpha = 0.3$'
# alpha_str_2 = r'$\alpha = 0.5$'
# alpha_str_3 = r'$\alpha = 0.8$'


time_evol = []
curr_time = 1.e2

while curr_time <= 2.e3:
    time_evol.append(curr_time)
    curr_time += dt

for key in results:
    curr_time = 1.e2
    ii = 1

    while curr_time <= 2.e3:
        r = dict[key][f'pf{ii}'][0, :]
        mdisk = (dict[key][f'pf{ii}'][5, :][-1])

        vphi_cs = dict[key][f'pf{ii}'][1,:]
        cs1 = dict[key][f'pf{ii}'][2,:]
        vr_cs1 = dict[key][f'pf{ii}'][3,:]


        mdot_acc = (dict[key][f'pf{ii}'][7, :])
        sinkind = np.where(r < 5)[0]
        sc_ind = sinkind[-1]
        Mdot_ps_acc = mdot_acc[sc_ind]
        mps = dict[key][f'pf{ii}'][5, :][sc_ind]
        Mdot_outflow = dict[key][f'pf{ii}'][17, :][-1]
        Mdot_disk_acc = mdot_acc[-1]

        dr = np.gradient(r)
        weights = 2 * np.pi * r * dr
        toomre = np.average(dict[key][f'pf{ii}'][8, :], weights=weights)

        if key == "alpha1":
            mps_acc1.append(Mdot_ps_acc)
            mdisk1.append(mdisk)
            qtoomre1.append(mps)
            mdisk_acc1.append(Mdot_disk_acc)
            toom1.append(toomre)
            # qtoomre2.append(Mdot_outflow)
            # qtoomre3.append(Mdot_disk_acc)
        
        elif key == "alpha2":
            mps_acc2.append(Mdot_ps_acc)
            mdisk2.append(mdisk)
            qtoomre2.append(mps)
            mdisk_acc2.append(Mdot_disk_acc)
            toom2.append(toomre)

        elif key == "alpha3":
            mps_acc3.append(Mdot_ps_acc)
            mdisk3.append(mdisk)
            qtoomre3.append(mps)
            mdisk_acc3.append(Mdot_disk_acc)
            toom3.append(toomre)

        else:
            mps_acc4.append(Mdot_ps_acc)
            mdisk4.append(mdisk)
            qtoomre4.append(mps)
            mdisk_acc4.append(Mdot_disk_acc)
            toom4.append(toomre)
        #     qtoomre4.append(num_dens)

        curr_time += dt
        ii += 1

for key in results:
    time_series[key] = {}

for key in results:
    if key == "alpha1":
        time_series[key]['mps'] = np.array(qtoomre1)
        time_series[key]['mdisk'] = np.array(mdisk1)
        time_series[key]['mps_acc'] = mps_acc1
        time_series[key]['mdisk_acc'] = mdisk_acc1
        time_series[key]['toomre'] = toom1
    elif key == "alpha2":
        time_series[key]['mps'] = np.array(qtoomre2)
        time_series[key]['mdisk'] = np.array(mdisk2)
        time_series[key]['mps_acc'] = mps_acc2
        time_series[key]['mdisk_acc'] = mdisk_acc2
        time_series[key]['toomre'] = toom2
    elif key == "alpha3":
        time_series[key]['mps'] = np.array(qtoomre3)
        time_series[key]['mdisk'] = np.array(mdisk3)
        time_series[key]['mps_acc'] = mps_acc3
        time_series[key]['mdisk_acc'] = mdisk_acc3
        time_series[key]['toomre'] = toom3
    else:
        time_series[key]['mps'] = np.array(qtoomre4)
        time_series[key]['mdisk'] = np.array(mdisk4)
        time_series[key]['mps_acc'] = mps_acc4
        time_series[key]['mdisk_acc'] = mdisk_acc4
        time_series[key]['toomre'] = toom4



# Convert lists to numpy arrays for easier handling
# for key in results.keys():
#     results[key]['tps'] = np.array(results[key]['tps'])
#     results[key]['Mdisk'] = np.array(results[key]['Mdisk'])
#     results[key]['Ewind'] = np.array(results[key]['Ewind'])


aplha_str_1 = r'$\Lambda_0 = 0.1 \,\, & \,\, \eta^{\prime}=10^{-3}$'
alpha_str_2 = r'$\Lambda_0 = 0.1 \,\, & \,\, \eta^{\prime}=10^{-2}$'
alpha_str_3 = r'$\Lambda_0 = 0.2 \,\, & \,\, \eta^{\prime}=10^{-2}$'
alpha_str_4 = r'$\Lambda_0 = 0.5 \,\, & \,\, \eta^{\prime}=10^{-1}$'

# aplha_str_1 = r'$\eta^{\prime}=10^{-3}$'
# alpha_str_2 = r'$\eta^{\prime}=10^{-2}$'
# alpha_str_3 = r'$\eta^{\prime}=10^{-1}$'
# alpha_str_4 = r'$\eta^{\prime}=0.5$'

# aplha_str_1 = r'$\Lambda_0 = 0.1$'
# alpha_str_2 = r'$\Lambda_0 = 0.2$'
# alpha_str_3 = r'$\Lambda_0 = 0.3$'
# alpha_str_4 = r'$\Lambda_0 = 0.4$'

plt.rcParams['mathtext.fontset'] = 'stix'     # or 'cm', 'dejavuserif', 'stixsans'
plt.rcParams['mathtext.rm'] = 'Times New Roman'  # serif font
# plt.rcParams['mathtext.it'] = 'Times New Roman:italic'
plt.rcParams['mathtext.bf'] = 'Times New Roman:bold'

# print(time_series.keys())

new_figure.plotme3times((plot_mat_1, aplha_str_1), (plot_mat_2, alpha_str_2), (plot_mat_3, alpha_str_3), (plot_mat_4, alpha_str_4), 'new_figure_10', time_series)

# Access results like this:
# post_eta2_tps = results['post_eta2']['tps']
# post_eta2_Mdisk = results['post_eta2']['Mdisk']
# etc.

# plt.rcParams.update({
#     "text.usetex": False,             # Set True if you want LaTeX rendering
#     "font.family": "serif",           # Clean serif font
#     "font.size": 14,                  # General font size
#     "axes.labelsize": 16,             # Axis label size
#     "axes.titlesize": 16,             # Title size
#     "xtick.labelsize": 13,
#     "ytick.labelsize": 13,
#     "legend.fontsize": 13,
#     "figure.figsize": (7, 5),         # Figure size in inches
#     "lines.linewidth": 2,
#     "lines.markersize": 6,
# })

# -------------------
# Create Plot
# -------------------
fig, ax = plt.subplots()
label_fsize = 14
ticklength = [0.035, 0.035]

plt.rcParams['font.size'] = 14
plt.rcParams["font.family"] = "Arial"
plt.rcParams["font.weight"] = "normal"
plt.rcParams["axes.labelweight"] = "bold"
plt.rcParams['axes.titlesize'] = 11
plt.rcParams['axes.labelsize'] = label_fsize
plt.rcParams['xtick.labelsize'] = 14
plt.rcParams['ytick.labelsize'] = 14


# Create grid for subplots
gs = gridspec.GridSpec(3, 2, wspace=0.0, hspace=0.0, 
                        left=0.1, right=0.9, bottom=0.1, top=0.9)

# # print(len(alpha1), len(time_evol))
# mdisk1 = savgol_filter(mdisk1, window_length=9, polyorder=3)
# mdisk2 = savgol_filter(mdisk2, window_length=9, polyorder=3)
# mdisk3 = savgol_filter(mdisk3, window_length=9, polyorder=3)
# mdisk4 = savgol_filter(mdisk4, window_length=9, polyorder=3)

# ax.plot(time_evol, mdisk1, color=Lcolor0, linestyle=Lstyle0)
# ax.plot(time_evol, mdisk2, color=Lcolor1, linestyle=Lstyle1)
# ax.plot(time_evol, mdisk3, color=Lcolor2, linestyle=Lstyle2)
# ax.plot(time_evol, mdisk4, color=Lcolor3, linestyle=Lstyle3)

# XTick = [100, 500, 1000, 1500, 2000]

# # Set logarithmic y-axis
# ax.set_yscale("log")
# # ax.set_xscale("log")
# ax.set_ylim(1e-6, 1e-4)
# ax.set_xlim([1e2, 2*(1e3)])
# ax.set_xticks(XTick)
# # ax.set_yticks([0.01, 0.1, 1])
# ax.xaxis.set_major_formatter(ScalarFormatter())
# ax.set_xticklabels([str(t) for t in XTick])
# ax.xaxis.set_minor_locator(ticker.AutoMinorLocator())
# ax.tick_params(axis='both', which='both', length=ticklength[0]*100*0.68)
# ax.set_xlabel(r'$time \, (yr)$', fontsize=14)
# ax.set_ylabel(r'$\dot{M}_{\rm protostar}\,(M_\odot \, \mathrm{yr}^{-1})$', fontsize=14)
# # ax.set_ylabel(r'$Mass \, \, (M_\odot)$', fontsize=14)
# ax.xaxis.tick_bottom()
# ax.xaxis.set_label_position('bottom')


# for tick in ax.get_xticklabels():
#     tick.set_fontweight('semibold')

# # Make **y-tick labels** bold
# for tick in ax.get_yticklabels():
#     tick.set_fontweight('semibold')

# for spine in ax.spines.values():
#     spine.set_linewidth(2)   # increase thickness
#     spine.set_color('0.2')  # optional: change color
# ax.tick_params(axis='both', which='major', width=2, length=6)  # make ticks bold
# ax.tick_params(axis='both', which='minor', width=1, length=3)  # minor ticksa

# # Labels and title
# # ax.set_title("accretion rates for low lambda")


# # Grid and minor ticks
# # Legend with frame
# # ax.legend(frameon=True, loc="best")

# handles = []
# labels = []

# handles.append(plt.Line2D([], [], color=Lcolor0, linestyle=Lstyle0, linewidth=Lwidth0))
# labels.append(aplha_str_1)
# # labels.append('M_dot_protostar')

# # handles.append(plt.Line2D([], [], color=Lcolor1, linestyle=Lstyle1, linewidth=Lwidth1))
# # labels.append('M_dot_outflow')

# # handles.append(plt.Line2D([], [], color=Lcolor2, linestyle=Lstyle2, linewidth=Lwidth2))
# # labels.append('M_dot_disk_acc')

# if plot_mat_2 is not None:
#     handles.append(plt.Line2D([], [], color=Lcolor1, linestyle=Lstyle1, linewidth=Lwidth1))
#     labels.append(alpha_str_2)

# if plot_mat_3 is not None:
#     handles.append(plt.Line2D([], [], color=Lcolor2, linestyle=Lstyle2, linewidth=Lwidth2))
#     labels.append(alpha_str_3)

# if plot_mat_4 is not None:
#     handles.append(plt.Line2D([], [], color=Lcolor3, linestyle=Lstyle3, linewidth=Lwidth3))
#     labels.append(alpha_str_4)


# leg = ax.legend(handles, labels, loc='best', frameon=False, fontsize=11)

# # Set legend text colors
# for text, color in zip(leg.get_texts(), [Lcolor0, Lcolor1, Lcolor2, Lcolor3]):
#     text.set_color(color)

# # for text, color in zip(leg.get_texts(), [Lcolor0, Lcolor1]):
# #     text.set_color(color)

# # Tight layout for clean spacing
# plt.tight_layout()
# plt.savefig('m_protostar_accretion.jpg', format='jpg', dpi=600)
# plt.show()

