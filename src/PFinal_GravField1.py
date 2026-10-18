#Importing math and plotting libraries
import numpy as np
import matplotlib.pyplot as plt
import bisect

# For finding R and epsilon------------------------------------------

import matplotlib.gridspec as gridspec
from matplotlib.ticker import ScalarFormatter
import matplotlib.ticker as ticker


# Defining function for calculating epsilon--------------------------

def func(npts, R, eps):
    func=(1+eps)**npts-1-eps/R
    return func

npts=100
# INITIALIZE r_min AND r_max
r_min = 0.1
r_max = 10e3


# For searching for epsilon------------------------------------------
small=0.000001
right=1.
left=small
eps=0.
R=r_min/r_max

if (func(npts, R, right)>0 and func(npts, R, left)>0):
    print("Epsilon out of range")

if (func(npts, R, right)<0 and func(npts, R, left)<0):
    print("Epsilon out of range")

while (eps==0):
    middle=(left+right)/2
    if (func(npts, R, right)<0 and func(npts, R, middle)>0):
        left=middle
    elif (func(npts, R, right)>0 and func(npts, R, middle)<0):
        left=middle
    elif (func(npts, R, middle)<0 and func(npts, R, left)>0):
        right=middle
    elif (func(npts, R, middle)>0 and func(npts, R, left)<0):
        right=middle

    if ((right-left)<small):
        eps=middle

# Filling arrays of zeta, zetab--------------------------------------

zeta=[0.00]*(npts+1)
zetab=[0.00]*(npts+1)
zetasq=[0.00]*(npts+1)

for i in range (1, npts+1):
    zeta[i]=R*r_max*((1+eps)**i-1)/eps

for i in range (1, npts+1):
    to3 = 2./3.
    zetasq[i] = zeta[i]*zeta[i]
    zetab[i] = to3*(zetasq[i] + zeta[i]*zeta[i-1]\
                    +zetasq[i-1])/(zeta[i] + zeta[i-1])
    
# For calculating density and filling density array------------------
f=[0.00]*(npts+1)

def dens(r):
    # INPUT SURFACE DENSITY FUNCTION HERE
    dens = 1 / np.sqrt(1 + (r)**2.8)
    return dens

for i in range (1, npts+1):
    f[i]=dens(zetab[i])

# Defining elliptic integral functions-------------------------------

def ellipe(x):

# Defining coefficients for elliptic integral
    ae=[1.0e-00,0.4431471805608895e-00,0.5680519456755915e-01,\
     0.2183181167613048e-01,0.1156959574529540e-01,\
     0.7595093422559432e-02,0.7820404060959553e-02,\
     0.1077063503986645e-01,0.8638442173604073e-02,\
     0.2468503330460722e-02,0.1494662175718132e-03]

    be=[0.0e-00,0.2499999999999017e-00,0.9374999972120313e-01,\
     0.5859366125553149e-01,0.4271789054738309e-01,\
     0.3347894366576162e-01,0.2614501470031388e-01,\
     0.1680402334636338e-01,0.6432146586438302e-02,\
     0.9898332846225384e-03,0.3185919565550157e-04]

    ellipe = ae[0]-be[0]*np.log(x)\
    +(ae[1]-be[1]*np.log(x))*x\
    +(ae[2]-be[2]*np.log(x))*x*x\
    +(ae[3]-be[3]*np.log(x))*x**3\
    +(ae[4]-be[4]*np.log(x))*x**4\
    +(ae[5]-be[5]*np.log(x))*x**5\
    +(ae[6]-be[6]*np.log(x))*x**6\
    +(ae[7]-be[7]*np.log(x))*x**7\
    +(ae[8]-be[8]*np.log(x))*x**8\
    +(ae[9]-be[9]*np.log(x))*x**9\
    +(ae[10]-be[10]*np.log(x))*x**10
    return ellipe

def ellipk(x):

# Defining coefficients for elliptic integral
    ak=[0.1386294361119890e+01,0.9657359028085625e-01,\
     0.3088514627130518e-01,0.1493801353268716e-01,\
     0.8789801874555064e-02,0.6179627446053317e-02,\
     0.6847909282624505e-02,0.9848929322176892e-02,\
     0.8003003980649985e-02,0.2296634898396958e-02,\
     0.1393087857006646e-03]

    bk=[0.5e-00,0.1249999999999080e-00,0.7031249973903835e-01,\
     0.4882804190686239e-01,0.3737773975862360e-01,\
     0.3012484901289892e-01,0.2393191332311079e-01,\
     0.1553094163197720e-01,0.5973904299155429e-02,\
     0.9215546349632497e-03,0.2970028096655561e-04]

    ellipk=(ak[0]-bk[0]*np.log(x))\
    +(ak[1]-bk[1]*np.log(x))*x\
    +(ak[2]-bk[2]*np.log(x))*x*x\
    +(ak[3]-bk[3]*np.log(x))*x**3\
    +(ak[4]-bk[4]*np.log(x))*x**4\
    +(ak[5]-bk[5]*np.log(x))*x**5\
    +(ak[6]-bk[6]*np.log(x))*x**6\
    +(ak[7]-bk[7]*np.log(x))*x**7\
    +(ak[8]-bk[8]*np.log(x))*x**8\
    +(ak[9]-bk[9]*np.log(x))*x**9\
    +(ak[10]-bk[10]*np.log(x))*x**10
    return ellipk

# For getting g[k] for 0, npts---------------------------------------

i0=[0.00]*(npts+1)
g=[0.00]*(npts+1)
topi=1./np.arcsin(1)
for k in range (1, npts+1):

# Want I0(i) for i=1, npts for this particular k
   for i in range (1, k):
       y1 = zeta[i]/zetab[k]
       y2 = zeta[i-1]/zetab[k]
       x1 = 1. - y1*y1
       x2 = 1. - y2*y2
       i0[i]=(-(ellipk(x1) - ellipe(x1) - ellipk(x2) + ellipe(x2)))

# For i=k, calculate so as to avoid logarithmic singularity
   y1 = zeta[k-1]/zetab[k]
   y2 = zetab[k]/zeta[k]
   x1 = 1. - y1*y1
   x2 = 1. - y2*y2
   i0[k]=( ellipk(x1) - ellipe(x1)\
            - 1./y2*(ellipk(x2)-ellipe(x2)))

   for i in range (k+1, npts+1):
       y1 = zetab[k]/zeta[i-1]
       y2 = zetab[k]/zeta[i]
       x1 = 1. - y1*y1
       x2 = 1. - y2*y2
       i0[i]=(1./y1*(ellipk(x1)-ellipe(x1))\
              - 1./y2*(ellipk(x2)-ellipe(x2)))

# Now get g[k]
   g[k]=0.00
   for i in range (1, npts+1):
       g[k]=g[k]+f[i]*i0[i]

print('density', f)
print('gravity', g)
print('radius', zetab)

pos_g = [abs(x) for x in g]

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



label_fsize = 14

plt.rcParams['mathtext.fontset'] = 'stix'     # or 'cm', 'dejavuserif', 'stixsans'
plt.rcParams['font.family'] = "Times New Roman"
plt.rcParams['mathtext.rm'] = 'Times New Roman'  # serif font
plt.rcParams['mathtext.it'] = 'Times New Roman:italic'
plt.rcParams['mathtext.bf'] = 'Times New Roman'
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

data = np.loadtxt("output_alpha_0.5_eta_0.01_lambda_0.1_time_3000.csv", delimiter=",", skiprows=1)
data = data.T

val = 1
left = 0
right = len(data) - 1
ans = None

while left < right:
    mid = int((left + right) / 2)

    if data[0][mid] <= 5:
        ans = mid
        left = mid + 1
    else:
        right = mid - 1

ref_radius = data[0][ans]
ref_sigma = data[4][ans]

ref_vphi = data[1][ans]
ref_cs = data[2][ans]

new_sigma = ref_sigma * np.pow(ref_radius, 1.4)
new_vphi = ref_vphi * ref_cs * np.pow(ref_radius, 0.2)

# print())

all_sigma = data[4][ans:] / new_sigma
all_vphi = (data[1][ans:] * data[2][ans:]) / (new_vphi)
all_radii = data[0][ans:]

AU_TO_CM = 1.49597870691e13  # Astronomical unit to meters
SOLAR_MASS = 1.989e33       # Solar mass in kg
G = 6.674e-8 # gravitational constant

all_g_disk = (G * data[5][ans:] * SOLAR_MASS) / (np.pow(all_radii * AU_TO_CM, 2))

# print("gravity self similar", all_g_disk)
# print("gravity analytical", pos_g)

ind_self_similar = bisect.bisect_left(all_radii, 50)
ind_analytical = bisect.bisect_left(zetab, 50)

rev_pos_g = pos_g[::-1]
zetab = np.array(zetab)
pos_g = np.array(pos_g)
sinkind = np.where((zetab >= 1) & (zetab <= 100))[0]


coeffs = np.polyfit(np.log(zetab[1:]), np.log(pos_g[1:]), 1)  
n = coeffs[0]   # slope (power-law exponent)
A = np.exp(coeffs[1])  # prefactor

r = np.array(zetab)
scaling = f[40] / np.pow(r[40], -1.4) # normalize at first point
scaled_arr = scaling * np.pow(r[1:], -1.4) * 2.4

fig = plt.figure(figsize=(30/2.54, 15/2.54))
gs = gridspec.GridSpec(1, 2, wspace=0.0, hspace=0.0, 
                          left=0.1, right=0.9, bottom=0.1, top=0.9)

# ax2 = fig.add_subplot(gs[0, 0])
# ax2.loglog(r[30:70], scaled_arr[30:70], '--', color = 'grey')

# x_text = r[40]       # pick middle of r-range
# y_text = scaling * x_text**(-1.4) * 2.8  # a bit above the line
# ax2.text(x_text, y_text, r"$ r^{-1.4}$", color="black", fontsize=14)

# ax2.loglog(r[1:], f[1:], color=Lcolor0, linestyle=Lstyle0, linewidth=Lwidth0, label = 'Analytic profile')
# # ax2.loglog(all_radii, all_sigma,  color=Lcolor2, linestyle=Lstyle2, linewidth=Lwidth2, label = 'Self Similar Analytical Model')

# ax2.set_xlim([4, 1.1e3])
# ax2.set_ylim([1e-5, 1])

# ax2.set_xlabel(r'$r/R$', fontsize = 18)
# ax2.set_ylabel(r'$\sigma/\sigma_{0}$', fontsize = 18)
# ax2.tick_params(axis='both', labelsize=16)
# # ax2.xaxis.tick_top()
# # ax2.xaxis.set_label_position('top')
# ax2.yaxis.tick_left()
# ax2.yaxis.set_label_position('left')
# ax2.legend(fontsize=14)
# ax2.legend(fontsize=16)

ax1 = fig.add_subplot(gs[0, 0])
scaling = pos_g[30] / np.pow(r[30], -1.4) # normalize at first point
scaled_arr = scaling * np.pow(r[1:], -1.4) * 0.4

x_text = r[30]       # pick middle of r-range
y_text = scaling * x_text**(-1.4) * 0.05  # a bit above the line
ax1.text(x_text, y_text, r"$ r^{-1.4}$", color="black", fontsize=14)
ax1.loglog(r[20:50], scaled_arr[20:50], '--', color = 'grey')


# sigma_0 = 1 and R = 1
mdisk = (10 * np.pi / 3) * (np.pow(r, 0.6))
print(mdisk)

# G = 1
spherical_g = mdisk / np.pow(r, 2)
print(spherical_g)
print(pos_g)

ax1.loglog(zetab, pos_g, color=Lcolor1, linestyle=Lstyle1, linewidth=Lwidth1, label = 'Thin disk solution')
ax1.loglog(zetab, spherical_g / (2*np.pi), color=Lcolor2, linestyle=Lstyle2, linewidth=Lwidth2, label = 'Spherical approximation')

print("Ratio of numerical to spherical g_disk", 2*np.pi*pos_g[sinkind][40] / spherical_g[sinkind][40])

# plt.xlim([1.1, 1e2]
# plt.ylim([1e-4, 1])

ax1.set_xlim([4, 1.1e3])
ax1.set_ylim([0.07, 10.1])
ax1.set_yticks([1e-4, 1e-3, 1e-2, 1e-1, 1.0, 10])
from matplotlib.ticker import LogFormatterMathtext
ax1.yaxis.set_major_formatter(LogFormatterMathtext())
# ax1.yaxis.set_major_formatter(ScalarFormatter())
# ax1.set_yticklabels([str(t) for t in [1e-4, 1e-3, 1e-2, 1e-1, 1.0, 1e1]])
# ax1.yaxis.set_minor_locator(ticker.NullLocator())
ax1.set_xlabel(r'$r/R$', fontsize = 18)
ax1.set_ylabel(r'$\left| g_{\mathrm{disk}} \right| / 2\pi G\sigma_{0}$', fontsize = 18)
ax1.tick_params(axis='both', labelsize=16)
# ax1.xaxis.tick_top()
# ax1.xaxis.set_label_position('top')
# ax1.yaxis.tick_right()
# ax1.yaxis.set_label_position('right')
ax1.legend(fontsize=14)

# fig_new = plt.figure(figsize=(15/2.54, 15/2.54))
# gs = gridspec.GridSpec(1, 1, wspace=0.0, hspace=0.0, 
#                           left=0.1, right=0.9, bottom=0.1, top=0.9)

ax3 = fig.add_subplot(gs[0, 1])

v_phi = []

for i in range(npts + 1):
    v_phi.append(np.sqrt(pos_g[i] * zetab[i]))
v_phi = np.array(v_phi)
scaling = v_phi[50] / np.pow(r[50], -0.2) # normalize at first point
# scaling = pos_g[30] / np.pow(r[30], -1.4) # normalize at first point
scaled_arr = scaling * np.pow(r[1:], -0.2) * 0.8

ax3.loglog(r[30:70], scaled_arr[30:70], '--', color = 'grey')

x_text = r[40]       # pick middle of r-range
y_text = scaling * x_text**(-0.2) * 0.6   # a bit above the line
ax3.text(x_text, y_text, r"$ r^{-0.2}$", color="black", fontsize=14)


ax3.loglog(r[1:], v_phi[1:], color=Lcolor3, linestyle=Lstyle3, linewidth=Lwidth3, label = 'Thin disk solution')

ax3.set_xlim([4, 1.1e3])
ax3.set_ylim([0.3, 1.5])

ax3.set_yticks([0.3, 0.4, 0.5, 0.6, 0.8, 1.0])  
ax3.set_yticklabels([str(t) for t in [0.3, 0.4, 0.5, 0.6, 0.8, 1.0]])

# ✅ Force normal decimal labels (no scientific notation)
formatter = ScalarFormatter(useMathText=False)
formatter.set_scientific(False)
formatter.set_useOffset(False)
ax3.yaxis.set_major_formatter(formatter)
# from matplotlib.ticker import FuncFormatter
# ax3.yaxis.set_major_formatter(FuncFormatter(lambda val, pos: f'{val:.2f}'))
# ax3.get_yaxis().get_major_formatter().set_scientific(False)
# ax3.get_yaxis().get_major_formatter().set_useOffset(False)
ax3.ticklabel_format(style='plain', axis='y', useOffset=False, scilimits=(-999, 999))

ax3.yaxis.set_minor_locator(ticker.NullLocator())
ax3.set_xlabel(r'$r/R$', fontsize=18)
ax3.set_ylabel(r'$v_{\phi} / \sqrt{2\pi G\sigma_{0} R}$', fontsize=18)
ax3.tick_params(axis='both', labelsize=16)
# ax3.yaxis.tick_left()
# ax3.yaxis.set_label_position('left')
ax3.yaxis.tick_right()
ax3.yaxis.set_label_position('right')
ax3.legend(fontsize=16)

for ax in [ax1, ax3]:
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


plt.tight_layout()
plt.savefig('gdisk_and_vphi.pdf', format='pdf', bbox_inches='tight')
plt.show()

# y_text = scaling * x_text**(-1.5) * 2.0  # a bit above the line
#--------------------------------THE END-----------------------------
