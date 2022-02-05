from packages import *
from classes import *

Oslo = Model(4, 0.5)
Oslo.simulate(10, animate=True, data_height_1=False)

#%%
# Task 2a

n = 7
L = np.logspace(2, n+1, base=2, num=n)
N = [100, 200, 600, 2500, 7500, 20000, 70000]
N = [70000, 70000, 70000, 70000, 70000, 70000, 70000]
c = np.arange(1, n+1)

norm = mpl.colors.Normalize(vmin=c.min(), vmax=c.max())
cmap = mpl.cm.ScalarMappable(norm=norm, cmap=mpl.cm.Blues)
cmap.set_array([])

for i in tqdm(range(n-1, -1, -1)):
    Oslo = Model(int(L[i]), 0.5)
    Oslo.simulate(N[i], data_height_1=True)
    height_1 = Oslo.height_1()
    plt.plot(np.arange(0, N[i], 1), height_1, c=cmap.to_rgba(i+1), label="L=%s" %(int(L[i])))
    mean = np.mean(height_1[(len(height_1)-100):])
    steady_pos= np.where(height_1 > mean)[0][0]
    plt.vlines(steady_pos, 0, 500, linestyles='dashed', color=cmap.to_rgba(i+1))

plt.title("Pile Height Against Time")
plt.xlabel("Number of Iterations / $N$")
plt.ylabel("Height of $i=1$")
plt.legend()
plt.grid()
plt.savefig("Figures/Fig_Task2a.png", dpi=600)
plt.show()

#%%
# Task 2b


