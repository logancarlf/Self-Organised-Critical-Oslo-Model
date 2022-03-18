import packages as pk
import classes as cl

pk.plt.rc('text', usetex=True)
pk.plt.rc('font', family='serif', size=14)

# %%
# Task 2b

## Rerun for L=128 run with latex


def linear(x, a, b, c):
    return a * x + b

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
    
#%%

def linear(x, a, b, c):
    return a * x ** b

fit = pk.curve_fit(linear, L, av_t_c)
x = pk.np.arange(3, L[len(L)-1]+100, 0.01)

pk.plt.plot(x, linear(x, *fit[0]), color='black', linestyle='dashed',
            label='Power Law Fit')
pk.plt.loglog(L, av_t_c,'.', marker='x', color='black',
               label='Average Time')
pk.plt.xlabel("System Size $L$")
pk.plt.ylabel(r"Average Cross-Over Time  $\langle {t_c(L)} \rangle$")
pk.plt.grid()
pk.plt.legend()
pk.plt.savefig("Figures/Fig_Task2b.png", dpi=600, bbox_inches='tight')
pk.plt.show()


