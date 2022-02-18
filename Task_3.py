import packages as pk
import classes as cl

n = 7
c = pk.np.arange(1, n+1)

norm = pk.mpl.colors.Normalize(vmin=c.min(), vmax=c.max())
cmap = pk.mpl.cm.ScalarMappable(norm=norm, cmap=pk.mpl.cm.Blues)
cmap.set_array([])

Oslo = cl.Model(8, 0.5)
Oslo.simulate(20000, avalanche_data=True)
S = Oslo.avalanche_size()
x, y = pk.logbin(S[-10001:])
pk.plt.xscale('log')
pk.plt.yscale('log')
prob_s = list()
s = list()
for j in range(n):
    for i in S:
        if i != 0:
            s.append(i)
            pos = pk.np.where(x == i)[0]
            if len(pos) != 0:
                prob_s.append(y[pos][0])
            else:
                prob_s.append(0)
pk.plt.yscale('log')
pk.plt.xscale('log')

pk.plt.scatter(s, prob_s, s=0.25, c=cmap.to_rgba(7), label="L=4")

#Oslo = cl.Model(8, 0.5)
#Oslo.simulate(20000, avalanche_data=True)
#S = Oslo.avalanche_size()
#x, y = pk.logbin(S[-10001:])
#prob_s = list()
#s = list()
#for j in range(n):
#    for i in S:
#        if i != 0:
#            s.append(i)
#            pos = pk.np.where(x == i)[0]
#            if len(pos) != 0:
#                prob_s.append(y[pos][0])
#            else:
#                prob_s.append(0)
#
#pk.plt.scatter(s, prob_s, s=0.25)


#Oslo = cl.Model(16, 0.5)
#Oslo.simulate(20000, avalanche_data=True)
#S = Oslo.avalanche_size()
#x, y = pk.logbin(S[-10001:])
#prob_s = list()
#s = list()
#for j in range(n):
#    for i in S:
#        if i != 0:
#            s.append(i)
#            pos = pk.np.where(x == i)[0]
#            if len(pos) != 0:
#                prob_s.append(y[pos][0])
#            else:
#                prob_s.append(0)
#
#pk.plt.scatter(s, prob_s, s=0.25, c=cmap.to_rgba(4), label="L=16")
#
#Oslo = cl.Model(32, 0.5)
#Oslo.simulate(20000, avalanche_data=True)
#S = Oslo.avalanche_size()
#x, y = pk.logbin(S[-10001:])
#prob_s = list()
#s = list()
#for j in range(n):
#    for i in S:
#        if i != 0:
#            s.append(i)
#            pos = pk.np.where(x == i)[0]
#            if len(pos) != 0:
#                prob_s.append(y[pos][0])
#            else:
#                prob_s.append(0)
#
#pk.plt.scatter(s, prob_s, s=0.25, c=cmap.to_rgba(5), label="L=32")
#
#Oslo = cl.Model(64, 0.5)
#Oslo.simulate(20000, avalanche_data=True)
#S = Oslo.avalanche_size()
#x, y = pk.logbin(S[-10001:])
#prob_s = list()
#s = list()
#for j in range(n):
#    for i in S:
#        if i != 0:
#            s.append(i)
#            pos = pk.np.where(x == i)[0]
#            if len(pos) != 0:
#                prob_s.append(y[pos][0])
#            else:
#                prob_s.append(0)
#
#pk.plt.scatter(s, prob_s, s=0.25, c=cmap.to_rgba(6), label="L=64")
#
#Oslo = cl.Model(128, 0.5)
#Oslo.simulate(50000, avalanche_data=True)
#S = Oslo.avalanche_size()
#x, y = pk.logbin(S[-10001:])
#prob_s = list()
#s = list()
#for j in range(n):
#    for i in S:
#        if i != 0:
#            s.append(i)
#            pos = pk.np.where(x == i)[0]
#            if len(pos) != 0:
#                prob_s.append(y[pos][0])
#            else:
#                prob_s.append(0)
#pk.plt.scatter(s, prob_s, s=0.25, c=cmap.to_rgba(7), label="L=128")
#
#Oslo = cl.Model(256, 0.5)
#Oslo.simulate(90000, avalanche_data=True)
#S = Oslo.avalanche_size()
#x, y = pk.logbin(S[-10001:])
#prob_s = list()
#s = list()
#for j in range(n):
#    for i in S:
#        if i != 0:
#            s.append(i)
#            pos = pk.np.where(x == i)[0]
#            if len(pos) != 0:
#                prob_s.append(y[pos][0])
#            else:
#                prob_s.append(0)
#pk.plt.scatter(s, prob_s, s=0.25, c=cmap.to_rgba(8), label="L=256")
pk.plt.legend()