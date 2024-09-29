
import pypuf.simulation
import pypuf.io
import pypuf.attack
import pypuf.metrics

# Initialize the XORArbiterPUF with n=64, k=4
puf = pypuf.simulation.XORArbiterPUF(n=64, k=2, seed=1)

accuracy_scores = []

# Loop over CRP sizes from 5000 to 50000 in steps of 5000
for N in range(50000, 550000, 50000):
    print(f"Training with {N} CRPs...")

    # Generate CRPs for the current iteration
    crps = pypuf.io.ChallengeResponseSet.from_simulation(puf, N=N, seed=2)

    # Create an LRAttack2021 attack with the current CRPs
    attack = pypuf.attack.LRAttack2021(crps, seed=3, k=6, bs=1000, lr=.001, epochs=100)

    # Train the attack model
    attack.fit()

    # Extract the trained model
    model = attack.model

    # Evaluate the accuracy (similarity score) of the model compared to the original PUF
    score = pypuf.metrics.similarity(puf, model, seed=4)
    print(f"Accuracy (similarity score) with {N} CRPs: {score}")

    # Store the accuracy score
    accuracy_scores.append(score)

# Print the final accuracy scores for each CRP size
print("Accuracy scores for different CRP sizes:")
for i, score in enumerate(accuracy_scores):
    crp_size = (i + 1) * 50000
    print(f"{crp_size} CRPs: {score}")

# 2-xor arbiter puf
# 5000 CRPs: [0.488]
# 10000 CRPs: [0.936]
# 15000 CRPs: [0.92]
# 20000 CRPs: [0.951]
# 25000 CRPs: [0.934]
# 30000 CRPs: [0.963]
# 35000 CRPs: [0.937]
# 40000 CRPs: [0.959]
# 45000 CRPs: [0.942]
# 50000 CRPs: [0.942]
# +++++++++++++++++
# 100000 CRPs: [0.934]
# 150000 CRPs: [0.955]
# 200000 CRPs: [0.957]
# 250000 CRPs: [0.973]
# 300000 CRPs: [0.97]
# 350000 CRPs: [0.944]
# 400000 CRPs: [0.944]
# 450000 CRPs: [0.967]
# 500000 CRPs: [0.948]

# For the plot: 4-xor-arbiter puf

# 5000 CRPs: [0.49]
# 10000 CRPs: [0.501]
# 15000 CRPs: [0.508]
# 20000 CRPs: [0.504]
# 25000 CRPs: [0.508]
# 30000 CRPs: [0.973]
# 35000 CRPs: [0.936]
# 40000 CRPs: [0.955]
# 45000 CRPs: [0.954]
# 50000 CRPs: [0.956]
# ++++++++++++++++++++++++
# 50000 CRPs: [0.493]
# 100000 CRPs: [0.497]
# 150000 CRPs: [0.954]
# 200000 CRPs: [0.951]
# 250000 CRPs: [0.508]
# 300000 CRPs: [0.979]
# 350000 CRPs: [0.966]
# 400000 CRPs: [0.977]
# 450000 CRPs: [0.97]
# 500000 CRPs: [0.968]

# import matplotlib.pyplot as plt
# import numpy as np

# # CRP sizes and corresponding accuracy scores
# crp_values = np.array([5000, 10000, 15000, 20000, 25000, 30000, 35000, 40000, 45000, 50000])
# accuracy_scores = np.array([0.49, 0.501, 0.508, 0.504, 0.508, 0.973, 0.936, 0.955, 0.954, 0.956])

# # Plotting the results
# plt.figure(figsize=(8, 6))
# plt.plot(crp_values / 1000, accuracy_scores, marker='o', linestyle='-', color='b')
# plt.xlabel('Number of CRPs (x 10^3)')
# plt.ylabel('Prediction Accuracy')
# # plt.title('Accuracy vs Number of CRPs')
# plt.grid(True)
# plt.show()

# arbiter puf
# 5000 CRPs: [0.948]
# 10000 CRPs: [0.921]
# 15000 CRPs: [0.931]
# 20000 CRPs: [0.955]
# 25000 CRPs: [0.947]
# 30000 CRPs: [0.944]
# 35000 CRPs: [0.944]
# 40000 CRPs: [0.944]
# 45000 CRPs: [0.931]
# 50000 CRPs: [0.967]
# ++++++++++++++++++++++++
# 50000 CRPs: [0.984]
# 100000 CRPs: [0.979]
# 150000 CRPs: [0.967]
# 200000 CRPs: [0.976]
# 250000 CRPs: [0.976]
# 300000 CRPs: [0.979]
# 350000 CRPs: [0.972]
# 400000 CRPs: [0.975]
# 450000 CRPs: [0.975]
# 500000 CRPs: [0.980]

# import matplotlib.pyplot as plt
# import numpy as np

# # CRP sizes and corresponding accuracy scores
# crp_values = np.array([5000, 10000, 15000, 20000, 25000, 30000, 35000, 40000, 45000, 50000])
# accuracy_scores = np.array([0.717, 0.844, 0.964, 0.955, 0.957, 0.958, 0.958, 0.949, 0.961, 0.94])

# # Plotting the results
# plt.figure(figsize=(8, 6))
# plt.plot(crp_values / 1000, accuracy_scores, marker='o', linestyle='-', color='b')
# plt.xlabel('Number of CRPs (x 10^3)')
# plt.ylabel('Accuracy')
# plt.grid(True)
# plt.show()