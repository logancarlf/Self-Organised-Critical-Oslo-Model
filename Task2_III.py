import packages as pk
import classes as cl

pk.plt.rc('text', usetex=True)
pk.plt.rc('font', family='serif', size=14)

# %%

n = 7
L = pk.np.logspace(2, n+1, base=2, num=n)
N = 100000
c = pk.np.arange(1, n+1)

norm = pk.mpl.colors.Normalize(vmin=c.min(), vmax=c.max())
cmap = pk.mpl.cm.ScalarMappable(norm=norm, cmap=pk.mpl.cm.Blues)
cmap.set_array([])

# %%

# Produce data
data_height_1 = list()
for i in pk.tqdm(range(n)):
    Oslo = cl.Model(int(L[i]), 0.5)
    Oslo.simulate(N, data_height_1=True)
    height_1 = Oslo.height_1()
    data_height_1.append(height_1)


# %%
# Task 2e

# Run latex

def first_order_fit(l, a0, a1, w1):
    return a0 * l * (1 - a1 * l ** (-w1))


h_ave = list()
for i in range(n):
    heights = data_height_1[i][-10001:-1]
    ave = pk.np.mean(pk.np.array(heights))
    h_ave.append(ave)

fit = pk.curve_fit(first_order_fit, L, h_ave)
x = pk.np.arange(1, L[len(L)-1]+10, 0.01)

fig, (ax1, ax2) = pk.plt.subplots(1, 2, figsize=(12.8, 4.8))
ax1.scatter(L, h_ave, marker='x', color='black', label='Data')
ax1.plot(x, first_order_fit(x, *fit[0]), color='black', linestyle='dashed',
         label='First Order Fit')
ax1.set_xlabel("System Size $L$")
ax1.set_ylabel(r"Average Height $\langle h \rangle $")
ax1.legend()
ax1.grid()

print("Fit Parameters:")
print("a0:", fit[0][0])
print("a1:", fit[0][1])
print("w0:", fit[0][2])

a0 = fit[0][0]

ax2.scatter(L, h_ave/(a0*L), marker='x', color='black', label='Data')
ax2.plot(x, first_order_fit(x, *fit[0])/(a0*x), color='black',
         linestyle='dashed', label='First Order Fit')
ax2.set_xlabel("System Size $L$")
ax2.set_ylabel(r"Scaled Average Height $\langle h \rangle/a_0L$")
ax2.legend()
ax2.grid()
fig.savefig("Figures/Fig_Task2e.png", dpi=600, bbox_inches='tight')
fig.show()


# %%

# task 2f

def root_fit(x, a, b):
    return a * x ** b


h_std= list()
for i in data_height_1:
    std = pk.np.std(i[len(data_height_1)-10000:])
    h_std.append(std)

fit = pk.curve_fit(root_fit, L, h_std)
x = pk.np.arange(1, h_ave[len(L)-1]+5, 0.01)

fig, (ax1, ax2) = pk.plt.subplots(1, 2, figsize=(12.8, 4.8)) 
ax1.scatter(L, h_std, color='black', label='Data', marker='x')
ax1.plot(x, root_fit(x, *fit[0]), color='black', linestyle='dashed',
            label='Power Law Fit')
ax1.set_xlabel("System Size $L$")
ax1.set_ylabel(r"Standard Deviation $\sigma_h(L)$")
ax1.ticklabel_format(useOffset=True)
ax1.set_xscale('log')
ax1.set_yscale('log')
ax1.legend()
ax1.grid()

h_std_scaled= list()
for i in range(n):
    std = pk.np.std(data_height_1[i][-10001:-1])
    h_std_scaled.append(std/root_fit(L[i], fit[0][0], fit[0][1]))


ax2.scatter(L, h_std_scaled, color='black', label='Scaled Data', marker='x')
ax2.set_xlabel("System Size $L$")
ax2.set_ylabel(r"Scaled Standard Deviation $\sigma_h(L)/aL^b$")
ax2.set_yscale('log')
ax2.yaxis.tick_right()
ax2.legend()
ax2.grid()
fig.savefig("Figures/Fig_Task2f.png", dpi=600, bbox_inches='tight')
fig.show()

print("w:", fit[0][1])

w = fit[0][1]

#%%
import packages as pk
import classes as cl

def gaussian(x, mu, sig):
    return (1/(pk.np.sqrt(6.28)))*pk.np.exp(-pk.np.power(x - mu, 2.) / (2 * pk.np.power(sig, 2.)))

h_prob = list()
h_values = list()
h_prob_scaled = list()
h_values_scaled = list()
for i in range(n):
    heights = data_height_1[i][-10001:-1]
    hist = pk.np.bincount(heights)
    x = pk.np.arange(0, pk.np.max(heights)+1, 1)
    xvalue = list()
    yvalue = list()
    xvalue_scaled = list()
    yvalue_scaled = list()
    for j in range(len(hist)):
        if hist[j] != 0:
            xvalue.append(x[j])
            yvalue.append(hist[j]/len(heights))
            xvalue_scaled.append((x[j]-h_ave[i]) * L[i] ** -w)
            yvalue_scaled.append((hist[j]/len(heights)* L[i] ** w))
    h_prob.append(yvalue)
    h_values.append(xvalue)
    h_prob_scaled.append(yvalue_scaled)
    h_values_scaled.append(xvalue_scaled)
    
fig, (ax1, ax2) = pk.plt.subplots(1, 2, figsize=(12.8, 4.8)) 
for i in range(n):
    ax1.plot(h_values[i], h_prob[i], c=cmap.to_rgba(i+2),
                label="L=%s" % (int(L[i])))
    ax2.plot(h_values_scaled[i], h_prob_scaled[i], c=cmap.to_rgba(i+2),
                label="L=%s" % (int(L[i])))
x = pk.np.arange(-3, 3, 0.01)
ax2.plot(x, gaussian(x, 0, 1), color='black', linestyle='dashed', label='Theoretical')
ax1.set_xlabel("Height $h$")
ax1.set_ylabel("Height Probability $P(h;L)$")
ax2.set_xlabel(r"Scaled Height $(h-\langle h\rangle)L^{-\beta}$")
ax2.set_ylabel(r"Scaled Height Probability $L^\beta P(h;L)$")
ax1.legend()
ax2.legend()
fig.savefig("Figures/Fig_Task2g.png", dpi=600, bbox_inches='tight')
fig.show()

#%%

# Task 2g

import packages as pk
import classes as cl

def gaussian(x, mu, sig, A):
    return A * pk.np.exp(-pk.np.power(x - mu, 2.) / (2 * pk.np.power(sig, 2.)))

# Task 2g_I
h_prob = list()
h_values = list()
for i in range(n):
    bin_points = pk.np.linspace(h_ave[i]-5*h_std[i], h_ave[i]+5*h_std[i], 100)
    bins = list()
    data = data_height_1[i][len(data_height_1[i])-10000:]
    for j in range(len(bin_points)-1):
        center = 0.5 * (bin_points[j] + bin_points[j+1])
        bins.append(center)
    hist = pk.np.histogram(data, bins=99, normed=True, density=True)[0]
    clean_hist = list()
    clean_bins = list()
    clean_hist.append(0)
    clean_bins.append(bins[0])
    for j in range(len(bin_points)-1):
        if hist[j] != 0:
            clean_hist.append(hist[j])
            clean_bins.append(bins[j])
    clean_hist.append(0)
    clean_bins.append(bins[-1])
    h_prob.append(clean_hist)
    h_values.append(clean_bins)

for i in range(n):
    fit = pk.curve_fit(gaussian, h_values[i], h_prob[i])
    print(fit[0][2])
    for j in range(len(h_prob)):
        h_prob[j] = h_prob[j]

for i in range(n):
    x_values = pk.np.arange(h_ave[i]-5*h_std[i], h_ave[i]+5*h_std[i], 0.01)
    y_values = pk.spstats.norm(h_ave[i], h_std[i])
    pk.plt.plot(x_values, y_values.pdf(x_values), c=cmap.to_rgba(i+2),
                label="L=%s" % (int(L[i])))
pk.plt.title("Height Probability Against Height")
pk.plt.xlabel("Height $h$")
pk.plt.ylabel("Height Probability $P(h;L)$")
pk.plt.legend()
pk.plt.savefig("Figures/Fig_Task2g_I.png", dpi=600)
pk.plt.show()

for i in range(n):
    x_values = pk.np.arange(h_ave[i]-5*h_std[i], h_ave[i]+5*h_std[i], 0.01)
    y_values = pk.spstats.norm(h_ave[i], h_std[i])
    y_values = y_values.pdf(x_values)* L[i] ** w
    x_values = (x_values-h_ave[i])*L[i] ** -w
    pk.plt.plot(x_values, y_values, c=cmap.to_rgba(i+2), label="L=%s" % (int(L[i])))
pk.plt.title("Height Probability Against Height")
pk.plt.xlabel("Height $hL^{-\omega}$")
pk.plt.ylabel("Height Probability $L^\omega P(h;L)$")
pk.plt.legend()
pk.plt.savefig("Figures/Fig_Task2g_II.png", dpi=600)
pk.plt.show()