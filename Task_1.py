import packages as pack
import classes as clas

pack.plt.rc('text', usetex=True)
pack.plt.rc('font', family='serif', size=14)

# %%
# Test 1

L = 4
T = 5

Oslo = clas.Model(L, 1)
Oslo.simulate(5, height_data_store=True)
data_heights = Oslo.data_heights()

fig, ax = pack.plt.subplots(1, T, figsize=(12.8, 2.4))
for k in range(T):
    plot = clas.Lattice(L)
    for i in range(L):
        for j in range(int(data_heights[k][i])):
            plot.add(i+1)
    grid = plot.grid()
    cmap = pk.mpl.colors.ListedColormap(['white', 'black'])
    bounds = [0, 0, 1, 1]
    norm = pk.mpl.colors.BoundaryNorm(bounds, cmap.N)
    ax[k].pcolormesh(grid, edgecolors=None, linewidth=1, norm=norm,
                      cmap=cmap)
    ax[k].set_yticks(pk.np.arange(0, L, 1))
    ax[k].set_xticks(pk.np.arange(0, L, 1))
    ax[k].set_xlim(0, L)
    ax[k].set_ylim(0, L)
    ax[k].grid()
ax[0].set_ylabel("Height $h$")
ax[2].set_xlabel("System Column $i$")
fig.savefig("Figures/Fig_Task1_I.png", dpi=600, bbox_inches='tight')
fig.show()

# %%
# Test 1.2

L = 4
T = 5

Oslo = clas.Model(L, 0)
Oslo.simulate(5, height_data_store=True)
data_heights = Oslo.data_heights()

fig, ax = pack.plt.subplots(1, T, figsize=(12.8, 2.4))
for k in range(T):
    plot = clas.Lattice(L)
    for i in range(L):
        for j in range(int(data_heights[k][i])):
            plot.add(i+1)
    grid = plot.grid()
    cmap = pk.mpl.colors.ListedColormap(['white', 'black'])
    bounds = [0, 0, 1, 1]
    norm = pk.mpl.colors.BoundaryNorm(bounds, cmap.N)
    ax[k].pcolormesh(grid, edgecolors=None, linewidth=1, norm=norm,
                      cmap=cmap)
    ax[k].set_yticks(pk.np.arange(0, L, 1))
    ax[k].set_xticks(pk.np.arange(0, L, 1))
    ax[k].set_xlim(0, L)
    ax[k].set_ylim(0, L)
    ax[k].grid()
ax[0].set_ylabel("Height $h$")
ax[2].set_xlabel("System Column $i$")
fig.savefig("Figures/Fig_Task1_II.png", dpi=60, bbox_inches='tight')
fig.show()



# %%
# Test 2

N = 1000
L = 16

Oslo = clas.Model(L, 0.5)
Oslo.simulate(N, data_height_1=True)
height_1 = Oslo.height_1()

pack.plt.figure()
pack.plt.plot(pack.np.arange(0, N, 1), height_1, color='black', label='Height')
pack.plt.vlines(300, 0, 35, linestyles='dashed', label="Steady-State")
pack.plt.xlabel("Number of Iterations $N$")
pack.plt.ylabel("Height $h$")
pack.plt.legend()
pack.plt.ylim(0, 35)
pack.plt.grid()
pack.plt.savefig("Figures/Fig_Task1_III.png", dpi=600)
pack.plt.show()

mean = pack.np.mean(height_1[400:])
print("Average Height i=1:", mean)

 #%%
# Test 3

N = 4000
L = 32

Oslo = clas.Model(L, 0.5)
Oslo.simulate(N, data_height_1=True)
height_1 = Oslo.height_1()

pack.plt.plot(pack.np.arange(0, N, 1), height_1, color='black', label='Height')
pack.plt.vlines(1000, 0, 65, linestyles='dashed', label="Steady-State")
pack.plt.xlabel("Number of Iterations $N$")
pack.plt.ylabel("Height $h$")
pack.plt.legend()
pack.plt.ylim(0, 65)
pack.plt.grid()
pack.plt.savefig("Figures/Fig_Task1_IV.png", dpi=600)
pack.plt.show()

mean = pack.np.mean(height_1[2000:])
print("Average Height i=1:", mean)

# %%
# Test 4

L = 16

Oslo = clas.Model(L, 1)
Oslo.simulate(1000, data_height_1=True)
height_1_p1 = Oslo.height_1()
heights_p1 = Oslo.heights()

Oslo = clas.Model(L, 0)
Oslo.simulate(1000, data_height_1=True)
height_1_p2 = Oslo.height_1()

pack.plt.plot(pack.np.arange(0, 1000, 1), height_1_p1, color='darkred',
              label='Height $p=1$')
pack.plt.plot(pack.np.arange(0, 1000, 1), height_1_p2, color='darkblue',
              label='Height $p=0$')
pack.plt.vlines(136, 0, 35, linestyles='dashed', color='darkred',
                label="Steady-State")
pack.plt.vlines(272, 0, 35, linestyles='dashed', color='darkblue',
                label="Steady-State")
pack.plt.xlabel("Number of Iterations $N$")
pack.plt.ylabel("Height $h$")
pack.plt.legend()
pack.plt.ylim(0, 35)
pack.plt.grid()
pack.plt.savefig("Figures/Fig_Task1_V.png", dpi=600)
pack.plt.show()




