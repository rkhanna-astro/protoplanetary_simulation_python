import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
import matplotlib.gridspec as gridspec
from matplotlib.ticker import ScalarFormatter
import matplotlib.ticker as ticker

# # plt.rcParams['font.family'] = 'sans-serif'
# # plt.rcParams['font.sans-serif'] = ['Arial']
# plt.rcParams['mathtext.fontset'] = 'stix'     # or 'cm', 'dejavuserif', 'stixsans'
# plt.rcParams['mathtext.rm'] = 'Times New Roman'  # serif font
# # plt.rcParams['mathtext.it'] = 'Times New Roman:italic'
# # plt.rcParams['mathtext.bf'] = 'Times New Roman:bold'

plt.rcParams['font.sans-serif'] = ['Times New Roman']
# plt.rcParams['mathtext.fontset'] = 'stix'     # or 'cm', 'dejavuserif', 'stixsans'
# plt.rcParams['mathtext.rm'] = 'Times New Roman'  # serif font
label_fsize = 18
plt.rcParams['font.size'] = 14
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = label_fsize
plt.rcParams['xtick.labelsize'] = 14
plt.rcParams['ytick.labelsize'] = 14
plt.rcParams['grid.linewidth'] = 1.5
plt.rcParams['grid.color'] = 'black'
plt.rcParams['grid.alpha'] = 0.7
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'

def plotme3times(plotmat_val, plotmat1_val=None, plotmat2_val=None, plotmat3_val=None, name = None, time_series=None):
    
    mps_accretion_paper = np.loadtxt("new_results\Protostar_accretion_Black_line_first_two_thousand_years_csv.csv", delimiter=",", skiprows=1)
    q_toomre_paper = np.loadtxt("new_results\Black_line_Toomre_parameter_Machida_2010_paper.csv", delimiter=",", skiprows=1)
    mps_vs_time = np.loadtxt("new_results\mps_GOOD_ONES_BLACK_LINE_csv.csv", delimiter=",", skiprows=1)

    mdisk_mps_time = np.loadtxt("new_results\Solid_black_line_Machia_2010_paper_csv.csv", delimiter=",", skiprows=1)

    mdisk_vs_mps = mdisk_mps_time.T
    mps_accretion_paper = mps_accretion_paper.T

    q_toom = q_toomre_paper.T
    mps_time = mps_vs_time.T
    print(mps_time[0])
    indexes = np.where((mps_time[0] >= 100) & (mps_time[0] <= 2000))
    all_times = mps_time[0][indexes]
    mass_ps = mps_time[1][indexes]

    # toom_ind = np.where((q_toom[0] >= mass_ps[0]) & (q_toom[0] <= mass_ps[-1]))
    # toom_ex = q_toom[1][toom_ind]
    # return

    time_evol = []
    dt = 50
    curr_time = 1.e2

    while curr_time <= 2.e3:
        time_evol.append(curr_time)
        curr_time += dt
    
    plotmat = plotmat_val[0]
    str0 = plotmat_val[1]

    plotmat1 = None
    str1 = None
    if plotmat1_val is not None:
        plotmat1 = plotmat1_val[0]
        str1 = plotmat1_val[1]
    
    plotmat2 = None
    str2 = None
    if plotmat2_val is not None:
        plotmat2 = plotmat2_val[0]
        str2 = plotmat2_val[1]

    plotmat3 = None
    str3 = None
    if plotmat3_val is not None:
        plotmat3 = plotmat3_val[0]
        str3 = plotmat3_val[1]

    # Set parameters
    frac_midtick = 0.45
    label_fsize = 18
    ticklength = [0.035, 0.035]
    XTick = [5, 10, 20, 30]
    XTick_time = [200, 500, 1000, 2000]
    
    # Line styles
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
    
    # Create figure with specific size (15.5cm x 17cm converted to inches)
    fig = plt.figure(figsize=(15.5/2.54, 17/2.54))
    
    # Create grid for subplots
    gs = gridspec.GridSpec(2, 2, wspace=0.0, hspace=0.0, 
                          left=0.1, right=0.9, bottom=0.1, top=0.9)
    
    # Extract data from plotmat
    r = plotmat[0,:]
    v_phi_cs = plotmat[1,:]
    cs = plotmat[2,:]
    vr_cs = plotmat[3,:]
    sigma = plotmat[4,:]
    Mdisk = plotmat[5,:]
    H_r = plotmat[6,:]
    Mdot_acc = plotmat[7,:]
    Qtoomre = plotmat[8,:]
    Mdot_w_Mdot_acc = plotmat[9,:]
    jmath = plotmat[10,:]
    
    xstart = 4
    xend = 38
    
    # ================== First Subplot (Top Left) ==================
    ax1 = fig.add_subplot(gs[0, 0])  # Spans rows 0-1, column 0
    
    # Plot velocities
    ax1.loglog(r, vr_cs / v_phi_cs, color=Lcolor0, linestyle=Lstyle0, linewidth=Lwidth0)
    # ax1.loglog(r, cs, color=Lcolor0, linestyle=Lstyle0, linewidth=Lwidth0)
    # ax1.loglog(r, vr_cs*cs, color=Lcolor0, linestyle=Lstyle0, linewidth=Lwidth0)
    
    # Plot additional datasets if provided
    if plotmat1 is not None:
        r1 = plotmat1[0,:]
        v_phi_cs1 = plotmat1[1,:]
        cs1 = plotmat1[2,:]
        vr_cs1 = plotmat1[3,:]
        ax1.loglog(r1, vr_cs1 / v_phi_cs1, color=Lcolor1, linestyle=Lstyle1, linewidth=Lwidth1)
        # ax1.loglog(r1, cs1, color=Lcolor1, linestyle=Lstyle1, linewidth=Lwidth1)
        # ax1.loglog(r1, vr_cs1*cs1, color=Lcolor1, linestyle=Lstyle1, linewidth=Lwidth1)
    
    if plotmat2 is not None:
        r2 = plotmat2[0,:]
        v_phi_cs2 = plotmat2[1,:]
        cs2 = plotmat2[2,:]
        vr_cs2 = plotmat2[3,:]
        ax1.loglog(r2, vr_cs2 / v_phi_cs2, color=Lcolor2, linestyle=Lstyle2, linewidth=Lwidth2)
        # ax1.loglog(r2, cs2, color=Lcolor2, linestyle=Lstyle2, linewidth=Lwidth2)
        # ax1.loglog(r2, vr_cs2*cs2, color=Lcolor2, linestyle=Lstyle2, linewidth=Lwidth2)
    
    if plotmat3 is not None:
        r3 = plotmat3[0,:]
        v_phi_cs3 = plotmat3[1,:]
        cs3 = plotmat3[2,:]
        vr_cs3 = plotmat3[3,:]
        ax1.loglog(r3, vr_cs3 / v_phi_cs3, color=Lcolor3, linestyle=Lstyle3, linewidth=Lwidth3)
        # ax1.loglog(r3, cs3, color=Lcolor3, linestyle=Lstyle3, linewidth=Lwidth3)
        # ax1.loglog(r3, vr_cs3*cs3, color=Lcolor3, linestyle=Lstyle3, linewidth=Lwidth3)
    
    # Set axis properties
    ax1.set_xlim([xstart, xend])
    ax1.set_ylim([0.002, 4])
    ax1.set_xticks(XTick)
    ax1.set_yticks([0.001, 0.01, 0.1])
    ax1.xaxis.set_major_formatter(ScalarFormatter())
    ax1.set_xticklabels([str(t) for t in XTick])
    ax1.xaxis.set_minor_locator(ticker.NullLocator())
    ax1.tick_params(axis='both', which='major', length=ticklength[0]*100*0.68)
    ax1.set_xlabel(r'radius (au)', fontsize=label_fsize)
    ax1.set_ylabel(r'$v_{r} / v_{\phi}$', fontsize=label_fsize)
    ax1.xaxis.tick_top()
    ax1.xaxis.set_label_position('top')
    
    # Add text labels
    # ax1.text(5, 1.23, r'$v_{\rm \phi}$', fontsize=15)
    # ax1.text(5, 0.19, r'$c_{\rm s}$', fontsize=15)
    # ax1.text(5, 0.020, r'$v_{\rm r}$', fontsize=15)
    
    # Add legend
    
    
    # Add horizontal reference lines
    # ax1.axhline(0.007, xmin=17/xend, xmax=30/xend, color=Lcolor0, linestyle='-', linewidth=Lwidth0)
    # ax1.axhline(0.00454, xmin=17/xend, xmax=30/xend, color=Lcolor1, linestyle='-', linewidth=Lwidth1)
    # ax1.axhline(0.00295, xmin=17/xend, xmax=30/xend, color=Lcolor2, linestyle='-', linewidth=Lwidth2)
    
    # ================== Second Subplot (Top Right) ==================
    # ax2 = fig.add_subplot(gs[1, 0])  # Row 0, column 1
    
    # if plotmat1 is not None:
    #     sigma1 = plotmat1[4,:]
    #     ax2.loglog(r1, sigma1, color=Lcolor1, linestyle=Lstyle1, linewidth=Lwidth1)
    
    # if plotmat2 is not None:
    #     sigma2 = plotmat2[4,:]
    #     ax2.loglog(r2, sigma2, color=Lcolor2, linestyle=Lstyle2, linewidth=Lwidth2)
    
    # if plotmat3 is not None:
    #     sigma3 = plotmat3[4,:]
    #     ax2.loglog(r3, sigma3, color=Lcolor3, linestyle=Lstyle3, linewidth=Lwidth3)
    
    # ax2.loglog(r, sigma, color=Lcolor0, linestyle=Lstyle0, linewidth=Lwidth0)
    # ax2.set_xlim([xstart, xend])
    # ax2.set_ylim([10, 4000])
    # ax2.set_xticks(XTick)
    # ax2.set_yticks([10, 100, 1000])
    # ax2.xaxis.set_major_formatter(ScalarFormatter())
    # ax2.set_xticklabels([str(t) for t in XTick])
    # ax2.xaxis.set_minor_locator(ticker.NullLocator())
    # ax2.tick_params(axis='both', which='major', length=ticklength[0]*100)
    # ax2.set_xlabel(r'radius (AU)', fontsize=label_fsize)
    # ax2.set_ylabel(r'$\sigma$ (g cm$^{-2}$)', fontsize=label_fsize)
    # # ax2.xaxis.tick_top()
    # # ax2.xaxis.set_label_position('top')
    
    # ================== Third Subplot (Middle Right) ==================
    ax3 = fig.add_subplot(gs[0, 1])  # Row 1, column 1
    
    if plotmat1 is not None:
        Mdot_acc1 = time_series['alpha2']['mps_acc']
        ax3.loglog(time_evol, Mdot_acc1, color=Lcolor1, linestyle=Lstyle1, linewidth=Lwidth1)
        # ax3.loglog(time_evol, time_series['alpha2']['mdisk_acc'], color=Lcolor1, linestyle=Lstyle1, linewidth=Lwidth1)
    
    if plotmat2 is not None:
        Mdot_acc2 = time_series['alpha3']['mps_acc']
        ax3.loglog(time_evol, Mdot_acc2, color=Lcolor2, linestyle=Lstyle2, linewidth=Lwidth2)
        # ax3.loglog(time_evol, time_series['alpha3']['mdisk_acc'], color=Lcolor2, linestyle=Lstyle2, linewidth=Lwidth2)
    
    if plotmat3 is not None:
        Mdot_acc3 = time_series['alpha4']['mps_acc']
        ax3.loglog(time_evol, Mdot_acc3, color=Lcolor3, linestyle=Lstyle3, linewidth=Lwidth3)
        # ax3.loglog(time_evol, time_series['alpha3']['mdisk_acc'], color=Lcolor3, linestyle=Lstyle3, linewidth=Lwidth3)
        
    
    ax3.loglog(time_evol, time_series['alpha1']['mps_acc'], color=Lcolor0, linestyle=Lstyle0, linewidth=Lwidth0)
    # ax3.axhline(np.mean(mps_accretion_paper[1]), color='purple', linestyle='--', linewidth=0.6)
    ax3.text(201.1, np.max(mps_accretion_paper[1]), 'Machida & Basu (2019)', fontsize=12, color='purple', va='bottom')
    ax3.loglog(mps_accretion_paper[0], mps_accretion_paper[1], color='purple', linestyle=Lstyle0, linewidth=Lwidth0)
    ax3.set_xlim([100, 2e3])
    ax3.set_ylim([5e-7, 2e-4])
    ax3.set_xticks(XTick_time)
    ax3.set_yticks([1e-6, 1e-5, 1e-4])
    ax3.xaxis.set_major_formatter(ScalarFormatter())
    ax3.set_xticklabels([str(t) for t in XTick_time])
    ax3.xaxis.set_minor_locator(ticker.NullLocator())
    ax3.tick_params(axis='both', which='major', length=ticklength[0]*100)
    ax3.set_xlabel(r'time (year)', fontsize=label_fsize)
    ax3.set_ylabel(r'$\dot{M}_{*}\, (\mathrm{M_{\odot} \, yr^{-1}})$', fontsize=label_fsize)
    ax3.yaxis.tick_right()
    ax3.yaxis.set_label_position('right')
    ax3.xaxis.tick_top()
    ax3.xaxis.set_label_position('top')
    
    # Add horizontal reference lines
    # Macc_Hunter = 5.723406e-5
    # Macc_Shu = 1.6306e-6
    # ax3.axhline(Macc_Hunter, color='purple', linestyle='--', linewidth=0.6)
    # ax3.axhline(Macc_Shu, color='purple', linestyle='--', linewidth=0.6)
    # ax3.text(11.1, Macc_Hunter, 'Hunter (1977)', fontsize=12, color='purple', va='bottom')
    # # bbox=dict(facecolor='white', edgecolor='none', pad=0.5)
    # ax3.text(13.5, Macc_Shu, 'Shu (1977)', fontsize=12, color='purple', va='bottom')
    
    # ================== Fourth Subplot (Bottom Left) ==================
    ax4 = fig.add_subplot(gs[1, 0])  # Row 2, column 0
    
    if plotmat1 is not None:
        r1 = plotmat1[0,:]
        Qtoomre1 = plotmat1[8,:]
        toomre1 = time_series['alpha2']['toomre']
        ax4.loglog(r1, Qtoomre1, color=Lcolor1, linestyle=Lstyle1, linewidth=Lwidth1)
    
    if plotmat2 is not None:
        r2 = plotmat2[0,:]
        Qtoomre2 = plotmat2[8,:]
        toomre2 = time_series['alpha3']['toomre']
        ax4.loglog(r2, Qtoomre2, color=Lcolor2, linestyle=Lstyle2, linewidth=Lwidth2)
    
    if plotmat3 is not None:
        r3 = plotmat3[0,:]
        Qtoomre3 = plotmat3[8,:]
        toomre3 = time_series['alpha4']['toomre']
        ax4.loglog(r3, Qtoomre3, color=Lcolor3, linestyle=Lstyle3, linewidth=Lwidth3)
    
    r = plotmat[0,:]
    toomre = time_series['alpha1']['toomre']
    ax4.loglog(r, plotmat[8,:], color=Lcolor0, linestyle=Lstyle0, linewidth=Lwidth0)

    handles = []
    labels = []

    handles.append(plt.Line2D([], [], color=Lcolor0, linestyle=Lstyle0, linewidth=Lwidth0))
    # labels.append(r'$\eta^{\prime}=10^{-1}$')
    labels.append(str0)
    
    if plotmat1 is not None:
        handles.append(plt.Line2D([], [], color=Lcolor1, linestyle=Lstyle1, linewidth=Lwidth1))
        labels.append(str1)
    
    if plotmat2 is not None:
        handles.append(plt.Line2D([], [], color=Lcolor2, linestyle=Lstyle2, linewidth=Lwidth2))
        labels.append(str2)
    
    if plotmat3 is not None:
        handles.append(plt.Line2D([], [], color=Lcolor3, linestyle=Lstyle3, linewidth=Lwidth3))
        labels.append(str3)
    
    
    leg = ax4.legend(handles, labels, loc='upper right', frameon=False, fontsize=12)
    
    # Set legend text colors
    for text, color in zip(leg.get_texts(), [Lcolor0, Lcolor1, Lcolor2, Lcolor3]):
        text.set_color(color)

    # max_mass = max(time_series['alpha2']['mps'][-1], time_series['alpha1']['mps'][-1], time_series['alpha3']['mps'][-1], time_series['alpha4']['mps'][-1])
    # min_mass  = min(time_series['alpha2']['mps'][0], time_series['alpha1']['mps'][0], time_series['alpha3']['mps'][0], time_series['alpha4']['mps'][0])

    # toom_ind = np.where((q_toom[0] >= min_mass) & (q_toom[0] <= max_mass))
    # toom_mass = q_toom[0][toom_ind]
    # toom_ex = q_toom[1][toom_ind]
    # print(toom_mass)
    # print(toom_ex)
    # print(np.mean(toom_ex))

    # ax4.axhline(np.mean(toom_ex), color='purple', linestyle='--', linewidth=0.6)
    # ax4.text(0.5, 0.2, 'Machida (2010)',
    #      transform=ax4.transAxes,
    #      fontsize=12, color='purple',
    #      ha='right', va='bottom')
    # ax4.text(1, 0.5, 'Machida (2010)', transform=ax4.transAxes, fontsize=5, color='purple', va='bottom')
    # ax4.loglog(toom_mass, toom_ex, color='purple', linestyle=Lstyle0, linewidth=Lwidth0)
    ax4.set_xlim(xstart, xend)
    ax4.set_ylim([0.39, 2])
    ax4.set_xticks(XTick)
    YTick = [0.5, 0.6, 1, 1.5]
    ax4.set_yticks(YTick)
    ax4.xaxis.set_major_formatter(ScalarFormatter())
    ax4.yaxis.set_major_formatter(ScalarFormatter())
    ax4.set_xticklabels([str(t) for t in XTick])
    ax4.set_yticklabels([str(t) for t in YTick])
    ax4.xaxis.set_minor_locator(ticker.NullLocator())
    ax4.yaxis.set_minor_locator(ticker.NullLocator())
    ax4.tick_params(axis='both', which='major', length=ticklength[0]*100)
    ax4.set_xlabel(r'radius (au)', fontsize=label_fsize)
    ax4.set_ylabel(r'$Q$', fontsize=label_fsize)
    ax4.yaxis.tick_left()
    ax4.yaxis.set_label_position('left')

    # ax4.axhline(2, color='purple', linestyle='--', linewidth=0.6)
    # ax4.axhline(1.5, color='purple', linestyle='--', linewidth=0.6)
    # ax4.axhline(1, color='purple', linestyle='--', linewidth=0.6)
    
    # ================== Fifth Subplot (Bottom Right) ==================
    ax5 = fig.add_subplot(gs[1, 1])  # Row 2, column 1

    print(mdisk_vs_mps[0])
    print(mdisk_vs_mps[1])

    max_mass = max(time_series['alpha2']['mps'][-1], time_series['alpha1']['mps'][-1], time_series['alpha3']['mps'][-1], time_series['alpha4']['mps'][-1])
    min_mass  = min(time_series['alpha2']['mps'][0], time_series['alpha1']['mps'][0], time_series['alpha3']['mps'][0], time_series['alpha4']['mps'][0])

    ratio = 1 / mdisk_vs_mps[1]
    print(ratio)

    indexes = np.where((mdisk_vs_mps[0] >= min_mass) & (mdisk_vs_mps[0] <= max_mass))

    print(np.mean(ratio[indexes]))
    
    if plotmat1 is not None:
        Mdot_w_Mdot_acc1 = plotmat1[9,:]
        ax5.loglog(time_evol, np.array(time_series['alpha2']['mps_acc']) / np.array(time_series['alpha2']['mdisk_acc']), color=Lcolor1, linestyle=Lstyle1, linewidth=Lwidth1)
        # ax5.loglog(time_evol, time_series['alpha2']['mdisk'], color=Lcolor1, linestyle=Lstyle1, linewidth=Lwidth1)
    
    if plotmat2 is not None:
        Mdot_w_Mdot_acc2 = plotmat2[9,:]
        ax5.loglog(time_evol, np.array(time_series['alpha3']['mps_acc']) / np.array(time_series['alpha3']['mdisk_acc']), color=Lcolor2, linestyle=Lstyle2, linewidth=Lwidth2)
        # ax5.loglog(time_evol, time_series['alpha3']['mdisk'], color=Lcolor2, linestyle=Lstyle2, linewidth=Lwidth2)
    
    if plotmat3 is not None:
        Mdot_w_Mdot_acc3 = plotmat3[9,:]
        ax5.loglog(time_evol, np.array(time_series['alpha4']['mps_acc']) / np.array(time_series['alpha4']['mdisk_acc']), color=Lcolor3, linestyle=Lstyle3, linewidth=Lwidth3)
        # ax5.loglog(time_evol, time_series['alpha4']['mdisk'], color=Lcolor3, linestyle=Lstyle3, linewidth=Lwidth3)
    
    ax5.loglog(time_evol, np.array(time_series['alpha1']['mps_acc']) / np.array(time_series['alpha1']['mdisk_acc']), color=Lcolor0, linestyle=Lstyle0, linewidth=Lwidth0)
    # ax5.loglog(time_evol, time_series['alpha1']['mdisk'], color=Lcolor0, linestyle=Lstyle0, linewidth=Lwidth0)
    # ax5.axhline(np.mean(ratio[indexes]), color='purple', linestyle='--', linewidth=0.6)
    ax5.set_xlim([100, 2e3])
    ax5.set_ylim([0.07, 2])
    ax5.set_xticks(XTick_time)
    ax5.set_yticks([0.1, 1])
    ax5.xaxis.set_major_formatter(ScalarFormatter())
    ax5.set_xticklabels([str(t) for t in XTick_time])
    ax5.set_yticklabels([0.1, 1])
    ax5.xaxis.set_minor_locator(ticker.NullLocator())
    ax5.tick_params(axis='both', which='major', length=ticklength[0]*100)
    ax5.set_ylabel(r'$\dot{M}_{*} /\dot{M}_{\mathrm{acc}}$', fontsize=label_fsize)
    ax5.set_xlabel(r'time (year)', fontsize=label_fsize)
    ax5.yaxis.tick_right()
    ax5.yaxis.set_label_position('right')
    ax5.xaxis.tick_bottom()
    ax5.xaxis.set_label_position('bottom')
    
    # Save figure
    # plt.grid(True)

    for ax in [ax1, ax3, ax4, ax5]:
        # for tick in ax.get_xticklabels():
        #     tick.set_fontweight('semibold')

        # # Make **y-tick labels** bold
        # for tick in ax.get_yticklabels():
        #     tick.set_fontweight('semibold')

        for spine in ax.spines.values():
            spine.set_linewidth(1.4)   # increase thickness
            spine.set_color('0.2')  # optional: change color
        ax.tick_params(axis='both', which='major', width=2, length=6)  # make ticks bold
        ax.tick_params(axis='both', which='minor', width=1, length=3)  # minor ticksa
        # ax.tick_params(direction='in', top=True, right=True)

    plt.tight_layout()
    if name is None:
        plt.savefig('finalPlot1.pdf', format='pdf', bbox_inches='tight')
    else:
        plt.savefig(f'{name}.pdf', format='pdf', bbox_inches='tight')
    plt.close()
