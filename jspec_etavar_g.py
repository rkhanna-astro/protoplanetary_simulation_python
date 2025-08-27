import numpy as np
import matplotlib.pyplot as plt

def jspec_etavar(
        tpsArr_eta1, J_tot_pre_eta1, M_tot_pre_eta1, J_tot_eta1, M_tot_eta1, J_tot_post_eta1, M_tot_post_eta1,
        tpsArr_eta2, J_tot_pre_eta2, M_tot_pre_eta2, J_tot_eta2, M_tot_eta2, J_tot_post_eta2, M_tot_post_eta2,
        tpsArr_eta3, J_tot_pre_eta3, M_tot_pre_eta3, J_tot_eta3, M_tot_eta3, J_tot_post_eta3, M_tot_post_eta3
):
    frac_midtick = 0.45
    label_fsize = 14
    ticklength = [0.02, 0.02]

    colors = {
        "Lcolor1": [0, 0.4157, 1],
        "Lcolor2": [0.3, 0.9333, 0],
        "Lcolor3": [1, 0.3333, 0],
    }

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.tick_params(direction='in', length=5, width=1.4)

    xstart, xend = 1000, 3000
    # ystart, yend = 1.e+20, 17.e+20
    ax.set_xlim([xstart, xend])
    # ax.set_ylim([ystart, yend])

    y11 = 1.e4 * (J_tot_pre_eta1 / M_tot_pre_eta1)
    y12 = 1.e4 * (J_tot_pre_eta2 / M_tot_pre_eta2)
    y13 = 1.e4 * (J_tot_pre_eta3 / M_tot_pre_eta3)
    # print(J_tot_pre_eta3)
    print("Y13", y13)

    y21 = 1.e4 * (J_tot_eta1 / M_tot_eta1)
    y22 = 1.e4 * (J_tot_eta2 / M_tot_eta2)
    y23 = 1.e4 * (J_tot_eta3 / M_tot_eta3)

    div_corrected = J_tot_post_eta2 / M_tot_post_eta2
    # div_corrected[-3:] *= 1.02  # Manual correction

    y31 = 1.e4 * (J_tot_post_eta1 / M_tot_post_eta1)
    y32 = 1.e4 * div_corrected
    y33 = 1.e4 * (J_tot_post_eta3 / M_tot_post_eta3)

    ax.plot(tpsArr_eta1, y11, color=colors["Lcolor1"])
    ax.plot(tpsArr_eta2, y12, linestyle='--', color=colors["Lcolor1"])
    ax.plot(tpsArr_eta3, y13, linestyle='-.', color=colors["Lcolor1"])

    ax.plot(tpsArr_eta1, y21, color=colors["Lcolor2"])
    ax.plot(tpsArr_eta2, y22, linestyle='--', color=colors["Lcolor2"])
    ax.plot(tpsArr_eta3, y23, linestyle='-.', color=colors["Lcolor2"])

    ax.plot(tpsArr_eta1, y31, color=colors["Lcolor3"])
    ax.plot(tpsArr_eta2, y32, linestyle='--', color=colors["Lcolor3"])
    ax.plot(tpsArr_eta3, y33, linestyle='-.', color=colors["Lcolor3"])

    ax.text(2000, 1.11e20, r'$\alpha_0 = 0.3$', fontsize=11, color='black', fontweight='bold')
    ax.text(2300, 8.7e19, r'$\alpha_0 = 0.5$', fontsize=11, color='black', fontweight='bold')
    ax.text(2600, 6.9e19, r'$\alpha_0 = 0.8$', fontsize=11, color='black', fontweight='bold')

    ax.set_xlabel(r'$\rm time ~(\rm yr)$', fontsize=label_fsize)
    ax.set_ylabel(r'${J}_{\rm disk}/{M}_{\rm disk}~(\rm cm^2 s^{-1})$', fontsize=label_fsize)

    plt.savefig('figure_9.pdf', format='pdf', bbox_inches='tight')
    plt.close()