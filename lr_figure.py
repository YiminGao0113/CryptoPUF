import matplotlib.pyplot as plt
import numpy as np

# Original CRP sizes up to 50,000
crp_values = np.array([1, 5000, 10000, 15000, 20000, 25000, 30000, 35000, 40000, 45000, 50000])

# Extend CRP sizes up to 500,000
extended_crp_values = np.concatenate([crp_values, np.array([100000, 150000, 200000, 250000, 300000, 350000, 400000, 450000, 500000])])

# Accuracy scores for Arbiter PUF (including points up to 500,000 CRPs)
arbiter_puf_scores = np.concatenate([np.array([0.5, 0.948, 0.921, 0.931, 0.955, 0.947, 0.944, 0.944, 0.949, 0.931, 0.967]),
                                     np.array([0.979, 0.967, 0.976, 0.976, 0.979, 0.972, 0.975, 0.975, 0.980])])

# Accuracy scores for 2-XOR Arbiter PUF (including points up to 500,000 CRPs)
two_xor_arbiter_puf_scores = np.concatenate([np.array([0.5, 0.49, 0.501, 0.508, 0.504, 0.508, 0.973, 0.936, 0.955, 0.954, 0.956]),
                                             np.array([0.934, 0.955, 0.957, 0.973, 0.970, 0.944, 0.944, 0.967, 0.948])])

# Accuracy scores for 4-XOR Arbiter PUF (including points up to 500,000 CRPs)
four_xor_arbiter_puf_scores = np.concatenate([np.array([0.5, 0.488, 0.498, 0.501, 0.499, 0.498, 0.539, 0.505, 0.494, 0.515, 0.484]),
                                              np.array([0.497, 0.954, 0.951, 0.508, 0.979, 0.966, 0.977, 0.970, 0.968])])

# Accuracy scores for CryptoPUF (including points up to 500,000 CRPs)
crypto_puf_scores = np.concatenate([np.array([0.5, 0.497, 0.491, 0.49, 0.504, 0.464, 0.52, 0.486, 0.503, 0.527, 0.521]),
                                    np.array([0.507, 0.509, 0.504, 0.482, 0.496, 0.515, 0.480, 0.518, 0.502])])

# Plotting the results
plt.figure(figsize=(8, 6))
plt.plot(extended_crp_values / 1000, arbiter_puf_scores, marker='o', linestyle='-.', color='b', label='Arbiter PUF')
plt.plot(extended_crp_values / 1000, two_xor_arbiter_puf_scores, marker='s', linestyle='--', color='g', label='2-XOR Arbiter PUF')
plt.plot(extended_crp_values / 1000, four_xor_arbiter_puf_scores, marker='x', linestyle='-.', color='purple', label='4-XOR Arbiter PUF')
plt.plot(extended_crp_values / 1000, crypto_puf_scores, marker='^', linestyle='-', color='r', label='CryptoPUF')

# Set y-axis range from 0 to 1
plt.ylim(0.3, 1)

# Labels and title
plt.xlabel('Number of CRPs (x 10^3)')
plt.ylabel('Prediction Accuracy')
plt.grid(True)
plt.legend()

# Show the plot
plt.show()
