import packages as pk
import classes as cl

pk.plt.rc('text', usetex=True)
pk.plt.rc('font', family='serif', size=14)

#%%

n = 7
L = pk.np.logspace(2, n+1, base=2, num=n)
N = 100000
M = 5
c = pk.np.arange(1, n+1) 

norm = pk.mpl.colors.Normalize(vmin=c.min(), vmax=c.max())
cmap = pk.mpl.cm.ScalarMappable(norm=norm, cmap=pk.mpl.cm.Blues)
cmap.set_array([])

#%%

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

# %%

# Task 2a
for i in range(n):
    pk.plt.plot(pk.np.arange(0, N, 1), data_height_1[i], c=cmap.to_rgba(i+2),
                label="L=%s" % (int(L[i])))
    mean = pk.np.mean(data_height_1[i][(len(height_1)-100):])
    steady_pos = pk.np.where(data_height_1[i] > mean)[0][0]
    pk.plt.vlines(steady_pos, 0, 500, linestyles='dashed',
                  color=cmap.to_rgba(i+2))

pk.plt.xlabel("Number of Iterations $N$")
pk.plt.ylabel("Height  $h$")
pk.plt.legend()
pk.plt.xscale('log')
pk.plt.yscale('log')
pk.plt.savefig("Figures/Fig_Task2a.png", dpi=600, bbox_inches='tight')
pk.plt.show()

#%%
# Task 2d

def power_law(x, a, b):
    return a * x ** b

xplot = list()
yplot = list()
for i in range(n):
    xplot.append(pk.np.arange(0, N, 1)/(L[i]**2))
    yplot.append(data_height_1[i]/(L[i]))
    
xplot2 = list()
yplot2 = list()
xplot3 = list()
yplot3 = list()
for i in range(n):
    x = list()
    y = list()
    for j in range(len(xplot[i])):
        if xplot[i][j] < 1:
            x.append(xplot[i][j])
            y.append(yplot[i][j])
            xplot3.append(xplot[i][j])
            yplot3.append(yplot[i][j])
    xplot2.append(x)
    yplot2.append(y)
    
fit = curve_fit(power_law, xplot3, yplot3)
x = np.linspace(1e-5, 2, 1000)

fig, (ax1, ax2) = pk.plt.subplots(1, 2, figsize=(12.8, 4.8))     
for i in range(n):
    ax1.loglog(xplot[i], yplot[i],'-',
                c=cmap.to_rgba(i+2), label="L=%s" % (int(L[i])))
    ax2.loglog(xplot2[i], yplot2[i],'.', ms=2, c=cmap.to_rgba(i+2))

ax1.vlines(1, 0.0001, 10, linestyles='dashed',
                  color='lightgrey')
ax2.loglog(xplot2[0], yplot2[0],'.', ms=2, c=cmap.to_rgba(9), label='Transient Data Collapsed')
ax2.plot(x, power_law(x, *fit[0]), linestyle='dashed', color='black', label='Power-Law Fit')
ax1.set_xlabel("Number of Iterations $N/L^2$")
ax1.set_ylabel(r"Height of $i=1$ $\tilde{h_i}/L$")
ax2.set_xlabel("Number of Iterations $N/L^2$")
ax2.set_ylabel(r"Height of $i=1$ $\tilde{h_i}/L$")
ax1.legend()
ax2.legend()
ax1.set_ylim(0.003, 3)
fig.savefig("Figures/Fig_Task2d.png", dpi=600, bbox_inches='tight')
fig.show()

print("b:", fit[0][1], "+/-", pk.np.sqrt(fit[1][1][1]))
