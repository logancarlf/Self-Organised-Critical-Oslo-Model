import packages as pk
import classes as cl

#%%

n = 7
L = pk.np.logspace(2, n+1, base=2, num=n)
N = 100000
M = 2
c = pk.np.arange(1, n+1)

norm = pk.mpl.colors.Normalize(vmin=c.min(), vmax=c.max())
cmap = pk.mpl.cm.ScalarMappable(norm=norm, cmap=pk.mpl.cm.Blues)
cmap.set_array([])

# Produce data
data_height_1 = list()
for i in pk.tqdm(range(n)):
    height_j = list()
    for j in range(M):
        Oslo = cl.Model(int(L[i]), 0.5)
        Oslo.simulate(N, data_height_1=True)
        height_1 = Oslo.height_1()
        height_j.append(height_1)
        if j != 0:
            height_j = pk.np.mean(height_j, axis=0)
            height_j = list(height_j)
    data_height_1.append(height_j)

#%%

# Task 2a
for i in range(n):
    pk.plt.plot(pk.np.arange(0, N, 1), data_height_1[i], c=cmap.to_rgba(i+2),
                label="L=%s" % (int(L[i])))
    mean = pk.np.mean(data_height_1[i][(len(height_1)-100):])
    steady_pos = pk.np.where(data_height_1[i] > mean)[0][0]
    pk.plt.vlines(steady_pos, 0, 500, linestyles='dashed',
                  color=cmap.to_rgba(i+2))

pk.plt.title("Pile Height Against Time")
pk.plt.xlabel("Number of Iterations / $N$")
pk.plt.ylabel("Height of $i=1$ / $h_i$")
pk.plt.legend()
pk.plt.xscale('log')
pk.plt.yscale('log')
pk.plt.savefig("Figures/Fig_Task2a.png", dpi=600)
pk.plt.show()

#%%


for i in range(n):
    pk.plt.plot(pk.np.arange(0, N, 1)/(L[i]**2), data_height_1[i]/(L[i]),
                c=cmap.to_rgba(i+2), label="L=%s" % (int(L[i])))
pk.plt.title("Scaled Pile Height Against Time")
pk.plt.xlabel("Number of Iterations $N/L^2$")
pk.plt.ylabel("Height of $i=1$ $\~{h_1}/L$")
pk.plt.legend()
pk.plt.xscale('log')
pk.plt.yscale('log')
pk.plt.savefig("Figures/Fig_Task2d.png", dpi=600)
pk.plt.show()

# %%
# Task 2e

# Run latex

def first_order_fit(l, a0, a1, w1):
    return a0 * l * (1 - a1 * l ** (-w1))


h_ave = list()
for i in data_height_1:
    ave = pk.np.mean(i[len(data_height_1)-10000:])
    h_ave.append(ave)

fit = pk.curve_fit(first_order_fit, L, h_ave)
x = pk.np.arange(1, h_ave[len(L)-1]+5, 0.01)

pk.plt.scatter(L, h_ave, marker='x', color='black', label='data')
pk.plt.plot(x, first_order_fit(x, *fit[0]), color='black', linestyle='dashed',
            label='First Order Fit')
pk.plt.title("Height against System Size")
pk.plt.xlabel("System Size $L$")
pk.plt.ylabel("Average Height $h$")
pk.plt.legend()
pk.plt.grid()
pk.plt.savefig("Figures/Fig_Task2e_I.png", dpi=600)
pk.plt.show()

print("Fit Parameters:")
print("a0:", fit[0][0])
print("a1:", fit[0][1])
print("w0:", fit[0][2])

a0 = fit[0][0]

pk.plt.scatter(L, h_ave/(a0*L), marker='x', color='black', label='data')
pk.plt.plot(x, first_order_fit(x, *fit[0])/(a0*x), color='black',
            linestyle='dashed', label='First Order Fit')
pk.plt.title("Correction to Scaling")
pk.plt.xlabel("System Size $L$")
pk.plt.ylabel("Average Height $h$")
pk.plt.legend()
pk.plt.grid()
pk.plt.savefig("Figures/Fig_Task2e_II.png", dpi=600)
pk.plt.show()


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

pk.plt.scatter(L, h_std, color='black', label='Data', marker='x')
pk.plt.plot(x, root_fit(x, *fit[0]), color='black', linestyle='dashed',
            label='Fit $\sigma_h(L)=aL^\omega$')
pk.plt.title("Error in Height")
pk.plt.xlabel("System Size $L$")
pk.plt.ylabel("Standard Deviation in $\~{h}$ / $\sigma$")
pk.plt.xscale('log')
pk.plt.yscale('log')
pk.plt.legend()
pk.plt.grid()
pk.plt.savefig("Figures/Fig_Task2f.png", dpi=600)
pk.plt.show()

print("w:", fit[0][1])

w = fit[0][1]

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