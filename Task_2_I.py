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
N = [100000, 100000, 100000, 100000, 100000, 100000, 100000]
c = pk.np.arange(1, n+1)

norm = pk.mpl.colors.Normalize(vmin=c.min(), vmax=c.max())
cmap = pk.mpl.cm.ScalarMappable(norm=norm, cmap=pk.mpl.cm.Blues)
cmap.set_array([])

for i in pk.tqdm(range(n-1, -1, -1)):
    Oslo = cl.Model(int(L[i]), 0.5)
    Oslo.simulate(N[i], data_height_1=True)
    height_1 = Oslo.height_1()
    pk.plt.plot(pk.np.arange(0, N[i], 1), height_1, c=cmap.to_rgba(i+2),
                label="L=%s" % (int(L[i])))
    mean = pk.np.mean(height_1[(len(height_1)-100):])
    steady_pos = pk.np.where(height_1 > mean)[0][0]
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

# %%
# Task 2b

## Rerun for L=128 run with latex


def linear(x, a, b, c):
    return a * x + b


L = pk.np.arange(2, 15, 1)
n = 7
L = pk.np.logspace(2, n+1, base=2, num=n)
N = 1000000
n = 10

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

fit = pk.curve_fit(linear, pk.np.log(L), pk.np.log(av_t_c))
x = pk.np.arange(0, pk.np.log(L)[len(L)-1]+0.5, 0.01)

pk.plt.plot(x, linear(x, *fit[0]), color='black', linestyle='dashed',
            label='Linear Fit')
pk.plt.scatter(pk.np.log(L), pk.np.log(av_t_c), marker='x', color='black',
               label='Average Time')
pk.plt.title("Cross-Over Time with System Size")
pk.plt.xlabel("System Size $\log (L)$")
pk.plt.ylabel("Average Cross-Over Time  $ \log\langle {t_c(L)}$")
pk.plt.grid()
pk.plt.legend()
pk.plt.savefig("Figures/Fig_Task2b.png", dpi=600)
pk.plt.show()

# %%
# Task 2d

# run for L=64 128 and 256 (inccrease N)

import packages as pk
import classes as cl


L = pk.np.arange(2, 8, 1)

n = 6
L = pk.np.logspace(2, n+1, base=2, num=n)
N=70000

norm = pk.mpl.colors.Normalize(vmin=c.min(), vmax=c.max())
cmap = pk.mpl.cm.ScalarMappable(norm=norm, cmap=pk.mpl.cm.Blues)
cmap.set_array([])

data_height_1 = list()
for i in pk.tqdm(range(len(L))):
    height_j = list()
    M = 6
    for j in range(M):
        Oslo = cl.Model(int(L[i]), 0.5)
        Oslo.simulate(N, data_height_1=True)
        height_1 = Oslo.height_1()
        height_j.append(height_1)
    height_j_smooth = list()
    for j in range(N):
        smooth = pk.np.mean(pk.np.transpose(height_j)[j])
        height_j_smooth.append(smooth)
    data_height_1.append(height_j_smooth)

for i in range(len(L)):
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
    ave = pk.np.mean(i[len(data_height_1)-100:])
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
    std = pk.np.std(i[len(data_height_1)-1000:])
    h_std.append(std)

fit = pk.curve_fit(root_fit, L, h_std)
x = pk.np.arange(1, h_ave[len(L)-1]+5, 0.01)

pk.plt.scatter(L, h_std, color='black', label='Data', marker='x')
pk.plt.plot(x, root_fit(x, *fit[0]), color='black', linestyle='dashed', label='Fit')
pk.plt.title("Error in Height")
pk.plt.xlabel("System Size $L$")
pk.plt.ylabel("Standard Deviation in $\~{h}$ $\sigma$")
pk.plt.xscale('log')
pk.plt.yscale('log')
pk.plt.legend()
pk.plt.grid()
pk.plt.savefig("Figures/Fig_Task2f.png", dpi=600)
pk.plt.show()

print("w:", fit[0][1])

