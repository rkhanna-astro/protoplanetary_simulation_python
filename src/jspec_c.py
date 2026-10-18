import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

def jspec(tpsArr_eta2, tpsArr_eta2nw, J_tot_pre_eta2, M_tot_pre_eta2, J_tot_eta2, 
          M_tot_eta2, J_tot_post_eta2, M_tot_post_eta2, J_tot_pre_eta2nw, M_tot_pre_eta2nw, 
          J_tot_eta2nw, M_tot_eta2nw, J_tot_post_eta2nw, M_tot_post_eta2nw, ax):
    frac_midtick = 0.45
    label_fsize = 14
    ticklength = [0.02, 0.02]

    Lstyle1 = '-'
    Lstyle2 = '--'
    Lstyle3 = '-'
    Lstyle4 = '-'
    Lwidth1 = 1.0
    Lwidth2 = 1.0
    Lwidth3 = 1.0
    Lwidth4 = 1.0
    Lcolor1 = [0, 0.4157, 1]  # 'blue'
    Lcolor2 = [0.3, 0.9333, 0]  # 'green'
    Lcolor3 = [1, 0.3333, 0]  # 'red'
    Lcolor4 = [0, 0.82, 0.82]  # cyan
    Lcolor5 = [0.84, 0.49, 0.18]  # burned brown
    Lcolor6 = 'magenta'  # brown

    # fig, ax = plt.subplots(figsize=(15 / 2.54, 15 / 2.54))  # Convert cm to inches
    # ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    ax.tick_params(direction='in', length=5, width=1.4)

    ax.set_xlabel(r'$\rm time ~(\rm yr)$', fontsize=label_fsize)
    ax.set_ylabel(r'${J}_{\rm disk}/{M}_{\rm disk}~(\rm cm^2 s^{-1})$', fontsize=label_fsize)
    ax.set_xlim([1000, 3000])
    # ax.set_ylim([1.e+19, 15.e+19])
    ax.tick_params(length=ticklength[0] * 72, width=1.4)  # Convert cm to points
    ax.set_yticks([ i*1e19 for i in range(1, 24, 2)])
    ax.set_xticks([ x for x in range(1000, 3000, 250)])

    # val = J_tot_eta2 / M_tot_eta2
    # print("Checking Jdisk", M_tot_eta2)

    ax.plot(tpsArr_eta2, 1.e4 * (J_tot_pre_eta2 / M_tot_pre_eta2), color=Lcolor1, linewidth=Lwidth1, linestyle=Lstyle1)
    ax.plot(tpsArr_eta2, 1.e4 * (J_tot_eta2 / M_tot_eta2), color=Lcolor2, linewidth=Lwidth2, linestyle=Lstyle1)
    # div_corrected = 0.994 * J_tot_post_eta2 / M_tot_post_eta2
    # div_corrected[-3:] = 1.02 * div_corrected[-3:]  # Manual correction
    ax.plot(tpsArr_eta2, 1.e4 * (J_tot_post_eta2 / M_tot_post_eta2), color=Lcolor3, linewidth=Lwidth3, linestyle=Lstyle1)

    ax.plot(tpsArr_eta2nw, 1.e4 * (J_tot_pre_eta2nw / M_tot_pre_eta2nw), color=Lcolor1, linewidth=Lwidth1, linestyle=Lstyle2)
    ax.plot(tpsArr_eta2nw, 1.e4 * (J_tot_eta2nw / M_tot_eta2nw), color=Lcolor2, linewidth=Lwidth1, linestyle=Lstyle2)
    ax.plot(tpsArr_eta2nw, 1.e4 * (J_tot_post_eta2nw / M_tot_post_eta2nw), color=Lcolor3, linewidth=Lwidth1, linestyle=Lstyle2)

    ax.fill_between(tpsArr_eta2, 1.e4 * (J_tot_pre_eta2 / M_tot_pre_eta2), 1.e4 * (J_tot_pre_eta2nw / M_tot_pre_eta2nw), color=Lcolor1, alpha=0.2)
    ax.fill_between(tpsArr_eta2, 1.e4 * (J_tot_eta2 / M_tot_eta2), 1.e4 * (J_tot_eta2nw / M_tot_eta2nw), color=Lcolor2, alpha=0.2)
    ax.fill_between(tpsArr_eta2, 1.e4 * (J_tot_post_eta2 / M_tot_post_eta2), 1.e4 * (J_tot_post_eta2nw / M_tot_post_eta2nw), color=Lcolor3, alpha=0.2)

    ax.text(2000, 1.46e20, r'$\alpha_0 = 0.3$', fontsize=12, color=Lcolor1, fontweight='bold')
    ax.text(2300, 1.11e20, r'$\alpha_0 = 0.5$', fontsize=12, color=Lcolor2, fontweight='bold')
    ax.text(2600, 7.2e19, r'$\alpha_0 = 0.7$', fontsize=12, color=Lcolor3, fontweight='bold')

    # ax.yaxis.set_major_locator(ticker.MultipleLocator(3))  # spacing = 1

    handles = []
    labels = []

    str1 = r'$\Lambda_0 = 0.1$'
    str2 = r'$\Lambda_0 = 0.0$'
    
    handles.append(plt.Line2D([], [], color='black', linestyle='-', linewidth=0.8))
    labels.append(str1)

    handles.append(plt.Line2D([], [], color='black', linestyle='--', linewidth=0.8))
    labels.append(str2)
    
    leg = ax.legend(handles, labels, loc='upper left', frameon=False, fontsize=14)
    ax.ticklabel_format(style='sci', axis='y', scilimits=(19,19))

    for spine in ax.spines.values():
        spine.set_linewidth(2)
        spine.set_color('black')

# --- Make ticks bold black ---
    ax.tick_params(axis='both', which='both', width=2, color='black', direction='in', length=6)

# --- Make tick labels bold black ---
    # for label in ax.get_xticklabels() + ax.get_yticklabels():
    #     label.set_fontweight('bold')
    #     label.set_color('black')

    # plt.tight_layout()
    # plt.savefig('figure_8.pdf', format='pdf')
    # plt.close()

# Example usage
# tpsArr_eta2 = np.linspace(1000, 3000, 100)
# tpsArr_eta2nw = np.linspace(1000, 3000, 100)
# J_tot_pre_eta2 = np.random.rand(100) * 1e20
# M_tot_pre_eta2 = np.random.rand(100) * 1e20
# J_tot_eta2 = np.random.rand(100) * 1e20
# M_tot_eta2 = np.random.rand(100) * 1e20
# J_tot_post_eta2 = np.random.rand(100) * 1e20
# M_tot_post_eta2 = np.random.rand(100) * 1e20
# J_tot_pre_eta2nw = np.random.rand(100) * 1e20
# M_tot_pre_eta2nw = np.random.rand(100) * 1e20
# J_tot_eta2nw = np.random.rand(100) * 1e20
# M_tot_eta2nw = np.random.rand(100) * 1e20
# J_tot_post_eta2nw = np.random.rand(100) * 1e20
# M_tot_post_eta2nw = np.random.rand(100) * 1e20

# jspec(tpsArr_eta2, tpsArr_eta2nw, J_tot_pre_eta2, M_tot_pre_eta2, J_tot_eta2, M_tot_eta2, J_tot_post_eta2, M_tot_post_eta2, J_tot_pre_eta2nw, M_tot_pre_eta2nw, J_tot_eta2nw, M_tot_eta2nw, J_tot_post_eta2nw, M_tot_post_eta2nw)