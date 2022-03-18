import packages as pk


class Lattice:

    def __init__(self, L):
        self.__L = L
        self.__gridh = 3 * L
        self.__grid = pk.np.zeros([self.__gridh, L])

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
        pk.plt.figure(figsize=(1, 3))
        cmap = pk.mpl.colors.ListedColormap(['white', 'black'])
        bounds = [0, 0, 1, 1]
        norm = pk.mpl.colors.BoundaryNorm(bounds, cmap.N)
        pk.plt.pcolormesh(self.__grid, edgecolors=None, linewidth=1, norm=norm,
                          cmap=cmap)
        pk.plt.yticks(pk.np.arange(0, self.__gridh, 1))
        pk.plt.xticks(pk.np.arange(0, self.__L, 1))
        pk.plt.xlim(0, self.__L)
        pk.plt.ylim(0, 3*self.__L)
        pk.plt.grid()
        pk.plt.show()
        
    def grid(self):
        return self.__grid

class Model:

    def __init__(self, L, p):
        self.__L = L
        self.__p = p
        self.__z = pk.np.zeros(L)
        self.__heights = pk.np.zeros(L)
        self.__steady = False
        self.__threshold = list()
        self.__avalanche_size = list()
        for i in range(L):
            self.__threshold.append(probz(p))
        self.__data_height_1 = list()
        self.__data_heights = list()

    def drive(self):
        self.__z[0] += 1
        self.__heights[0] += 1

    def relax(self, animate, grain_leave_stop):
        self.__s = 0
        relax_sites = [0]
        avalanche_size = 0
        while len(relax_sites) != 0:
            relax_sites = list()
            for i in range(self.__L):
                if self.__z[i] > self.__threshold[i]:
                    relax_sites.append(i)
            for i in relax_sites:
                self.__s += 1
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
                    self.__steady = True
                self.__threshold[i] = probz(self.__p)

            if animate is True:
                self.animate()

    def simulate(self, N, animate=False, data_height_1=False,
                 grain_leave_stop=False, avalanche_data=False,
                 height_data_store=False):
        for i in range(N):
            self.drive()
            self.relax(animate=animate, grain_leave_stop=grain_leave_stop)
            if animate is True:
                pk.time.sleep(0)
            if data_height_1 is True:
                self.__data_height_1.append(self.__heights[0])
            if grain_leave_stop is True:
                if self.__steady is True:
                    break
            if avalanche_data is True:
                if self.__steady is True:
                    self.__avalanche_size.append(self.__s)
            if height_data_store is True:
                self.__data_heights.append(list(self.__heights))

    def avalanche_size(self):
        return self.__avalanche_size

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
    
    def data_heights(self):
        return self.__data_heights

    def solid_state(self):
        array_size = len(self.height_1())
        minr = pk.np.max(self.__data_height_1[array_size-100:])
        for i in range(len(self.__data_height_1)):
            if self.__data_height_1[i] > minr:
                return i + 100

    def ave_height_1(self):
        ss_time = self.solid_state()
        av = pk.np.mean(self.__data_height_1[ss_time:])
        return av

    def grains(self):
        return pk.np.sum(self.__heights)


def probz(p):
    x = pk.np.random.uniform(0, 1)
    if x < p:
        return 1
    else:
        return 2
