import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import random
import time


class Lattice:

    def __init__(self, L):
        self.__L = L
        self.__gridh = 3 * L
        self.__grid = np.zeros([self.__gridh, L])

    def add(self, i):
        for j in range(self.__gridh):
            if self.__grid[j][i-1] == 0:
                self.__grid[j][i-1] = 1
                break

    def remove(self, i):
        for j in range(self.__gridh-1, 0, -1):
            if self.__grid[j][i-1] == 1:
                self.__grid[j][i-1] = 0
                break

    def display(self):
        plt.figure(figsize=(1, 3))
        cmap = mpl.colors.ListedColormap(['white', 'black'])
        bounds = [0, 0, 1, 1]
        norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
        plt.pcolormesh(self.__grid, edgecolors=None, linewidth=1, norm=norm,
                       cmap=cmap)
        plt.yticks(np.arange(0, self.__gridh, 1))
        plt.xticks(np.arange(0, self.__L, 1))
        plt.xlim(0, self.__L)
        plt.ylim(0, 3*self.__L)
        plt.grid()
        plt.show()


class Model:

    def __init__(self, L):
        self.__L = L
        self.__z = np.zeros(L)
        self.__heights = np.zeros(L)
        self.__threshold = list()
        for i in range(L):
            self.__threshold.append(random.randint(1, 2))

    def drive(self):
        self.__z[0] += 1
        self.__heights[0] += 1

    def relax(self):
        relax_sites = [0]
        avalanche_size = 0
        while len(relax_sites) != 0:
            relax_sites = list()
            for i in range(self.__L):
                if self.__z[i] > self.__threshold[i]:
                    relax_sites.append(i)
            for i in relax_sites:
                avalanche_size += 1
                self.__heights[i] -= 1
                if i != self.__L-1:
                    self.__heights[i+1] += 1
                if i == 0:
                    self.__z[i] -= 2
                    self.__z[i+1] += 1
                elif i != 0 and i != self.__L-1:
                    self.__z[i] -= 2
                    self.__z[i-1] += 1
                    self.__z[i+1] += 1
                elif i == self.__L-1:
                    self.__z[i] -= 1
                    self.__z[i-1] += 1
                self.__threshold[i] = random.randint(1, 2)
                self.animate()

    def simulate(self, N):
        for i in range(N):
            self.drive()
            self.relax()
            time.sleep(0.1)

    def animate(self):
        plot = Lattice(self.__L)
        for i in range(self.__L):
            for j in range(int(self.__heights[i])):
                plot.add(i+1)
        plot.display()


y = Model(10)
y.simulate(100)


