import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
import matplotlib.gridspec as gridspec
from matplotlib.ticker import ScalarFormatter
import matplotlib.ticker as ticker


# Use LaTeX for text rendering
# rc('text', usetex=True)
# rc('font', family='helvetica')
# rc('font', sans-serif=['helvetica'])

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial']

def plotme3times(plotmat, plotmat1=None, plotmat2=None, plotmat3=None, name = None):
    # Set parameters
    frac_midtick = 0.45
    label_fsize = 14
    ticklength = [0.035, 0.035]
    XTick = [5, 10, 20, 30]
    
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
    
    # Set global font sizes
    plt.rcParams['font.size'] = 11
    plt.rcParams['axes.titlesize'] = 11
    plt.rcParams['axes.labelsize'] = label_fsize
    plt.rcParams['xtick.labelsize'] = 11
    plt.rcParams['ytick.labelsize'] = 11
    
    # Create grid for subplots
    gs = gridspec.GridSpec(3, 2, wspace=0.0, hspace=0.0, 
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
    xend = 128
    
    # ================== First Subplot (Top Left) ==================
    ax1 = fig.add_subplot(gs[0:2, 0])  # Spans rows 0-1, column 0
    
    # Plot velocities
    ax1.loglog(r, v_phi_cs*cs, color=Lcolor0, linestyle=Lstyle0, linewidth=Lwidth0)
    ax1.loglog(r, cs, color=Lcolor0, linestyle=Lstyle0, linewidth=Lwidth0)
    ax1.loglog(r, vr_cs*cs, color=Lcolor0, linestyle=Lstyle0, linewidth=Lwidth0)
    
    # Plot additional datasets if provided
    if plotmat1 is not None:
        r1 = plotmat1[0,:]
        v_phi_cs1 = plotmat1[1,:]
        cs1 = plotmat1[2,:]
        vr_cs1 = plotmat1[3,:]
        ax1.loglog(r1, v_phi_cs1*cs1, color=Lcolor1, linestyle=Lstyle1, linewidth=Lwidth1)
        ax1.loglog(r1, cs1, color=Lcolor1, linestyle=Lstyle1, linewidth=Lwidth1)
        ax1.loglog(r1, vr_cs1*cs1, color=Lcolor1, linestyle=Lstyle1, linewidth=Lwidth1)
    
    if plotmat2 is not None:
        r2 = plotmat2[0,:]
        v_phi_cs2 = plotmat2[1,:]
        cs2 = plotmat2[2,:]
        vr_cs2 = plotmat2[3,:]
        ax1.loglog(r2, v_phi_cs2*cs2, color=Lcolor2, linestyle=Lstyle2, linewidth=Lwidth2)
        ax1.loglog(r2, cs2, color=Lcolor2, linestyle=Lstyle2, linewidth=Lwidth2)
        ax1.loglog(r2, vr_cs2*cs2, color=Lcolor2, linestyle=Lstyle2, linewidth=Lwidth2)
    
    if plotmat3 is not None:
        r3 = plotmat3[0,:]
        v_phi_cs3 = plotmat3[1,:]
        cs3 = plotmat3[2,:]
        vr_cs3 = plotmat3[3,:]
        ax1.loglog(r3, v_phi_cs3*cs3, color=Lcolor3, linestyle=Lstyle3, linewidth=Lwidth3)
        ax1.loglog(r3, cs3, color=Lcolor3, linestyle=Lstyle3, linewidth=Lwidth3)
        ax1.loglog(r3, vr_cs3*cs3, color=Lcolor3, linestyle=Lstyle3, linewidth=Lwidth3)
    
    # Set axis properties
    ax1.set_xlim([xstart, xend])
    ax1.set_ylim([0.002, 4])
    ax1.set_xticks(XTick)
    ax1.set_yticks([0.01, 0.1, 1])
    ax1.xaxis.set_major_formatter(ScalarFormatter())
    ax1.set_xticklabels([str(t) for t in XTick])
    ax1.xaxis.set_minor_locator(ticker.NullLocator())
    ax1.tick_params(axis='both', which='major', length=ticklength[0]*100*0.68)
    ax1.set_xlabel(r'radius (AU)', fontsize=label_fsize)
    ax1.set_ylabel(r'Velocity (km s$^{-1}$)', fontsize=label_fsize)
    ax1.xaxis.tick_top()
    ax1.xaxis.set_label_position('top')
    
    # Add text labels
    ax1.text(5, 1.23, r'$v_{\rm \phi}$', fontsize=15)
    ax1.text(5, 0.19, r'$c_{\rm s}$', fontsize=15)
    ax1.text(5, 0.020, r'$v_{\rm r}$', fontsize=15)
    
    # Add legend
    handles = []
    labels = []

    handles.append(plt.Line2D([], [], color=Lcolor0, linestyle=Lstyle0, linewidth=Lwidth0))
    labels.append(r'$\eta^{\prime}=10^{-1}$')
    
    if plotmat1 is not None:
        handles.append(plt.Line2D([], [], color=Lcolor1, linestyle=Lstyle1, linewidth=Lwidth1))
        labels.append(r'$\eta^{\prime}=10^{-2}$')
    
    if plotmat2 is not None:
        handles.append(plt.Line2D([], [], color=Lcolor2, linestyle=Lstyle2, linewidth=Lwidth2))
        labels.append(r'$\eta^{\prime}=10^{-3}$')
    
    if plotmat3 is not None:
        handles.append(plt.Line2D([], [], color=Lcolor3, linestyle=Lstyle3, linewidth=Lwidth3))
        labels.append(r'$\eta^{\prime}=10^{-4}$')
    
    
    leg = ax1.legend(handles, labels, loc='lower right', frameon=False, fontsize=11)
    
    # Set legend text colors
    for text, color in zip(leg.get_texts(), [Lcolor0, Lcolor1, Lcolor2, Lcolor3]):
        text.set_color(color)
    
    # Add horizontal reference lines
    # ax1.axhline(0.007, xmin=17/xend, xmax=30/xend, color=Lcolor0, linestyle='-', linewidth=Lwidth0)
    # ax1.axhline(0.00454, xmin=17/xend, xmax=30/xend, color=Lcolor1, linestyle='-', linewidth=Lwidth1)
    # ax1.axhline(0.00295, xmin=17/xend, xmax=30/xend, color=Lcolor2, linestyle='-', linewidth=Lwidth2)
    
    # ================== Second Subplot (Top Right) ==================
    ax2 = fig.add_subplot(gs[2, 0])  # Row 0, column 1
    
    if plotmat1 is not None:
        sigma1 = plotmat1[4,:]
        ax2.loglog(r1, sigma1, color=Lcolor1, linestyle=Lstyle1, linewidth=Lwidth1)
    
    if plotmat2 is not None:
        sigma2 = plotmat2[4,:]
        ax2.loglog(r2, sigma2, color=Lcolor2, linestyle=Lstyle2, linewidth=Lwidth2)
    
    if plotmat3 is not None:
        sigma3 = plotmat3[4,:]
        ax2.loglog(r3, sigma3, color=Lcolor3, linestyle=Lstyle3, linewidth=Lwidth3)
    
    ax2.loglog(r, sigma, color=Lcolor0, linestyle=Lstyle0, linewidth=Lwidth0)
    ax2.set_xlim([xstart, xend])
    ax2.set_ylim([10, 4000])
    ax2.set_xticks(XTick)
    ax2.set_yticks([10, 100, 1000])
    ax2.xaxis.set_major_formatter(ScalarFormatter())
    ax2.set_xticklabels([str(t) for t in XTick])
    ax2.xaxis.set_minor_locator(ticker.NullLocator())
    ax2.tick_params(axis='both', which='major', length=ticklength[0]*100)
    ax2.set_xlabel(r'radius (AU)', fontsize=label_fsize)
    ax2.set_ylabel(r'$\sigma$ (g cm$^{-2}$)', fontsize=label_fsize)
    # ax2.xaxis.tick_top()
    # ax2.xaxis.set_label_position('top')
    
    # ================== Third Subplot (Middle Right) ==================
    ax3 = fig.add_subplot(gs[0, 1])  # Row 1, column 1
    
    if plotmat1 is not None:
        Mdot_acc1 = plotmat1[7,:]
        ax3.loglog(r1, Mdot_acc1, color=Lcolor1, linestyle=Lstyle1, linewidth=Lwidth1)
    
    if plotmat2 is not None:
        Mdot_acc2 = plotmat2[7,:]
        ax3.loglog(r2, Mdot_acc2, color=Lcolor2, linestyle=Lstyle2, linewidth=Lwidth2)
    
    if plotmat3 is not None:
        Mdot_acc3 = plotmat3[7,:]
        ax3.loglog(r3, Mdot_acc3, color=Lcolor3, linestyle=Lstyle3, linewidth=Lwidth3)
    
    ax3.loglog(r, Mdot_acc, color=Lcolor0, linestyle=Lstyle0, linewidth=Lwidth0)
    ax3.set_xlim([xstart, xend])
    ax3.set_ylim([5e-7, 2e-4])
    ax3.set_xticks(XTick)
    ax3.set_yticks([1e-6, 1e-5, 1e-4])
    ax3.xaxis.set_major_formatter(ScalarFormatter())
    ax3.set_xticklabels([str(t) for t in XTick])
    ax3.xaxis.set_minor_locator(ticker.NullLocator())
    ax3.tick_params(axis='both', which='major', length=ticklength[0]*100)
    ax3.set_xlabel(r'radius (AU)', fontsize=label_fsize)
    ax3.set_ylabel(r'$\dot{M}_{\rm acc}$ (M$_\odot$ yr$^{-1}$)', fontsize=label_fsize)
    ax3.yaxis.tick_right()
    ax3.yaxis.set_label_position('right')
    ax3.xaxis.tick_top()
    ax3.xaxis.set_label_position('top')
    
    # Add horizontal reference lines
    Macc_Hunter = 5.723406e-5
    Macc_Shu = 1.6306e-6
    ax3.axhline(Macc_Hunter, color='purple', linestyle='--', linewidth=0.6)
    ax3.axhline(Macc_Shu, color='purple', linestyle='--', linewidth=0.6)
    ax3.text(11.1, Macc_Hunter, 'Hunter (1977)', fontsize=12, color='purple', va='bottom')
    # bbox=dict(facecolor='white', edgecolor='none', pad=0.5)
    ax3.text(13.5, Macc_Shu, 'Shu (1977)', fontsize=12, color='purple', va='bottom')
    
    # ================== Fourth Subplot (Bottom Left) ==================
    ax4 = fig.add_subplot(gs[2, 1])  # Row 2, column 0
    
    if plotmat1 is not None:
        Qtoomre1 = plotmat1[8,:]
        ax4.loglog(r1, Qtoomre1, color=Lcolor1, linestyle=Lstyle1, linewidth=Lwidth1)
    
    if plotmat2 is not None:
        Qtoomre2 = plotmat2[8,:]
        ax4.loglog(r2, Qtoomre2, color=Lcolor2, linestyle=Lstyle2, linewidth=Lwidth2)
    
    if plotmat3 is not None:
        Qtoomre3 = plotmat3[8,:]
        ax4.loglog(r3, Qtoomre3, color=Lcolor3, linestyle=Lstyle3, linewidth=Lwidth3)
    
    ax4.loglog(r, Qtoomre, color=Lcolor0, linestyle=Lstyle0, linewidth=Lwidth0)
    ax4.set_xlim([xstart, xend])
    ax4.set_ylim([0.39, 5.2])
    ax4.set_xticks(XTick)
    YTick = [0.5, 1, 1.5, 2, 5]
    ax4.set_yticks(YTick)
    ax4.xaxis.set_major_formatter(ScalarFormatter())
    ax4.yaxis.set_major_formatter(ScalarFormatter())
    ax4.set_xticklabels([str(t) for t in XTick])
    ax4.set_yticklabels([str(t) for t in YTick])
    ax4.xaxis.set_minor_locator(ticker.NullLocator())
    # ax4.yaxis.set_minor_locator(ticker.NullLocator())
    ax4.tick_params(axis='both', which='major', length=ticklength[0]*100)
    ax4.set_xlabel(r'radius (AU)', fontsize=label_fsize)
    ax4.set_ylabel(r'$Q$', fontsize=label_fsize)
    ax4.yaxis.tick_right()
    ax4.yaxis.set_label_position('right')

    ax4.axhline(2, color='purple', linestyle='--', linewidth=0.6)
    ax4.axhline(1.5, color='purple', linestyle='--', linewidth=0.6)
    ax4.axhline(1, color='purple', linestyle='--', linewidth=0.6)
    
    # ================== Fifth Subplot (Bottom Right) ==================
    ax5 = fig.add_subplot(gs[1, 1])  # Row 2, column 1
    
    if plotmat1 is not None:
        Mdot_w_Mdot_acc1 = plotmat1[9,:]
        ax5.loglog(r1, Mdot_w_Mdot_acc1, color=Lcolor1, linestyle=Lstyle1, linewidth=Lwidth1)
    
    if plotmat2 is not None:
        Mdot_w_Mdot_acc2 = plotmat2[9,:]
        ax5.loglog(r2, Mdot_w_Mdot_acc2, color=Lcolor2, linestyle=Lstyle2, linewidth=Lwidth2)
    
    if plotmat3 is not None:
        Mdot_w_Mdot_acc3 = plotmat3[9,:]
        ax5.loglog(r3, Mdot_w_Mdot_acc3, color=Lcolor3, linestyle=Lstyle3, linewidth=Lwidth3)
    
    ax5.loglog(r, Mdot_w_Mdot_acc, color=Lcolor0, linestyle=Lstyle0, linewidth=Lwidth0)
    ax5.set_xlim([xstart, xend])
    ax5.set_ylim([0.007, 1.2])
    ax5.set_xticks(XTick)
    ax5.set_yticks([0.01, 0.1, 1.0])
    ax5.xaxis.set_major_formatter(ScalarFormatter())
    ax5.set_xticklabels([str(t) for t in XTick])
    ax5.xaxis.set_minor_locator(ticker.NullLocator())
    ax5.tick_params(axis='both', which='major', length=ticklength[0]*100)
    ax5.set_ylabel(r'$M_{\rm disk}/M_{\rm env}$', fontsize=label_fsize)
    ax5.yaxis.tick_right()
    ax5.yaxis.set_label_position('right')
    
    # Save figure
    plt.tight_layout()
    if name is None:
        plt.savefig('finalPlot1.pdf', format='pdf', bbox_inches='tight')
    else:
        plt.savefig(f'{name}.pdf', format='pdf', bbox_inches='tight')
    plt.close()
