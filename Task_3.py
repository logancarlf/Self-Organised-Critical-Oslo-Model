import packages as pk
import classes as cl

n = 7
L = pk.np.logspace(2, n+1, base=2, num=n)
c = pk.np.arange(1, n+1)
N = 500000

norm = pk.mpl.colors.Normalize(vmin=c.min(), vmax=c.max())
cmap = pk.mpl.cm.ScalarMappable(norm=norm, cmap=pk.mpl.cm.Blues)
cmap.set_array([])

fig, (ax1, ax2) = pk.plt.subplots(1, 2, figsize=(12.8, 4.8))
avalanche_sizes = list()
data_prob_s = list()
data_s = list()
curve_prob_s = list()
curve_s = list()
for j in pk.tqdm(range(n)):
    Oslo = cl.Model(int(L[j]), 0.5)
    Oslo.simulate(N, avalanche_data=True)
    S = Oslo.avalanche_size()
    avalanche_sizes.append(S)
    x, y = pk.logbin(S[-400001:], zeros=True)
    data_prob_s.append(y)
    data_s.append(x)
    x, y = pk.logbin(S[-400001:], zeros=True, scale=1.25)
    curve_prob_s.append(y)
    curve_s.append(x)

# %%
# Avalanche Probability Plot

for i in range(n):
    ax1.loglog(data_s[i], data_prob_s[i], '.', c=cmap.to_rgba(i+2), ms=1,
               label="L=%s" % (int(L[i])))
for i in range(n):
    ax2.loglog(curve_s[i], curve_prob_s[i], '-', c=cmap.to_rgba(i+2),
               label="L=%s" % (int(L[i])))
ax1.set_xlabel("Avalanche Size / $s$")
ax1.set_ylabel("Probability $P_N(s;L)$")
ax1.legend()
ax2.set_xlabel("Avalanche Size / $s$")
ax2.set_ylabel("Probability $P_N(s;L)$")
ax2.legend()
fig.suptitle("Avalanche Probability Distribution")
fig.savefig("Figures/Fig_Task3a_I.png", dpi=600)
fig.show()

# %%

# Log Bin Scaling Graphs

fig, (ax1, ax2) = pk.plt.subplots(1, 2, figsize=(12.8, 4.8))
Oslo = cl.Model(int(128), 0.5)
Oslo.simulate(N, avalanche_data=True)

# %%

fig, (ax1, ax2, ax3) = pk.plt.subplots(1, 3, figsize=(12.8, 3.2))
S = Oslo.avalanche_size()
x, y = pk.logbin(S[-400001:], zeros=True, scale=1)
ax1.loglog(data_s[5], data_prob_s[5], '.', color='lightblue', ms=1)
ax2.loglog(data_s[5], data_prob_s[5], '.', color='lightblue', ms=1)
ax3.loglog(data_s[5], data_prob_s[5], '.', color='lightblue', ms=1)
x, y = pk.logbin(S[-400001:], zeros=True, scale=1.1)
ax1.loglog(x, y, '-', c=cmap.to_rgba(7), label="Scale = 1.1")
x, y = pk.logbin(S[-400001:], zeros=True, scale=1.2)
ax2.loglog(x, y, '-', c=cmap.to_rgba(7), label="Scale = 1.2")
x, y = pk.logbin(S[-400001:], zeros=True, scale=1.3)
ax3.loglog(x, y, '-', c=cmap.to_rgba(7), label="Scale = 1.3")
ax1.set_ylabel("Probability $P_N(s;L)$")
ax2.set_xlabel("Avalanche Size / $s$")
fig.suptitle("Binning Scale Comparison")
ax1.legend()
ax2.legend()
ax3.legend()
fig.savefig("Figures/Fig_Task3a_II.png", dpi=600)
fig.show()

# %%


def power_law(x, a, b):
    return a * x ** b


fit = pk.curve_fit(power_law, curve_s[6][10:30], curve_prob_s[6][10:30],
                   p0=[0.4, -1.5])
x = pk.np.logspace(-1, 1+pk.np.log10(pk.np.max(curve_s[6])), num=1000)

pk.plt.loglog(x, power_law(x, *fit[0]), linestyle='dashed', c=cmap.to_rgba(8),
              label='Power Law Fit')
pk.plt.loglog(curve_s[6], curve_prob_s[6], '.', c=cmap.to_rgba(8),
              label='L=128')
pk.plt.xlabel("Avalanche Size / $s$")
pk.plt.ylabel("Probability $P_N(s;L)$")
pk.plt.legend()
pk.plt.title("Avalanche Probability Distribution")
pk.plt.savefig("Figures/Fig_Task3a_III.png", dpi=600)
pk.plt.show()

tau_s = -1 * fit[0][1]
print()
print("Tau:", tau_s, "+/-", pk.np.sqrt(fit[1][1][1]))

# %%

# Data Collapse 1

for i in range(n):
    yplot = list()
    for j in range(len(curve_s[i])):
        cs = curve_prob_s[i][j] * curve_s[i][j] ** tau_s
        yplot.append(cs)
    pk.plt.loglog(curve_s[i], yplot, '-', c=cmap.to_rgba(i+2),
                  label="L=%s" % (int(L[i])))
pk.plt.xlabel("Avalanche Size / $s$")
pk.plt.ylabel("Probability $s^{\tau_s}P_N(s;L)$")
pk.plt.legend()
pk.plt.title("Avalanche Probability $L$-Scaled")
pk.plt.savefig("Figures/Fig_Task3a_IV.png", dpi=600)
pk.plt.show()

# %%

# Data Collapse 2
D = 2.1

maxy = list()
for i in range(n):
    yplot = list()
    xplot = list()
    for j in range(len(curve_s[i])):
        cs = curve_prob_s[i][j] * curve_s[i][j] ** tau_s
        yplot.append(cs)
        xs = curve_s[i][j] / (L[i] ** D)
        xplot.append(xs)
    max_y = pk.np.max(yplot)
    pos_max = pk.np.where(yplot == max_y)[0][0]
    maxy.append(xplot[pos_max])
    pk.plt.loglog(xplot, yplot, '-', c=cmap.to_rgba(i+2),
                  label="L=%s" % (int(L[i])))
pk.plt.xlabel("Avalanche Size / $s/L^D$")
pk.plt.ylabel("Probability $s^{\tau_s}P_N(s;L)$")
pk.plt.legend()
pk.plt.title("Avalanche Probability $L,P$-Scaled")
pk.plt.savefig("Figures/Fig_Task3a_V.png", dpi=600)
pk.plt.show()

differences = list()
for i in maxy:
    for j in maxy:
        if i != j:
            differences.append(abs(i-j))
print("Score:", pk.np.mean(differences))

# %%

import packages as pk
import classes as cl


def linear(x, a, b):
    return a * x + b

def power_law(x, a, b):
    return a * x ** b

#n = 4
#L = pk.np.logspace(2, n+1, base=2, num=n)
#c = pk.np.arange(1, n+1)
#N = 20000
#
#norm = pk.mpl.colors.Normalize(vmin=c.min(), vmax=c.max())
#cmap = pk.mpl.cm.ScalarMappable(norm=norm, cmap=pk.mpl.cm.Blues)
#cmap.set_array([])
#cmap2 = pk.mpl.cm.ScalarMappable(norm=norm, cmap=pk.mpl.cm.YlGn)
#cmap2.set_array([])
#
#avalanche_sizes = list()
#for j in pk.tqdm(range(n)):
#    Oslo = cl.Model(int(L[j]), 0.5)
#    Oslo.simulate(N, avalanche_data=True)
#    S = Oslo.avalanche_size()
#    avalanche_sizes.append(S)

k = [1, 2, 3, 4]

data_k_moments = list()
for j in k:
    k_moments_L = list()
    for i in range(n):
        moment = 0
        for s in avalanche_sizes[i]:
            moment += s ** j
        moment = moment / len(avalanche_sizes[i])
        k_moments_L.append(moment)
    data_k_moments.append(k_moments_L)

fits = list()
covs = list()
for i in range(len(k)):
    pk.plt.loglog(L, data_k_moments[i], '.', marker='x',
                  c=cmap2.to_rgba(i+2), label='k=$%s$' % (k[i]))
    fit, cov = pk.curve_fit(linear, pk.np.log10(L),
                            pk.np.log10(data_k_moments[i]))
    fits.append(fit[0])
    covs.append(covs)
    pk.plt.loglog(L, power_law(L, 10 ** fit[1], fit[0]), c=cmap2.to_rgba(i+2),
                  linestyle='dashed')
pk.plt.title("Avalanche Moments")
pk.plt.xlabel("System Size / $L$")
pk.plt.ylabel("k'th Moment ave $s^k$")
pk.plt.legend()
pk.plt.grid()
pk.plt.savefig("Figures/Fig_Task3a_VI.png", dpi=600)
pk.plt.show()

#%%
fit = curve_fit(linear, k, fits)
x = np.arange(0, 4.5, 0.001)
pk.plt.plot(x, linear(x, *fit[0]), color='black', linestyle='dashed')
pk.plt.scatter(k, fits, color='black', marker='x')
plt.xlabel("Moment $k$")
plt.ylabel("$k$-slope Gradient $alpha $")
plt.title("Scaling Ansatz")
plt.grid()
pk.plt.savefig("Figures/Fig_Task3a_VII.png", dpi=600)
pk.plt.show()

print()
print("Tau:", fit[0][1])
print("D:", fit[0][0])


