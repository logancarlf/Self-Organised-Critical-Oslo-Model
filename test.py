from packages import *
from classes import *

#%%
# Test 1

N = 1000
L = 16

Oslo = Model(L, 0.5)
Oslo.simulate(N, data_height_1=True)
height_1 = Oslo.height_1()

plt.plot(np.arange(0, N, 1), height_1, color='black', label='Height')
plt.vlines(300, 0, 35, linestyles='dashed', label="Steady-State")
plt.xlabel("Number of Iterations / $N$")
plt.ylabel("Height of $i=1$")
plt.legend()
plt.ylim(0, 35)
plt.grid()
plt.show()

mean = np.mean(height_1[400:])
print("Average Height i=1:", mean)

#%%
# Test 2

N = 6000
L = 32

Oslo = Model(L, 0.5)
Oslo.simulate(N, data_height_1=True)
height_1 = Oslo.height_1()

plt.plot(np.arange(0, N, 1), height_1, color='black', label='Height')
plt.vlines(1000, 0, 65, linestyles='dashed', label="Steady-State")
plt.xlabel("Number of Iterations / $N$")
plt.ylabel("Height of $i=1$")
plt.legend()
plt.ylim(0, 65)
plt.grid()
plt.show()

mean = np.mean(height_1[2000:])
print("Average Height i=1:", mean)

#%%
# Test 3

L=16

Oslo = Model(L, 1)
Oslo.simulate(1000, data_height_1=True)
height_1_p1 = Oslo.height_1()
heights_p1 = Oslo.heights()

Oslo = Model(L, 0)
Oslo.simulate(1000, data_height_1=True)
height_1_p2 = Oslo.height_1()

plt.plot(np.arange(0, 1000, 1), height_1_p1, color='darkred',
         label='Height $p=1$')
plt.plot(np.arange(0, 1000, 1), height_1_p2, color='darkblue',
         label='Height $p=0$')
plt.vlines(134, 0, 35, linestyles='dashed', color='darkred',
           label="Steady-State")
plt.vlines(271, 0, 35, linestyles='dashed', color='darkblue',
           label="Steady-State")
plt.xlabel("Number of Iterations / $N$")
plt.ylabel("Height of $i=1$")
plt.legend()
plt.ylim(0, 35)
plt.grid()
plt.show()

plot = Lattice(L)
for i in range(L):
    for j in range(int(heights_p1[i])):
        plot.add(i+1)
plot.display()





