import packages as pk
import classes as cl

# %%

Oslo = cl.Model(4, 0.5)
Oslo.simulate(10, animate=True, data_height_1=False)

# %%
# Task 2a

n = 7
L = pk.np.logspace(2, n+1, base=2, num=n)
N = [100, 200, 600, 2500, 7500, 20000, 70000]
N = [70000, 70000, 70000, 70000, 70000, 70000, 70000]
c = pk.np.arange(1, n+1)

norm = pk.mpl.colors.Normalize(vmin=c.min(), vmax=c.max())
cmap = pk.mpl.cm.ScalarMappable(norm=norm, cmap=pk.mpl.cm.Blues)
cmap.set_array([])

for i in pk.tqdm(range(n-1, -1, -1)):
    Oslo = cl.Model(int(L[i]), 0.5)
    Oslo.simulate(N[i], data_height_1=True)
    height_1 = Oslo.height_1()
    pk.plt.plot(pk.np.arange(0, N[i], 1), height_1, c=cmap.to_rgba(i+1),
                label="L=%s" % (int(L[i])))
    mean = pk.np.mean(height_1[(len(height_1)-100):])
    steady_pos = pk.np.where(height_1 > mean)[0][0]
    pk.plt.vlines(steady_pos, 0, 500, linestyles='dashed',
                  color=cmap.to_rgba(i+1))

pk.plt.title("Pile Height Against Time")
pk.plt.xlabel("Number of Iterations / $N$")
pk.plt.ylabel("Height of $i=1$")
pk.plt.legend()
pk.plt.grid()
pk.plt.savefig("Figures/Fig_Task2a.png", dpi=600)
pk.plt.show()

# %%
# Task 2b


def quad(x, a, b, c):
    return a * x ** 2 + b * x + c


L = pk.np.arange(2, 10, 1)
N = 1000000
n = 100

av_t_c = list()
av_t_c_error = list()

for i in pk.tqdm(L):
    t_c = list()
    for j in range(n):
        Oslo = cl.Model(int(i), 0.5)
        Oslo.simulate(N, grain_leave_stop=True)
        t_c.append(Oslo.grains())
    av_t_c.append(pk.np.mean(t_c))
    av_t_c_error.append(pk.np.std(t_c)/pk.np.sqrt(n))

fit = pk.curve_fit(quad, L, av_t_c)
x = pk.np.arange(0, L[len(L)-1]+1, 0.01)

pk.plt.plot(x, quad(x, *fit[0]), color='black', linestyle='dashed',
            label='Quadratic Fit')
pk.plt.errorbar(L, av_t_c, yerr=av_t_c_error, ls='none', marker='x',
                color='black', label='Average Time')
pk.plt.title("Cross-Over Time with System Size")
pk.plt.xlabel("System Size $L$")
pk.plt.ylabel("Average Cross-Over Time  $av(t_c(L) )$")
pk.plt.grid()
pk.plt.legend()
pk.plt.savefig("Figures/Fig_Task2b.png", dpi=600)
pk.plt.show()

# %%
# Task 2c

