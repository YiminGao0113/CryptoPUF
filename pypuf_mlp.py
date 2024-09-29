
import pypuf.simulation
from pypuf.simulation import PermutationPUF
import pypuf.io
import pypuf.attack
import pypuf.metrics

# Initialize the XORArbiterPUF with n=64, k=4
puf = pypuf.simulation.XORArbiterPUF(n=64,k=4, seed=1)

accuracy_scores = []

# Loop over CRP sizes from 5000 to 50000 in steps of 5000
for N in range(500000, 550000, 50000):
# for N in range(5000, 105000, 5000):
    print(f"Training with {N} CRPs...")

    # Generate CRPs for the current iteration
    crps = pypuf.io.ChallengeResponseSet.from_simulation(puf, N=N, seed=2)

    # Create an LRAttack2021 attack with the current CRPs
    # attack = pypuf.attack.LRAttack2021(crps, seed=3, k=4, bs=1000, lr=.001, epochs=100)
    
    attack = pypuf.attack.MLPAttack2021(
        crps, seed=3, net=[2 ** 4, 2 ** 5, 2 ** 4],
        epochs=30, lr=.001, bs=1000, early_stop=.08
    )

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
    crp_size = (i + 1) * 5000
    print(f"{crp_size} CRPs: {score}")


# arbiter:
# 5000 CRPs: [0.985]
# 10000 CRPs: [0.984]
# 15000 CRPs: [0.98]
# 20000 CRPs: [0.989]
# 25000 CRPs: [0.991]
# 30000 CRPs: [0.979]
# 35000 CRPs: [0.982]
# 40000 CRPs: [0.987]
# 45000 CRPs: [0.98]
# 50000 CRPs: [0.975]
# 55000 CRPs: [0.980]
# 60000 CRPs: [0.983]
# 65000 CRPs: [0.989]
# 70000 CRPs: [0.99]
# 75000 CRPs: [0.99]
# 80000 CRPs: [0.99]
# 85000 CRPs: [0.99]
# 90000 CRPs: [0.99]
# 95000 CRPs: [0.99]
# 100000 CRPs: [0.989]
# 150000 CRPs: [0.988]
# 200000 CRPs: [0.99]
# 250000 CRPs: [0.988]
# 300000 CRPs: [0.989]
# 350000 CRPs: [0.988]
# 400000 CRPs: [0.987]
# 450000 CRPs: [0.991]
# 500000 CRPs: [0.989]

# 2-xor arbiter:
# 5000 CRPs: [0.62]
# 10000 CRPs: [0.876]
# 15000 CRPs: [0.953]
# 20000 CRPs: [0.988]
# 25000 CRPs: [0.982]
# 30000 CRPs: [0.984]
# 35000 CRPs: [0.979]
# 40000 CRPs: [0.985]
# 45000 CRPs: [0.982]
# 50000 CRPs: [0.979]
# 55000 CRPs: [0.988]
# 60000 CRPs: [0.986]
# 65000 CRPs: [0.979]
# 70000 CRPs: [0.981]
# 75000 CRPs: [0.974]
# 80000 CRPs: [0.976]
# 85000 CRPs: [0.977]
# 90000 CRPs: [0.981]
# 95000 CRPs: [0.985]
# 100000 CRPs: [0.981]
# 150000 CRPs: [0.982]
# 200000 CRPs: [0.981]
# 250000 CRPs: [0.993]
# 300000 CRPs: [0.987]
# 350000 CRPs: [0.986]
# 400000 CRPs: [0.993]
# 450000 CRPs: [0.992]
# 500000 CRPs: [0.991]

# 4-xor arbiter:
# 5000 CRPs: [0.482]
# 10000 CRPs: [0.486]
# 15000 CRPs: [0.493]
# 20000 CRPs: [0.481]
# 25000 CRPs: [0.469]
# 30000 CRPs: [0.492]
# 35000 CRPs: [0.51]
# 40000 CRPs: [0.49]
# 45000 CRPs: [0.498]
# 50000 CRPs: [0.477]
# 55000 CRPs: [0.538]
# 60000 CRPs: [0.496]
# 65000 CRPs: [0.588]
# 70000 CRPs: [0.472]
# 75000 CRPs: [0.591]
# 80000 CRPs: [0.888]
# 85000 CRPs: [0.919]
# 90000 CRPs: [0.930]
# 95000 CRPs: [0.925]
# 100000 CRPs: [0.96]
# 150000 CRPs: [0.976]
# 200000 CRPs: [0.967]
# 250000 CRPs: [0.979]
# 300000 CRPs: [0.978]
# 350000 CRPs: [0.978]
# 400000 CRPs: [0.983]
# 450000 CRPs: [0.981]
# 500000 CRPs: [0.973]


# CryptoPUF: 5000 CRPs: [0.501]
# 10000 CRPs: [0.519]
# 15000 CRPs: [0.495]
# 20000 CRPs: [0.5]
# 25000 CRPs: [0.505]
# 30000 CRPs: [0.532]
# 35000 CRPs: [0.494]
# 40000 CRPs: [0.496]
# 45000 CRPs: [0.504]
# 50000 CRPs: [0.508]
# 55000 CRPs: [0.472]
# 60000 CRPs: [0.475]
# 65000 CRPs: [0.519]
# 70000 CRPs: [0.494]
# 75000 CRPs: [0.502]
# 80000 CRPs: [0.497]
# 85000 CRPs: [0.504]
# 90000 CRPs: [0.536]
# 95000 CRPs: [0.533]
# 100000 CRPs: [0.477]
# 100000 CRPs: [0.507]
# 150000 CRPs: [0.461]
# 200000 CRPs: [0.48]
# 250000 CRPs: [0.503]
# 300000 CRPs: [0.481]
# 350000 CRPs: [0.487]
# 400000 CRPs: [0.503]
# 450000 CRPs: [0.5]
# 500000 CRPs: [0.491]