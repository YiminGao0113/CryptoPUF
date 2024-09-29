import matplotlib.pyplot as plt
import numpy as np

# CRP values (limited to 200,000)
crp_values = np.array([1, 5000, 10000, 15000, 20000, 25000, 30000, 35000, 40000, 45000, 50000,
                       55000, 60000, 65000, 70000, 75000, 80000, 85000, 90000, 95000, 100000,
                       150000, 200000])

# Accuracy scores for Arbiter PUF
arbiter_scores = np.array([0.5, 0.985, 0.984, 0.98, 0.989, 0.991, 0.979, 0.982, 0.987, 0.98, 0.975,
                           0.980, 0.983, 0.989, 0.99, 0.99, 0.99, 0.99, 0.99, 0.99, 0.989,
                           0.988, 0.99])

# Accuracy scores for 2-XOR Arbiter PUF
xor_2_scores = np.array([0.5,0.62, 0.876, 0.953, 0.988, 0.982, 0.984, 0.979, 0.985, 0.982, 0.979,
                         0.988, 0.986, 0.979, 0.981, 0.974, 0.976, 0.977, 0.981, 0.985, 0.981,
                         0.982, 0.981])

# Accuracy scores for 4-XOR Arbiter PUF
xor_4_scores = np.array([0.5,0.482, 0.486, 0.493, 0.481, 0.469, 0.492, 0.51, 0.49, 0.498, 0.477,
                         0.538, 0.496, 0.588, 0.472, 0.591, 0.888, 0.919, 0.93, 0.925, 0.96,
                         0.976, 0.967])

# Accuracy scores for CryptoPUF
crypto_puf_scores = np.array([0.5,0.501, 0.519, 0.495, 0.5, 0.505, 0.532, 0.494, 0.496, 0.504, 0.508,
                              0.472, 0.475, 0.519, 0.494, 0.502, 0.497, 0.504, 0.536, 0.533, 0.507,
                              0.507, 0.491])

# Plotting the results (up to 200,000 CRPs)
plt.figure(figsize=(8, 6))

# Arbiter PUF
plt.plot(crp_values / 1000, arbiter_scores, marker='o', linestyle='-.', color='b', label='Arbiter PUF')
# 2-XOR Arbiter PUF
plt.plot(crp_values / 1000, xor_2_scores, marker='s', linestyle='--', color='g', label='2-XOR Arbiter PUF')
# 4-XOR Arbiter PUF
plt.plot(crp_values / 1000, xor_4_scores, marker='x', linestyle='-.', color='purple', label='4-XOR Arbiter PUF')
# CryptoPUF
plt.plot(crp_values / 1000, crypto_puf_scores, marker='^', linestyle='-', color='r', label='CryptoPUF')

# Set y-axis range from 0 to 1
plt.ylim(0.3, 1)

# Labels, grid, and legend
plt.xlabel('Number of CRPs (x 10^3)')
plt.ylabel('Prediction Accuracy (Multilayer Perceptron Attack)')
plt.grid(True)
plt.legend()

# Show the plot
plt.show()
