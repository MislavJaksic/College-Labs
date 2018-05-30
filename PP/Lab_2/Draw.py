import matplotlib.pyplot as plt

E = [1.00, 0.47, 0.55, 0.61, 0.68, 0.71, 0.67, 0.76]
S = [1.00, 0.95, 1.64, 2.45, 3.42, 4.26, 4.66, 6.09]

plt.plot(range(1,9), S)
plt.xlabel('Number of processors')
plt.ylabel('Speedup')
plt.grid(True)
plt.show()


