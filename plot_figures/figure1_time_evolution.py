import numpy as np
import time
import process
import plot_me_3times
import menv
import matplotlib.pyplot as plt
from matplotlib import rc
import matplotlib.gridspec as gridspec
from matplotlib.ticker import ScalarFormatter
import matplotlib.ticker as ticker

# Constants and initial parameters
tps = 5.e2
x_sh_test = 1.0
# gamma_eff = 1.1
# etaprime = 1.e-2
Mdot_stable = -999
dt = 50  # time increment [yr]
Minfall = 6.1341e-5  # 1.4086e-5 | 2.8509e-5 | 6.1341e-5

M_outflow = []

# Initialize storage dictionaries
results = {
    # 'post_eta2': {'tps': [], 'Mdisk': [], 'Ewind': [], 'alpha': 0.1, 'func': 'process'},
    # 'post_eta2nw': {'tps': [], 'Mdisk': [], 'Ewind': [], 'alpha': 0.2, 'func': 'process'},
    'eta2': {'tps': [], 'Mdisk': [], 'Ewind': [], 'alpha': 0.5, 'etaprime': 0.01, 'gamma': 1.1, 'lambda': 0.1, 'func': 'process'},
    # 'eta2nw': {'tps': [], 'Mdisk': [], 'Ewind': [], 'alpha': 0.5, 'etaprime': 0.01, 'gamma': 1.1, 'lambda': 0.1, 'func': 'process'},
    # 'pre_eta2': {'tps': [], 'Mdisk': [], 'Ewind': [], 'alpha': 0.5, 'etaprime': 0.01, 'gamma': 1.1, 'lambda': 0.2, 'func': 'process'},
    # 'pre_eta2nw': {'tps': [], 'Mdisk': [], 'Ewind': [], 'alpha': 0.5, 'etaprime': 0.1, 'gamma': 1.1, 'lambda': 0.5, 'func': 'process'}
}

def run_simulation(result_key):
    """Run simulation for a given configuration"""
    tps = 5.e2
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

# ii = 1
# time_evol = []
# curr_time = 1.e2

for key in results.keys():
    dict[key] = run_simulation(key)

time_str_1 = r't = 500 yr'
time_str_2 = r't = 1000 yr'
time_str_3 = r't = 2000 yr'
time_str_4 = r't = 3000 yr'

plot_mat_1 = dict['eta2']['pf1']
plot_mat_2 = dict['eta2']['pf11']
plot_mat_3 = dict['eta2']['pf31']
plot_mat_4 = dict['eta2']['pf51']

plot_me_3times.plotme3times((plot_mat_1, time_str_1), (plot_mat_2, time_str_2), (plot_mat_3, time_str_3), (plot_mat_4, time_str_4), 'figure_1')

# while curr_time < 2.e3:
#     M_dot_winds = (dict['eta2'][f'pf{ii}'][17, :][-1])
#     M_outflow.append(M_dot_winds)
#     time_evol.append(curr_time)
#     curr_time += 50
#     print(curr_time)
#     ii += 1

# # Convert lists to numpy arrays for easier handling
# for key in results.keys():
#     results[key]['tps'] = np.array(results[key]['tps'])
#     results[key]['Mdisk'] = np.array(results[key]['Mdisk'])
#     results[key]['Ewind'] = np.array(results[key]['Ewind'])

# plot_mat_1 = dict['eta2']['pf17']
# plot_mat_2 = dict['eta2nw']['pf17']
# plot_mat_3 = dict['pre_eta2']['pf17']
# plot_mat_4 = dict['pre_eta2nw']['pf17']



# # time_str_1 = r'$\Lambda_0 = 0.1 \,\, & \,\, \eta^{\prime}=10^{-3}$'
# # time_str_2 = r'$\Lambda_0 = 0.1 \,\, & \,\, \eta^{\prime}=10^{-2}$'
# # time_str_3 = r'$\Lambda_0 = 0.2 \,\, & \,\, \eta^{\prime}=10^{-2}$'
# # time_str_4 = r'$\Lambda_0 = 0.5 \,\, & \,\, \eta^{\prime}=10^{-1}$'

# # plot_me_3times.plotme3times((plot_mat_1, time_str_1), (plot_mat_2, time_str_2), (plot_mat_3, time_str_3), (plot_mat_4, time_str_4), 'figure_1')

# # Access results like this:
# # post_eta2_tps = results['post_eta2']['tps']
# # post_eta2_Mdisk = results['post_eta2']['Mdisk']
# # etc.

# # -------------------
# # Example Data
# # -------------------
# # -------------------
# # Plot Style Settings
# # -------------------
# # plt.rcParams.update({
# #     "text.usetex": False,             # Set True if you want LaTeX rendering
# #     "font.family": "serif",           # Clean serif font
# #     "font.size": 14,                  # General font size
# #     "axes.labelsize": 16,             # Axis label size
# #     "axes.titlesize": 16,             # Title size
# #     "xtick.labelsize": 13,
# #     "ytick.labelsize": 13,
# #     "legend.fontsize": 13,
# #     "figure.figsize": (7, 5),         # Figure size in inches
# #     "lines.linewidth": 2,
# #     "lines.markersize": 6,
# # })

# # -------------------
# # Create Plot
# # -------------------
# # fig, ax = plt.subplots()
# # ax.plot(time_evol, M_outflow, marker="o", color="royalblue", label="Sample Data")

# # # Set logarithmic y-axis
# # # ax.set_yscale("log")
# # ax.set_ylim(1e-6, 1e-5)

# # # Labels and title
# # ax.set_xlabel("Time (Yr)")
# # ax.set_ylabel("M_outflow_rate")
# # ax.set_title("Time Evolution of M_outflow")

# # # Grid and minor ticks
# # ax.grid(True, which="both", ls="--", lw=0.7, alpha=0.7)
# # ax.minorticks_on()

# # # Legend with frame
# # # ax.legend(frameon=True, loc="best")

# # # Tight layout for clean spacing
# # plt.tight_layout()
# # plt.show()

# frac_midtick = 0.45
# label_fsize = 14
# ticklength = [0.035, 0.035]
# XTick = [5, 10, 20, 30, 50]

# # Line styles
# Lstyle0 = '-'
# Lstyle1 = '--'
# Lstyle2 = '-.'
# Lstyle3 = ':'
# Lwidth0 = 0.8
# Lwidth1 = 0.8
# Lwidth2 = 0.8
# Lwidth3 = 0.8
# Lcolor0 = np.array([0, 0.4157, 1])       # blue
# Lcolor1 = np.array([0.3, 0.9333, 0])     # green
# Lcolor2 = np.array([1, 0.3333, 0])       # red
# Lcolor3 = 'magenta'

# # Create figure with specific size (15.5cm x 17cm converted to inches)
# fig = plt.figure()

# # Set global font sizes
# plt.rcParams['font.size'] = 11
# plt.rcParams['axes.titlesize'] = 11
# plt.rcParams['axes.labelsize'] = label_fsize
# plt.rcParams['xtick.labelsize'] = 11
# plt.rcParams['ytick.labelsize'] = 11

# plt.rcParams['mathtext.fontset'] = 'stix'     # or 'cm', 'dejavuserif', 'stixsans'
# plt.rcParams['mathtext.rm'] = 'Times New Roman'  # serif font
# # plt.rcParams['mathtext.it'] = 'Times New Roman:italic'
# plt.rcParams['mathtext.bf'] = 'Times New Roman:bold'

# # Create grid for subplots
# gs = gridspec.GridSpec(3, 2, wspace=0.0, hspace=0.0, 
#                         left=0.1, right=0.9, bottom=0.1, top=0.9)

# # Extract data from plot_mat_1
# r = plot_mat_1[0,:]
# vphi_cs = plot_mat_1[1,:]
# vr_cs = plot_mat_1[3,:]
# qtoomre = plot_mat_1[8,:]

# number_dens = vr_cs / vphi_cs

# xstart = 4
# xend = 38

# # ================== First Subplot (Top Left) ==================
# ax1 = fig.add_subplot()  # Spans rows 0-1, column 0

# # Plot velocities
# ax1.loglog(r, qtoomre, color=Lcolor0, linestyle=Lstyle0, linewidth=Lwidth0)

# # Plot additional datasets if provided
# if plot_mat_2 is not None:
#     r1 = plot_mat_2[0,:]
#     vphi_cs = plot_mat_2[1,:]
#     vr_cs = plot_mat_2[3,:]
#     qtoomre = plot_mat_2[8,:]

#     number_dens_2 = vr_cs / vphi_cs
#     ax1.loglog(r1, qtoomre, color=Lcolor1, linestyle=Lstyle1, linewidth=Lwidth1)

# if plot_mat_3 is not None:
#     r2 = plot_mat_3[0,:]
#     vphi_cs = plot_mat_3[1,:]
#     vr_cs = plot_mat_3[3,:]
#     qtoomre = plot_mat_3[8,:]

#     number_dens_3 = vr_cs / vphi_cs
#     ax1.loglog(r2, qtoomre, color=Lcolor2, linestyle=Lstyle2, linewidth=Lwidth2)

# if plot_mat_4 is not None:
#     r3 = plot_mat_4[0,:]
#     vphi_cs = plot_mat_4[1,:]
#     vr_cs = plot_mat_4[3,:]
#     qtoomre = plot_mat_4[8,:]


#     number_dens_4 = vr_cs / vphi_cs
#     ax1.loglog(r3, qtoomre, color=Lcolor3, linestyle=Lstyle3, linewidth=Lwidth3)

# # Set axis properties
# ax1.set_xlim([xstart, xend])
# # ax1.set_ylim([10e-5, 10e-2])
# ax1.set_xticks(XTick)
# # ax1.set_yticks([0.01, 0.1, 1])
# ax1.xaxis.set_major_formatter(ScalarFormatter())
# ax1.set_xticklabels([str(t) for t in XTick])
# ax1.xaxis.set_minor_locator(ticker.NullLocator())
# # ax1.xaxis.set_minor_locator(ticker.AutoMinorLocator())
# ax1.tick_params(axis='both', which='major', length=ticklength[0]*100*0.68)
# ax1.set_xlabel(r'$radius \, (AU)$', fontsize=label_fsize)
# ax1.set_ylabel(r'$Q$', fontsize=label_fsize)
# ax1.xaxis.tick_bottom()
# ax1.xaxis.set_label_position('bottom')
# # ax1.set_title('eta = 0.01 and lambda0 = 0.4')

# for tick in ax1.get_xticklabels():
#     tick.set_fontweight('semibold')

# # Make **y-tick labels** bold
# for tick in ax1.get_yticklabels():
#     tick.set_fontweight('semibold')

# for spine in ax1.spines.values():
#     spine.set_linewidth(2)   # increase thickness
#     spine.set_color('0.2')  # optional: change color
# ax1.tick_params(axis='both', which='major', width=1, length=4)  # make ticks bold
# ax1.tick_params(axis='both', which='minor', width=1, length=2)  # minor ticksa

# handles = []
# labels = []

# handles.append(plt.Line2D([], [], color=Lcolor0, linestyle=Lstyle0, linewidth=Lwidth0))
# # labels.append(r'$\eta^{\prime}=10^{-1}$')
# labels.append(time_str_1)

# if plot_mat_2 is not None:
#     handles.append(plt.Line2D([], [], color=Lcolor1, linestyle=Lstyle1, linewidth=Lwidth1))
#     labels.append(time_str_2)

# if plot_mat_3 is not None:
#     handles.append(plt.Line2D([], [], color=Lcolor2, linestyle=Lstyle2, linewidth=Lwidth2))
#     labels.append(time_str_3)

# if plot_mat_4 is not None:
#     handles.append(plt.Line2D([], [], color=Lcolor3, linestyle=Lstyle3, linewidth=Lwidth3))
#     labels.append(time_str_4)


# leg = ax1.legend(handles, labels, loc='best', frameon=False, fontsize=11)

# # Set legend text colors
# for text, color in zip(leg.get_texts(), [Lcolor0, Lcolor1, Lcolor2, Lcolor3]):
#     text.set_color(color)

# plt.tight_layout()
# plt.savefig('finalPlot1.pdf', format='pdf', bbox_inches='tight')
# plt.savefig('qtoomre.jpg', format='jpg', dpi=600)
# plt.close()
