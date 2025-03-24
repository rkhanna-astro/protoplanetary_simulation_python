import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc

# Use LaTeX for text rendering
rc('text', usetex=True)

def menv(Menv_a4eta2, MdMenv_a4eta2, Menv_a5eta2, MdMenv_a5eta2, 
         Menv_a6eta2, MdMenv_a6eta2, Menv_a1eta2, MdMenv_a1eta2, 
         Menv_a2eta2, MdMenv_a2eta2, Menv_a3eta2, MdMenv_a3eta2):
    
    frac_midtick = 0.45
    label_fsize = 14
    ticklength = [0.02, 0.02]
    
    Lstyle1 = '-'
    Lstyle2 = '-'
    Lstyle3 = '-'
    Lstyle4 = '-'
    Lwidth1 = 1.0
    Lwidth2 = 1.0
    Lwidth3 = 1.0
    Lwidth4 = 1.0
    Lcolor1 = np.array([0, 0.4157, 1])  # blue
    Lcolor2 = np.array([0.3, 0.9333, 0])  # green
    Lcolor3 = np.array([1, 0.3333, 0])  # red
    Lcolor4 = np.array([0, 0.82, 0.82])  # cyan
    Lcolor5 = np.array([0.84, 0.49, 0.18])  # burned brown
    Lcolor6 = 'magenta'  # magenta
    
    # Create figure and set properties
    fig = plt.figure(figsize=(15/2.54, 15/2.54))  # Convert cm to inches (15 cm)
    
    # Set default font properties
    plt.rcParams['font.size'] = 11
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['helvetica']
    plt.rcParams['text.usetex'] = True
    plt.rcParams['axes.linewidth'] = 1.4
    
    xstart = 0.01
    xend = 10
    ystart = -0.1
    yend = 1.3
    
    # Load observational data
    mm = np.loadtxt('jes2.dat')  # Make sure this file is in your working directory
    
    # Create plot
    ax = fig.add_subplot(111)
    
    # Set axis properties
    ax.set_xlim([xstart, xend])
    ax.set_ylim([ystart, yend])
    ax.tick_params(axis='both', which='major', length=ticklength[0]*100)
    ax.set_xscale('log')
    ax.invert_xaxis()
    
    # Plot the data
    ax.plot(1./Menv_a1eta2, MdMenv_a1eta2, color=Lcolor1, linestyle=Lstyle1, linewidth=Lwidth1)
    ax.plot(1./Menv_a2eta2, MdMenv_a2eta2, color=Lcolor2, linestyle=Lstyle2, linewidth=Lwidth2)
    ax.plot(1./Menv_a3eta2, MdMenv_a3eta2, color=Lcolor3, linestyle=Lstyle3, linewidth=Lwidth3)
    ax.plot(1./Menv_a4eta2, MdMenv_a4eta2, color=Lcolor4, linestyle=Lstyle4, linewidth=Lwidth4)
    ax.plot(1./Menv_a5eta2, MdMenv_a5eta2, color=Lcolor5)
    ax.plot(1./Menv_a6eta2, MdMenv_a6eta2, color=Lcolor6)
    
    # Plot observational data
    ax.plot(mm[0:7,0], mm[0:7,1], 's', color=Lcolor1, markersize=6, markerfacecolor=[.49, 1, .63])  # Class 0
    ax.plot(mm[7:15,0], mm[7:15,1], 'o', color=Lcolor3, markersize=6, markerfacecolor=[0.98, 0.66, 0.44])  # Class I
    
    # Add text labels
    ax.text(0.43, 0.29, '1.0', fontsize=9, color=Lcolor4)
    ax.text(0.57, 0.33, '0.8', fontsize=9, color=Lcolor1)
    ax.text(0.84, 0.41, '0.5', fontsize=9, color=Lcolor2)
    ax.text(1.28, 0.55, '0.3', fontsize=9, color=Lcolor3)
    ax.text(1.76, 0.71, '0.2', fontsize=9, color=Lcolor6)
    ax.text(2.67, 1.25, '0.1', fontsize=9, color=Lcolor5)
    
    # Add axis labels
    ax.set_xlabel(r'$M_{\rm env}~(\rm M_{\odot})$', fontsize=label_fsize)
    ax.set_ylabel(r'$M_{\rm disk,tot}/M_{\rm env}$', fontsize=label_fsize)
    
    # Add class labels and markers
    ax.text(0.03, 1.2, 'Class 0', fontsize=12, color='black')
    ax.text(0.03, 1.1, 'Class I', fontsize=12, color='black')
    ax.plot(0.04, 1.2, 's', color=Lcolor1, markersize=6, markerfacecolor=[.49, 1, .63])
    ax.plot(0.04, 1.1, 'o', color=Lcolor3, markersize=6, markerfacecolor=[0.98, 0.66, 0.44])
    
    # Adjust aspect ratio
    ax.set_aspect(1/0.8)
    
    # Save figure
    plt.tight_layout()
    plt.savefig('MenvMdisk.pdf', format='pdf', bbox_inches='tight')
    plt.close()
