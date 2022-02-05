from packages import *

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

    def __init__(self, L, p):
        self.__L = L
        self.__p = p
        self.__z = np.zeros(L)
        self.__heights = np.zeros(L)
        self.__stop = False
        self.__threshold = list()
        for i in range(L):
            self.__threshold.append(probz(p))
        self.__data_height_1 = list()

    def drive(self):
        self.__z[0] += 1
        self.__heights[0] += 1

    def relax(self, animate, grain_leave_stop):
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
                    if grain_leave_stop == True:
                        self.__stop = True
                self.__threshold[i] = probz(self.__p)
            if animate == True:
                self.animate()

    def simulate(self, N, animate=False, data_height_1=False, grain_leave_stop=False):
        for i in tqdm(range(N)):
            self.drive()
            self.relax(animate=animate)
            if animate == True:
                time.sleep(0)
            if data_height_1 == True:
                self.__data_height_1.append(self.__heights[0])
            if grain_leave_stop == True:
                if self.__stop == True:
                    break


    def animate(self):
        plot = Lattice(self.__L)
        for i in range(self.__L):
            for j in range(int(self.__heights[i])):
                plot.add(i+1)
        plot.display()

    def heights(self):
        return self.__heights

    def height_1(self):
        return self.__data_height_1

    def grains(self):
        return np.sum(self.__heights)


def probz(p):
    x = np.random.uniform(0, 1)
    if x < p:
        return 1
    else:
        return 2

