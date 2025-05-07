import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc

def menv(Menv_a1eta2, MdMenv_a1eta2, Menv_a2eta2, MdMenv_a2eta2, 
         Menv_a3eta2, MdMenv_a3eta2, Menv_a4eta2, MdMenv_a4eta2, 
         Menv_a5eta2, MdMenv_a5eta2, Menv_a6eta2, MdMenv_a6eta2):
    
    # Set up LaTeX font
    rc('text', usetex=True)
    rc('font', family='serif')
    
    # Parameters
    frac_midtick = 0.45
    label_fsize = 14
    ticklength = [0.02, 0.02]
    
    # Line styles
    Lstyle1 = '-'
    Lstyle2 = '-'
    Lstyle3 = '-'
    Lstyle4 = '-'
    Lwidth1 = 1.0
    Lwidth2 = 1.0
    Lwidth3 = 1.0
    Lwidth4 = 1.0
    Lcolor1 = [0, 0.4157, 1]       # blue
    Lcolor2 = [0.3, 0.9333, 0]     # green
    Lcolor3 = [1, 0.3333, 0]       # red
    Lcolor4 = [0, 0.82, 0.82]      # cyan
    Lcolor5 = [0.84, 0.49, 0.18]   # brown
    Lcolor6 = 'magenta'            # magenta
    
    # Create figure
    fig = plt.figure(figsize=(15/2.54, 15/2.54))  # Convert cm to inches
    ax = fig.add_subplot(111)
    
    # Axis limits
    xstart = 0.01
    xend = 10
    ystart = -0.1
    yend = 1.3
    
    # Load observational data (assuming jes2.dat is a space/tab-delimited file)
    mm = np.loadtxt('jes2.dat')
    
    # Set up plot
    ax.set_xlim([xstart, xend])
    ax.set_ylim([ystart, yend])
    ax.set_xscale('log')
    ax.invert_xaxis()
    
    # Plot model data
    ax.plot(Menv_a1eta2, MdMenv_a1eta2, color=Lcolor1, linestyle=Lstyle1, linewidth=Lwidth1)
    ax.plot(Menv_a2eta2, MdMenv_a2eta2, color=Lcolor2, linestyle=Lstyle2, linewidth=Lwidth2)
    ax.plot(Menv_a3eta2, MdMenv_a3eta2, color=Lcolor3, linestyle=Lstyle3, linewidth=Lwidth3)
    ax.plot(Menv_a4eta2, MdMenv_a4eta2, color=Lcolor4, linestyle=Lstyle4, linewidth=Lwidth4)
    ax.plot(Menv_a5eta2, MdMenv_a5eta2, color=Lcolor5, linestyle=Lstyle1, linewidth=Lwidth1)
    ax.plot(Menv_a6eta2, MdMenv_a6eta2, color=Lcolor6, linestyle=Lstyle2, linewidth=Lwidth2)
    
    # Plot observational data
    ax.plot(mm[0:7,0], mm[0:7,1], 's', color=Lcolor1, markersize=6, markerfacecolor=[.49, 1, .63])  # Class 0
    ax.plot(mm[7:15,0], mm[7:15,1], 'o', color=Lcolor3, markersize=6, markerfacecolor=[0.98, 0.66, 0.44])  # Class I
    
    # Add text labels
    ax.text(0.43, 0.29, '1.0', fontsize=9, color=Lcolor6)
    ax.text(0.57, 0.33, '0.8', fontsize=9, color=Lcolor5)
    ax.text(0.84, 0.41, '0.5', fontsize=9, color=Lcolor4)
    ax.text(1.28, 0.55, '0.3', fontsize=9, color=Lcolor3)
    ax.text(1.76, 0.71, '0.2', fontsize=9, color=Lcolor2)
    ax.text(2.62, 1.23, '0.1', fontsize=9, color=Lcolor1)
    
    # Add axis labels
    ax.set_xlabel(r'$M_{\rm env}~(\rm M_{\odot})$', fontsize=label_fsize)
    ax.set_ylabel(r'$M_{\rm disk,tot}/M_{\rm env}$', fontsize=label_fsize)
    
    # Add class labels
    ax.text(0.03, 1.2, 'Class 0', fontsize=12, color='black')
    ax.text(0.03, 1.1, 'Class I', fontsize=12, color='black')
    
    # Add markers for legend
    ax.plot(0.04, 1.2, 's', color=Lcolor1, markersize=6, markerfacecolor=[.49, 1, .63])
    ax.plot(0.04, 1.1, 'o', color=Lcolor3, markersize=6, markerfacecolor=[0.98, 0.66, 0.44])
    
    # Adjust aspect ratio
    ax.set_aspect(1/0.8)
    
    # Save figure
    plt.tight_layout()
    plt.savefig('figure_7.jpg', format='jpg', dpi=1000)
    plt.close()

# Example usage (you would call this with your actual data):
# menv(Menv_a4eta2, MdMenv_a4eta2, Menv_a5eta2, MdMenv_a5eta2, 
#      Menv_a6eta2, MdMenv_a6eta2, Menv_a1eta2, MdMenv_a1eta2, 
#      Menv_a2eta2, MdMenv_a2eta2, Menv_a3eta2, MdMenv_a3eta2)
